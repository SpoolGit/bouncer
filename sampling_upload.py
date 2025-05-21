# sampling_upload.py
import streamlit as st
import pandas as pd

def display_sampling_upload():
    csv_path = "outputs/unusual-n-sampling.csv"
    st.markdown("<h1 style='text-align: center;'>📤 Upload Supporting Files for Sampling</h1>", unsafe_allow_html=True)
    st.markdown("---")

    df = pd.read_csv(csv_path)
    df['Is selected for Sampling'] = df['Is selected for Sampling'].astype(str).str.upper() == "TRUE"

    sampled_df = df[df['Is selected for Sampling']]

    for idx, row in sampled_df.iterrows():
        with st.expander(f"📌 {row['DESCRIPTION']} ({row['DATE']}) - £{row['AMOUNT']:.2f}"):
            desc_key = row['DESCRIPTION'].replace(" ", "_")
            uploaded_file = st.file_uploader(
                label="Upload supporting document (PDF, CSV, Excel, DOCX)",
                type=["pdf", "csv", "xlsx", "docx"],
                key=f"file_{desc_key}"
            )
            if uploaded_file:
                st.session_state[f"uploaded_{desc_key}"] = uploaded_file
                st.success("✅ File uploaded and saved.")

    st.markdown("---")
    if st.button("⬅️ Back to Risk View"):
        st.session_state.page = 'view'
        st.rerun()
