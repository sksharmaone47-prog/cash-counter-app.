import streamlit as st
from datetime import datetime
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered")

# CSS for Strict Single Line, No Buttons, and Settings Toggle
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #ffffff; }
    
    /* Hide +/- Buttons */
    button[data-testid="step-up"], button[data-testid="step-down"] {
        display: none !important;
    }
    
    /* Force Row to stay in one line */
    .custom-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        width: 100%;
        margin-bottom: 12px;
    }

    /* Input Box size & style */
    div[data-baseweb="input"] {
        width: 70px !important;
        height: 38px !important;
        background-color: white !important;
        border: 1px solid #999 !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
    }

    .row-label { font-weight: bold; font-size: 17px; min-width: 50px; }
    .row-sign { font-weight: bold; font-size: 17px; margin: 0 5px; }
    .row-total { font-weight: bold; font-size: 18px; color: #1b5e20; text-align: right; min-width: 80px; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

# --- AUTOMATIC DATE & DAY ---
now = datetime.now()
current_day = now.strftime("%A")  # Thursday
current_date = now.strftime("%d %b %Y") # 26 Mar 2026

# --- SETTINGS OPTION ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Sandeep"

show_settings = st.checkbox("⚙️ Open Settings (Name Change)")
if show_settings:
    st.session_state.user_name = st.text_input("Edit Name:", value=st.session_state.user_name)

# --- APP HEADER ---
st.markdown(f"<h3 style='text-align: center; margin-bottom: 0;'>Name : {st.session_state.user_name}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 18px; color: #555;'>{current_day} | {current_date}</p>", unsafe_allow_html=True)
st.divider()

# Reset functionality
if 'reset_val' not in st.session_state:
    st.session_state.reset_val = 0

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- CALCULATION SECTION ---
for n in notes:
    # Manual row layout using columns but with tight control
    c1, c2, c3, c4, c5 = st.columns([1, 0.4, 1.2, 0.4, 2])
    
    with c1:
        st.markdown(f"<p class='row-label' style='margin-top:8px;'>₹{n}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p class='row-sign' style='margin-top:8px;'>x</p>", unsafe_allow_html=True)
    with c3:
        # number_input with hidden buttons for 'Next' key support
        count = st.number_input(f"n_{n}", min_value=0, step=1, value=0, key=f"k_{n}_{st.session_state.reset_val}", label_visibility="collapsed")
        counts[n] = count
    with c4:
        st.markdown("<p class='row-sign' style='margin-top:8px;'>=</p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p class='row-total' style='margin-top:8px;'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Section (No line between 10 and Coins)
cc1, cc2, cc3, cc4, cc5 = st.columns([1, 0.4, 1.2, 0.4, 2])
with cc1:
    st.markdown("<p class='row-label' style='margin-top:8px;'>Coins</p>", unsafe_allow_html=True)
with cc2:
    st.markdown("<p class='row-sign' style='margin-top:8px;'>+</p>", unsafe_allow_html=True)
with cc3:
    coin_val = st.number_input("cv", min_value=0, step=1, value=0, key=f"c_{st.session_state.reset_val}", label_visibility="collapsed")
with cc4:
    st.markdown("<p class='row-sign' style='margin-top:8px;'>=</p>", unsafe_allow_html=True)
with cc5:
    st.markdown(f"<p class='row-total' style='margin-top:8px;'>{coin_val}</p>", unsafe_allow_html=True)

# Final Total
grand_total = sum(totals) + coin_val
try:
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words = "Zero Only"

# --- SUMMARY ---
st.divider()
st.markdown(f"<h2 style='text-align: center;'>Total = ₹ {grand_total}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 18px;'>{words}</p>", unsafe_allow_html=True)

# --- ACTION BUTTONS ---
st.divider()

# WhatsApp Button
whatsapp_text = f"Name : {st.session_state.user_name}\nDay : {current_day}\nDate : {current_date}\n\n"
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

# Clear Button
if st.button("🔄 Clear / Reset App", use_container_width=True):
    st.session_state.reset_val += 1
    st.rerun()
