import streamlit as st
import pandas as pd
from datetime import date
from num2words import num2words

# --- APP CONFIGURATION & ICON ---
# Yahan 'page_icon' mein aap koi bhi emoji daal sakte hain jo icon ban jayega
st.set_page_config(
    page_title="Cash Report Pro", 
    page_icon="🏦", 
    layout="centered"
)

# Custom Green Theme (Like WhatsApp/Cash Receipt)
st.markdown("""
    <style>
    .stApp { background-color: #e8f5e9; }
    .main-card { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        border-top: 5px solid #2e7d32;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Cash Counter Pro")

# --- SIDEBAR SETTINGS ---
st.sidebar.header("📋 Report Details")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

# --- INPUT SECTION ---
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.subheader("Enter Quantities")

notes = [500, 200, 100, 50, 20, 10]
counts = {}
totals = []

for n in notes:
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        st.write(f"**₹{n}**")
    with col2:
        counts[n] = st.number_input(f"Qty {n}", min_value=0, step=1, key=f"n_{n}", label_visibility="collapsed")
    with col3:
        subtotal = n * counts[n]
        totals.append(subtotal)
        st.write(f"**= ₹{subtotal}/-**")

coin_val = st.number_input("Total Coins (₹):", min_value=0, step=1)
st.markdown('</div>', unsafe_allow_html=True)

# --- CALCULATIONS ---
grand_total = sum(totals) + coin_val
total_items = sum(counts.values())

try:
    words = num2words(grand_total, lang='en_IN').title() + " Only"
except:
    words = "Zero Only"

# --- DISPLAY SUMMARY ---
st.divider()
st.success(f"### Total Amount: ₹{grand_total}/-")
st.write(f"**In Words:** {words}")
st.write(f"**Total Notes/Coins:** {total_items}")

# --- ACTION BUTTONS ---
st.divider()
c1, c2 = st.columns(2)

# WhatsApp Link Generator
raw_text = f"Entry Name: {user_name}\nDate: {report_date.strftime('%d/%m/%Y')}\n\n"
for n in notes:
    if counts[n] > 0:
        raw_text += f"₹{n} x {counts[n]} = ₹{n*counts[n]}/-\n"
if coin_val > 0:
    raw_text += f"Coins = ₹{coin_val}/-\n"
raw_text += f"\nTotal = ₹{grand_total}/-\n{words}"

whatsapp_url = f"https://wa.me/?text={raw_text.replace(' ', '%20').replace('\n', '%0A')}"

with c1:
    st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer;">📲 Send WhatsApp</button></a>''', unsafe_allow_html=True)

with c2:
    # PDF/Print functionality (Simulated via Download)
    st.download_button(
        label="📄 Save/Print Report",
        data=raw_text,
        file_name=f"Report_{user_name}_{report_date}.txt",
        mime="text/plain"
    )

if st.button("🔄 Clear All"):
    st.rerun()
