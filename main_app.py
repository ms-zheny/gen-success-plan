import streamlit as st
import urllib.request
import json
import os
import utils

from dotenv import load_dotenv
load_dotenv()

utils.setup_page("Home")

st.info ("This application is based on GPT-4 model, it includes a range of sources, such as sucess center, and websites, up until 26 Feb 24",icon="ℹ️")

tpid = st.text_input("TPID", help="Enter TPID")
website = st.text_input("Website URL",help="Enter Customer's website URL")

if tpid and website:

    data = {
        'TPID': tpid,
        'CustomerSiteURL': website
    }

    body = str.encode(json.dumps(data))

    url = os.getenv("ENDPOINT")
    api_key = os.getenv("API_KEY")
    azureml_model_deployment = os.getenv("ENDPOINT_DEPLOYMENT_MODEL")

    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")


    # 'azureml-model-deployment': azureml_model_deployment 
    # The azureml-model-deployment header will force the request to go to a specific deployment.
    # Remove this header to have the request observe the endpoint traffic rules
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

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


