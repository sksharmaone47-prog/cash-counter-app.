import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# CSS for Strict Single Line Table & Green Theme
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; }
    
    /* Table Styling for Absolute Alignment */
    table { width: 100%; border-collapse: collapse; }
    td { padding: 5px 2px; vertical-align: middle; }
    .label-cell { font-weight: bold; font-size: 16px; width: 50px; }
    .sign-cell { font-weight: bold; font-size: 16px; width: 20px; text-align: center; }
    .total-cell { font-weight: bold; font-size: 18px; text-align: right; width: 100px; font-family: monospace; color: #1b5e20; }
    
    /* Input Styling */
    div[data-baseweb="input"] {
        width: 75px !important;
        height: 38px !important;
        background-color: white !important;
        border: 1px solid #999 !important;
    }
    input { text-align: center !important; font-weight: bold !important; font-size: 18px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Cash Denomination")

# Sidebar
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

st.markdown(f"**Entry Name :** {user_name}")
st.markdown(f"**Date :** {report_date.strftime('%a, %d %b %Y')}")
st.divider()

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- HTML TABLE FOR FIXED LAYOUT ---
# Is tareeke se layout kabhi nahi tootega
for n in notes:
    col_label, col_input, col_total = st.columns([1, 1, 2])
    with col_label:
        st.markdown(f"<p style='margin-top:8px;'><b>₹{n} x</b></p>", unsafe_allow_html=True)
    with col_input:
        val = st.text_input(f"q_{n}", value="", placeholder="0", key=f"k_{n}", label_visibility="collapsed")
        count = int(val) if val.isdigit() else 0
        counts[n] = count
    with col_total:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p style='margin-top:8px; text-align:right; font-family:monospace;'><b>= {subtotal}</b></p>", unsafe_allow_html=True)

# Coins Row (No Divider here)
col_l, col_i, col_t = st.columns([1, 1, 2])
with col_l:
    st.markdown("<p style='margin-top:8px;'><b>Coins</b></p>", unsafe_allow_html=True)
with col_i:
    c_str = st.text_input("c_v", value="", placeholder="0", key="c_k", label_visibility="collapsed")
    coin_val = int(c_str) if c_str.isdigit() else 0
with col_t:
    st.markdown(f"<p style='margin-top:8px; text-align:right; font-family:monospace;'><b>= {coin_val}</b></p>", unsafe_allow_html=True)

# Calculations
grand_total = sum(totals) + coin_val
total_items = sum(counts.values())

try:
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words = "Zero Only"

# --- SUMMARY ---
st.divider()
st.markdown(f"### Total = ₹ {grand_total}")
st.write(f"*{words}*")

# --- WHATSAPP SHARE ---
whatsapp_text = f"Entry Name : {user_name}\nDate : {report_date.strftime('%d %b %y')}\n\n"
for n in notes:
    if counts[n] > 0:
        whatsapp_text += f"₹{n:<4} x {counts[n]:<2} = {n*counts[n]:>7}\n"
if coin_val > 0:
    whatsapp_text += f"Coins      = {coin_val:>7}\n"
whatsapp_text += "------------------------------\n"
whatsapp_text += f"Total      = ₹ {grand_total:>7}\n"
whatsapp_text += f"{words}"

whatsapp_url = f"https://wa.me/?text={whatsapp_text.replace(' ', '%20').replace('\n', '%0A')}"

st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-size:18px; font-weight:bold;">📲 Share on WhatsApp</button></a>''', unsafe_allow_html=True)

if st.button("🔄 Reset"):
    st.rerun()
