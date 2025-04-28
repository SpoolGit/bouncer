import streamlit as st

def show_page1():
    st.title("User Information")

    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}

    st.session_state.user_info['name'] = st.text_input("Name", st.session_state.user_info.get('name', ''))
    st.session_state.user_info['email'] = st.text_input("Email", st.session_state.user_info.get('email', ''))
    st.session_state.user_info['address'] = st.text_area("Address", st.session_state.user_info.get('address', ''))
    st.session_state.user_info['company_info'] = st.text_area("Company Info", st.session_state.user_info.get('company_info', ''))
    st.session_state.user_info['company_domain'] = st.selectbox("Company Domain", ["Technology", "Finance", "Healthcare", "Other"], index=["Technology", "Finance", "Healthcare", "Other"].index(st.session_state.user_info.get('company_domain', 'Technology')))

    if st.session_state.user_info.get('name') and st.session_state.user_info.get('email'):
        st.success("User information saved successfully. You can now navigate to other pages.")
    else:
        st.info("Please fill in the Name and Email fields to access other pages.")