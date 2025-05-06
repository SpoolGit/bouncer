import streamlit as st
from page2 import show_page2
import time
import json

def show_uInfo():
    st.info(" Enter as much information as you can for an accurate provisional audit report.")

    # Initialize session state
    if "audit_step" not in st.session_state:
        st.session_state.audit_step = 1

    if "audit_inputs" not in st.session_state:
        st.session_state.audit_inputs = {
            "generic": {},
            "revenue": {}
        }
    @st.cache_data
    def load_audit_metadata():
        with open("data/audit_metadata_structured.json", "r") as f:
            return json.load(f)

    audit_metadata = load_audit_metadata()

   
    def process_and_call_AI():
        with st.spinner("Calling OpenAI..."):
            generic_info = st.session_state.audit_inputs.get("generic", {})
            
            # Build natural-sounding prompt from key-value pairs
            lines = []
            for key, value in generic_info.items():
                if value:  # Only include non-empty fields
                    pretty_key = key.replace("_", " ").capitalize()
                    lines.append(f"{pretty_key}: {value}")

            # Combine lines into final prompt
            formatted_generic_info = "\n".join(lines)
            prompt = f"Please find below the company generic information:\n\n{formatted_generic_info}"

            # You can now use this with OpenAI:
            # openai.ChatCompletion.create(...)

            # For now just display the prompt:
            st.text_area("Generated Prompt", prompt, height=300)

            # Simulate delay            
            time.sleep(2)
            
            st.success("Prompt built and (optionally) sent to backend.")            
    
    def finish_clicked():           
        process_and_call_AI()
        st.session_state.page = 2
        st.session_state.selection = "Document Upload"
        st.session_state.page_reroute = True  # trigger rerun
        
    def next_step():
        st.session_state.audit_step += 1

    def previous_step():
        st.session_state.audit_step -= 1

    if st.session_state.audit_step == 1:
        st.subheader("Step 1: Generic Information")
        g = st.session_state.audit_inputs["generic"]  # shortcut

        g["company_name"] = st.text_input("Company name", g.get("company_name", ""))
        g["legal_structure"] = st.text_input("Legal structure", g.get("legal_structure", ""))
        g["FY_Dates"] = st.text_input("FY dates", g.get("FY_Dates", ""))
        
        g["services"] = st.text_area("Services offered (with examples)", g.get("services", ""))
        g["revenue_model"] = st.text_area("Revenue model (recurring? project-based? etc.)", g.get("revenue_model", ""))
        g["billing_method"] = st.text_area("Billing method (upfront, milestone, completion)", g.get("billing_method", ""))
        g["key_clients"] = st.text_area("Key clients (volume vs. high value)", g.get("key_clients", ""))
        g["tools_used"] = st.text_area("Tools used (CRM, invoicing, accounting software)", g.get("tools_used", ""))
        g["industry"] = st.selectbox("Industry and subsector", ["Tech", "Finance", "Healthcare", "Other"],
                                     index=["Tech", "Finance", "Healthcare", "Other"].index(g.get("industry", "Tech")))
        g["customer_types"] = st.text_area("Customer types and geographies", g.get("customer_types", ""))
        g["ownership_structure"] = st.text_input("Ownership structure", g.get("ownership_structure", ""))
        g["num_employees"] = st.number_input("Number of employees", min_value=0, step=1, value=g.get("num_employees", 0))
        g["company_size"] = st.text_area("Company size (Revenue, Assets)", g.get("company_size", ""))
        g["audit_committee"] = st.text_area("Board / audit committee presence?", g.get("audit_committee", ""))
        g["related_parties"] = st.text_area("Are there related parties (e.g., customers owned by shareholders)?", g.get("related_parties", ""))
        g["management_incentives"] = st.text_area("Are there management incentives tied to revenue?", g.get("management_incentives", ""))

        st.button("Next ➡️", on_click=next_step)

    elif st.session_state.audit_step == 2:
        st.subheader("Step 2: Revenue Specific Questions")
        r = st.session_state.audit_inputs["revenue"]  # shortcut

        r["revenue_recognition"] = st.text_area("How is revenue earned and recognized?", r.get("revenue_recognition", ""))
        r["contracts"] = st.text_area("Are contracts involved? If yes, are they standardized or custom?", r.get("contracts", ""))
        r["deferred_revenue"] = st.text_area("Is there deferred revenue or prepayments?", r.get("deferred_revenue", ""))
        r["systems_used"] = st.text_input("What systems (ERP/accounting) are used to record revenue?", r.get("systems_used", ""))
        r["collection_period"] = st.text_input("What is the average collection period? What is the policy approved by the company?", r.get("collection_period", ""))
        r["segregation_duties"] = st.text_input("Is there segregation of duties between collection, recording and approval?", r.get("segregation_duties", ""))
        r["access_logs"] = st.text_area("Are there system access logs?", r.get("access_logs", ""))
        r["journal_approval"] = st.text_input("Who approves journal entries?", r.get("journal_approval", ""))
        r["review_process"] = st.text_input("Are revenues reviewed periodically?", r.get("review_process", ""))
        r["contract_type"] = st.text_area("Are contracts fixed fee or variable? Any performance obligations?", r.get("contract_type", ""))
        r["billing_process"] = st.text_area("Is billing automated? How many invoices/month?", r.get("billing_process", ""))

        col1, col2 = st.columns([1, 1])
        with col1:
            st.button("⬅️ Back", on_click=previous_step)
        with col2:
            st.button("Finish ✅", on_click=finish_clicked)

        if st.session_state.get("page_reroute"):
            #time.sleep(3)
            st.session_state.page_reroute = False
            st.rerun() 
