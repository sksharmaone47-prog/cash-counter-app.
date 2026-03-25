import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered")

# CSS for Strict Single Line & Clean UI
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #ffffff; }
    
    /* Input box styling - No borders, just a simple underline */
    div[data-baseweb="input"] {
        width: 60px !important;
        height: 32px !important;
        background-color: transparent !important;
        border: none !important;
        border-bottom: 2px solid #1b5e20 !important;
        border-radius: 0px !important;
        margin: 0px !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
        padding: 0px !important;
    }
    
    /* Hide +/- Buttons */
    button[data-testid="step-up"], button[data-testid="step-down"] {
        display: none !important;
    }

    /* Column spacing for straight line */
    [data-testid="column"] {
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .row-text { font-size: 18px; font-weight: bold; margin: 0; white-space: nowrap; }
    .total-text { font-size: 18px; font-weight: bold; color: #1b5e20; text-align: right; width: 100%; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- AUTOMATIC DATE & DAY ---
today = date.today()
current_day = today.strftime("%A") # Jaise: Monday, Tuesday
current_date = today.strftime("%d %b %Y")

# Sidebar for Name
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Name:", value="Sandeep")

# Header Display
st.markdown(f"<h3 style='text-align: center; margin-bottom: 0;'>Name : {user_name}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 18px; color: #555;'>{current_day} | {current_date}</p>", unsafe_allow_html=True)
st.divider()

# Reset functionality using session state
if 'reset_key' not in st.session_state:
    st.session_state.reset_key = 0

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- CALCULATION TABLE ---
for n in notes:
    c1, c2, c3, c4, c5 = st.columns([1, 0.3, 1, 0.3, 2])
    
    with c1:
        st.markdown(f"<p class='row-text'>₹{n}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p class='row-text'>x</p>", unsafe_allow_html=True)
    with c3:
        # text_input with dynamic key for reset
        val = st.text_input(f"q_{n}", value="0", key=f"n_{n}_{st.session_state.reset_key}", label_visibility="collapsed")
        count = int(val) if val.isdigit() else 0
        counts[n] = count
    with c4:
        st.markdown("<p class='row-text'>=</p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p class='total-text'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Row
st.divider()
cl1, cl2, cl3, cl4, cl5 = st.columns([1, 0.3, 1, 0.3, 2])
with cl1:
    st.markdown("<p class='row-text'>Coins</p>", unsafe_allow_html=True)
with cl2:
    st.markdown("<p class='row-text'>+</p>", unsafe_allow_html=True)
with cl3:
    c_val_str = st.text_input("cv", value="0", key=f"coin_{st.session_state.reset_key}", label_visibility="collapsed")
    coin_val = int(c_val_str) if c_val_str.isdigit() else 0
with cl4:
    st.markdown("<p class='row-text'>=</p>", unsafe_allow_html=True)
with cl5:
    st.markdown(f"<p class='total-text'>{coin_val}</p>", unsafe_allow_html=True)

# Final Total
grand_total = sum(totals) + coin_val
try:
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words = "Zero Only"

# --- SUMMARY ---
st.markdown("<p style='text-align:center;'>-----------------------------------------</p>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align:center; color: black;'>Total = ₹ {grand_total}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-weight:bold; font-size:18px;'>{words}</p>", unsafe_allow_html=True)

# --- BUTTONS ---
st.divider()

# WhatsApp Share
whatsapp_text = f"Name : {user_name}\nDay : {current_day}\nDate : {current_date}\n\n"
for n in notes:
    if counts[n] > 0:
        whatsapp_text += f"₹{n:<4} x {counts[n]:<2} = {n*counts[n]:>7}\n"
if coin_val > 0:
    whatsapp_text += f"Coins      = {coin_val:>7}\n"
whatsapp_text += "------------------------------\n"
whatsapp_text += f"Total      = ₹ {grand_total:>7}\n"
whatsapp_text += f"{words}"

whatsapp_url = f"https://wa.me/?text={whatsapp_text.replace(' ', '%20').replace('\n', '%0A')}"
st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; cursor:pointer; font-weight:bold; font-size:18px; margin-bottom:10px;">📲 WhatsApp Share</button></a>''', unsafe_allow_html=True)

# Working Reset Button
if st.button("🔄 Reset / Clear All", use_container_width=True):
    st.session_state.reset_key += 1
    st.rerun()
