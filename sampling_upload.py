# sampling_upload.py
import streamlit as st
import pandas as pd
#from utils import get_assertOccurrence_LLM

def display_sampling_upload():

    st.markdown("<h1 style='text-align: center;'>📄 Upload Supporting Files for Sampling</h1>", unsafe_allow_html=True)
    st.subheader("Occurrence & Accuracy Assertsion")
    st.markdown("---")

    df = st.session_state.get("llm_sampling_df", pd.DataFrame())
    if not isinstance(df, pd.DataFrame) or df.empty:
        st.info("DF not found...")
        return

    df['Is selected for Sampling'] = df['Is selected for Sampling'].astype(str).str.upper() == "TRUE"
    sampled_df = df[df['Is selected for Sampling']]


    for idx, row in sampled_df.iterrows():
        desc_key = row['DESCRIPTION'].replace(" ", "_").replace("/", "_").replace("\\", "_")
        row_key = f"row_{desc_key}_{idx}"

        with st.expander(f"📌 {row['DESCRIPTION']} ({row['DATE']}) - £{row['AMOUNT']:.2f}"):
            uploaded_files = st.file_uploader(
                label="Upload supporting documents (PDF, CSV, Excel, DOCX)",
                type=["pdf", "csv", "xlsx", "docx"],
                key=f"file_{row_key}",
                accept_multiple_files=True
            )

            # Save uploads in session state under a list per row
            if uploaded_files:
                st.session_state[f"uploaded_{row_key}"] = uploaded_files
                st.success(f"✅ {len(uploaded_files)} file(s) uploaded and saved.")

            # Action button per row

            if st.button(f"⚖️ Run Assertions for {desc_key}", key=f"check_{row_key}"):
                if not uploaded_files:
                    st.warning("⚠️ Please upload at least one file before running the check.")
                else:
                    st.session_state["selected_description"] = row["DESCRIPTION"]
                    st.session_state["selected_date"] = row["DATE"]
                    st.session_state["selected_row_key"] = row_key

                    st.session_state.page = 'as_verdict'
                    st.rerun()

    st.markdown("---")

    if st.button("⬅️ Back to Risk View"):
        st.session_state.page = 'view'
        st.rerun()

