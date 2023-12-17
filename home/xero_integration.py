from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

# Replace these with your client ID and client secret
CLIENT_ID = 'A87B79D4DBD74902B6CE91813AF3B179'
CLIENT_SECRET = 'peagvqofmFjiYo1G1xP-0P4jJd8O2aZBZUlXsYBEHZC03i1W'
REDIRECT_URI = 'https://pods-app-git-4779450e3d53.herokuapp.com/xero/callback'
SCOPE = ["offline_access", "openid", "profile", "email", 
         "accounting.transactions", "accounting.reports.read", 
         "accounting.journals.read", "accounting.settings", 
         "accounting.contacts", "accounting.attachments", 
         "assets", "projects"]

def refresh_xero_token(refresh_token):
    extra = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }

    oauth = OAuth2Session(CLIENT_ID, token={'refresh_token': refresh_token, 'token_type': 'Bearer'})
    new_token = oauth.refresh_token('https://identity.xero.com/connect/token', **extra)

    return new_token

def get_xero_oauth2_session():
    oauth = OAuth2Session(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, state = oauth.authorization_url("https://login.xero.com/identity/connect/authorize")
    
    # Redirect user to Xero for authorization
    # The user will then be redirected back to your REDIRECT_URI

    return oauth

def fetch_xero_token(code):
    oauth = get_xero_oauth2_session()
    token = oauth.fetch_token(token_url="https://identity.xero.com/connect/token",
                              client_secret=CLIENT_SECRET,
                              code=code)
    return token

def get_invoices(oauth_session):
    url = 'https://api.xero.com/api.xro/2.0/Invoices'
    try:
        response = oauth_session.get(url)
        response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return response.json()
    except Exception as e:
        print(f"Error fetching invoices: {e}")
        return None
