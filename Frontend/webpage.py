import streamlit as st
import requests

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000"  # Replace this with your backend server URL

# Function to send the pincode to the backend for retrieval
def retrieve_pincode_from_backend(pincode):
    response = requests.post(f"{BACKEND_URL}/retrieve_pincode", json={"pincode": pincode})
    return response.json()

# Streamlit interface
def main():
    st.title("Pincode Serviceability Checker")

    st.subheader("Enter Pincode to Search:")
    pincode = st.text_input("Enter Pincode:")

    # Button to trigger the retrieval process
    if st.button("Search"):
        if pincode:
            result = retrieve_pincode_from_backend(pincode)
            st.success(result["message"])
            st.success("Thank for visiting")
        else:
            st.warning("Please enter a pincode to search.")

if __name__ == "__main__":
    main()
