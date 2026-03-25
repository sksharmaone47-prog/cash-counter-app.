import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Cash Counter Pro", page_icon="🏦")

# Styling: BOLD text and Clean Layout
st.markdown("""
    <style>
    .stApp { background-color: #e8f5e9; }
    .bold-text { font-size: 22px !important; font-weight: bold !important; color: #000000; margin-bottom: 5px; }
    .calc-text { font-size: 18px !important; font-weight: bold !important; color: #1b5e20; padding-top: 10px; }
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
st.markdown(f'<p class="bold-text">Date : {report_date.strftime("%a, %d %b %Y")}</p>', unsafe_allow_html=True)

st.divider()

# Denominations list
notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

st.subheader("Enter Quantities")

# --- INPUT SECTION (₹500 x Qty = ₹1500/- Format) ---
for n in notes:
    col1, col2 = st.columns([2, 3])
    with col1:
        # Mobile par number keyboard khulega
        count = st.number_input(f"₹{n} x", min_value=0, step=1, value=0, key=f"q_{n}")
        counts[n] = count
    with col2:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f'<p class="calc-text">= ₹{subtotal}/-</p>', unsafe_allow_html=True)

# Coins input
st.divider()
coin_val = st.number_input("Coins = ₹", min_value=0, step=1, value=0)

# Final Calculations
grand_total = sum(totals) + coin_val
total_items = sum(counts.values())

try:
    # Hindi/English format with gaps
    words_hi = num2words(grand_total, lang='en_IN').title().replace("-", " ") + " Only"
except:
    words_hi = "Zero Only"

# --- SUMMARY SECTION ---
st.divider()
st.markdown(f'<p class="bold-text">Total = ₹{grand_total}/-</p>', unsafe_allow_html=True)
st.write(f"**{words_hi}**")
st.write(f"**Total {total_items} Notes / Coins**")

# --- WHATSAPP BUTTON ---
st.divider()

# Format: Exact as image
whatsapp_text = f"Entry Name : {user_name}\n"
whatsapp_text += f"Date : {report_date.strftime('%a, %d %b %Y')}\n\n"

for n in notes:
    if counts[n] > 0:
        whatsapp_text += f"₹{n} x {counts[n]} = ₹{n*counts[n]}/-\n"

if coin_val > 0:
    whatsapp_text += f"Coins = ₹{coin_val}/-\n"

whatsapp_text += "--------------------------------\n"
whatsapp_text += f"Total = ₹{grand_total}/-\n"
whatsapp_text += f"{words_hi}\n"
whatsapp_text += f"Total {total_items} Notes / Coins"

whatsapp_url = f"https://wa.me/?text={whatsapp_text.replace(' ', '%20').replace('\n', '%0A')}"

st.markdown(f'''
    <a href="{whatsapp_url}" target="_blank">
        <button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-size:18px; font-weight:bold;">
            📲 Share on WhatsApp
        </button>
    </a>
''', unsafe_allow_html=True)

if st.button("🔄 Reset / Clear All"):
    st.rerun()
with c1:
    st.markdown(f'''<a href="{format1_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer;">📲 Send Simple Text</button></a>''', unsafe_allow_html=True)

with c2:
    st.markdown(f'''<a href="{format2_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:10px; cursor:pointer;">📲 Send Detail Text</button></a>''', unsafe_allow_html=True)
