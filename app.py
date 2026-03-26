import streamlit as st
from datetime import datetime
import pytz
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered")

# CSS for STRICT SINGLE LINE (Table Layout)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; }
    
    /* Hide +/- Buttons Always */
    button[data-testid="step-up"], button[data-testid="step-down"] {
        display: none !important;
    }

    /* Professional Table Styling */
    .denom-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }
    .denom-table td {
        padding: 8px 2px;
        vertical-align: middle;
    }

    /* Input Box Styling inside Table */
    div[data-baseweb="input"] {
        width: 65px !important;
        height: 35px !important;
        background-color: white !important;
        border: 1px solid #1b5e20 !important;
        border-radius: 4px !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
        padding: 0px !important;
    }
    
    .label-cell { font-weight: bold; font-size: 17px; width: 20%; }
    .sign-cell { font-weight: bold; font-size: 16px; width: 10%; text-align: center; }
    .input-cell { width: 25%; text-align: center; }
    .equal-cell { font-weight: bold; font-size: 16px; width: 10%; text-align: center; }
    .total-cell { font-weight: bold; font-size: 18px; color: #1b5e20; text-align: right; width: 35%; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- LIVE DATE & SETTINGS ---
IST = pytz.timezone('Asia/Kolkata')
now = datetime.now(IST)
auto_day = now.strftime("%A") 
auto_date = now.strftime("%d %b %Y")

with st.sidebar:
    st.markdown("## ⚙️ Settings")
    user_name = st.text_input("Name:", value="Sandeep")
    st.divider()
    st.info(f"Today: {auto_day}\n{auto_date}")

# --- HEADER ---
st.markdown(f"<h2 style='text-align: center; margin-bottom: 0;'>🏦 Cash Denomination</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 18px; font-weight: bold;'>Name: {user_name} | {auto_day}</p>", unsafe_allow_html=True)
st.divider()

if 'rid' not in st.session_state:
    st.session_state.rid = 0

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- CALCULATION SECTION (STRICT TABLE) ---
for n in notes:
    # We use Streamlit columns but with very tiny gaps and forced alignment
    c1, c2, c3, c4, c5 = st.columns([0.6, 0.2, 0.8, 0.2, 1.5])
    
    with c1:
        st.markdown(f"<p style='font-weight:bold; font-size:17px; margin-top:8px;'>₹{n}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<p style='font-weight:bold; font-size:17px; margin-top:8px; text-align:center;'>x</p>", unsafe_allow_html=True)
    with c3:
        # number_input without buttons for best focus
        count = st.number_input(f"q_{n}", min_value=0, step=1, value=0, key=f"n_{n}_{st.session_state.rid}", label_visibility="collapsed")
        counts[n] = count
    with c4:
        st.markdown(f"<p style='font-weight:bold; font-size:17px; margin-top:8px; text-align:center;'>=</p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p style='font-weight:bold; font-size:18px; color:#1b5e20; margin-top:8px; text-align:right; font-family:monospace;'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Section
st.write("")
cc1, cc2, cc3, cc4, cc5 = st.columns([0.6, 0.2, 0.8, 0.2, 1.5])
with cc1:
    st.markdown(f"<p style='font-weight:bold; font-size:17px; margin-top:8px;'>Coins</p>", unsafe_allow_html=True)
with cc2:
    st.markdown(f"<p style='font-weight:bold; font-size:17px; margin-top:8px; text-align:center;'>+</p>", unsafe_allow_html=True)
with cc3:
    coin_val = st.number_input("c_v", min_value=0, step=1, value=0, key=f"c_{st.session_state.rid}", label_visibility="collapsed")
with cc4:
    st.markdown(f"<p style='font-weight:bold; font-size:17px; margin-top:8px; text-align:center;'>=</p>", unsafe_allow_html=True)
with cc5:
    st.markdown(f"<p style='font-weight:bold; font-size:18px; color:#1b5e20; margin-top:8px; text-align:right; font-family:monospace;'>{coin_val}</p>", unsafe_allow_html=True)

# Grand Total
grand_total = sum(totals) + coin_val
try:
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words = "Zero Only"

st.divider()
st.markdown(f"<h2 style='text-align: center; color: #1b5e20;'>Total = ₹ {grand_total}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 16px;'>{words}</p>", unsafe_allow_html=True)

# --- WHATSAPP & DOWNLOAD ---
st.divider()
whatsapp_msg = f"*Cash Denomination Report*\nName: {user_name}\nDate: {auto_date}\n\n"
for n in notes:
    if counts[n] > 0:
        whatsapp_msg += f"₹{n:<4} x {counts[n]:<2} = {n*counts[n]:>7}\n"
if coin_val > 0:
    whatsapp_msg += f"Coins      = {coin_val:>7}\n"
whatsapp_msg += "------------------------------\n"
whatsapp_msg += f"Total      = ₹ {grand_total:>7}\n"
whatsapp_msg += f"{words}"

wa_url = f"https://wa.me/?text={whatsapp_msg.replace(' ', '%20').replace('\n', '%0A')}"
st.markdown(f'''<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-weight:bold; font-size:18px; margin-bottom:10px;">📲 WhatsApp Share</button></a>''', unsafe_allow_html=True)

if st.button("🔄 Reset / Clear All", use_container_width=True):
    st.session_state.rid += 1
    st.rerun()
    
