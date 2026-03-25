import streamlit as st

st.title("Cash Counter")

# 4 columns ek line me
col1, col2, col3, col4 = st.columns(4)

with col1:
    cash_100 = st.number_input("₹100", min_value=0)

with col2:
    cash_200 = st.number_input("₹200", min_value=0)

with col3:
    cash_500 = st.number_input("₹500", min_value=0)

with col4:
    cash_2000 = st.number_input("₹2000", min_value=0)

# Calculation
total = (cash_100 * 100 +
         cash_200 * 200 +
         cash_500 * 500 +
         cash_2000 * 2000)

st.write("### Total:", total)
