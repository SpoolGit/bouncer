import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from scipy.stats import zscore
import holidays
import re
from io import StringIO
import time


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
    

def get_llm_sampling_csv ():
    
    try:
        stats_df = st.session_state.get("stats_df")

        if stats_df is None or not isinstance(stats_df, pd.DataFrame) or stats_df.empty:
            st.warning("⚠️ No statistics DataFrame found in session or it is empty.")
            return pd.DataFrame()
        
        cleaned_csv_text = st.session_state.get("stats_df").to_csv(index=False)
        #print(cleaned_csv_text)

        import openai
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

        #print(final_prompt) 
        time.sleep(5) 
        csv_path = "outputs/unusual-n-sampling.csv"  
        df_llm = pd.read_csv(csv_path)
        
        #st.session_state["sampling_LLM_df"] = df_llm
        return df_llm
        #print("Response: ", stage1_response_message)
    
    except Exception as e:
        st.error(f"🚫 Error reading stats file: {e}")
        return pd.DataFrame()
        

def get_llm_sampling_summary ():
    
    try:
        stats_df = st.session_state.get("stats_df")

        if stats_df is None or not isinstance(stats_df, pd.DataFrame) or stats_df.empty:
            st.warning("⚠️ No statistics DataFrame found in session or it is empty.")
            return pd.DataFrame()
        
        cleaned_csv_text = st.session_state.get("stats_df").to_csv(index=False)
        #print(cleaned_csv_text)

        import openai
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

        #print(final_prompt) 
        time.sleep(5) 
        csv_path = "outputs/unusual-n-sampling.csv"  
        df_llm_summary = pd.read_csv(csv_path)
        
        return df_llm_summary
        #print("Response: ", stage1_response_message)
    
    except Exception as e:
        st.error(f"🚫 Error reading stats file: {e}")
        return pd.DataFrame()