from dotenv import load_dotenv
import os
import datetime
import pandas as pd
import openpyxl
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from copy import copy

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

def access_token_handler(client_id: str, client_secret: str, redirect_uri: str) -> Authentication | None:
    try:
        response: list[str, str, int] = db.fetch_access_token()

        if response and len(response) == 3 and all(response):
            access_token, refresh_token, expiry = response[0], response[1], response[2]

            if helper.is_token_expired(expiry):
                print("\nAccess token is expired. Generating a new token...")
                access_token: str
                refresh_token: str
                expiry: str

                access_token, refresh_token, expiry = fetch_access_token(client_id, client_secret, redirect_uri)

                monzo_client: Authentication = create_initial_client(access_token, refresh_token, expiry)
        else:
            print("\nNo usable token found. Generating a new token...")
            access_token: str
            refresh_token: str
            expiry: str

            access_token, refresh_token, expiry = fetch_access_token(client_id, client_secret, redirect_uri)
            
            monzo_client: Authentication = create_initial_client(access_token, refresh_token, expiry)

        monzo_client: Authentication = create_client(client_id, client_secret, redirect_uri, access_token, refresh_token, expiry)
        return monzo_client
    
    except Exception as e:
        print("\nUnable to connect to local database.", e)

            
def fetch_access_token(client_id: str, client_secret: str, redirect_uri: str) -> tuple[str, str, int]:
    db.drop_expired_access_token()

    monzo: Authentication = Authentication(client_id=client_id, client_secret=client_secret, redirect_url=redirect_uri)
    print(f"\n{monzo.authentication_url}")
    print("\nPlease paste the above URL into your browser and enter the email address associated with your Monzo account.")

    helper.wait_event()

    state: str = monzo.authentication_url.split("=")[-1]
    print("\nThe previous action will have sent an email from Monzo to your email address, please paste the attached login URL here: ")
    monzo_login_url: str = str(input("\nPlease enter your login url: "))
    code: str = monzo_login_url.replace("&state", "").strip().split("=")[1]

    try:
        monzo.authenticate(authorization_token=code, state_token=state)
        print("\nAuthentication Successful.")
    except MonzoAuthenticationError:
        print("\nState code does not match")
        exit(1)
    except MonzoServerError:
        print("\nMonzo Server Error")
        exit(1)

    access_token: str = monzo.access_token
    refresh_token: str = monzo.refresh_token
    expiry: int = monzo.access_token_expiry

    db.insert_access_token(access_token, refresh_token, expiry)

    return access_token, refresh_token, expiry


def create_initial_client(access_token, refresh_token, expiry) -> Authentication:
    '''
    This step is necessary as the initial client creation will require the end-user to 
    approve a data access request in their monzo app before they can use their newly 
    generated token to perform any api calls.
    '''

    monzo_client: Authentication = create_client(client_id, client_secret, redirect_uri, access_token, refresh_token, expiry)
    print("\nApp Authorization Required\n")
    print("\nPlease approve this access request in your Monzo app. You’ll receive a push notification shortly.\n")

    helper.wait_event()

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


def fetch_joint_account(monzo_client: Authentication) -> str:
    try:
        for account in Account.fetch(monzo_client):
            if "joint account" in account.description.lower():
                print("\nJoint account fetched successfully")
                joint_account_id: str = account.account_id

        return joint_account_id
    
    except MonzoError:
        print("\nFailed to retrieve accounts")


def fetch_transactions(monzo_client: str, joint_account_id: str) -> list[Transaction]:
    from_date: datetime = datetime.datetime.now().replace(day=1)
    to_date: datetime = datetime.datetime.today()

    transactions = Transaction.fetch(monzo_client, joint_account_id, since=from_date, before=to_date, expand=["merchant"], limit=100)

    return transactions


def process_transactions(transactions: Transaction) -> tuple[list[str], list[str], list[str], list[str]]:
    transaction_dates: list[str] = [str(transaction.created).split(" ")[0] for transaction in transactions]

    transaction_merchant: list[str] = [
        str(transaction.merchant['name']) if transaction.merchant is not None else "UNKNOWN MERCHANT"
        for transaction in transactions
    ]

    transaction_amount: list[str] = [helper.normalise_cost(transaction.amount) for transaction in transactions]

    transaction_category: list[str] = [
        str(transaction.merchant['category'].replace("_", " ").capitalize()) if transaction.merchant is not None else "UNKNOWN CATEGORY"
        for transaction in transactions
    ]

    return transaction_dates, transaction_merchant, transaction_amount, transaction_category


def create_transactions_df(transaction_dates: list[str], transaction_merchant: list[str], 
                           transaction_amount: list[str], transaction_category: list[str]) -> pd.DataFrame:
    
    transactions_df: pd.DataFrame = pd.DataFrame({
        "Date": transaction_dates,
        "Merchant": transaction_merchant,
        "Amount (£)": transaction_amount,
        "Category": transaction_category
    })

    transactions_df["Cumulative Amount (£)"] = transactions_df["Amount (£)"].cumsum()

    return transactions_df


def export_to_excel(transactions_df: pd.DataFrame) -> tuple[str, str]:
    export_directory: str = "excel_exports"
    current_month: str = helper.current_month()
    workbook_name: str = f'Joint_Spending_{current_month}.xlsx'
    export_path: str = f"./{export_directory}/{workbook_name}"

    transactions_df.to_excel(f"./{export_directory}/{workbook_name}", sheet_name=current_month)

    print("\nDataFrame exported to Excel successfully")

    return export_path, current_month


def format_excel_workbook(export_path: str, current_month: str):
    workbook: Workbook = openpyxl.load_workbook(export_path)
    sheet: Worksheet = workbook[current_month]

    for column in sheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                alignment_obj = copy(cell.alignment)
                alignment_obj.horizontal = 'center'
                alignment_obj.vertical = 'center'
                cell.alignment = alignment_obj
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2) * 2
        sheet.column_dimensions[column_letter].width = adjusted_width

    workbook.save(export_path)

    print("\nExcel workbook formatted successfully.")
    

if __name__ == "__main__":
    monzo_client = access_token_handler(client_id, client_secret, redirect_uri)
    joint_account_id = fetch_joint_account(monzo_client)
    transactions = fetch_transactions(monzo_client, joint_account_id)
    transaction_dates, transaction_merchant, transaction_amount, transaction_category = process_transactions(transactions)
    transactions_df = create_transactions_df(transaction_dates, transaction_merchant, transaction_amount, transaction_category )
    export_path, current_month = export_to_excel(transactions_df)
    format_excel_workbook(export_path, current_month)