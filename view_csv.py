# view_csv.py
import streamlit as st
import pandas as pd

def display_csv(csv_path: str):
    st.markdown("<h1 style='text-align: center;'>📊 Audit Sampling</h1>", unsafe_allow_html=True)
    st.markdown("---")

    df = pd.read_csv(csv_path)

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
        st.session_state.page = 'upload'
        st.rerun()