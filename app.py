import streamlit as st
from datetime import datetime
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# CSS for Strict Single Line, No Buttons, and No Gaps
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #ffffff; }
    
    /* Remove +/- Buttons from Number Inputs */
    button[data-testid="step-up"], button[data-testid="step-down"] {
        display: none !important;
    }
    
    /* Remove column gaps and padding */
    [data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
        width: fit-content !important;
        flex: unset !important;
    }

    /* Tighten Input Box */
    div[data-baseweb="input"] {
        width: 70px !important;
        height: 38px !important;
        background-color: white !important;
        border: 1px solid #999 !important;
        margin: 0 5px !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
        padding: 0px !important;
    }

    .row-text {
        font-weight: bold;
        font-size: 18px;
        margin-top: 10px;
        white-space: nowrap;
    }
    </style>
    """, unsafe_allow_html=True)

# --- AUTOMATIC DATE & DAY ---
# Aaj ki date aur din automatic change hoga
now = datetime.now()
current_day = now.strftime("%A")  # Jaise: Thursday
current_date = now.strftime("%d %b %Y")

# Sidebar
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Name:", value="Sandeep")

# Header
st.markdown(f"<h3 style='text-align: center; margin-bottom: 0;'>Name : {user_name}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 18px;'>{current_day} | {current_date}</p>", unsafe_allow_html=True)
st.divider()

# Reset functionality
if 'reset_counter' not in st.session_state:
    st.session_state.reset_counter = 0

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- FIXED SINGLE LINE LAYOUT ---
for n in notes:
    # Tight columns for absolute alignment
    c1, c2, c3, c4, c5 = st.columns([0.6, 0.3, 1, 0.3, 2])
    
    with c1:
        st.markdown(f"<p class='row-text'>₹{n}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p class='row-text'>x</p>", unsafe_allow_html=True)
    with c3:
        # number_input helps "Next" button work on mobile keyboards
        count = st.number_input(f"n_{n}", min_value=0, step=1, value=0, key=f"k_{n}_{st.session_state.reset_counter}", label_visibility="collapsed")
        counts[n] = count
    with c4:
        st.markdown("<p class='row-text'>=</p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p class='row-text' style='color:#1b5e20; text-align:right;'>{subtotal}</p>", unsafe_allow_html=True)

# --- COINS SECTION (No Divider line here) ---
cc1, cc2, cc3, cc4, cc5 = st.columns([0.6, 0.3, 1, 0.3, 2])
with cc1:
    st.markdown("<p class='row-text'>Coins</p>", unsafe_allow_html=True)
with cc2:
    st.markdown("<p class='row-text'>+</p>", unsafe_allow_html=True)
with cc3:
    coin_val = st.number_input("coin_in", min_value=0, step=1, value=0, key=f"c_{st.session_state.reset_counter}", label_visibility="collapsed")
with cc4:
    st.markdown("<p class='row-text'>=</p>", unsafe_allow_html=True)
with cc5:
    st.markdown(f"<p class='row-text' style='color:#1b5e20; text-align:right;'>{coin_val}</p>", unsafe_allow_html=True)

# Calculations
grand_total = sum(totals) + coin_val
try:
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words = "Zero Only"

# --- SUMMARY ---
st.divider()
st.markdown(f"<h2 style='text-align: center;'>Total = ₹ {grand_total}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold;'>{words}</p>", unsafe_allow_html=True)

# --- BUTTONS ---
st.divider()

# WhatsApp
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
st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-weight:bold; font-size:18px;">📲 WhatsApp Share</button></a>''', unsafe_allow_html=True)

# Working Reset Button
if st.button("🔄 Clear / Reset App", use_container_width=True):
    st.session_state.reset_counter += 1
    st.rerun()
