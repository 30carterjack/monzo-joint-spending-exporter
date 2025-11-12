from dotenv import load_dotenv
import os

from monzo.authentication import Authentication
from monzo.exceptions import MonzoAuthenticationError, MonzoServerError

load_dotenv()

client_id: str = os.getenv("MONZO_CLIENT_ID")
client_secret: str = os.getenv("MONZO_CLIENT_SECRET")
redirect_uri: str = os.getenv("MONZO_REDIRECT_URI")
state: str = os.getenv("MONZO_STATE")
code: str = os.getenv("MONZO_CODE")

monzo = Authentication(client_id=client_id, client_secret=client_secret, redirect_url=redirect_uri)
try:
    monzo.authenticate(authorization_token=code, state_token=state)
except MonzoAuthenticationError:
    print('State code does not match')
    exit(1)
except MonzoServerError:
    print('Monzo Server Error')
    exit(1)

# The following 3 items should be stored for future requests
print(f"access_token = '{monzo.access_token}'")
print(f'expiry = {monzo.access_token_expiry}')
print(f"refresh_token = '{monzo.refresh_token}'")

# Now authorise access in the Monzo app
# The user should visit this url
print(monzo.authentication_url)