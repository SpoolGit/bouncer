# app.py
import streamlit as st
from view_csv import display_csv
from stats_csv import display_stats
from sampling_upload import display_sampling_upload
from user_inputs import user_inputs
from assert_verdict import show_assert_verdict
from sign_in import show_sign_in

# Page config
st.set_page_config(page_title="Audit CSV App", layout="wide")

allowed_users = st.secrets["auth"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    show_sign_in()
    st.stop()

# Navigation using session state
if 'page' not in st.session_state:
    st.session_state.page = 'userip'  # default page

# Routing logic
if st.session_state.page == 'userip':
    user_inputs()
elif st.session_state.page == 'stats':
    display_stats()
elif st.session_state.page == 'view':
    display_csv()
elif st.session_state.page == 'upload':
    display_sampling_upload()
elif st.session_state.page == 'as_verdict':
    show_assert_verdict()
