import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Cash Counter Pro", page_icon="🏦")

# Styling: BOLD text and Clean Layout for Input Screen
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

# Display Name & Date in BOLD on Main Screen
st.markdown(f'<p class="bold-text">Entry Name : {user_name}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="bold-text">Date : {report_date.strftime("%a, %d %B %Y")}</p>', unsafe_allow_html=True)

st.divider()

# Denominations list
notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

st.subheader("Enter Quantities")

# --- INPUT SECTION (Displays as Note * Qty = Total) ---
for n in notes:
    col1, col2 = st.columns([2, 3])
    with col1:
        count = st.number_input(f"{n} *", min_value=0, step=1, value=0, key=f"q_{n}")
        counts[n] = count
    with col2:
        subtotal = n * count
        totals.append(subtotal)
        # Format as Note * Qty = Total
        st.markdown(f'<p class="calc-text">= {subtotal}</p>', unsafe_allow_html=True)

# Coins input
st.divider()
coin_val = st.number_input("Total Coins Value (₹):", min_value=0, step=1, value=0)

# Final Calculations
grand_total = sum(totals) + coin_val
total_items = sum(counts.values())

try:
    words_hi = num2words(grand_total, lang='en_IN').title().replace("-", " ") + " Only"
except:
    words_hi = "Zero Only"

# --- DISPLAY SUMMARY ---
st.divider()
st.markdown(f'<p class="bold-text">Total = ₹{grand_total}/-</p>', unsafe_allow_html=True)
st.write(f"**{words_hi}**")
st.write(f"**Total {total_items} Notes / Coins**")

# --- ACTION BUTTONS ---
st.divider()
st.subheader("Send to WhatsApp")
c1, c2 = st.columns(2)

# --- Format 1: Simple ---
format1_raw = f"Total = {grand_total}\n"
format1_raw += f"Coins = {coin_val}\n"
format1_raw += "----------------------\n"
format1_raw += f"Total Notes {total_items}\n"
format1_hi = f"{words_hi}\n"
format1_text = format1_raw + format1_hi
format1_url = f"https://wa.me/?text={format1_text.replace(' ', '%20').replace('\n', '%0A')}"

# --- Format 2: Details ---
format2_head = f"Entry Name : {user_name}\nDate : {report_date.strftime('%a, %d %b %Y')}\n\n"
format2_body = ""
for n in notes:
    if counts[n] > 0:
        format2_body += f"{n} * {counts[n]} = {n*counts[n]}\n"
if coin_val > 0:
    format2_body += f"Coins = {coin_val}\n"
format2_body += "----------------------\n"
format2_total = f"Total = {grand_total}\n\n"
format2_hi = f"{words_hi}\n"
format2_summary = f"Total {total_items} Notes / Coins\n"
format2_text = format2_head + format2_body + format2_total + format2_hi + format2_summary
format2_url = f"https://wa.me/?text={format2_text.replace(' ', '%20').replace('\n', '%0A')}"

with c1:
    st.markdown(f'''<a href="{format1_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer;">📲 Send Simple Text</button></a>''', unsafe_allow_html=True)

with c2:
    st.markdown(f'''<a href="{format2_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer;">📲 Send Detail Text</button></a>''', unsafe_allow_html=True)
