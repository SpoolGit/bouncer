import streamlit as st
import pandas as pd

def show_page7():
    st.title("IFRS15 Verdict")  

    with st.spinner("Doing Magic..."):
        import time
        time.sleep(2)
    st.success("Magician has given below Verdict!")

    # ----- Invoice Matching Table -----
    st.markdown("#### Detailed Invoice Matching:")

    invoice_data = [
        ["Inv #1", "Booking Set-up Installation Fee", "Wednesday, July 01, 2020", "Wednesday, April 01, 2020", 250000, 250000, "⚠️ Mismatch: Date"],
        ["Inv #2", "Booking Software License Fee", "Tuesday, December 29, 2020", "Tuesday, December 29, 2020", 25000, 25000, "✅ Match"],
        ["Inv #3", "Booking Software Support Fee", "Tuesday, December 29, 2020", "Tuesday, December 29, 2020", 10000, 10000, "✅ Match"],
        ["Inv #4", "Booking Software License Fee", "Tuesday, January 26, 2021", "Tuesday, January 26, 2021", 25000, 25000, "✅ Match"],
        ["Inv #5", "Booking Software Support Fee", "Tuesday, January 26, 2021", "Tuesday, January 26, 2021", 10000, 10000, "✅ Match"],
        ["Inv #6", "Booking Software License Fee", "Friday, February 26, 2021", "Friday, February 26, 2021", 25000, 25000, "✅ Match"],
        ["Inv #7", "Booking Software Support Fee", "Friday, February 26, 2021", "Friday, February 26, 2021", 10000, 10000, "✅ Match"],
        ["Inv #8", "Booking Product Support Fee", "Sunday, February 28, 2021", "Sunday, February 28, 2021", 25000, 25000, "✅ Match"],
        ["Inv #9", "Booking Software License Fee", "Monday, March 22, 2021", "Monday, March 22, 2021", 25000, 25000, "✅ Match"],
        ["Inv #10", "Booking Software Support Fee", "Monday, March 22, 2021", "Monday, March 22, 2021", 10000, 10000, "✅ Match"],
        ["Inv #12", "Booking Software License Fee", "Thursday, April 29, 2021", "Thursday, April 29, 2021", 25000, 25000, "✅ Match"],
        ["Inv #14", "Booking Software Support Fee", "Thursday, April 29, 2021", "Thursday, April 29, 2021", 10000, 10000, "✅ Match"],
        ["Inv #15", "Booking Software License Fee", "Saturday, May 29, 2021", "Saturday, May 29, 2021", 25000, 25000, "✅ Match"],
        ["Inv #16", "Booking Software Support Fee", "Saturday, May 29, 2021", "Sunday, May 29, 2022", 10000, 10000, "🚨 Mismatch: Cut-off"],
    ]
    invoice_columns = [
        "Invoice Number", "Description", "Receivable Date", "Revenue Date",
        "Receivable Amount", "Revenue Amount", "MATCH STATUS"
    ]
    invoice_df = pd.DataFrame(invoice_data, columns=invoice_columns)
    st.dataframe(invoice_df, use_container_width=True)

    # ----- Performance Obligation Summary Table -----
    st.markdown("#### Summary Table of Performance Obligations:")

    perf_data = [
        ["Installation Fee", 250000, "⚠️ Date mismatch"],
        ["Software License Fee", 150000, "None"],
        ["Software Support Fee", 85000, "🚨 Cut-off error (Inv #16)"],
        ["Product Support Fee", 25000, "None"],
    ]
    perf_columns = ["Performance Obligation", "Assigned Value", "Red Flags"]
    perf_df = pd.DataFrame(perf_data, columns=perf_columns)
    st.dataframe(perf_df, use_container_width=True)

    # ----- Final Summary -----
    st.markdown("### Final Summary:")
    st.markdown("- **Overall IFRS 15 compliance status:** ⚠️ Partially Compliant")
    st.markdown("- **Key risks or audit flags to escalate:**")
    st.markdown("  - Date mismatch for Inv #1 (Installation Fee recorded earlier in Revenue than in Receivables).")
    st.markdown("  - Cut-off error for Inv #16 (Revenue recorded a year later than in Receivables).")
    st.markdown("- **Additional documents required:**")
    st.markdown("  - Explanation for the date mismatch of Inv #1.")
    st.markdown("  - Clarification on the delayed revenue recognition for Inv #16.")

    # ----- Navigation -----
    col1, col2 = st.columns([1, 1])
    def go_back():
        st.session_state.page = 6
        st.session_state.selection = "IFRS 15 Analysis"
        st.session_state.page_reroute = True
    def go_next():
        st.session_state.page = 8
        st.session_state.selection = "TB Re-generation"
        st.session_state.page_reroute = True

    with col1:
        st.button("⬅️ Back", key="page7_back", on_click=go_back)

    with col2:
        st.button("Next ➡️", key="page7_next", on_click=go_next)
        
    if st.session_state.get("page_reroute"):
        st.session_state.page_reroute = False
        st.rerun()
