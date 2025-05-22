# stats_csv.py
import streamlit as st
import pandas as pd
from utils import get_stats_csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def display_stats():
    st.markdown("<h1 style='text-align: center;'>📈 Analytical Statistics Overview</h1>", unsafe_allow_html=True)
    st.subheader("Completeness & Accuracy Assertsion")
    st.markdown("---")
    
    df = get_stats_csv()
    
    if df.empty:
        st.warning("⚠️ Please upload a valid file to continue.")        
        if st.button("⬅️ Back to User Inputs"):
            st.session_state.page = 'userip'
            st.rerun()
        return
        
    if st.button("➡️ Perform Risk-Based Sampling", key="view_risk_btn_1"):
        st.session_state.page = 'view'
        st.rerun()
        
    #df = pd.read_csv("outputs/Statisctics_out.csv")

    # ---------- CLUSTERING SUMMARY ----------
    st.subheader("📊 K-Means Clustering Summary")
    cluster_summary = df.groupby('K_means Lable')['Amount'].agg(['mean', 'count']).reset_index()
    cluster_summary.columns = ['Cluster', 'Average Amount (£)', 'Number of Transactions']
    st.table(cluster_summary)

    # ---------- BENFORD'S LAW (LEADING DIGIT) ----------
    st.subheader("🔢 First Digit (Benford's Law) Distribution")
    #leading_digit_counts = df['LeadingDigit'].value_counts().sort_index()
    #fig2, ax2 = plt.subplots(figsize=(4, 2))
    #sns.barplot(x=leading_digit_counts.index.astype(str), y=leading_digit_counts.values, ax=ax2, palette='Blues_d')
    #ax2.set_xlabel("Leading Digit")
    #ax2.set_ylabel("Frequency")
    #ax2.set_title("Distribution of Leading Digits (Benford's Law)")
    #st.pyplot(fig2)
    
    leading_counts = df['LeadingDigit'].value_counts().sort_index()
    total = leading_counts.sum()

    # Expected Benford % for digits 1–9
    expected_distribution = {d: np.log10(1 + 1/d) * 100 for d in range(1, 10)}

    # Prepare table rows
    table_rows = []

    for d in range(1, 6):
        actual = leading_counts.get(d, 0) / total * 100
        table_rows.append((str(d), f"{expected_distribution[d]:.2f}%", f"{actual:.2f}%"))

    # Group 6–9
    expected_6_9 = sum(expected_distribution[d] for d in range(6, 10))
    actual_6_9 = sum(leading_counts.get(d, 0) for d in range(6, 10)) / total * 100
    table_rows.append(("6–9", f"{expected_6_9:.2f}% (total)", f"{actual_6_9:.2f}% (total)"))

    # Create DataFrame and show
    benford_df = pd.DataFrame(table_rows, columns=["Digit", "Expected %", "Actual %"])
    st.table(benford_df)
    
    # ---------- Unusual Pattern Detection Summary ----------
    st.subheader("🔎 Unusual Pattern Detection Summary")

    unusual_summary = pd.DataFrame([
        ["Round-number Transactions", df['Rounded'].sum(), "Often signals estimation or intentional rounding."],
        ["Weekend Transactions", df['Weekend'].sum(), "Potential flag depending on company policy."],
        ["Holiday Transactions", df['Holiday'].sum(), "Unusual unless specifically allowed."],
        ["Even-Dollar Amounts", df['EvenDollar'].sum(), "Small, but worth noting in manual reviews."],
        ["Unusual Precision (non-typical decimals)", (df['Precision'] > 0).sum(), "Could indicate system-generated or unusually precise values."],
        ["Month-End Transactions", df[df['DATE'].dt.is_month_end].shape[0], "Month-end spikes could reflect accruals or adjustments."]
    ], columns=["Pattern", "Count", "Notes"])

    st.table(unusual_summary)

    # ---------- Additional Descriptive Statistics ----------
    st.subheader("📊 Descriptive Statistics (Amount Column)")

    desc_stats = pd.DataFrame([
        ["Mean", f"£{df['Amount'].mean():,.2f}"],
        ["Median", f"£{df['Amount'].median():,.2f}"],
        ["Standard Deviation", f"£{df['Amount'].std():,.2f}"],
        ["Min", f"£{df['Amount'].min():,.2f}"],
        ["Max", f"£{df['Amount'].max():,.2f}"],
        ["Total Transactions", len(df)],
    ], columns=["Statistic", "Value"])

    st.table(desc_stats)


    # ---------- CLUSTERING PLOT ----------st.subheader("🔍 K-Means Clustering Of Meals & Entertainment Transactions")

    fig, ax = plt.subplots(figsize=(3, 1.6), dpi=150)  # HIGH DPI makes it sharp & smaller
    scatter = ax.scatter(
        df.index,
        df['Amount'],
        c=df['K_means Lable'].astype('category').cat.codes,
        cmap='viridis',
        s=10,              # small dot size
        alpha=0.8,
        edgecolors='none'
    )

    # Smaller axis labels
    ax.set_xlabel("Index", fontsize=6)
    ax.set_ylabel("Amount (£)", fontsize=6)

    # Smaller ticks
    ax.tick_params(axis='both', labelsize=6)

    # Remove chart border padding
    fig.tight_layout()

    # Render it
    st.pyplot(fig)

    
    st.markdown("---")
    st.subheader("🧾 Full Dataset Below")

    # Alternate row coloring (light blue tone)
    def alternate_row_colors(row_index):
        if row_index % 2 == 0:
            return ['background-color: #E6F2FF'] * df.shape[1]  # light blue
        else:
            return [''] * df.shape[1]

    styled_df = df.style.apply(lambda row: alternate_row_colors(row.name), axis=1)

    st.dataframe(styled_df, use_container_width=True)

    # Next button to go to view
    if st.button("⬅️ Back to User Inputs"):
        st.session_state.page = 'userip'
        st.rerun()
    if st.button("➡️ Perform Risk-Based Sampling"):
        st.session_state.page = 'view'
        st.rerun()