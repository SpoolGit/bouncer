import streamlit as st
from page1 import show_page1
from page2 import show_page2
from page3 import show_page3

st.set_page_config(page_title="Multi-Page App", layout="wide")

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["User Information", "Document Upload", "API Call"])

    if selection == "User Information":
        show_page1()
    elif selection == "Document Upload":
        if 'user_info' in st.session_state and st.session_state.user_info.get('name') and st.session_state.user_info.get('email'):
            show_page2()
        else:
            st.error("Please fill in the mandatory fields (Name and Email) on the User Information page before accessing this page.")
            show_page1()
    elif selection == "API Call":
        if 'user_info' in st.session_state and st.session_state.user_info.get('name') and st.session_state.user_info.get('email'):
            show_page3()
        else:
            st.error("Please fill in the mandatory fields (Name and Email) on the User Information page before accessing this page.")
            show_page1()

if __name__ == "__main__":
    main()