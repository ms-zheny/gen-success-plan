import streamlit as st
import urllib.request
import json
import os
import ssl
from dotenv import load_dotenv


load_dotenv()

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


