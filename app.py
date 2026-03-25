import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Counter Pro", page_icon="🏦")

# Styling for perfect alignment and Green Theme
st.markdown("""
    <style>
    .stApp { background-color: #e8f5e9; }
    .bold-text { font-size: 22px !important; font-weight: bold !important; color: #000000; }
    /* Monospace font for perfect straight alignment */
    .calc-row { 
        font-family: 'Courier New', Courier, monospace; 
        font-size: 20px; 
        font-weight: bold; 
        color: #1b5e20; 
        white-space: pre;
    }
    input { font-size: 18px !important; font-weight: bold !important; }
    .logo-img { display: block; margin-left: auto; margin-right: auto; width: 100px; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO SECTION ---
# Aapka bataya hua Bank Logo
st.markdown('<img src="https://raw.githubusercontent.com/sksharmaone47-prog/cash-counter-app/main/logo.png" class="logo-img">', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Cash Counter Pro</h1>", unsafe_allow_html=True)

# Sidebar Settings
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

# Header BOLD
st.markdown(f'<p class="bold-text">Entry Name : {user_name}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="bold-text">Date : {report_date.strftime("%a, %d %b %Y")}</p>', unsafe_allow_html=True)

st.divider()

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- INPUT SECTION ---
for n in notes:
    col1, col2, col3 = st.columns([1.5, 2, 3])
    with col1:
        st.write(f"**₹{n}**")
    with col2:
        count = st.number_input(f"x {n}", min_value=0, step=1, value=0, key=f"q_{n}", label_visibility="collapsed")
        counts[n] = count
    with col3:
        subtotal = n * count
        totals.append(subtotal)
        # Perfect spacing for straight '=' line
        st.markdown(f'<p class="calc-row"> x {count:<2} = ₹{subtotal:>5}/-</p>', unsafe_allow_html=True)

# Coins Section (Fixed Alignment)
st.divider()
c_col1, c_col2 = st.columns([3.5, 3])
with c_col1:
    coin_val = st.number_input("Coins Value (₹)", min_value=0, step=1, value=0)
with c_col2:
    st.markdown(f'<p class="calc-row">Coins   = ₹{coin_val:>5}/-</p>', unsafe_allow_html=True)

# Calculations
grand_total = sum(totals) + coin_val
total_items = sum(counts.values())

try:
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ") + " Only"
except:
    words = "Zero Only"

# --- SUMMARY ---
st.divider()
st.markdown(f'<p class="bold-text">Total      = ₹{grand_total}/-</p>', unsafe_allow_html=True)
st.write(f"**{words}**")
st.write(f"**Total {total_items} Notes / Coins**")

# --- WHATSAPP TEXT (Aligned) ---
st.divider()

whatsapp_text = f"Entry Name : {user_name}\n"
whatsapp_text += f"Date : {report_date.strftime('%a, %d %b %Y')}\n\n"

for n in notes:
    if counts[n] > 0:
        # padding added for straight lines on WhatsApp
        whatsapp_text += f"₹{n:<4} x {counts[n]:<2} = ₹ {n*counts[n]:>5}/-\n"

if coin_val > 0:
    whatsapp_text += f"Coins      = ₹ {coin_val:>5}/-\n"

whatsapp_text += "--------------------------------\n"
whatsapp_text += f"Total      = ₹ {grand_total:>5}/-\n"
whatsapp_text += f"{words}\n"
whatsapp_text += f"Total {total_items} Notes / Coins"

whatsapp_url = f"https://wa.me/?text={whatsapp_text.replace(' ', '%20').replace('\n', '%0A')}"

st.markdown(f'''
    <a href="{whatsapp_url}" target="_blank">
        <button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-size:18px; font-weight:bold;">
            📲 Share on WhatsApp
        </button>
    </a>
''', unsafe_allow_html=True)
