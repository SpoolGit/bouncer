# user_inputs.py
import streamlit as st

def user_inputs():
     

    st.markdown("""
        <style>
        .block-container {
            max-width: 900px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Please add below inputs")
    

    with st.form("user_form"): 
        submitted = st.form_submit_button("➡️ View Stats")   

        # Test Setup
        st.subheader("🔹 Testing Setup")
        account_y = st.text_input("What account are you testing? ", value=st.session_state.get("account_y", ""))
        testing_year = st.text_input("Which Year Are you Testing?", value=st.session_state.get("testing_year", ""))
        
        # Testing Year
        st.subheader(f"📌 Testing Year {testing_year}")
        col3, col4 = st.columns(2)
        with col3:
            test_headcount = st.text_input(f"Total Headcount ({testing_year})", value=st.session_state.get("test_headcount", ""))
            test_opex = st.text_input(f"Operating Expenses ({testing_year})", value=st.session_state.get("test_opex", ""))
        with col4:
            test_revenue = st.text_input(f"Revenue ({testing_year})", value=st.session_state.get("test_revenue", ""))
            test_gl = st.file_uploader(
                f"Upload GL File for {account_y}", 
                type=["csv", "xlsx"], 
                key="test_gl_upload"
            )

            if test_gl is not None:
                st.session_state["test_gl"] = test_gl  # save it
                st.session_state["llm_sampling_df"] = None  # clear old LLM output
                st.success("✅ File uploaded successfully.")
            
        # Basic Info
        st.subheader("🔹 Company & User Info")
        user_name = st.text_input("User Name:", value=st.session_state.get("user_name", ""))
        company_url = st.text_input("Company URL:", value=st.session_state.get("company_url", ""))
        email = st.text_input("Email:", value=st.session_state.get("email", ""))
                
            
        num_compare = st.number_input("Insert the number of years you want to compare:", min_value=0, step=1, value=st.session_state.get("num_compare", 0))
        industry = st.selectbox("In what industry is the company you are testing?",
                                ["Technology", "Healthcare", "Finance", "Retail", "Manufacturing", "Other"],
                                index=["Technology", "Healthcare", "Finance", "Retail", "Manufacturing", "Other"].index(
                                    st.session_state.get("industry", "Technology")
                                ))

        # Comparison Years
        if num_compare > 0:
            st.subheader("🔄 Comparison Years")
        compare_data = []
        for i in range(num_compare):
            year_label = f"Year {i + 1}"
            st.markdown(f"**{year_label}**")
            col1, col2 = st.columns(2)
            with col1:
                headcount = st.text_input(f"Total Headcount ({year_label})", key=f"headcount_{i}")
                opex = st.text_input(f"Operating Expenses ({year_label})", key=f"opex_{i}")
            with col2:
                revenue = st.text_input(f"Revenue ({year_label})", key=f"revenue_{i}")
                gl = st.file_uploader(f"Upload GL File ({year_label})", type=["csv"], key=f"gl_{i}")
            compare_data.append({"headcount": headcount, "opex": opex, "revenue": revenue, "gl": gl})



        #submitted = st.form_submit_button("➡️ View Stats")

        if submitted:
            # Store everything in session
            st.session_state.user_name = user_name
            st.session_state.company_url = company_url
            st.session_state.email = email
            st.session_state.account_y = account_y
            st.session_state.testing_year = testing_year
            st.session_state.num_compare = num_compare
            st.session_state.industry = industry
            st.session_state.test_headcount = test_headcount
            st.session_state.test_opex = test_opex
            st.session_state.test_revenue = test_revenue
            st.session_state.test_gl = test_gl

            for i in range(num_compare):
                st.session_state[f"compare_headcount_{i}"] = compare_data[i]['headcount']
                st.session_state[f"compare_opex_{i}"] = compare_data[i]['opex']
                st.session_state[f"compare_revenue_{i}"] = compare_data[i]['revenue']
                st.session_state[f"compare_gl_{i}"] = compare_data[i]['gl']

            st.session_state.page = 'stats'
            st.rerun()
