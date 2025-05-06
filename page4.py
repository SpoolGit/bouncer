import streamlit as st



def add_more_docs():
    if 'additional_docs' not in st.session_state:
        st.session_state.additional_docs = 0
    st.session_state.additional_docs += 1
    st.session_state.needs_rerun = True
    st.session_state.uploader_counter += 1   # force new uploader widget

def remove_trial_balance():
    if 'trial_balance_file' in st.session_state:
        del st.session_state.trial_balance_file
    st.session_state.needs_rerun = True
    st.session_state.uploader_counter += 1   # force new uploader widget

def remove_evidence_file(idx):
    if 'evidence_files' in st.session_state:
        if 0 <= idx < len(st.session_state.evidence_files):
            st.session_state.evidence_files.pop(idx)
    st.session_state.needs_rerun = True
    st.session_state.uploader_counter += 1   # force new uploader widget

def show_page4():
    st.markdown("""
        <h1 style="
            color: #3A5EFF;
            font-family: 'Segoe UI', sans-serif;
            font-size: 2.8rem;
            font-weight: 600;
            margin-bottom: 0.5em;">
            Bouncer: Magician Needs more...
        </h1>
    """, unsafe_allow_html=True)

    if 'user_info' in st.session_state and 'name' in st.session_state.user_info:
        st.write(f"Welcome, {st.session_state.user_info['name']}!")
    #else:
    #    st.error("User information missing. Please complete Page 1 first.")
        #return

    # NEW: Initialize uploader_counter if not present
    if 'uploader_counter' not in st.session_state:
        st.session_state.uploader_counter = 0

    st.subheader("Upload Files:")
    
    st.markdown("""
        <p style="font-size: 1.5rem; font-weight: 400; color: #3A5EFF;">
            Please upload precisely what Bouncer has asked for
        </p>
    """, unsafe_allow_html=True)

    

    # Upload Evidence Doc 1
    uploaded_evidence_doc1 = st.file_uploader(
        "Upload Evidence/Split-up Doc 1", 
        type=["pdf", "docx", "xlsx", "csv"], 
        key=f"evidence_doc1_upload_{st.session_state.uploader_counter}"  # dynamic key
    )
    if uploaded_evidence_doc1:
        if 'evidence_files' not in st.session_state:
            st.session_state.evidence_files = []
        st.session_state.evidence_files.append(uploaded_evidence_doc1)

    # Upload Additional Evidence Docs
    if 'additional_docs' not in st.session_state:
        st.session_state.additional_docs = 0

    for i in range(st.session_state.additional_docs):
        additional_uploaded_file = st.file_uploader(
            f"Upload Additional Evidence Doc {i+2}", 
            type=["pdf", "docx"],
            key=f"additional_evidence_{i}_{st.session_state.uploader_counter}"  # NEW: dynamic key
        )
        if additional_uploaded_file:
            if 'evidence_files' not in st.session_state:
                st.session_state.evidence_files = []
            st.session_state.evidence_files.append(additional_uploaded_file)

    st.button("+ Add More Evidence Docs", on_click=add_more_docs)

    # Display already uploaded files with delete buttons
    st.subheader("Uploaded Files So Far:")

    # Trial Balance
    if 'trial_balance_file' in st.session_state and st.session_state.trial_balance_file is not None:
        cols = st.columns([8, 1])
        with cols[0]:
            st.write(f"📊 Trial Balance: `{st.session_state.trial_balance_file.name}`")
        with cols[1]:
            if st.button("❌", key="remove_trial_balance"):
                remove_trial_balance()

    # Evidence Files
    if 'evidence_files' in st.session_state and st.session_state.evidence_files:
        for idx, file in enumerate(st.session_state.evidence_files):
            if file is not None:
                cols = st.columns([8, 1])
                with cols[0]:
                    st.write(f"📄 Evidence Doc {idx+1}: `{file.name}`")
                with cols[1]:
                    if st.button("❌", key=f"remove_evidence_{idx}"):
                        remove_evidence_file(idx)

    # End: Safe rerun if needed
    if st.session_state.get('needs_rerun', False):
        st.session_state.needs_rerun = False
        st.rerun()


    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])

    def go_back():
        st.session_state.page = 1
        st.session_state.selection = "Magic"
        st.session_state.page_reroute = True

    def go_next():
        st.session_state.page = 5
        st.session_state.selection = "Assertion Verdict"
        st.session_state.page_reroute = True

    with col1:
        st.button("⬅️ Back", key="page4_back", on_click=go_back)

    with col2:
        st.button("Next ➡️", key="page4_next", on_click=go_next)

    if st.session_state.get("page_reroute"):
        st.session_state.page_reroute = False
        st.rerun()
