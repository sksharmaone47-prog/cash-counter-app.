import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# CSS for Strict Single Line & Professional Flat Look
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #ffffff; }
    
    /* Input box ko ekdum simple underline banane ke liye */
    div[data-baseweb="input"] {
        width: 65px !important;
        height: 32px !important;
        background-color: transparent !important;
        border: none !important;
        border-bottom: 2px solid #1b5e20 !important;
        border-radius: 0px !important;
        margin: 0 5px !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
        padding: 0px !important;
        background-color: transparent !important;
    }
    
    /* Hide +/- Buttons Always */
    button[data-testid="step-up"], button[data-testid="step-down"] {
        display: none !important;
    }

    /* Fixed Row Layout for Mobile Portrait */
    .calc-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        margin-bottom: 12px;
    }
    .row-item { font-weight: bold; font-size: 18px; color: black; }
    .result-item { font-weight: bold; font-size: 18px; color: #1b5e20; min-width: 80px; text-align: right; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

# Header
st.markdown(f"<h3 style='text-align: center; margin-bottom: 0;'>Name : {user_name}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold;'>Date : {report_date.strftime('%d %b %y')}</p>", unsafe_allow_html=True)
st.divider()

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- CLEAN TABLE LAYOUT ---
for n in notes:
    # Creating a manual row that NEVER wraps
    col_label, col_input, col_equal, col_total = st.columns([1, 1, 0.5, 2])
    
    with col_label:
        st.markdown(f"<p style='margin-top:5px; font-weight:bold; font-size:18px;'>₹{n} &nbsp; x</p>", unsafe_allow_html=True)
    with col_input:
        # text_input used to avoid all boxes and buttons
        val = st.text_input(f"q_{n}", value="0", key=f"k_{n}", label_visibility="collapsed")
        count = int(val) if val.isdigit() else 0
        counts[n] = count
    with col_equal:
        st.markdown("<p style='margin-top:5px; font-weight:bold; font-size:18px;'>=</p>", unsafe_allow_html=True)
    with col_total:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p style='margin-top:5px; font-weight:bold; font-size:18px; text-align:right; color:#1b5e20;'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Row
st.divider()
cl1, cl2, cl3, cl4 = st.columns([1, 1, 0.5, 2])
with cl1:
    st.markdown("<p style='margin-top:5px; font-weight:bold; font-size:18px;'>Coins</p>", unsafe_allow_html=True)
with cl2:
    c_val_str = st.text_input("c_v", value="0", key="c_key", label_visibility="collapsed")
    coin_val = int(c_val_str) if c_val_str.isdigit() else 0
with cl3:
    st.markdown("<p style='margin-top:5px; font-weight:bold; font-size:18px;'>=</p>", unsafe_allow_html=True)
with cl4:
    st.markdown(f"<p style='margin-top:5px; font-weight:bold; font-size:18px; text-align:right; color:#1b5e20;'>{coin_val}</p>", unsafe_allow_html=True)

# Calculations
grand_total = sum(totals) + coin_val
try:
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words = "Zero Only"

# --- SUMMARY ---
st.markdown("<p style='text-align:center;'>-----------------------------------------</p>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center;'>Total &nbsp; = &nbsp; ₹ {grand_total}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-weight:bold;'>{words}</p>", unsafe_allow_html=True)

# --- WHATSAPP ---
st.divider()
whatsapp_text = f"Name : {user_name}\nDate : {report_date.strftime('%d %b %y')}\n\n"
for n in notes:
    if counts[n] > 0:
        whatsapp_text += f"₹{n:<4} x {counts[n]:<2} = {n*counts[n]:>7}\n"
if coin_val > 0:
    whatsapp_text += f"Coins      = {coin_val:>7}\n"
whatsapp_text += "------------------------------\n"
whatsapp_text += f"Total      = ₹ {grand_total:>7}\n"
whatsapp_text += f"{words}"

whatsapp_url = f"https://wa.me/?text={whatsapp_text.replace(' ', '%20').replace('\n', '%0A')}"

st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-weight:bold; font-size:18px;">📲 Share on WhatsApp</button></a>''', unsafe_allow_html=True)

if st.button("🔄 Reset App"):
    st.rerun()
