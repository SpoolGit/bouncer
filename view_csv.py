# view_csv.py
import streamlit as st
import pandas as pd
from utils import get_llm_sampling_csv

def display_csv(): 
    st.markdown("<h1 style='text-align: center;'>📊 Audit Sampling</h1>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.get("page") == "view":
        if st.session_state.get("llm_sampling_df") is None:
            #st.info("Calling LLM...")
            df = get_llm_sampling_csv()
            st.session_state["llm_sampling_df"] = df
    
    if st.button("📤 Go to Upload Page", key="view_upload_btn_1"):
        st.session_state.page = 'upload'
        st.rerun()

    df = st.session_state["llm_sampling_df"]
    if not isinstance(df, pd.DataFrame) or df.empty:
        st.info("DF not found...")
        df = pd.DataFrame() 
        return
        
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
    if st.button("⬅️ Back to Stats View"):
        st.session_state.page = 'stats'
        st.rerun()
    if st.button("📤 Go to Upload Page"):
        flag = True;
        st.session_state.page = 'upload'
        st.rerun()