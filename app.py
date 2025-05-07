import streamlit as st

st.set_page_config(page_title="Multi-Page App", layout="wide")

# Import page functions
from page1 import show_page1
from page2 import show_page2
from page3 import show_page3
from page4 import show_page4
from page5 import show_page5
from page6 import show_page6
from page7 import show_page7
from uInfo import show_uInfo

#from page4_audit_inputs import show_page4
params = st.query_params
if "page" in params:
    if params["page"] == "pg1":
        st.session_state.page = 1
        st.session_state.selection = "Welcome"
    elif params["page"] == "pg2":
        st.session_state.page = 2
        st.session_state.selection = "Document Upload"
    elif params["page"] == "pg6":
        st.session_state.page = 6
        st.session_state.selection = "IFRS 15 Analysis"
        
# Initialize routing state
if "page" not in st.session_state:
    st.session_state.page = None  # for programmatic routing

if "selection" not in st.session_state:
    st.session_state.selection = "Welcome"  # sidebar default

if "active_selection" not in st.session_state:
    st.session_state.active_selection = "Welcome"  # track user change

def main():

    # Sidebar radio
    sidebar_options = ["Welcome", "Document Upload", "Magic", "Supplementary Upload", "Assertion Verdict", "IFRS 15 Analysis", "IFRS 15 Verdict"]
    selection = st.sidebar.radio(
        "Go to",
        sidebar_options,
        index=sidebar_options.index(st.session_state.selection),
        key="selection"
    )

    # Detect manual user change
    if st.session_state.selection != st.session_state.active_selection:
        st.session_state.page = None
        st.session_state.active_selection = st.session_state.selection

    # --------------------
    # ROUTING
    # --------------------

    if st.session_state.page is not None:
        # Programmatic routing
        if st.session_state.page == 1:
            st.session_state.selection = None
            show_page1()
        elif st.session_state.page == 2:
            st.session_state.selection = None
            show_page2()
        elif st.session_state.page == 3:
            st.session_state.selection = None
            show_page3()
        elif st.session_state.page == 4:
            st.session_state.selection = None
            show_page4()
        elif st.session_state.page == 5:
            st.session_state.selection = None
            show_page5()
        elif st.session_state.page == 6:
            st.session_state.selection = None
            show_page6()
        elif st.session_state.page == 7:
            st.session_state.selection = None
            show_page7()
    else:
        # Manual sidebar routing
        if st.session_state.selection == "Welcome":
            show_page1()
        elif st.session_state.selection == "Document Upload":
            #if 'user_info' in st.session_state and st.session_state.user_info.get('name') and st.session_state.user_info.get('email'):
            # show_page2()
            #else:
            #    st.error("Please fill in the mandatory fields (Name and Email) on the User Information page before accessing this page.")
            #    show_page1()
            show_page2()
        elif st.session_state.selection == "Magic":
            show_page3()
        elif st.session_state.selection == "Supplementary Upload":
            show_page4()
        elif st.session_state.selection == "Assertion Verdict":
            show_page5()
        elif st.session_state.selection == "IFRS 15 Analysis":
            show_page6()
        elif st.session_state.selection == "IFRS 15 Verdict":
            show_page7()
        #elif st.session_state.selection == "Audit Inputs":
        #    show_page4()

if __name__ == "__main__":
    main()
    
    
