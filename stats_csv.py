# stats_csv.py
import streamlit as st
import pandas as pd

def display_stats(csv_path: str):
    st.markdown("<h1 style='text-align: center;'>📈 Audit Stats Overview</h1>", unsafe_allow_html=True)
    st.markdown("---")

    df = pd.read_csv(csv_path)

    # Alternate row coloring (light blue tone)
    def alternate_row_colors(row_index):
        if row_index % 2 == 0:
            return ['background-color: #E6F2FF'] * df.shape[1]  # light blue
        else:
            return [''] * df.shape[1]

    styled_df = df.style.apply(lambda row: alternate_row_colors(row.name), axis=1)

    st.dataframe(styled_df, use_container_width=True)

    # Next button to go to view
    if st.button("➡️ View Risk Sampling"):
        st.session_state.page = 'view'
        st.rerun()