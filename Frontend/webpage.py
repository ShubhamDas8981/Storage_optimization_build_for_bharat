import streamlit as st
import requests

def send_to_backend(pincodes):
    backend_url = 'http://127.0.0.1:5000/process_pincodes'  # Backend URL

    # Sending a POST request to the backend
    response = requests.post(backend_url, json={'pincodes': pincodes})

    if response.ok:
        st.success("Pincodes sent successfully to backend!")
    else:
        st.error("Failed to send pincodes to backend.")

def main():
    st.title('Pin Code Input')
    st.write("Enter multiple pin codes separated by commas (e.g., 110001, 400001)")

    # Input field for the user to enter pin codes
    pin_input = st.text_input("Enter pin codes:")

    if st.button("Submit"):
        # Splitting the entered text into individual pincodes
        pincodes = [code.strip() for code in pin_input.split(',') if code.strip()]
        
        # Check if all pincodes are 6 digits
        if all(len(pin) == 6 for pin in pincodes):
            send_to_backend(pincodes)
        else:
            st.warning("Please enter valid pin codes (6 digits each).")

if __name__ == "__main__":
    main()




