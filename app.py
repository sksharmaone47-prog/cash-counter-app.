import streamlit as st
import pandas as pd
from datetime import date
from num2words import num2words

# Page Setup
st.set_page_config(page_title="Cash Report Pro", page_icon="💰", layout="wide")

# Styling for Green Theme (like your image)
st.markdown("""
    <style>
    .stApp { background-color: #e8f5e9; }
    .main-box { background-color: #c8e6c9; padding: 20px; border-radius: 10px; border: 1px solid #4caf50; }
    </style>
    """, unsafe_allow_html=True)

# Session State for History
if 'history' not in st.session_state:
    st.session_state.history = []

st.title("💸 Cash Counter & Work Report")

# --- SIDEBAR: Name & Date Settings ---
st.sidebar.header("User Settings 👤")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Select Date:", date.today())

# --- MAIN SECTION ---
with st.container():
    st.markdown('<div class="main-box">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Enter Quantities")
        notes = [500, 200, 100, 50, 20, 10]
        counts = {}
        subtotals = []
        
        for n in notes:
            c_label, c_input = st.columns([1, 2])
            c_label.write(f"**₹{n}**")
            counts[n] = c_input.number_input(f"Qty {n}", min_value=0, step=1, key=f"note_{n}", label_visibility="collapsed")
            subtotals.append(n * counts[n])
        
        coin_total = st.number_input("Total Coins Value (₹)", min_value=0, step=1)
    
    with col2:
        st.subheader("Summary")
        grand_total = sum(subtotals) + coin_total
        total_items = sum(counts.values()) + (1 if coin_total > 0 else 0)
        
        # Amount in Words
        try:
            amt_words = num2words(grand_total, lang='en_IN').title() + " Only"
        except:
            amt_words = "Zero"

        st.write(f"**Name:** {user_name}")
        st.write(f"**Date:** {report_date.strftime('%a, %d %b %Y')}")
        st.divider()
        st.metric("Total Amount", f"₹{grand_total}/-")
        st.write(f"**In Words:** {amt_words}")
        st.write(f"**Total Notes/Coins:** {total_items}")

        if st.button("Save Entry to History ✅"):
            entry = {
                "Date": report_date.strftime("%d-%m-%Y"),
                "Name": user_name,
                "Total": f"₹{grand_total}",
                "Words": amt_words
            }
            st.session_state.history.append(entry)
            st.success("Entry Saved!")

    st.markdown('</div>', unsafe_allow_html=True)

# --- WHATSAPP / TEXT REPORT ---
st.divider()
if st.checkbox("Show Report for WhatsApp"):
    report_text = f"Entry Name : {user_name}\nDate : {report_date.strftime('%a, %d %B %Y')}\n\n"
    for n in notes:
        if counts[n] > 0:
            report_text += f"₹{n} x {counts[n]} = ₹{n*counts[n]}/-\n"
    if coin_total > 0:
        report_text += f"Coins = ₹{coin_total}/-\n"
    report_text += f"----------------------\nTotal = ₹{grand_total}/-\n{amt_words}\nTotal {total_items} Notes/Coins"
    
    st.code(report_text)
    st.download_button("📥 Download Text File", report_text, file_name=f"Report_{user_name}.txt")

# --- HISTORY TABLE ---
if st.session_state.history:
    st.subheader("📜 History (Saved Entries)")
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)
    
    csv = history_df.to_csv(index=False).encode('utf-8')
    st.download_button("📊 Download All History (Excel/CSV)", csv, "history.csv", "text/csv")
  
