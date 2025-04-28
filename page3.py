import streamlit as st
import time

def dummy_api_call():
    time.sleep(2)  # Simulate API call
    return "Response from backend"

def show_page3():
    st.title("API Call")
    
    if st.button("Make API Call"):
        with st.spinner("Calling API..."):
            response = dummy_api_call()
        st.success(f"Got response from BE: {response}")