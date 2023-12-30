import streamlit as st
from msal_streamlit_authentication import msal_authentication
import urllib.request
import json
import os
import ssl


from dotenv import load_dotenv
load_dotenv()


with st.sidebar:
    st.write("## User Sign In/out:")
    auth_data = msal_authentication(
            auth={
                "clientId":  os.getenv("CLIENT_ID"),
                "authority": os.getenv("AUTHORITY"),
                "redirectUri": "/",
                "postLogoutRedirectUri": "/"
            }, # Corresponds to the 'auth' configuration for an MSAL Instance
            cache={
                "cacheLocation": "sessionStorage",
                "storeAuthStateInCookie": False
            }, # Corresponds to the 'cache' configuration for an MSAL Instance
            login_request={}, # Optional
            logout_request={}, # Optional
            login_button_text="Login", # Optional, defaults to "Login"
            logout_button_text="Logout", # Optional, defaults to "Logout"
            class_name="css_button_class_selector", # Optional, defaults to None. Corresponds to HTML class.
            html_id="btnLogin", # Optional, defaults to None. Corresponds to HTML id.
            key=1 # Optional if only a single instance is needed
    )

if not auth_data:
    st.image('./assets/home.jpg', caption='Created by Zhen YUAN', use_column_width='auto')
    st.stop()


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


tpid = st.text_input("TPID", help="Enter TPID")
website = st.text_input("Website URL",help="Enter Customer's website URL")



if tpid and website:

    #st.write("TPID: ", tpid)
    #st.write("Website: ", website)

    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

    data = {
        'TPID': tpid,
        'CustomerSiteURL': website
    }

    body = str.encode(json.dumps(data))

    url = os.getenv("ENDPOINT")
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key), 'azureml-model-deployment': 'smb-csa-success-plan-endpoint-2' }

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()

        json_result =json.loads(result)

        st.markdown(json_result['response'])
        
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))


