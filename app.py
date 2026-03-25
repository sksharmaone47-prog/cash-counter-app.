import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# Styling for rigid single-line row (No wrapping)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; }
    .bold-text { font-size: 20px !important; font-weight: bold !important; color: #000000; }
    
    /* Chrome/Safari arrows remove */
    input::-webkit-outer-spin-button, input::-webkit-inner-spin-button {
        -webkit-appearance: none; margin: 0;
    }
    
    /* Table row setup for absolute straight line */
    .row-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
        background-color: transparent;
    }
    .label-box { width: 60px; font-weight: bold; font-size: 18px; }
    .sign-box { width: 20px; font-weight: bold; font-size: 18px; text-align: center; }
    .total-box { width: 100px; font-weight: bold; font-size: 18px; color: #1b5e20; text-align: right; font-family: monospace; }
    
    /* Small Input Box */
    div[data-baseweb="input"] {
        width: 80px !important;
        height: 40px !important;
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

# Header
st.markdown(f'<p class="bold-text">Entry Name : {user_name}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="bold-text">Date : {report_date.strftime("%a, %d %b %Y")}</p>', unsafe_allow_html=True)

st.divider()

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- RIGID SINGLE LINE LAYOUT ---
for n in notes:
    # Creating a manual row using columns but with tight spacing
    col1, col2, col3, col4, col5 = st.columns([1, 0.5, 1.5, 0.5, 2])
    
    with col1:
        st.markdown(f"<p style='margin-top:10px; font-size:18px;'><b>₹{n}</b></p>", unsafe_allow_html=True)
    with col2:
        st.markdown("<p style='margin-top:10px; font-size:18px;'><b>x</b></p>", unsafe_allow_html=True)
    with col3:
        # Input Box
        val = st.text_input(f"qty_{n}", value="0", key=f"k_{n}", label_visibility="collapsed")
        count = int(val) if val.isdigit() else 0
        counts[n] = count
    with col4:
        st.markdown("<p style='margin-top:10px; font-size:18px;'><b>=</b></p>", unsafe_allow_html=True)
    with col5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p style='margin-top:10px; font-size:18px; text-align:right; font-family:monospace;'><b>{subtotal}</b></p>", unsafe_allow_html=True)

# Coins Row
st.divider()
cc1, cc2, cc3 = st.columns([1.5, 1.5, 2.5])
with cc1:
    st.markdown("<p style='margin-top:10px; font-size:18px;'><b>Coins</b></p>", unsafe_allow_html=True)
with cc2:
    c_str = st.text_input("c_v", value="0", key="c_k", label_visibility="collapsed")
    coin_val = int(c_str) if c_str.isdigit() else 0
with cc3:
    st.markdown(f"<p style='margin-top:10px; font-size:18px; text-align:right; font-family:monospace;'><b>= {coin_val}</b></p>", unsafe_allow_html=True)

# Final Calculations
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
st.write(f"Total {total_items} Notes / Coins")

# --- WHATSAPP ---
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

st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-weight:bold;">📲 Share on WhatsApp</button></a>''', unsafe_allow_html=True)

if st.button("🔄 Clear"):
    st.rerun()
