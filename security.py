import streamlit as st
import msal
import requests
import os

from dotenv import load_dotenv
load_dotenv()

# Replace with your own values
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')
AUTHORITY = os.getenv('AUTHORITY')
REDIRECT_URI = os.getenv('REDIRECT_URI')
SCOPE = []



app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)


def get_auth_url():
    auth_url = app.get_authorization_request_url(SCOPE, redirect_uri=REDIRECT_URI)
    return auth_url


def get_token_from_code(auth_code):
    app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
    result = app.acquire_token_by_authorization_code(auth_code, scopes=SCOPE, redirect_uri=REDIRECT_URI)
    return result


def get_user_info(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
    return response.json()


def handle_redirect():
    if not st.session_state.get('access_token'):
        code = st.experimental_get_query_params().get('code')
        if code:
            result = get_token_from_code(code)
            st.session_state['access_token'] = result['access_token']
            st.session_state['user_info'] = result['id_token_claims']['name']
            st.experimental_set_query_params()