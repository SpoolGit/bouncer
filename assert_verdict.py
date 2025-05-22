import streamlit as st
import pandas as pd
import io
import streamlit.components.v1 as components
from utils import get_assertOccurrence_LLM, get_assertCutoff_LLM, display_llm_verdict_pretty

def show_assert_verdict():
    st.title("Assertions Verdict")  
    if st.button("⬅️ Back to Evidence Upload page", key="assert_back_1"):
        st.session_state.page = 'upload'
        st.rerun()
        
    # Insert audit explanation block
    
    if st.session_state.get("page") != "as_verdict":
        return
    with st.spinner("Checking for Occurence..."):
        # Simulate backend call
        #import time
        #time.sleep(2)
        desc = st.session_state.get("selected_description")
        date = st.session_state.get("selected_date")
        row_key = st.session_state.get("selected_row_key")
        get_assertOccurrence_LLM(desc, date, row_key)
        #st.success("Bouncing Magician has given below Verdict!")
        dfOcc_combined = st.session_state.get(f"llm_assertOcc_df_{row_key}", pd.DataFrame())
        st.subheader("Occurrence Check")
        display_llm_verdict_pretty(dfOcc_combined)
    
    with st.spinner("Checking for Classification..."):
        # Simulate backend call
        #import time
        #time.sleep(2)
        #st.success("Bouncing Magician has given below Verdict!")
        desc = st.session_state.get("selected_description")
        date = st.session_state.get("selected_date")
        row_key = st.session_state.get("selected_row_key")
        get_assertCutoff_LLM(desc, date, row_key)
        dfCutOff_combined = st.session_state.get(f"llm_assertCutoff_df_{row_key}", pd.DataFrame())
        st.subheader("Cut-off Check")
        display_llm_verdict_pretty(dfCutOff_combined)
        
    if st.button("⬅️ Back to Evidence Upload page"):
        st.session_state.page = 'upload'
        st.rerun()
    if st.button("⬅️ Home"):
        st.session_state.page = 'userip'
        st.rerun()