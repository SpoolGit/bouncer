import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from scipy.stats import zscore
import holidays
import re
from io import StringIO
import time
import pdfplumber
import openai
import json


def verdict_icon(val):
    if val is True:
        return "✅ Yes"
    elif val is False:
        return "❌ No"
    elif val in ["none", None]:
        return "⚠️ Not Available"
    return str(val)

def display_llm_verdict_pretty(df):
    if df.empty:
        st.info("⚠️ No assertion results to display.")
        return

    for i, row in df.iterrows():
        st.markdown(f"### 📄 `{row.get('file_name', 'Unknown File')}`")
        with st.container():
            cols = st.columns(2)

            # Left column - Invoice metadata
            with cols[0]:
                st.markdown(f"**Subtotal (before VAT):** £{row.get('subtotal_before_vat', 'N/A')}")
                st.markdown(f"**Total (after VAT):** £{row.get('total_after_vat', 'N/A')}")
                st.markdown(f"**Customer Name:** {row.get('customer_name', 'N/A')}")
                st.markdown(f"**Matched Amount Type:** `{row.get('matched_amount_type', 'N/A')}`")
                st.markdown(f"**Amount Difference:** £{row.get('amount_difference', 'N/A')}")

            # Right column - Verdicts
            with cols[1]:
                st.markdown(f"**Subtotal Match:** {verdict_icon(row.get('does_subtotal_match'))}")
                st.markdown(f"**Total Match:** {verdict_icon(row.get('does_total_match'))}")
                st.markdown(f"**Customer Match:** {verdict_icon(row.get('does_customer_match'))}")
                st.markdown(f"**Exact Date Match:** {verdict_icon(row.get('does_invoice_date_match_exact'))}")
                st.markdown(f"**Same Month:** {verdict_icon(row.get('is_same_month'))}")
                st.markdown(f"**Cut-off Issue:** {verdict_icon(row.get('is_cutoff_issue'))}")
                mismatch_reason = row.get("mismatch_reason") or row.get("cutoff_issue_description")
                if mismatch_reason:
                    st.markdown(f"**📝 Reason:** _{mismatch_reason}_")

        st.markdown("---")

def extract_text_from_csv(uploaded_file_path):
    try:
        # Read file content as raw text
        with open(uploaded_file_path, 'r', encoding='utf-8', errors='replace') as f:
            raw_text = f.read()

        # Determine the likely separator
        first_line = raw_text.split('\n')[0]
        if first_line.count(',') > first_line.count(';') and first_line.count(',') > first_line.count('\t'):
            sep = ','
        elif first_line.count(';') > first_line.count('\t'):
            sep = ';'
        else:
            sep = '\t'

        # Parse the raw text into a DataFrame
        df = pd.read_csv(StringIO(raw_text), sep=sep, engine='python')

        return df.to_string()

    except Exception as e:
        return f"Error reading CSV: {e}"

def extract_text_from_csv_from_session(row_key: str):
    uploaded_files = st.session_state.get(f"uploaded_{row_key}", [])
    if not uploaded_files:
        return "⚠️ No uploaded files found for this row."

    output = ""

    try:
        for file in uploaded_files:
            if "csv" not in file.type.lower():
                continue  # Skip non-CSV files

            # Read file content as text
            raw_text = file.read().decode('utf-8', errors='replace')

            # Detect separator
            first_line = raw_text.split('\n')[0]
            if first_line.count(',') > first_line.count(';') and first_line.count(',') > first_line.count('\t'):
                sep = ','
            elif first_line.count(';') > first_line.count('\t'):
                sep = ';'
            else:
                sep = '\t'

            # Convert to DataFrame
            df = pd.read_csv(StringIO(raw_text), sep=sep, engine='python')
            output += f"--- CSV File: {file.name} ---\n"
            output += df.to_string(index=False)
            output += "\n\n"

        return output.strip() if output else "No valid CSV text found in uploaded files."

    except Exception as e:
        return f"❌ Error reading CSV(s): {e}"


def extract_text_from_pdf(pdf_file_path):
    try:
        all_text = ""
        with pdfplumber.open(pdf_file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text += text + "\n"
        return all_text.strip() if all_text else "No text found in PDF."
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_text_from_pdf_from_session(row_key: str):
    uploaded_files = st.session_state.get(f"uploaded_{row_key}", [])
    if not uploaded_files:
        return "⚠️ No uploaded files found for this row."

    all_text = ""
    try:
        for file in uploaded_files:
            if "pdf" not in file.type.lower():
                continue  # Skip non-PDF files

            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        all_text += text + "\n"

        return all_text.strip() if all_text else "No text found in any uploaded PDFs."
    except Exception as e:
        return f"❌ Error reading PDF(s): {e}"

def clean_amount(val):
    if pd.isna(val) or str(val).strip() == '':
        return 0
    val = str(val).upper()
    val = re.sub(r'[^\d\.-]', '', val)  # keep digits, dot, minus only
    try:
        return float(val)
    except:
        return 0

def extract_account_rows_from_CSV(file_path, account_name):
    try:
        # Read file content as raw text
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            raw_text = f.read()

        # Normalize the account name for comparison
        account_name_clean = account_name.strip().lower()

        # Find all lines that contain the account name (case-insensitive)
        lines = raw_text.splitlines()
        matching_lines = []

        for line in lines:
            if account_name_clean in line.strip().lower():
                matching_lines.append(line)

        return "\n".join(matching_lines) if matching_lines else "No matching rows found."

    except Exception as e:
        return f"Error reading CSV: {e}"

        
def get_account_balance_data (file_path):

  # Read file content as raw text
  with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
      raw_text = f.read()
      #print(raw_text)

  # Determine the likely separator
  first_line = raw_text.split('\n')[0]
  if first_line.count(',') > first_line.count(';') and first_line.count(',') > first_line.count('\t'):
      sep = ','
  elif first_line.count(';') > first_line.count('\t'):
      sep = ';'
  else:
      sep = '\t'

  # Parse the raw text into a DataFrame
  df = pd.read_csv(StringIO(raw_text), sep=sep, engine='python', header=None)
  #print(df.columns.tolist())


  # Find the row index where the actual data starts
  flag = False
  # Init result dicts
  account_debits = {}
  account_credits = {}

  for i, row in df.iterrows():
      row_lower = row.astype(str).str.lower().tolist()
      #print(row_lower)

      if (
          any('account' in cell for cell in row_lower)
          and any('debit' in cell for cell in row_lower)
          and any('credit' in cell for cell in row_lower)
      ):
        #print("@@@")
        flag = True
        continue

      if flag:
          # Now row_lower is the actual data row (a list), get by index
          #print(row_lower)
          try:
              acc = str(row_lower[0]).strip()
              # IF
              if len(row_lower) > 4:
                  debit_raw = row_lower[3]
                  credit_raw = row_lower[4]
              elif len(row_lower) > 2:
                  debit_raw = row_lower[1]
                  credit_raw = row_lower[2]
              else:
                  debit_raw = '0'
                  credit_raw = '0'
          except IndexError:
              continue  # skip rows with missing values

          # Parse debit
          try:
              debit = clean_amount(debit_raw)
          except:
              debit = 0

          # Parse credit
          try:
              credit = clean_amount(credit_raw)
          except:
              credit = 0

          # Accumulate
          account_debits[acc] = account_debits.get(acc, 0) + debit
          account_credits[acc] = account_credits.get(acc, 0) + credit

  total_balance = 0
  output_str = ""

  for acc in sorted(set(account_debits) | set(account_credits)):
      output_str += f"Account: {acc}\n"
      total_balance += (account_debits.get(acc, 0) + account_credits.get(acc, 0))
      output_str += f"  Total Debit:  £{account_debits.get(acc, 0):,.2f}\n"
      output_str += f"  Total Credit: £{account_credits.get(acc, 0):,.2f}\n\n"

  #print(output_str)
  return total_balance
  
  
def get_stats_csv ():
    # Get uploaded file from session
    uploaded_file = st.session_state.get("test_gl")

    if uploaded_file is None:
        st.warning("No file uploaded in user inputs.")
        return pd.DataFrame()  # or raise Exception or return None
    
    try:
        uploaded_file.seek(0)  # rewind
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return pd.DataFrame()

    # Dynamically find debit and credit columns
    debit_col = [col for col in df.columns if 'debit' in col.lower()][0]
    credit_col = [col for col in df.columns if 'credit' in col.lower()][0]
    #balance_col = [col for col in df.columns if 'balance' in col.lower()][0]

    # Clean and convert values
    df['debit_clean'] = pd.to_numeric(df[debit_col].replace('[£,]', '', regex=True), errors='coerce')
    df['credit_clean'] = pd.to_numeric(df[credit_col].replace('[£,]', '', regex=True), errors='coerce')
    #df['balance_clean'] = pd.to_numeric(df[balance_col].replace('[£,]', '', regex=True), errors='coerce')

    # Compute Amount column
    df['Amount'] = df['debit_clean'].fillna(0) + df['credit_clean'].fillna(0)

    # Drop invalid rows
    df = df.dropna(subset=['Amount'])

    # Compute stats
    df['Z_score'] = zscore(df['Amount']).round(2)
    df['LeadingDigit'] = pd.to_numeric(df['Amount'].astype(str).str.extract(r'([1-9])')[0], errors='coerce').fillna(0).astype(int)
    df['Rounded'] = df['Amount'] % 1 == 0
    df['Precision'] = df['Amount'] % 1

    # Add global stats for the column (same value repeated for all rows)
    df['Mean'] = round(df['Amount'].mean(), 2)
    df['Median'] = round(df['Amount'].median(), 2)
    df['StdDev'] = round(df['Amount'].std(), 2)

    # KMeans Clustering
    kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
    df['K_means Cluster'] = kmeans.fit_predict(df[['Amount']])
    # Step 1: Get the cluster centers
    centers = kmeans.cluster_centers_.flatten()

    # Step 2: Sort cluster labels by ascending center value
    sorted_labels = np.argsort(centers)

    # Step 3: Create a mapping from label to string
    label_map = {sorted_labels[0]: 'Low', sorted_labels[1]: 'Medium', sorted_labels[2]: 'High'}

    # Step 4: Apply the mapping
    df['K_means Lable'] = df['K_means Cluster'].map(label_map)


    # Step 1: Detect the date column (case-insensitive search for 'date')
    date_col = next((col for col in df.columns if 'date' in col.lower()), None)
    if not date_col:
        raise ValueError("No column with 'date' in the name found.")

    # Step 2: Parse the date column
    df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors='coerce')  # adjust dayfirst=True/False based on format

    # Step 3: Add Weekend column (Saturday=5, Sunday=6)
    df['Weekend'] = df[date_col].dt.weekday >= 5

    # Step 4: Add Holiday column (using UK public holidays)
    uk_holidays = holidays.CountryHoliday('UK')
    df['Holiday'] = df[date_col].isin(uk_holidays)

    # Step 5: Add EvenDollar column (checks if decimal part is exactly .00)
    df['EvenDollar'] = df['Amount'].apply(lambda x: float(x).is_integer() and str(x).endswith('.00'))

    df = df.drop(debit_col, axis=1)
    df = df.drop(credit_col, axis=1)
    #df = df.drop(balance_col, axis=1)
    df = df.drop('K_means Cluster', axis=1)
    st.session_state["stats_df"] = df

    return df
    
# Fix the malformed lines by quoting the 4th field if it contains comma
def fix_csv_text(csv_text):
    fixed_lines = []
    lines = csv_text.strip().split('\n')
    header = lines[0]
    fixed_lines.append(header)

    for line in lines[1:]:
        parts = line.split(',')
        if len(parts) > 6:
            # Fixing by assuming 4th field may contain commas
            fixed_line = ','.join(parts[:3] + ['"' + ','.join(parts[3:-2]).strip() + '"'] + parts[-2:])
            fixed_lines.append(fixed_line)
        else:
            fixed_lines.append(line)
    return '\n'.join(fixed_lines)
    
def get_llm_sampling_csv ():
    
    try:
        stats_df = st.session_state.get("stats_df")

        if stats_df is None or not isinstance(stats_df, pd.DataFrame) or stats_df.empty:
            st.warning("⚠️ No statistics DataFrame found in session or it is empty.")
            return pd.DataFrame()
        
        cleaned_csv_text = st.session_state.get("stats_df").to_csv(index=False)
        #print(cleaned_csv_text)

        reconciliation_prompt = """
        You are a senior audit data analytics assistant.

        You are given a dataset where each transaction has the following fields:
        DATE, DESCRIPTION, debit_clean, credit_clean, balance_clean, Amount, Z_score, LeadingDigit, Rounded, Precision, Mean, Median, StdDev, 
        K_means Cluster, Cluster Label, Weekend, Holiday, EvenDollar.

        Using this data, perform the following checks and mark each transaction with appropriate audit flags:

        1. **Verify sequential transaction numbering** – flag if any transaction appears out of sequence based on date order.
        2. **Identify duplicate account structures** – flag if two or more transactions have the same DATE, DESCRIPTION, and AMOUNT.
        3. **Identify blank or null fields in critical data** – flag if any of DATE, DESCRIPTION, or AMOUNT is missing or null.
        4. **Test for impossible values** – flag if Amount < 0, or dates in the future.
        5. **Identify nonsensical descriptions or coding** – flag if DESCRIPTION contains only special characters, numeric-only values, 
        or generic placeholders like “test,” “xx,” “...” etc.
        6. **Identify round number transactions** – flag if Precision = 0 and Rounded is TRUE.
        7. **Detect unusually large transactions relative to account average** – flag if Z_score > 2.5 or Amount > Mean + 2 * StdDev.
        8. **Test for unusual even-dollar amounts** – flag if Amount is a large round figure and EvenDollar is TRUE.
        9. **Identify recurring identical amounts to same vendors** – flag repeating amounts and descriptions across different dates.
        10. **Identify transactions posted on weekends or holidays** – flag if Weekend = TRUE or Holiday = TRUE.
        11. **Detect unusual concentration of entries at period-end** – flag if DATE is in last 3 days of any month and volume spikes.
        12. **Identify transactions posted after business hours** – (if timestamp is available), flag if posted outside 9am–6pm.
        13. **Use propoer materiality and proper sampling method, and based on that, flag if tranasction needs to be sampled ** 
        select propoer amount of transactions for sampling  

        Return the result as a CSV table with these columns:
        - DATE
        - DESCRIPTION
        - AMOUNT
        - Anomaly Flags (reasons why flagged, DO NOT USE COMMA HERE)
        - Is High Risk? (TRUE/FALSE, based on combination of red flags)
        - Is selected for Sampling (TRUE/FALSE)

        Do not hallucinate data. Only use what is present. If a rule can’t be applied (e.g., timestamp not available), skip it.

        Output ONLY the final result as CSV.


        Here is the data:



        {{Account_GL_Data}}
        """

        final_prompt = reconciliation_prompt.replace('{{Account_GL_Data}}', cleaned_csv_text)

        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]  
        isDummy = st.secrets["Dummy"]

        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        messages_1 = [
            {
                "role": "system",
                "content": "You are a financial data reconciliation and audit assertiosn expert.",
            },
            {
                "role": "user",
                "content": final_prompt,
            },
        ]

        ##print(final_prompt)
        if isDummy == True: 
            time.sleep(2) 
            #csv_path = "outputs/Meals 2024_sampling_out.csv"  
            #df_llm = pd.read_csv(csv_path) 
            csv_path = "outputs/Radwanium Account Transactions 2025-04-28-13_09_sampling_out.csv" 
            df_llm = pd.read_csv(csv_path)
        else: 
            ## Call OpenAI's API
            chat_completion = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages_1,
                temperature=0,
            )
            stage1_response_message = chat_completion.choices[0].message.content
            fixed_csv = fix_csv_text(stage1_response_message)
            df_llm = pd.read_csv(StringIO(fixed_csv))
        
        
        #st.session_state["sampling_LLM_df"] = df_llm
        ##st.info(stage1_response_message)
        return df_llm
        #print("Response: ", stage1_response_message)
    
    except Exception as e:
        st.error(f"🚫 Error reading stats file: {e}")
        return pd.DataFrame()
        
import pandas as pd
import streamlit as st

def get_GLEntry_fromCSV(uploaded_file, desc: str, date: str):
    if uploaded_file is None:
        st.warning("⚠️ No GL file uploaded.")
        return pd.DataFrame()

    try:
        uploaded_file.seek(0)  # Ensure pointer is at the beginning

        # Load file based on extension
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("❌ Unsupported file type.")
            return pd.DataFrame()

        # Normalize column names
        df.columns = [col.strip().upper() for col in df.columns]

        # Sanity checks
        if "DESCRIPTION" not in df.columns or "DATE" not in df.columns:
            st.error("❌ Required columns 'DESCRIPTION' or 'DATE' not found in file.")
            return pd.DataFrame()

        # Normalize for comparison
        df["DESCRIPTION"] = df["DESCRIPTION"].astype(str).str.strip().str.upper()
        df["DATE"] = pd.to_datetime(df["DATE"], errors='coerce').dt.strftime('%Y-%m-%d')

        desc = desc.strip().upper()
        date = pd.to_datetime(date, errors='coerce').strftime('%Y-%m-%d')

        # Filter the entry
        match = df[(df["DESCRIPTION"] == desc) & (df["DATE"] == date)]

        if match.empty:
            st.info("No matching GL entry found for the given description and date.")
        return match

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
        return pd.DataFrame()

        
def get_assertOccurrence_LLM (desc:str, date: str, row_key:str):
    
    """Access uploaded files for the selected row and print file names."""
    uploaded_files = st.session_state.get(f"uploaded_{row_key}", [])
    
    GL_entry = get_GLEntry_fromCSV(st.session_state.get("test_gl"), desc, date);
    gl_row_str = GL_entry.to_string(index=False)
    #st.info(gl_row_str)
    LLM_promt = """
        You are a professional audit assistant with expertise in financial audits, IFRS 15 revenue recognition, invoice reconciliation, and transaction testing. 
        You follow accounting best practices and NEVER make assumptions or hallucinate.

        You are given a **sampled transaction** from the General Ledger:

        {{row_details}}

        You are also given **uploaded documents** including invoices and bank statements, extracted as raw text. Based only on these, follow the instructions below and return your answer in strict JSON format — no extra commentary, no markdown, no explanation.

        ---

        ### For Each Uploaded Invoice:
        1. Extract:
           - **subtotal_before_vat**
           - **total_after_vat**
           - **customer_name**
        2. Compare each of the above with the GL transaction:
           - **does_subtotal_match**: true/false
           - **does_total_match**: true/false
           - **matched_amount_type**: "subtotal" / "total" / "none"
           - **amount_difference**: numeric difference from GL amount if not matched
           - **mismatch_reason**: why so think there mismatch
           - **does_customer_match**: true/false

        ---

        ### For Each Uploaded Bank Statement:
        1. Extract:
           - **payment_date**
           - **description**
           - **amount**
        2. Compare with the GL transaction:
           - **does_payment_match**: true/false
           - If matched:
             - **matched_entry_date**
             - **matched_entry_description**

        ---

        ### Strict Output Format:
        ```json
        {
          "invoices": [
            {
              "file_name": "invoice_ABC.pdf",
              "subtotal_before_vat": 1000.00,
              "total_after_vat": 1200.00,
              "customer_name": "ABC Services Ltd",
              "does_subtotal_match": false,
              "does_total_match": false,
              "matched_amount_type": "total",
              "amount_difference": 20.00,
              "mismatch_reason": "amount and currency do not match"
              "does_customer_match": true
            },
            ...
          ],
          "bank_statements": [
            {
              "file_name": "bank_statement_sep.csv",
              "entries": [
                {
                  "payment_date": "2024-09-02",
                  "description": "Payment to ABC Services Ltd",
                  "amount": 1200.00,
                  "does_payment_match": true,
                  "matched_entry_date": "2024-09-02",
                  "matched_entry_description": "Payment to ABC Services Ltd"
                }
              ]
            }
          ]
        }
    
        If values cannot be extracted or are missing, return null for those fields.
        
        Below is the data user submitted: 
        
        {{invoices_data}}
        
        
        DO NOT return any explanation, intro, or summary. 
        Respond with only the JSON object shown above.
    """
    
    if not uploaded_files:
        st.warning("⚠️ No files uploaded for this row.")
        return

    #st.success(f"📁 Found {len(uploaded_files)} uploaded file(s):")
    complete_invoices_string = ""
    for i, file in enumerate(uploaded_files, start=1):
        complete_invoices_string += f"Invoice no. {i} below:\n\n"
        complete_invoices_string += f"file name: {file.name}\n\n"
        file_type = file.type

        if "pdf" in file_type.lower():
            pdf_text = extract_text_from_pdf_from_session(row_key)
            complete_invoices_string += pdf_text + "\n\n"
            #st.text_area("📄 Extracted PDF Text", pdf_text, height=300)

        if "csv" in file_type.lower():
            csv_text = extract_text_from_csv_from_session(row_key)
            complete_invoices_string += csv_text + "\n\n"
            #st.text_area("📄 Extracted CSV Content", csv_text, height=300)
            
    final_prompt = LLM_promt.replace('{{row_details}}', gl_row_str).replace('{{invoices_data}}', complete_invoices_string)
    
    #st.text_area("📄 Extracted CSV Content", final_prompt, height=300)
    
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]  
    isDummy = st.secrets["Dummy"]

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    messages_1 = [
        {
            "role": "system",
            "content": "You are a financial data reconciliation and audit assertiosn expert.",
        },
        {
            "role": "user",
            "content": final_prompt,
        },
    ]

    ##print(final_prompt)
    if isDummy == True: 
        time.sleep(2) 
        json_path = "outputs/assertOcc_fail.json"  
        
        # Step 1: Read JSON file
        with open(json_path, "r") as f:
            data = json.load(f)
            #st.info(data)

        # Step 2: Combine invoices and bank entries into one DF
        rows = []

        # Add invoice rows
        for inv in data.get("invoices", []):
            inv["source"] = "invoice"
            rows.append(inv)

        # Add bank statement entries
        for bank in data.get("bank_statements", []):
            for entry in bank.get("entries", []):
                entry["file_name"] = bank.get("file_name", "unknown")
                entry["source"] = "bank_statement"
                rows.append(entry)

        # Final DataFrame
        df_combined = pd.DataFrame(rows)
    else:
        ## Call OpenAI's API
        chat_completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages_1,
            temperature=0,
        )
        stage1_response_message = chat_completion.choices[0].message.content
        #st.text_area("📄 LLM reply", stage1_response_message, height=300)
        try:
            if stage1_response_message.startswith("```json"):
                stage1_response_message = stage1_response_message[len("```json"):].strip()
            if stage1_response_message.startswith("```"):
                stage1_response_message = stage1_response_message[len("```"):].strip()
            if stage1_response_message.endswith("```"):
                stage1_response_message = stage1_response_message[:-3].strip()
            response_json = json.loads(stage1_response_message)
        except json.JSONDecodeError as e:
            st.error(f"❌ Failed to parse LLM JSON: {e}")
            response_json = {}

        # Step 2: Flatten and label each section
        rows = []

        # Add invoices
        for inv in response_json.get("invoices", []):
            inv["source"] = "invoice"
            rows.append(inv)

        # Add bank statement entries
        for bank in response_json.get("bank_statements", []):
            file_name = bank.get("file_name", "unknown")
            for entry in bank.get("entries", []):
                entry["source"] = "bank_statement"
                entry["file_name"] = file_name
                rows.append(entry)

        # Step 3: Convert to a single DataFrame
        df_combined = pd.DataFrame(rows)
    
    # Save the entire LLM DataFrame for this row in session_state
    st.session_state[f"llm_assertOcc_df_{row_key}"] = df_combined
    #st.text_area("📄 Extracted CSV Content", df_llm, height=300)
    
def get_assertCutoff_LLM (desc:str, date: str, row_key:str):
    
    """Access uploaded files for the selected row and print file names."""
    uploaded_files = st.session_state.get(f"uploaded_{row_key}", [])
    
    GL_entry = get_GLEntry_fromCSV(st.session_state.get("test_gl"), desc, date);
    gl_row_str = GL_entry.to_string(index=False)
    #st.info(gl_row_str)

    LLM_prompt = """
        You are a professional audit assistant with expertise in financial audits, IFRS 15 revenue recognition, invoice reconciliation, and transaction testing. 
        You follow accounting best practices and NEVER make assumptions or hallucinate.

        You are given a **sampled transaction** from the General Ledger:

        {{row_details}}

        You are also given **uploaded documents** including invoices and bank statements, extracted as raw text. Based only on these, follow the instructions below and return your answer in strict JSON format — no extra commentary, no markdown, no explanation.

        ---

        ### For Each Uploaded Invoice:
        1. Extract the **invoice date** (as YYYY-MM-DD).
        2. Compare it with the **transaction date** from the sampled row:
           - **does_invoice_date_match_exact**: true/false
           - **is_same_month**: true/false
           - **is_cutoff_issue**: true/false (set to true if both exact match and same month are false)
           - **cutoff_issue_reason**: why so think there cutoff issue
        3. If invoice date cannot be determined, return nulls.

        ---

        ### JSON Output Format:
        {
          "invoice_date_checks": [
            {
              "file_name": "Invoice_87_2025-04-30.pdf",
              "extracted_invoice_date": "2025-04-30",
              "does_invoice_date_match_exact": false,
              "is_same_month": true,
              "is_cutoff_issue": false,
              "cutoff_issue_description": "Payment is post dated"
            }
          ]
        }

        ---

        If values cannot be extracted or are missing, return null for those fields.

        Below is the data user submitted: 

        {{invoices_data}}

        DO NOT return any explanation, intro, or summary. 
        Respond with only the JSON object shown above.
    """

    
    if not uploaded_files:
        st.warning("⚠️ No files uploaded for this row.")
        return

    #st.success(f"📁 Found {len(uploaded_files)} uploaded file(s):")
    complete_invoices_string = ""
    for i, file in enumerate(uploaded_files, start=1):
        complete_invoices_string += f"Invoice no. {i} below:\n\n"
        complete_invoices_string += f"file name: {file.name}\n\n"
        file_type = file.type

        if "pdf" in file_type.lower():
            pdf_text = extract_text_from_pdf_from_session(row_key)
            complete_invoices_string += pdf_text + "\n\n"
            #st.text_area("📄 Extracted PDF Text", pdf_text, height=300)

        if "csv" in file_type.lower():
            csv_text = extract_text_from_csv_from_session(row_key)
            complete_invoices_string += csv_text + "\n\n"
            #st.text_area("📄 Extracted CSV Content", csv_text, height=300)
            
    final_prompt = LLM_prompt.replace('{{row_details}}', gl_row_str).replace('{{invoices_data}}', complete_invoices_string)
    
    #st.text_area("📄 Extracted CSV Content", final_prompt, height=300)
    
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]  
    isDummy = st.secrets["Dummy"]

    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    messages_1 = [
        {
            "role": "system",
            "content": "You are a financial data reconciliation and audit assertiosn expert.",
        },
        {
            "role": "user",
            "content": final_prompt,
        },
    ]

    ##print(final_prompt)
    if isDummy == True: 
        time.sleep(2) 
        json_path = "outputs/assertCutoff_success.json"  
        
        # Step 1: Read JSON file
        with open(json_path, "r") as f:
            data = json.load(f)
            #st.info(data)

        # Step 2: Combine invoices and bank entries into one DF
        rows = []

        # Add invoice rows
        for inv in data.get("invoice_date_checks", []):
            inv["source"] = "invoice_date_check"
            rows.append(inv)

        # Add bank statement entries
        # check wht resposn LLM gives in JSON n checj fron tag for bank statement
        #maybe you need to change it if its not bank_statements
        for bank in data.get("bank_statements", []):
            for entry in bank.get("entries", []):
                entry["file_name"] = bank.get("file_name", "unknown")
                entry["source"] = "bank_statement"
                rows.append(entry)

        # Final DataFrame
        df_combined = pd.DataFrame(rows)
    else:
        ## Call OpenAI's API
        chat_completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages_1,
            temperature=0,
        )
        stage1_response_message = chat_completion.choices[0].message.content
        #st.text_area("📄 LLM reply", stage1_response_message, height=300)
        try:
            if stage1_response_message.startswith("```json"):
                stage1_response_message = stage1_response_message[len("```json"):].strip()
            if stage1_response_message.startswith("```"):
                stage1_response_message = stage1_response_message[len("```"):].strip()
            if stage1_response_message.endswith("```"):
                stage1_response_message = stage1_response_message[:-3].strip()
            response_json = json.loads(stage1_response_message)
        except json.JSONDecodeError as e:
            st.error(f"❌ Failed to parse LLM JSON: {e}")
            response_json = {}

        # Step 2: Flatten and label each section
        rows = []

        # Add invoices
        for inv in response_json.get("invoice_date_checks", []):
            inv["source"] = "invoice_date_check"
            rows.append(inv)

        # Add bank statement entries
        # check wht resposn LLM gives in JSON n checj fron tag for bank statement
        #maybe you need to change it if its not bank_statements
        for bank in response_json.get("bank_statements", []):
            file_name = bank.get("file_name", "unknown")
            for entry in bank.get("entries", []):
                entry["source"] = "bank_statement"
                entry["file_name"] = file_name
                rows.append(entry)

        # Step 3: Convert to a single DataFrame
        df_combined = pd.DataFrame(rows)
    
    # Save the entire LLM DataFrame for this row in session_state
    st.session_state[f"llm_assertCutoff_df_{row_key}"] = df_combined
    #st.text_area("📄 Extracted CSV Content", df_llm, height=300)
    
