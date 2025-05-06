import streamlit as st
def show_page1():
    st.image("data/logo_full.png", use_container_width=True)

    st.markdown("""
        <style>
            .btn-wrapper {
                display: flex;
                justify-content: center;
                margin-top: 2rem;
            }
            .try-btn {
                background-color: #f4cd59;
                color: black;
                font-size: 1.5rem;
                font-style: italic;
                font-family: 'Segoe UI', sans-serif;
                padding: 0.75rem 2rem;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .try-btn:hover {
                background-color: #eec944;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    def go_back():
        st.session_state.page = 1
        st.session_state.selection = "Welcome"
        st.session_state.page_reroute = True

    def go_next():
        st.session_state.page = 3
        st.session_state.selection = "Document Upload"
        st.session_state.page_reroute = True


    with col2:
        st.button("Try it ➡️", key="page1_next", on_click=go_next)

    if st.session_state.get("page_reroute"):
        st.session_state.page_reroute = False
        st.rerun()


