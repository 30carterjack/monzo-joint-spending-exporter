from dotenv import load_dotenv
import os
import time
import datetime
import pandas as pd
from rich.console import Console
import openpyxl

from monzo.authentication import Authentication
from monzo.exceptions import MonzoAuthenticationError, MonzoServerError
from monzo.endpoints.account import Account
from monzo.exceptions import MonzoError
from monzo.endpoints.transaction import Transaction

import db
import helper

load_dotenv()

client_id: str = os.getenv("MONZO_CLIENT_ID")
client_secret: str = os.getenv("MONZO_CLIENT_SECRET")
redirect_uri: str = os.getenv("MONZO_REDIRECT_URI")

def access_token_handler(client_id: str, client_secret: str, redirect_uri: str):
    try:
        response = db.fetch_access_token()

        if response and len(response) == 3 and all(response):
            access_token, refresh_token, expiry = response[0], response[1], response[2]

            if is_token_expired(expiry):
                print("Access token is expired. Generating a new token...")
                access_token, refresh_token, expiry = fetch_access_token(client_id, client_secret, redirect_uri)
                monzo_client = create_initial_client(access_token, refresh_token, expiry)
        else:
            print("No usable token found. Generating a new token...")
            access_token, refresh_token, expiry = fetch_access_token(client_id, client_secret, redirect_uri)
            monzo_client = create_initial_client(access_token, refresh_token, expiry)

        monzo_client = create_client(client_id, client_secret, redirect_uri, access_token, refresh_token, expiry)
        return monzo_client
    
    except Exception as e:
        print("Unable to connect to local database.", e)

def is_token_expired(expiry: int) -> bool:
    return int(expiry) - time.time() < 0
            
def fetch_access_token(client_id: str, client_secret: str, redirect_uri: str):
    db.drop_expired_access_token()
    monzo = Authentication(client_id=client_id, client_secret=client_secret, redirect_url=redirect_uri)
    print(monzo.authentication_url)

    state: str = monzo.authentication_url.split("=")[-1]

    monzo_login_url: str = str(input("\nPlease enter your login url: "))
    code = monzo_login_url.replace("&state", "").strip().split("=")[1]

    try:
        monzo.authenticate(authorization_token=code, state_token=state)
        print("\nAuthentication Successful.")
    except MonzoAuthenticationError:
        print("\nState code does not match")
        exit(1)
    except MonzoServerError:
        print("\nMonzo Server Error")
        exit(1)

    access_token = monzo.access_token
    refresh_token = monzo.refresh_token
    expiry = monzo.access_token_expiry

    db.insert_access_token(access_token, refresh_token, expiry)

    return access_token, refresh_token, expiry

def create_initial_client(access_token, refresh_token, expiry) -> Authentication:
    '''
    This step is necessary as the initial client creation will require the end-user to 
    approve a data access request in their monzo app before they can use their newly 
    generated token to perform any api calls.
    '''
    monzo_client = create_client(client_id, client_secret, redirect_uri, access_token, refresh_token, expiry)
    print("\nApp Authorization Required")
    print("\nPlease approve this access request in your Monzo app. You’ll receive a push notification shortly.")

    while True:
        user_input = input("Press ENTER once approved, or type 'cancel' to abort: ").strip().lower()
        if user_input == "":
            print("continuing...")
            break
        elif user_input == "cancel":
            print("Operation cancelled by user.")
            exit(0)
        else:
            print("Invalid input. Please press ENTER after approving the request.")

    return monzo_client

def create_client(client_id: str, client_secret: str, redirect_uri: str, access_token: str, refresh_token: str, expiry: int) -> Authentication:
    monzo_client = Authentication(
        client_id=client_id,
        client_secret=client_secret,
        redirect_url=redirect_uri,
        access_token=access_token,
        refresh_token=refresh_token,
        access_token_expiry=expiry
    )

    return monzo_client

def fetch_joint_account(monzo_client):
    try:
        for account in Account.fetch(monzo_client):
            if "joint account" in account.description.lower():
                print("Joint account fetched successfully")
                joint_account: Account = account
                joint_account_id: str = account.account_id
                print(f"Joint account - Balance: {helper.normalise_cost(joint_account.balance.total_balance) if joint_account.balance else 0}")

        return joint_account_id
    
    except MonzoError:
        print("Failed to retrieve accounts")

def fetch_transactions(monzo_client, joint_account_id) -> list[float]:
    from_date: datetime = datetime.datetime.now().replace(day=1)
    to_date: datetime = datetime.datetime.today()
    
    transactions = Transaction.fetch(monzo_client, joint_account_id, since=from_date, before=to_date, expand=["merchant"], limit=100)

    return transactions

def process_transactions(transactions):
    transaction_dates = [str(transaction.created).split(" ")[0] for transaction in transactions]
    transaction_merchant = [
        str(transaction.merchant['name']) if transaction.merchant is not None else "UNKNOWN MERCHANT"
        for transaction in transactions
    ]
    transaction_amount = [helper.normalise_cost(transaction.amount) for transaction in transactions]
    transaction_category = [
        str(transaction.merchant['category'].replace("_", " ").capitalize()) if transaction.merchant is not None else "UNKNOWN CATEGORY"
        for transaction in transactions
    ]

    return transaction_dates, transaction_merchant, transaction_amount, transaction_category

def create_transactions_df(transaction_dates, transaction_merchant, transaction_amount, transaction_category):
    transactions_df = pd.DataFrame({
        "Date": transaction_dates,
        "Merchant": transaction_merchant,
        "Amount (£)": transaction_amount,
        "Category": transaction_category
    })

    transactions_df["Cumulative Amount (£)"] = transactions_df["Amount (£)"].cumsum()

    return transactions_df

def export_to_excel(transactions_df):
    directory: str = "excel_exports"
    name: str = f'Joint_Spending_{helper.current_month()}.xlsx'
    transactions_df.to_excel(f"./{directory}/{name}")
    print("DataFrame exported to Excel successfully")

if __name__ == "__main__":
    monzo_client = access_token_handler(client_id, client_secret, redirect_uri)
    joint_account_id = fetch_joint_account(monzo_client)
    transactions = fetch_transactions(monzo_client, joint_account_id)
    transaction_dates, transaction_merchant, transaction_amount, transaction_category = process_transactions(transactions)
    transactions_df = create_transactions_df(transaction_dates, transaction_merchant, transaction_amount, transaction_category )
    export_to_excel(transactions_df)