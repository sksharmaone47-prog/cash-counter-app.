import streamlit as st
from datetime import date
from num2words import num2words

# Page Setup
st.set_page_config(page_title="Cash Counter Pro", page_icon="🏦")

# Styling: Text ko Bold aur Green karne ke liye
st.markdown("""
    <style>
    .stApp { background-color: #e8f5e9; }
    .bold-text { font-size: 22px !important; font-weight: bold !important; color: #000000; }
    .main-card { background-color: #ffffff; padding: 20px; border-radius: 15px; border-top: 5px solid #2e7d32; }
    input { font-size: 18px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Cash Counter Pro")

# Sidebar
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

# --- Display Name & Date in BOLD ---
st.markdown(f'<p class="bold-text">Entry Name : {user_name}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="bold-text">Date : {report_date.strftime("%a, %d %B %Y")}</p>', unsafe_allow_html=True)

st.divider()

notes = [500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# Input Section
for n in notes:
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        st.write(f"**₹{n}**")
    with col2:
        val = st.text_input(f"Qty {n}", value="", placeholder="0", key=f"q_{n}", label_visibility="collapsed")
        count = int(val) if val.isdigit() else 0
        counts[n] = count
    with col3:
        subtotal = n * count
        totals.append(subtotal)
        st.write(f"**= ₹{subtotal}/-**")

# Coins input
st.divider()
coin_in = st.text_input("Total Coins (₹):", value="", placeholder="0")
coin_val = int(coin_in) if coin_in.isdigit() else 0

# Calculations
grand_total = sum(totals) + coin_val
total_notes = sum(counts.values())

try:
    words = num2words(grand_total, lang='en_IN').title() + " Only"
except:
    words = "Zero Only"

# --- SUMMARY SECTION (BOLD) ---
st.divider()
st.markdown(f'<p class="bold-text">Total = ₹{grand_total}/-</p>', unsafe_allow_html=True)
st.write(f"**{words}**")
st.write(f"**Total {total_notes} Notes / Coins**")

# Action Buttons
st.divider()
c1, c2 = st.columns(2)

raw_text = f"Entry Name : {user_name}\nDate : {report_date.strftime('%a, %d %b %Y')}\n\n"
for n in notes:
    if counts[n] > 0:
        raw_text += f"₹{n} x {counts[n]} = ₹{n*counts[n]}/-\n"
if coin_val > 0:
    raw_text += f"Coins = ₹{coin_val}/-\n"
raw_text += f"----------------------\nTotal = ₹{grand_total}/-\n{words}\nTotal {total_notes} Notes / Coins"

whatsapp_url = f"https://wa.me/?text={raw_text.replace(' ', '%20').replace('\n', '%0A')}"

with c1:
    st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer; font-weight:bold;">📲 Send WhatsApp</button></a>''', unsafe_allow_html=True)

with c2:
    st.download_button("📄 Save Report (PDF/TXT)", raw_text, file_name=f"Report_{user_name}.txt")

if st.button("🔄 Clear All"):
    st.rerun()
