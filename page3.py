import streamlit as st
import pandas as pd
import pdfplumber
import io
import streamlit.components.v1 as components

def show_page3():
    st.title("Assertions & Reconcilliation")  

    with st.spinner("Doing Magic..."):
        # Simulate backend call
        import time
        time.sleep(2)
    st.success("Below is what our Buncing Magician Thinks!")
    
        # Insert audit explanation block
    st.markdown("""
        <style>
            .audit-section h2 {
                color: #3A5EFF;
                font-size: 1.8rem;
                font-weight: 700;
                margin-top: 2rem;
                margin-bottom: 1rem;
            }
            .audit-section h3 {
                font-size: 1.4rem;
                font-weight: 600;
                color: #444;
                margin-top: 1rem;
            }
            .audit-section p, .audit-section li {
                font-size: 1.05rem;
                line-height: 1.6;
                color: #222;
            }
            .audit-section ul {
                padding-left: 1.2rem;
            }
            .audit-box {
                background-color: #f5f8ff;
                border-left: 5px solid #3A5EFF;
                padding: 1rem;
                margin-top: 1rem;
                border-radius: 6px;
            }
        </style>
        <div class="audit-box">
            <h2>Step 1</h2>
            <h3>📌 ASSERTION-BASED DOCUMENT REQUEST LIST</h3>
            <p>For each of the 7 assertions, I would request the following documents for a selected sample (details below):</p>
            <ul>
                <li><strong>1. "Agree to underlying contracts/invoices"</strong>
                    <br>&emsp;✔️ Signed contracts with customers
                    <br>&emsp;✔️ Original invoices issued
                </li>
                <li><strong>2. "Verify evidence of delivery/performance"</strong>
                    <br>&emsp;✔️ Timesheets
                    <br>&emsp;✔️ Email delivery confirmations
                    <br>&emsp;✔️ Signed work acceptance forms from clients
                    <br>&emsp;✔️ Consulting logs or outputs delivered
                </li>
                <li><strong>3. "Trace to cash receipt or receivable ledger"</strong>
                    <br>&emsp;✔️ Bank statement extract for December/January
                    <br>&emsp;✔️ Receivables ledger (Aged AR)
                </li>
                <li><strong>4. "Ensure recognition in correct period"</strong>
                    <br>&emsp;✔️ Invoice date and service period breakdown
                    <br>&emsp;✔️ Accounting policy on revenue recognition
                    <br>&emsp;✔️ GL entries with dates
                </li>
                <li><strong>5. "Trace invoice to ledger"</strong>
                    <br>&emsp;✔️ Invoice copies
                    <br>&emsp;✔️ General ledger (already uploaded)
                </li>
                <li><strong>6. "Trace ledger to invoice"</strong>
                    <br>&emsp;✔️ GL dump with invoice number/description field
                    <br>&emsp;✔️ Original matching invoices
                </li>
                <li><strong>7. "Identify if revenue recognised in FY was subsequently reversed"</strong>
                    <br>&emsp;✔️ Jan–Feb 2025 general ledger extract
                    <br>&emsp;✔️ Credit notes, if any issued in Jan/Feb
                    <br>&emsp;✔️ Reversals or adjustments journal vouchers
                </li>
            </ul>
        </div>

        <div class="audit-box">
            <h3>🔎 SAMPLING STRATEGY</h3>
            <ul>
                <li>✔️ Suggested: Monetary Unit Sampling (MUS)</li>
                <li>Select high-value entries first (e.g. >£4,000)</li>
                <li>Then use MUS to randomly select based on £ values</li>
            </ul>
            <p><strong>✔️ Materiality Assumption:</strong><br>
            Planning Materiality: £5,000<br>
            Performance Materiality: £3,500</p>
            <p>Invoices like £8,000 and £4,658 will be automatically selected.</p>
        </div>

        <div class="audit-box">
            <h3>✅ JUSTIFICATION</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr><th style="text-align:left; padding: 0.3rem;">🔍 Objective</th><th style="text-align:left; padding: 0.3rem;">📂 Justification</th></tr>
                <tr><td>Agreement to contracts</td><td>Confirms that revenue was based on real, agreed-upon services</td></tr>
                <tr><td>Evidence of performance</td><td>Substantiates actual delivery of service before recognition</td></tr>
                <tr><td>Trace to cash / AR ledger</td><td>Validates collection or legitimate receivable (existence of asset)</td></tr>
                <tr><td>Cut-off testing</td><td>Detects premature or deferred revenue — crucial for period-end assertions</td></tr>
                <tr><td>Invoice-to-ledger and reverse</td><td>Ensures all recorded revenues are traceable both ways and detects manipulations</td></tr>
                <tr><td>Reversal testing in next period</td><td>Detects fictitious revenue booked in Dec and reversed in Jan</td></tr>
                <tr><td>Sampling and materiality basis</td><td>Focuses audit effort on high-risk items and avoids over-testing</td></tr>
            </table>
        </div>
            <br>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    def go_back():
        st.session_state.page = 2
        st.session_state.selection = "Document Upload"
        st.session_state.page_reroute = True

    def go_next():
        st.session_state.page = 4
        st.session_state.selection = "Supplementary Upload"  # hypothetical next section
        st.session_state.page_reroute = True

    with col1:
        st.button("⬅️ Back", key="page3_back", on_click=go_back)

    with col2:
        st.button("Next ➡️", key="page3_next", on_click=go_next)

    if st.session_state.get("page_reroute"):
        st.session_state.page_reroute = False
        st.rerun()
