import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# CSS for Strict Single Line Layout & Professional Look
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #f1f8e9; }
    
    /* Input box styling to look like a simple underline/flat box */
    div[data-baseweb="input"] {
        width: 60px !important;
        height: 30px !important;
        background-color: white !important;
        border: none !important;
        border-bottom: 2px solid #1b5e20 !important;
        border-radius: 0px !important;
        margin: 0 10px !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
        padding: 0px !important;
    }
    
    /* Row styling to keep everything in one straight line */
    .calc-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        font-family: 'Courier New', Courier, monospace;
        font-size: 20px;
        font-weight: bold;
        color: #000;
        margin-bottom: 15px;
        white-space: nowrap;
    }
    .result-text { color: #1b5e20; margin-left: auto; padding-right: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Cash Denomination")

# Sidebar for metadata
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

st.markdown(f"**Entry Name:** {user_name} | **Date:** {report_date.strftime('%d %b %Y')}")
st.divider()

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- STABLE ROW LAYOUT ---
for n in notes:
    # Manual Row Construction using HTML + Streamlit Input
    container = st.container()
    col_label, col_input, col_equal, col_total = st.columns([1, 1, 0.5, 2])
    
    with col_label:
        st.markdown(f"<p style='font-size:18px; font-weight:bold; margin-top:5px;'>₹{n} x</p>", unsafe_allow_html=True)
    with col_input:
        # text_input is used to avoid +/- buttons and large boxes
        val = st.text_input(f"q_{n}", value="0", key=f"k_{n}", label_visibility="collapsed")
        count = int(val) if val.isdigit() else 0
        counts[n] = count
    with col_equal:
        st.markdown("<p style='font-size:18px; font-weight:bold; margin-top:5px;'>=</p>", unsafe_allow_html=True)
    with col_total:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p style='font-size:18px; font-weight:bold; margin-top:5px; text-align:right; color:#1b5e20;'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Section (Tight Alignment)
st.divider()
c_col1, c_col2, c_col3, c_col4 = st.columns([1, 1, 0.5, 2])
with c_col1:
    st.markdown("<p style='font-size:18px; font-weight:bold; margin-top:5px;'>Coins</p>", unsafe_allow_html=True)
with c_col2:
    c_val_str = st.text_input("c_v", value="0", key="c_key", label_visibility="collapsed")
    coin_val = int(c_val_str) if c_val_str.isdigit() else 0
with c_col3:
    st.markdown("<p style='font-size:18px; font-weight:bold; margin-top:5px;'>=</p>", unsafe_allow_html=True)
with c_col4:
    st.markdown(f"<p style='font-size:18px; font-weight:bold; margin-top:5px; text-align:right; color:#1b5e20;'>{coin_val}</p>", unsafe_allow_html=True)

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

st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; cursor:pointer; font-weight:bold;">📲 WhatsApp Share</button></a>''', unsafe_allow_html=True)

if st.button("🔄 Reset App"):
    st.rerun()
