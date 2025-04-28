import streamlit as st

def add_more_docs():
    if 'additional_docs' not in st.session_state:
        st.session_state.additional_docs = 0
    st.session_state.additional_docs += 1

def show_page2():
    st.title("Document Upload")
    
    if 'user_info' in st.session_state and 'name' in st.session_state.user_info:
        st.write(f"Welcome, {st.session_state.user_info['name']}!")

    st.file_uploader("Upload Trial Balance", type=["xlsx", "csv"])
    st.file_uploader("Upload Evidence Doc 1", type=["pdf", "docx"])
    
    if 'additional_docs' not in st.session_state:
        st.session_state.additional_docs = 0
    
    for i in range(st.session_state.additional_docs):
        st.file_uploader(f"Upload Additional Evidence Doc {i+2}", type=["pdf", "docx"])
    
    st.button("+ Add More Evidence Docs", on_click=add_more_docs)