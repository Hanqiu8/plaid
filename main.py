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
    with st.spinner(text='Waiting for Webhook'):
        while True:
            data = fetch_events(URL)
            if data:
                st.success(data)
                return
            time.sleep(5)
    



def get_known_issue():
    try:
        # Sending a GET request to the URL
        response = requests.post("https://api.dashboard.plaid.com/teams/5e1f7c6f21bd680011c481bf/known-issues", headers={
    "Authorization": "Bearer 73d9372ea6636ec1c573705de81c089c",
    "Content-Type": "application/json"
}, data = json.dumps({"itemID": "64581ea558d4f200157fb90f"}))
        # Returning the status code and response content
        formatted_data = response.json()
        return formatted_data['knownIssue']['title'], formatted_data['knownIssue']['plaidErrorCode']
    except requests.exceptions.RequestException as e:
        # Handling exceptions and returning the error
        return "Error: ", str(e)

@st.experimental_fragment
def follow_issue_button():
    if st.button("FOLLOW ISSUE", type='primary'):
        st.success("Following")
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
            border: 1px solid #aaa;
            border-radius: 15px;
            padding: 10px;
                
        }
        .block-container {
            padding: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)


    # Initialize session state for showing error
    if 'show_error' not in st.session_state:
        st.session_state.show_error = False

    if not st.session_state.show_error:
        st.title("Add Accounts")
        st.image("./bank.png", width=55)
        banks = ["Bank of America", "Chase", "Wells Fargo", "Citi Bank", "US Bank"]
        bank_selected = st.radio("Select a bank:", banks)

        # Button triggers a fast state change
        if st.button("Connect"):
            st.session_state.show_error = True
            st.rerun()
    else:
        st.empty()  # Clear previous content quickly
        st.markdown("<h1 style='text-align: center;'>Error</h1>", unsafe_allow_html=True)
        st.text("Institution Error")
        with st.spinner(text='Checking for Known Issues'):
            data, data2 = get_known_issue()
        st.warning(data + '\n' + data2)
        follow_issue_button()
            


    

if __name__ == "__main__":
    main()
