import streamlit as st
import pandas as pd
import pdfplumber
import io
import streamlit.components.v1 as components



def extract_text_from_pdf(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_text_from_csv(uploaded_file):
    try:
        uploaded_file.seek(0)  # Reset stream

        # Read as raw text
        raw_text = uploaded_file.read().decode('utf-8', errors='replace')

        # Check what separator is more likely
        first_line = raw_text.split('\n')[0]
        if first_line.count(',') > first_line.count(';') and first_line.count(',') > first_line.count('\t'):
            sep = ','
        elif first_line.count(';') > first_line.count('\t'):
            sep = ';'
        else:
            sep = '\t'

        # Now re-read with StringIO
        from io import StringIO
        uploaded_file.seek(0)  # Reset again
        df = pd.read_csv(StringIO(raw_text), sep=sep, engine='python')

        return df.to_string()

    except Exception as e:
        return f"Error reading CSV: {e}"

def extract_text_from_excel(uploaded_file):
    try:
        uploaded_file.seek(0)  # Reset the stream position
        df = pd.read_excel(uploaded_file)
        return df.to_string()
    except Exception as e:
        return f"Error reading Excel: {e}"


def show_page3():
    st.title("File Processing and API Call")
  
    
    # Ensure user_info is initialized
    if 'user_info' not in st.session_state:
        st.session_state.user_info = {}


    col1, col2, _ = st.columns(3)
    with col1:
        st.session_state.user_info['materiality_threshold'] = st.selectbox(
            "Materiality Threshold (%)",
            ["10", "20", "30", "40", "50"],
            index=["10", "20", "30", "40", "50"].index(
                st.session_state.user_info.get('materiality_threshold', '10')
            )
        )
    with col2:
        st.session_state.user_info['account'] = st.selectbox(
            "Account to review",
            ["Payroll", "Revenue", "Expenses", "Assets"],
            index=["Payroll", "Revenue", "Expenses", "Assets"].index(
                st.session_state.user_info.get('account', 'Revenue')
            )
        )


    # Process Trial Balance
    trial_balance_file = st.session_state.get('trial_balance_file')
    if trial_balance_file:
        st.header("Trial Balance File")
        file_name = trial_balance_file.name.lower()
        if file_name.endswith('.csv'):
            text = extract_text_from_csv(trial_balance_file)
        elif file_name.endswith('.xlsx'):
            text = extract_text_from_excel(trial_balance_file)
        else:
            text = "Unsupported Trial Balance file format."
        with st.expander(f"View Extracted Text - {trial_balance_file.name}"):
            st.text(text)
    else:
        st.warning("No Trial Balance file uploaded.")

    # Process Evidence Documents
    evidence_files = st.session_state.get('evidence_files', [])
    if evidence_files:
        st.header("Evidence Documents")
        for idx, file in enumerate(evidence_files):
            if file is not None:
                file_name = file.name.lower()
                if file_name.endswith('.pdf'):
                    text = extract_text_from_pdf(file)
                elif file_name.endswith('.csv'):
                    text = extract_text_from_csv(file)
                elif file_name.endswith('.xlsx'):
                    text = extract_text_from_excel(file)
                else:
                    text = "Unsupported Evidence file format."

                with st.expander(f"View Extracted Text - Evidence {idx+1} - {file.name}"):
                    st.text(text)
    else:
        st.warning("No Evidence Documents uploaded.")

    # Dummy API Call Button (kept from your old page3)
    if st.button("Get Reconcilliation"):
        with st.spinner("Calling API..."):
            # Simulate backend call
            import time
            time.sleep(2)
        st.success("Got response from backend!")
    
        st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    def go_back():
        st.session_state.page = 2
        st.session_state.selection = "Document Upload"
        st.session_state.page_reroute = True

    def go_next():
        st.session_state.page = 4
        st.session_state.selection = "Document Upload"  # hypothetical next section
        st.session_state.page_reroute = True

    with col1:
        st.button("⬅️ Back", key="page3_back", on_click=go_back)

    with col2:
        st.button("Next ➡️", key="page3_next", on_click=go_next)

    if st.session_state.get("page_reroute"):
        st.session_state.page_reroute = False
        st.rerun()
