import streamlit as st
import json
import os

WEBOOK_URL = 'https://webhook.site/d9618ce6-8095-4343-96c7-1299cac0f0f9'


def load_data():
    """ Load the webhook data from the file. """
    if os.path.exists('webhook_data.json'):
        with open('webhook_data.json', 'r') as f:
            data = json.load(f)
        return data
    return "No data yet."

def main():
    st.set_page_config(page_title="Bank Connector", layout="centered")

    # Styling to mimic a mobile app
    st.markdown("""
        <style>
        .main {
            margin: auto;
            max-width: 400px;
            border: 1px solid #eee;
            border-radius: 5px;
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
        st.title("Bank Connector")
        banks = ["Bank of America", "Chase", "Wells Fargo", "Citi Bank", "US Bank"]
        bank_selected = st.radio("Select a bank:", banks)

        # Button triggers a fast state change
        if st.button("Connect"):
            st.session_state.show_error = True
    else:
        st.empty()  # Clear previous content quickly
        st.markdown("<h1 style='text-align: center;'>Error</h1>", unsafe_allow_html=True)
        data = load_data()
        st.write(data)

if __name__ == "__main__":
    main()
