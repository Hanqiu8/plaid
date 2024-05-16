import streamlit as st
import json
import time
import requests

WEBOOK_URL = 'https://webhook.site/d9618ce6-8095-4343-96c7-1299cac0f0f9'
URL = 'https://hanqiu8.pythonanywhere.com/events'

import requests

@st.experimental_fragment
def fetch_events(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        print(response.json())
        return response.json()  # Parse JSON response and return the data
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

@st.experimental_fragment
def wait_for_webhook():
    with st.spinner(text='Waiting for Issue Resolution'):
        while True:
            data = fetch_events(URL)
            if data:
                st.empty()
                st.success("Your issue has been resolved!")
                st.button("Link Again")
                return
            time.sleep(5)
    



def get_known_issue():
    try:
        # Sending a GET request to the URL
        response = requests.post("https://api.dashboard.plaid.com/teams/5e1f7c6f21bd680011c481bf/known-issues", headers={
    "Authorization": "Bearer 73d9372ea6636ec1c573705de81c089c",
    "Content-Type": "application/json"
}, data = json.dumps({"requestID": "CZKYYPAkMGaL3r0"}))
        # Returning the status code and response content
        formatted_data = response.json()
        return formatted_data['knownIssue']['title'], formatted_data['knownIssue']['plaidErrorCode']
    except requests.exceptions.RequestException as e:
        # Handling exceptions and returning the error
        return "Error: ", str(e)

@st.experimental_fragment
def follow_issue_button():
    # st.text("We can notify you when this is fixed")
    st.markdown("We can notify you when this is fixed"
    )
    if st.button("🔔 Notify me", type='primary'):
        response = requests.post("https://api.dashboard.plaid.com/teams/5e1f7c6f21bd680011c481bf/cases", headers={
            "Authorization": "Bearer 73d9372ea6636ec1c573705de81c089c",
            "Content-Type": "application/json"
        }, data = json.dumps({
            "useHtml": True,
            "accessTokens":[],
            "accountIDs":[],
            "assetReportTokens":[],
            "missingDataShownTransactionIDs":[],
            "body":"<p>Hi Avi,</p><p><em>We are tracking your follow request for issue KI374487. You will be notified here once the issue is resolved.</em></p><br/><p><h5>Issue KI374456: Connections are timing out with FNBO Direct - Personal</h5></p><p>Connection attempts are timing out for some users connecting to FNBO Direct - Personal. Users encountering this issue will see an error indicating that the institution is not responding. The API request will result in the error INTERNAL_SERVER_ERROR</p>",
            "investmentTransactionIDs":[],
            "institutionID":"",
            "institutionName":"",
            "issueId":"374487",
            "itemIDs":[],
            "labels":["authentication-issues","known-issue"],
            "minimumTransactionAmount":None,
            "maximumTransactionAmount":None,
            "paymentIDs":[],
            "primaryCategory":"authentication-issues",
            "requestIDs":["CZKYYPAkMGaL3r0"],
            "secondaryCategory":"known-issue","subject":"Encountering issue KI374456",
            "tags":[""],
            "transactionIDs":[],
            "type":"incident",
            "uploads":[],
            "virtualWalletIDs":[],
            "walletTransactionIDs":[]
        }))
        # Returning the status code and response content

        # st.success(response.json()['case']['id'])
        st.text("Following Issue: " + str(response.json()['case']['id']))
        wait_for_webhook()
    return False

def main():
    st.set_page_config(page_title="Bank Connector", layout="centered")

    # Styling to mimic a mobile app
    st.markdown("""
        <style>
        .main {
            margin: auto;
            height: 700px;
            max-width: 400px;
            border: 1px solid #ddd;
            border-radius: 15px;
            padding: 10px;
                
        }
        .block-container {
            padding: 2rem;
        }
        .follow_issue_button {
                height: 23px;
        }
        </style>
        """, unsafe_allow_html=True)

    # Initialize session state for showing error
    if 'link' not in st.session_state:
        st.session_state.link = True

    if st.session_state.link:
        with st.spinner(text='Attempting to Link to account'):
            col1, col2, col3 = st.columns([1,1,1])
            with col2: 
                st.image('./bank.png', width=55)
            time.sleep(10)
            st.session_state.link = False
            st.rerun()

    # if not st.session_state.show_error:
    #     st.title("Add Accounts")
    #     st.image("./bank.png", width=55)
    #     banks = ["Bank of America", "Chase", "Wells Fargo", "Citi Bank", "US Bank", "First National Bank of Omaha"]
    #     bank_selected = st.radio("Select a bank:", banks)

    #     # Button triggers a fast state change
    #     if st.button("Connect"):
    #         st.session_state.show_error = True
    #         st.rerun()
    # else:
    # st.empty()  # Clear previous content quickly
    st.markdown("<h2 style='text-align: center;'>Error Linking Account</h2>", unsafe_allow_html=True)
    with st.spinner(text='Checking for Known Issues'):
        time.sleep(5)
        data, data2 = get_known_issue()
    # st.warning(data + '\n' + data2)
    st.warning("You're experiencing a known connection issue with FNBO", icon="⚠️")
    follow_issue_button()

            


    

if __name__ == "__main__":
    main()
