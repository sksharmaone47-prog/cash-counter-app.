import streamlit as st
from datetime import datetime
import pytz
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered")

# CSS for ZERO GAP & STRICT SINGLE LINE
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

    /* Force all columns to have zero gap and stay in one line */
    [data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
        min-width: unset !important;
        flex: unset !important;
        display: flex !important;
        align-items: center !important;
    }

    /* Input Box Styling - Very Tight */
    div[data-baseweb="input"] {
        width: 65px !important;
        height: 35px !important;
        background-color: white !important;
        border: 1px solid #1b5e20 !important;
        border-radius: 4px !important;
        margin: 0 5px !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
        padding: 0px !important;
    }
    
    .row-text { font-weight: bold; font-size: 17px; margin: 0px !important; white-space: nowrap; }
    .total-text { font-weight: bold; font-size: 18px; color: #1b5e20; font-family: monospace; text-align: right; width: 100%; }
    
    .header-info { text-align: center; font-weight: bold; margin-bottom: 0px; }
    </style>
    """, unsafe_allow_html=True)

# --- SETTINGS SECTION (Sidebar) ---
IST = pytz.timezone('Asia/Kolkata')
default_now = datetime.now(IST)

with st.sidebar:
    st.markdown("## ⚙️ App Settings")
    # Editable Name
    user_name = st.text_input("Edit Name:", value="Sandeep")
    # Editable Date
    selected_date = st.date_input("Edit Date:", value=default_now)
    
    display_day = selected_date.strftime("%A")
    display_date = selected_date.strftime("%d %b %Y")
    st.divider()
    st.success(f"Updated:\n{display_day}\n{display_date}")

# --- HEADER (Displaying Edited Name & Date) ---
st.markdown(f"<h2 style='text-align: center; margin-bottom: 0;'>🏦 Cash Denomination</h2>", unsafe_allow_html=True)
st.markdown(f"<p class='header-info' style='font-size: 20px; color: black;'>Name: {user_name}</p>", unsafe_allow_html=True)
st.markdown(f"<p class='header-info' style='font-size: 18px; color: #1b5e20;'>{display_day} | {display_date}</p>", unsafe_allow_html=True)
st.divider()

if 'rid' not in st.session_state:
    st.session_state.rid = 0

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- CALCULATION SECTION (STRICT 5-COLUMN) ---
for n in notes:
    c1, c2, c3, c4, c5 = st.columns([0.5, 0.2, 0.8, 0.2, 1.5])
    
    with c1:
        st.markdown(f"<p class='row-text'>₹{n}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<p class='row-text'>x</p>", unsafe_allow_html=True)
    with c3:
        # number_input with hidden buttons for 'Next' key support
        count = st.number_input(f"q_{n}", min_value=0, step=1, value=0, key=f"n_{n}_{st.session_state.rid}", label_visibility="collapsed")
        counts[n] = count
    with c4:
        st.markdown(f"<p class='row-text'>=</p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p class='total-text'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Row
st.markdown("<div style='margin-top:5px;'></div>", unsafe_allow_html=True)
cc1, cc2, cc3, cc4, cc5 = st.columns([0.5, 0.2, 0.8, 0.2, 1.5])
with cc1:
    st.markdown(f"<p class='row-text'>Coins</p>", unsafe_allow_html=True)
with cc2:
    st.markdown(f"<p class='row-text'>+</p>", unsafe_allow_html=True)
with cc3:
    coin_val = st.number_input("c_v", min_value=0, step=1, value=0, key=f"c_{st.session_state.rid}", label_visibility="collapsed")
with cc4:
    st.markdown(f"<p class='row-text'>=</p>", unsafe_allow_html=True)
with cc5:
    st.markdown(f"<p class='total-text'>{coin_val}</p>", unsafe_allow_html=True)

# Calculations
grand_total = sum(totals) + coin_val
try:
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words = "Zero Only"

# --- SUMMARY ---
st.divider()
st.markdown(f"<h2 style='text-align: center; color: #1b5e20;'>Total = ₹ {grand_total}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 16px; color: black;'>{words}</p>", unsafe_allow_html=True)

# --- WHATSAPP SHARE ---
st.divider()
whatsapp_msg = f"*Cash Denomination Report*\nName: {user_name}\nDate: {display_date} ({display_day})\n\n"
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
