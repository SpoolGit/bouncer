import streamlit as st
import pandas as pd
from io import StringIO
def show_page9():
   
    st.title("TB Regeneration Verdict")  

    with st.spinner("Doing Magic..."):
        import time
        time.sleep(2)
    st.success("Magician has given below Verdict!")

    # Function to extract and render CSV sections from text
    def display_csv_sections(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by section headings
        sections = content.split('### ')
        for section in sections:
            if not section.strip():
                continue

            lines = section.strip().split('\n')
            title = lines[0].strip()
            csv_data = '\n'.join(lines[1:]).strip('`\n ')

            # Try reading the CSV string into DataFrame
            try:
                df = pd.read_csv(StringIO(csv_data))
                st.subheader(title)
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.warning(f"Could not parse section '{title}': {e}")

    file_path = "out_9.csv"
    display_csv_sections(file_path)

    # ----- Navigation -----
    col1, col2 = st.columns([1, 1])
    def go_back():
        st.session_state.page = 8
        st.session_state.selection = "TB Re-generation"
        st.session_state.page_reroute = True

    with col1:
        st.button("⬅️ Back", key="page9_back", on_click=go_back)

    if st.session_state.get("page_reroute"):
        st.session_state.page_reroute = False
        st.rerun()
