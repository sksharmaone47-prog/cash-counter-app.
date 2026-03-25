import streamlit as st
from datetime import datetime
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Cash Denomination", 
    page_icon="🏦", 
    layout="centered"
)

# Professional Green Theme & Strict Alignment CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; } /* Light Green Background */
    
    /* Hide +/- Buttons Always */
    button[data-testid="step-up"], button[data-testid="step-down"] {
        display: none !important;
    }
    
    /* Input box styling - White box with border */
    div[data-baseweb="input"] {
        width: 70px !important;
        height: 38px !important;
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

    .row-text { font-size: 18px; font-weight: bold; color: #000; margin-top: 10px; white-space: nowrap; }
    .total-val { font-size: 19px; font-weight: bold; color: #1b5e20; text-align: right; margin-top: 10px; font-family: monospace; width: 100%; }
    
    /* Sidebar styling */
    .sidebar-title { color: #1b5e20; font-weight: bold; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- AUTOMATIC DATE & DAY ---
now = datetime.now()
auto_day = now.strftime("%A") 
auto_date = now.strftime("%d %b %Y")

# --- SIDEBAR: LOGO & NAME ---
with st.sidebar:
    st.markdown("<h2 class='sidebar-title'>🏦 Cash Denomination</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=100)
    st.divider()
    user_name = st.text_input("Entry Name:", value="Sandeep")
    st.info(f"Today: {auto_day}\n{auto_date}")

# --- MAIN HEADER ---
st.title("🏦 Cash Denomination")
st.markdown(f"<p style='font-size: 20px; font-weight: bold; color: #000;'>Name : {user_name}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size: 18px; font-weight: bold; color: #1b5e20;'>{auto_day} | {auto_date}</p>", unsafe_allow_html=True)
st.divider()

# Reset state
if 'reset_id' not in st.session_state:
    st.session_state.reset_id = 0

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- CALCULATION SECTION ---
for n in notes:
    c1, c2, c3, c4, c5 = st.columns([1, 0.4, 1.2, 0.4, 2.3])
    
    with c1:
        st.markdown(f"<p class='row-text'>₹{n}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p class='row-text'>x</p>", unsafe_allow_html=True)
    with c3:
        # number_input without buttons for best focus and Next key
        count = st.number_input(f"qty_{n}", min_value=0, step=1, value=0, key=f"k_{n}_{st.session_state.reset_id}", label_visibility="collapsed")
        counts[n] = count
    with c4:
        st.markdown("<p class='row-text'>=</p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p class='total-val'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Row (No line between 10 and Coins)
cc1, cc2, cc3, cc4, cc5 = st.columns([1, 0.4, 1.2, 0.4, 2.3])
with cc1:
    st.markdown("<p class='row-text'>Coins</p>", unsafe_allow_html=True)
with cc2:
    st.markdown("<p class='row-text'>+</p>", unsafe_allow_html=True)
with cc3:
    coin_val = st.number_input("cv", min_value=0, step=1, value=0, key=f"c_{st.session_state.reset_id}", label_visibility="collapsed")
with cc4:
    st.markdown("<p class='row-text'>=</p>", unsafe_allow_html=True)
with cc5:
    st.markdown(f"<p class='total-val'>{coin_val}</p>", unsafe_allow_html=True)

# Calculation logic
grand_total = sum(totals) + coin_val
try:
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words = "Zero Only"

# --- SUMMARY SECTION ---
st.divider()
st.markdown(f"<h2 style='text-align: center; color: #1b5e20;'>Total = ₹ {grand_total}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 18px; color: #000;'>{words}</p>", unsafe_allow_html=True)

# --- FOOTER ---
st.divider()

# WhatsApp Share
whatsapp_msg = f"*Cash Denomination*\nName: {user_name}\nDay: {auto_day}\nDate: {auto_date}\n\n"
for n in notes:
    if counts[n] > 0:
        whatsapp_msg += f"₹{n:<4} x {counts[n]:<2} = {n*counts[n]:>7}\n"
if coin_val > 0:
    whatsapp_msg += f"Coins      = {coin_val:>7}\n"
whatsapp_msg += "------------------------------\n"
whatsapp_msg += f"Total      = ₹ {grand_total:>7}\n"
whatsapp_msg += f"{words}"

wa_url = f"https://wa.me/?text={whatsapp_msg.replace(' ', '%20').replace('\n', '%0A')}"
st.markdown(f'''<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-weight:bold; font-size:18px;">📲 WhatsApp Share</button></a>''', unsafe_allow_html=True)

# Reset Button
if st.button("🔄 Clear / Reset App", use_container_width=True):
    st.session_state.reset_id += 1
    st.rerun()
    
