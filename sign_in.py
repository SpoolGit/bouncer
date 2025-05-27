# sign_in.py

import streamlit as st


allowed_users = st.secrets["auth"]

def show_sign_in():
    st.title("🔐 Welcome")

    option = st.radio("Choose an option:", ["Sign In", "Sign Up"])

    if option == "Sign In":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in allowed_users and allowed_users[username] == password:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    elif option == "Sign Up":
        st.subheader("📝 Sign Up")

        name = st.text_input("Name (required)", key="signup_name")
        email = st.text_input("Email (required)", key="signup_email")
        company = st.text_input("Company Name (required)", key="signup_company")
        address = st.text_input("Address (required)", key="signup_address")
        phone = st.text_input("Phone", key="signup_phone")
        url = st.text_input("Company Website URL", key="signup_url")
        linkedin = st.text_input("LinkedIn Profile", key="signup_linkedin")

        if st.button("Submit Sign Up"):

            if not name.strip() or not email.strip() or not company.strip() or not address.strip():
                st.error("❌ Please fill in all mandatory fields (Name, Email, Company, Address).")
            else:
                st.success(f"✅ Thank you, {name.strip()}! Your sign-up information has been submitted. You will soon receive your login credentials. Please sign-in again once you receive those")
                  

