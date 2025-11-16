from dotenv import load_dotenv
import os

from monzo.authentication import Authentication
from monzo.exceptions import MonzoAuthenticationError, MonzoServerError
from monzo.endpoints.account import Account
from monzo.exceptions import MonzoError
from monzo.endpoints.transaction import Transaction
import time



load_dotenv()

client_id: str = os.getenv("MONZO_CLIENT_ID")
client_secret: str = os.getenv("MONZO_CLIENT_SECRET")
redirect_uri: str = os.getenv("MONZO_REDIRECT_URI")

def obtain_access_token(client_id: str, client_secret: str, redirect_uri: str):
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

    access_token =  monzo.access_token
    refresh_token = monzo.refresh_token
    expiry = monzo.access_token_expiry

    return access_token, refresh_token, expiry

def create_client(access_token, refresh_token, expiry) -> Authentication:
    monzo_client = Authentication(
        client_id=client_id,
        client_secret=client_secret,
        redirect_url=redirect_uri,
        access_token=access_token,
        access_token_expiry=expiry,
        refresh_token=refresh_token
    )

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

def obtain_account_list(monzo):
    try:
        accounts = Account.fetch(monzo)
        for account in accounts:
            print(
                f"Account ID: {account.account_type()} - Balance: {(account.balance.total_balance / 100) if account.balance else 0}"
            )
    except MonzoError:
        print("Failed to retrieve accounts")

if __name__ == "__main__":
    access_token, refresh_token, expiry = obtain_access_token(client_id, client_secret, redirect_uri)
    monzo = create_client(access_token, refresh_token, expiry)
    obtain_account_list(monzo)
    
