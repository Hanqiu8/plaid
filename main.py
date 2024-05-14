import streamlit as st

def main():
    st.set_page_config(page_title="Bank Connector", layout="centered")
    
    # Mobile app layout mimic
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

    st.title("Bank Connector")

    # List of banks (you can modify this list as needed)
    banks = ["Bank of America", "Chase", "Wells Fargo", "Citi Bank", "US Bank"]
    bank_selected = st.radio("Select a bank:", banks)

    # Space before the button
    st.write(" ")
    st.write(" ")

    # Connect button
    if st.button("Connect"):
        st.success(f"Connected to {bank_selected} successfully!")

if __name__ == "__main__":
    main()