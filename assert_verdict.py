import streamlit as st
import pandas as pd
import pdfplumber
import io
import streamlit.components.v1 as components

def show_assert_verdict():
    st.title("Assertions Verdict")  

    with st.spinner("Doing Magic..."):
        # Simulate backend call
        import time
        time.sleep(2)
    st.success("Bouncing Magician has given below Verdict!")
    
    if st.button("⬅️ Back to Stats page", key="assert_back_1"):
        st.session_state.page = 'stats'
        st.rerun()
        
    # Insert audit explanation block

    st.markdown("""    
    <style>
    .audit-step {
        background-color: #f5f8ff;
        border-left: 5px solid #28a745;
        padding: 1.5rem;
        border-radius: 8px;
        font-family: 'Segoe UI', sans-serif;
        margin-top: 2rem;
    }
    .audit-step h2 {
        color: #2b5fc7;
        font-size: 1.6rem;
        margin-bottom: 1rem;
    }
    .audit-step h3 {
        font-size: 1.3rem;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        color: #000;
    }
    .audit-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1rem;
        font-size: 1.05rem;
    }
    .audit-table th, .audit-table td {
        border: 1px solid #ccc;
        padding: 0.6rem;
        text-align: left;
        vertical-align: top;
    }
    .audit-table th {
        background-color: #e6f0ff;
        font-weight: bold;
    }
    .passed {
        color: green;
        font-weight: bold;
    }
    .failed {
        color: red;
        font-weight: bold;
    }
    .inconclusive {
        color: orange;
        font-weight: bold;
    }
    .audit-note {
        margin-top: 1.5rem;
        padding: 1rem;
        background-color: #fff8e6;
        border-left: 4px solid #ffc107;
        border-radius: 6px;
    }
</style>
<div class="audit-step">
    <h2>Step 2</h2>
    <h3>✅ Assertion Evaluation Table</h3>
    <table class="audit-table">
        <tr>
            <th>#</th>
            <th>Assertion</th>
            <th>Result</th>
            <th>Justification</th>
        </tr>
        <tr>
            <td>1</td>
            <td>Agree to underlying contracts/invoices</td>
            <td class="passed">✅ Passed</td>
            <td>Both invoices are available, complete, addressed to the correct client (Blox Tech Solution FZ-LLC), and contain matching line items.</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Verify evidence of delivery/performance</td>
            <td class="inconclusive">⚠️ Inconclusive</td>
            <td>No delivery logs, timesheets, emails, or work acceptance reports were provided to confirm that services were delivered.</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Trace to cash receipt or receivable ledger</td>
            <td class="passed">✅ Passed</td>
            <td>Revolut statement dated Dec 27, 2024 clearly shows £12,658 received from Blox Tech Solution, which exactly matches £8,000 (Inv 79) + £4,658 (Inv 78).</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Ensure recognition in correct period</td>
            <td class="failed">❌ Failed</td>
            <td>Invoices dated Dec 2, 2024, but previous GL review showed they were recorded in January, not December — violating cut-off.</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Trace invoice to ledger</td>
            <td class="passed">✅ Passed</td>
            <td>Previously matched both invoices 78 and 79 to general ledger entries (though they were posted in Jan). Amounts match exactly.</td>
        </tr>
        <tr>
            <td>6</td>
            <td>Trace ledger to invoice</td>
            <td class="passed">✅ Passed</td>
            <td>GL entries labeled with invoice numbers 78 and 79 can be traced directly back to corresponding PDF invoices.</td>
        </tr>
        <tr>
            <td>7</td>
            <td>Identify if revenue recognised in FY was subsequently reversed</td>
            <td class="passed">✅ Passed</td>
            <td>No reversal or credit note is visible for these entries in the Jan–Apr Revolut bank statement. Revenue appears to be sustained.</td>
        </tr>
    </table>
    <h3>📌 Summary of Failures and Gaps</h3>
    <div class="audit-note">
        <strong>Assertion 2 (Evidence of Delivery):</strong> Missing timesheets, confirmations, or work logs.<br><br>
        <strong>Assertion 4 (Cut-off):</strong> Revenue was recorded in January despite being invoiced and (likely) earned in December.
    </div>
    <h3>📄 Recommendation to Rectify</h3>
    <div class="audit-note">
        Upload delivery logs, project files, or signed confirmations from the client to satisfy delivery evidence (<strong>Assertion 2</strong>).<br><br>
        Adjust accounting period via journal entry to accrue this revenue into December (<strong>Assertion 4</strong>) or provide accounting policy if deferral was intentional and consistent.
    </div>
</div> 
<br>   
    """, unsafe_allow_html=True)


    if st.button("⬅️ Back to Stats page"):
        st.session_state.page = 'stats'
        st.rerun()
