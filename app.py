# app.py
import streamlit as st
from view_csv import display_csv
from stats_csv import display_stats

# Page config
st.set_page_config(page_title="Audit CSV App", layout="wide")

# Navigation using session state
if 'page' not in st.session_state:
    st.session_state.page = 'stats'  # default page

# Routing logic
if st.session_state.page == 'stats':
    display_stats("outputs/Statisctics_out.csv")
elif st.session_state.page == 'view':
    display_csv("outputs/unusual-n-sampling.csv")
