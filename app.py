import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# CSS for Strict Single Line & Professional Alignment (Matching your Image)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #ffffff; }
    
    /* Hide +/- Buttons Always */
    button[data-testid="step-up"], button[data-testid="step-down"] {
        display: none !important;
    }
    
    /* Input Box Styling */
    div[data-baseweb="input"] {
        width: 60px !important;
        height: 35px !important;
        background-color: #f0f2f6 !important;
        border: 1px solid #ccc !important;
        margin: 0 5px !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
    }

    /* Fixed Row Layout */
    .calc-container {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        width: 100%;
        margin-bottom: 10px;
    }
    .label-box { min-width: 60px; font-weight: bold; font-size: 18px; }
    .sign-box { min-width: 20px; text-align: center; font-weight: bold; }
    .result-box { flex-grow: 1; text-align: right; font-weight: bold; font-size: 19px; font-family: monospace; padding-right: 15px; }
    
    .summary-text { font-size: 20px; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar for Settings
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

# --- APP HEADER (Matching your Image) ---
st.markdown(f"<p class='summary-text'>Name : {user_name}</p>", unsafe_allow_html=True)
st.markdown(f"<p class='summary-text'>Date : {report_date.strftime('%d %b %y')}</p>", unsafe_allow_html=True)
st.divider()

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- CALCULATION SECTION ---
for n in notes:
    # We use columns but with very tight ratios to keep it on one line
    c1, c2, c3, c4, c5 = st.columns([1, 0.4, 1.2, 0.4, 2])
    
    with c1:
        st.markdown(f"<p style='font-size:18px; font-weight:bold; margin-top:8px;'>₹{n}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p style='font-size:18px; font-weight:bold; margin-top:8px;'>x</p>", unsafe_allow_html=True)
    with c3:
        # User Input Box
        count = st.number_input(f"n_{n}", min_value=0, step=1, value=0, key=f"key_{n}", label_visibility="collapsed")
        counts[n] = count
    with c4:
        st.markdown("<p style='font-size:18px; font-weight:bold; margin-top:8px;'>=</p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p style='font-size:18px; font-weight:bold; margin-top:8px; text-align:right; font-family:monospace;'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Section
c_col1, c_col2, c_col3, c_col4, c_col5 = st.columns([1, 0.4, 1.2, 0.4, 2])
with c_col1:
    st.markdown("<p style='font-size:18px; font-weight:bold; margin-top:8px;'>Coins</p>", unsafe_allow_html=True)
with c_col2:
    pass
with c_col3:
    pass # Empty
with c_col4:
    st.markdown("<p style='font-size:18px; font-weight:bold; margin-top:8px;'>=</p>", unsafe_allow_html=True)
with c_col5:
    coin_val = st.number_input("coin_v", min_value=0, step=1, value=0, key="coin_k", label_visibility="collapsed")
    st.markdown(f"<p style='font-size:18px; font-weight:bold; margin-top:8px; text-align:right; font-family:monospace;'>{coin_val}</p>", unsafe_allow_html=True)

# Final Calculations
grand_total = sum(totals) + coin_val
total_items = sum(counts.values())

try:
    # Hindi/English Numbers to Words
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words = "Zero Only"

# --- TOTAL SUMMARY (Matching your Image) ---
st.markdown("<p style='text-align:center;'>-----------------------------------------</p>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align:center;'>Total &nbsp;&nbsp;&nbsp; = ₹ &nbsp; {grand_total}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-weight:bold; font-size:18px;'>{words}</p>", unsafe_allow_html=True)

# --- WHATSAPP BUTTON ---
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
