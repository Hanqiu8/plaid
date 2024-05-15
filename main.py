import streamlit as st
import json
import os

WEBOOK_URL = 'https://webhook.site/d9618ce6-8095-4343-96c7-1299cac0f0f9'
url = 'https://hanqiu8.pythonanywhere.com/events'

import requests

@st.experimental_fragment
def fetch_events(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()  # Parse JSON response and return the data
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None


import requests

def get_known_issue():
    try:
        # Sending a GET request to the URL
        response = requests.post("https://api.dashboard.plaid.com/teams/5e1f7c6f21bd680011c481bf/known-issues", headers={
    "Authorization": "Bearer 73d9372ea6636ec1c573705de81c089c",
    "Content-Type": "application/json"
}, data = json.dumps({"itemID": "64581ea558d4f200157fb90f"}))
        # Returning the status code and response content
        formatted_data = response.json()
        return formatted_data[0]
    except requests.exceptions.RequestException as e:
        # Handling exceptions and returning the error
        return "Error: ", str(e)


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
    else:
        st.empty()  # Clear previous content quickly
        st.markdown("<h1 style='text-align: center;'>Error</h1>", unsafe_allow_html=True)
        st.text("Institution Error")
        data = ""
        data = get_known_issue()
        # while (len(data) < 10):
        #     data = fetch_events(url='https://hanqiu8.pythonanywhere.com/events')
        st.write(data)

if __name__ == "__main__":
    main()
