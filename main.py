from dotenv import load_dotenv
import os

from monzo.authentication import Authentication
from monzo.exceptions import MonzoAuthenticationError, MonzoServerError
from monzo.endpoints.account import Account
from monzo.exceptions import MonzoError

load_dotenv()

client_id: str = os.getenv("MONZO_CLIENT_ID")
client_secret: str = os.getenv("MONZO_CLIENT_SECRET")
redirect_uri: str = os.getenv("MONZO_REDIRECT_URI")

def obtain_access_token(client_id: str, client_secret: str, redirect_uri: str):
    monzo = Authentication(client_id=client_id, client_secret=client_secret, redirect_url=redirect_uri)
    
    print(monzo.authentication_url) 

    state: str = monzo.authentication_url.split("=")[-1]
    return state

def retrieve_access_token(client_id, client_secret, redirect_uri, state):
    monzo = Authentication(client_id=client_id, client_secret=client_secret, redirect_url=redirect_uri)

    code: str = str(input("\nPlease enter your authentication code: "))

    try:
        monzo.authenticate(authorization_token=code, state_token=state)
    except MonzoAuthenticationError:
        print('State code does not match')
        exit(1)
    except MonzoServerError:
        print('Monzo Server Error')
        exit(1)

    access_token =  monzo.access_token
    refresh_token = monzo.refresh_token
    expiry = monzo.access_token_expiry

    return access_token, refresh_token, expiry

if __name__ == "__main__":
    state = obtain_access_token(client_id, client_secret, redirect_uri)
    access_token, refresh_token, expiry = retrieve_access_token(client_id, client_secret, redirect_uri, state)
    
