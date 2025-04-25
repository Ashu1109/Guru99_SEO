import requests
from config.oauth_config import oauth
def refresh_access_token(refresh_token):
    data = {
        "client_id": oauth["client_id"],
        "client_secret": oauth["client_secret"],
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    response = requests.post(oauth["token_uri"], data=data)
    return response.json()