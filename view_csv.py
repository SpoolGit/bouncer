# view_csv.py
import streamlit as st
import pandas as pd
from utils import get_llm_sampling_csv

def display_csv(): 
    st.markdown("<h1 style='text-align: center;'>📊 Risk-Based Sampling</h1>", unsafe_allow_html=True)
    st.subheader("Existence & Occurrence Assertsion")
    st.markdown("---")

    if st.session_state.get("page") == "view":
        if st.session_state.get("llm_sampling_df") is None:
            #st.info("Calling LLM...")
            df = get_llm_sampling_csv()
            st.session_state["llm_sampling_df"] = df
    
    df = st.session_state["llm_sampling_df"]
    if not isinstance(df, pd.DataFrame) or df.empty:
        st.info("DF not found...")
        df = pd.DataFrame() 
        if st.button("⬅️ Back to Analytical Statistics", key="view_stats_btn_1"):
            st.session_state.page = 'stats'
            st.rerun()
        return
    
    if st.button("📤 Upload Supporting Docs", key="view_upload_btn_1"):
        st.session_state.page = 'upload'
        st.rerun()
        
    # Normalize booleans
    df['Is High Risk?'] = df['Is High Risk?'].astype(str).str.upper() == "TRUE"
    df['Is selected for Sampling'] = df['Is selected for Sampling'].astype(str).str.upper() == "TRUE"

    # Styling logic
    def highlight_row(row):
        styles = [''] * len(row)
        if row['Is High Risk?']:
            styles = ['background-color: #FFF4CC'] * len(row)  # soft yellow
        if row['Is selected for Sampling']:
            styles = ['background-color: #FFD6D6; font-weight: bold; color: black'] * len(row)  # soft pink
        if row['Is High Risk?'] and row['Is selected for Sampling']:
            styles = ['background-color: #FFC2B3; font-weight: bold; color: black'] * len(row)  # soft peach
        return styles

    st.dataframe(
        df.style.apply(highlight_row, axis=1),
        use_container_width=True
    )
    
    # Back button to go to stats
    if st.button("⬅️ Back to Analytical Statistics"):
        st.session_state.page = 'stats'
        st.rerun()
    if st.button("📤 Upload Supporting Docs"):
        flag = True;
        st.session_state.page = 'upload'
        st.rerun()