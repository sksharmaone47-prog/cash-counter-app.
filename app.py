import streamlit as st
from datetime import date
from num2words import num2words

# Page Setup
st.set_page_config(page_title="Cash Counter Pro", page_icon="🏦")

# Styling: BOLD text aur Clean Layout
st.markdown("""
    <style>
    .stApp { background-color: #e8f5e9; }
    .bold-text { font-size: 20px !important; font-weight: bold !important; color: #000000; margin-bottom: 5px; }
    .calc-text { font-size: 18px !important; font-weight: bold !important; color: #2e7d32; padding-top: 10px; }
    input { font-size: 18px !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Cash Counter Pro")

# Sidebar
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

# Display Name & Date in BOLD
st.markdown(f'<p class="bold-text">Entry Name : {user_name}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="bold-text">Date : {report_date.strftime("%a, %d %B %Y")}</p>', unsafe_allow_html=True)

st.divider()

# Denominations list (Added 2000)
notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

st.subheader("Enter Quantities")

# Input Section with Number Keyboard
for n in notes:
    col1, col2 = st.columns([2, 3])
    with col1:
        # number_input ka use kiya hai taki mobile par sirf Number Keyboard khule
        count = st.number_input(f"{n} *", min_value=0, step=1, value=0, key=f"q_{n}")
        counts[n] = count
    with col2:
        subtotal = n * count
        totals.append(subtotal)
        # Naya format jaisa aapne image mein dikhaya
        st.markdown(f'<p class="calc-text">= {subtotal}</p>', unsafe_allow_html=True)

# Coins input
st.divider()
coin_val = st.number_input("Total Coins Value (₹):", min_value=0, step=1, value=0)

# Calculations
grand_total = sum(totals) + coin_val
total_items = sum(counts.values())

try:
    words = num2words(grand_total, lang='en_IN').title() + " Only"
except:
    words = "Zero Only"

# --- SUMMARY SECTION ---
st.divider()
st.markdown(f'<p class="bold-text">Total = ₹{grand_total}/-</p>', unsafe_allow_html=True)
st.write(f"**{words}**")
st.write(f"**Total {total_items} Notes / Coins**")

# Action Buttons
st.divider()
c1, c2 = st.columns(2)

# WhatsApp Message Text
raw_text = f"Entry Name : {user_name}\nDate : {report_date.strftime('%a, %d %b %Y')}\n\n"
for n in notes:
    if counts[n] > 0:
        raw_text += f"{n} * {counts[n]} = {n*counts[n]}\n"
if coin_val > 0:
    raw_text += f"Coins = {coin_val}\n"
raw_text += f"----------------------\nTotal = {grand_total}\n{words}\nTotal {total_items} Notes / Coins"

whatsapp_url = f"https://wa.me/?text={raw_text.replace(' ', '%20').replace('\n', '%0A')}"

with c1:
    st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer; font-weight:bold;">📲 WhatsApp Share</button></a>''', unsafe_allow_html=True)

with c2:
    st.download_button("📄 Save Report", raw_text, file_name=f"Report_{user_name}.txt")

if st.button("🔄 Reset App"):
    st.rerun()
