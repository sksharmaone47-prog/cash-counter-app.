import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Cash Counter Pro", page_icon="🏦")

# Styling: BOLD text and Alignment
st.markdown("""
    <style>
    .stApp { background-color: #e8f5e9; }
    .bold-text { font-size: 22px !important; font-weight: bold !important; color: #000000; }
    input { font-size: 18px !important; font-weight: bold !important; }
    /* Calculation text ko align karne ke liye style */
    .calc-row { font-family: monospace; font-size: 18px; font-weight: bold; color: #1b5e20; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Cash Counter Pro")

# Sidebar
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

# Main Screen Header
st.markdown(f'<p class="bold-text">Entry Name : {user_name}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="bold-text">Date : {report_date.strftime("%a, %d %b %Y")}</p>', unsafe_allow_html=True)

st.divider()

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

st.subheader("Enter Quantities")

# --- ALIGNED INPUT SECTION ---
for n in notes:
    col1, col2, col3 = st.columns([1.5, 2, 2.5])
    with col1:
        st.write(f"**₹{n}**")
    with col2:
        count = st.number_input(f"x", min_value=0, step=1, value=0, key=f"q_{n}", label_visibility="collapsed")
        counts[n] = count
    with col3:
        subtotal = n * count
        totals.append(subtotal)
        # Yahan spacing ka use kiya hai taki '=' ek line mein rahe
        st.markdown(f'<p class="calc-row">= ₹{subtotal:>6}/-</p>', unsafe_allow_html=True)

# Coins Section
st.divider()
c_col1, c_col2 = st.columns([3.5, 2.5])
with c_col1:
    coin_val = st.number_input("Coins Value (₹)", min_value=0, step=1, value=0)
with c_col2:
    st.markdown(f'<p class="calc-row">= ₹{coin_val:>6}/-</p>', unsafe_allow_html=True)

# Calculations
grand_total = sum(totals) + coin_val
total_items = sum(counts.values())

try:
    words_hi = num2words(grand_total, lang='en_IN').title().replace("-", " ") + " Only"
except:
    words_hi = "Zero Only"

# --- SUMMARY ---
st.divider()
st.markdown(f'<p class="bold-text">Total = ₹{grand_total}/-</p>', unsafe_allow_html=True)
st.write(f"**{words_hi}**")
st.write(f"**Total {total_items} Notes / Coins**")

# --- WHATSAPP TEXT GENERATION (With Alignment) ---
st.divider()

# WhatsApp format with padding for perfect alignment
whatsapp_text = f"Entry Name : {user_name}\n"
whatsapp_text += f"Date : {report_date.strftime('%a, %d %b %Y')}\n\n"

for n in notes:
    if counts[n] > 0:
        # {:>5} ka matlab hai spaces add karna taki numbers align ho jayein
        whatsapp_text += f"₹{n:<4} x {counts[n]:<3} = ₹{n*counts[n]:>6}/-\n"

if coin_val > 0:
    whatsapp_text += f"Coins      = ₹{coin_val:>6}/-\n"

whatsapp_text += "--------------------------------\n"
whatsapp_text += f"Total      = ₹{grand_total:>6}/-\n"
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
