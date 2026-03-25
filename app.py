import streamlit as st
from datetime import import streamlit as st
from datetime import datetime
from num2words import num2words

# --- PAGE CONFIG (Setting Logo & Name for Browser Tab) ---
st.set_page_config(
    page_title="Cash Denomination - Sandeep", 
    page_icon="🏦", # Logo/Icon in Tab
    layout="centered"
)

# CSS for Strict Single Line & Professional Flat Look
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #ffffff; }
    
    /* Input box styling - Simple Underline (No Box/Borders) */
    div[data-baseweb="input"] {
        width: 65px !important;
        height: 32px !important;
        background-color: transparent !important;
        border: none !important;
        border-bottom: 2px solid #1b5e20 !important;
        border-radius: 0px !important;
        margin: 0px 5px !important;
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

    /* Column alignment for vertical portrait */
    [data-testid="column"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .row-item { font-weight: bold; font-size: 18px; color: black; white-space: nowrap; margin: 0; }
    .result-item { font-weight: bold; font-size: 19px; color: #1b5e20; text-align: right; width: 100%; font-family: monospace; }
    
    p { margin-bottom: 0px !important; line-height: 1.2 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- AUTOMATIC DATE & DAY (Dynamics) ---
# Ye page open karne par aaj ki date dikhayega
now = datetime.now()
auto_day = now.strftime("%A")  # Example: Friday
auto_date = now.strftime("%d %b %Y") # Example: 27 Mar 2026

# --- SIDEBAR: LOGO, NAME & SETTINGS ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🏦 Cash Denomination</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=100)
    st.sidebar.header("⚙️ Settings")
    user_name = st.sidebar.text_input("Change Name:", value="Sandeep")
    st.sidebar.divider()
    st.sidebar.info(f"Day: {auto_day}\nDate: {auto_date}")

# --- APP HEADER (Matching your portrait style) ---
st.markdown(f"<h3 style='text-align: center; margin-bottom: 0;'>Name : {user_name}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 18px; color: #666;'>{auto_day} | {auto_date}</p>", unsafe_allow_html=True)
st.divider()

# Reset functionality
if 'res' not in st.session_state:
    st.session_state.res = 0

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- CALCULATION TABLE ---
for n in notes:
    # 5 Tight columns for perfect portrait spacing
    c1, c2, c3, c4, c5 = st.columns([1, 0.4, 1.2, 0.4, 2.3])
    
    with c1:
        st.markdown(f"<p class='row-item'>₹{n}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p class='row-item'>x</p>", unsafe_allow_html=True)
    with c3:
        # number_input without buttons for best focus
        count = st.number_input(f"n_{n}", min_value=0, step=1, value=0, key=f"k_{n}_{st.session_state.res}", label_visibility="collapsed")
        counts[n] = count
    with c4:
        st.markdown("<p class='row-item'>=</p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p class='result-item'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Row (No Divider line here)
cc1, cc2, cc3, cc4, cc5 = st.columns([1, 0.4, 1.2, 0.4, 2.3])
with cc1:
    st.markdown("<p class='row-item'>Coins</p>", unsafe_allow_html=True)
with cc2:
    st.markdown("<p class='row-item'>+</p>", unsafe_allow_html=True)
with cc3:
    coin_val = st.number_input("cv", min_value=0, step=1, value=0, key=f"c_{st.session_state.res}", label_visibility="collapsed")
with cc4:
    st.markdown("<p class='row-item'>=</p>", unsafe_allow_html=True)
with cc5:
    st.markdown(f"<p class='result-item'>{coin_val}</p>", unsafe_allow_html=True)

# Calculation logic
grand_total = sum(totals) + coin_val
try:
    # Words to Words Language IN
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words = "Zero Only"

# --- SUMMARY SECTION ---
st.divider()
st.markdown(f"<h2 style='text-align: center;'>Total = ₹ {grand_total}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 18px;'>{words}</p>", unsafe_allow_html=True)

# --- FOOTER BUTTONS ---
st.divider()

# WhatsApp Share Message
whatsapp_msg = f"Cash Denomination\nName: {user_name}\nDay: {auto_day}\nDate: {auto_date}\n\n"
for n in notes:
    if counts[n] > 0:
        whatsapp_msg += f"₹{n:<4} x {counts[n]:<2} = {n*counts[n]:>7}\n"
if coin_val > 0:
    whatsapp_msg += f"Coins      = {coin_val:>7}\n"
whatsapp_msg += "------------------------------\n"
whatsapp_msg += f"Total      = ₹ {grand_total:>7}\n"
whatsapp_msg += f"{words}"

# Safe Share URL
wa_url = f"https://wa.me/?text={whatsapp_msg.replace(' ', '%20').replace('\n', '%0A')}"
st.markdown(f'''<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-weight:bold; font-size:18px;">📲 WhatsApp Share</button></a>''', unsafe_allow_html=True)

# Clear Button
if st.button("🔄 Clear / Reset Everything", use_container_width=True):
    st.session_state.res += 1
    st.rerun()
    
from num2words import num2words

# --- PAGE CONFIG (Setting Logo & Name for Browser Tab) ---
st.set_page_config(
    page_title="Cash Denomination - Sandeep", 
    page_icon="🏦", # Logo/Icon in Tab
    layout="centered"
)

# CSS for Strict Single Line & Professional Flat Look
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #ffffff; }
    
    /* Input box styling - Simple Underline (No Box/Borders) */
    div[data-baseweb="input"] {
        width: 65px !important;
        height: 32px !important;
        background-color: transparent !important;
        border: none !important;
        border-bottom: 2px solid #1b5e20 !important;
        border-radius: 0px !important;
        margin: 0px 5px !important;
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

    /* Column alignment for vertical portrait */
    [data-testid="column"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    .row-item { font-weight: bold; font-size: 18px; color: black; white-space: nowrap; margin: 0; }
    .result-item { font-weight: bold; font-size: 19px; color: #1b5e20; text-align: right; width: 100%; font-family: monospace; }
    
    p { margin-bottom: 0px !important; line-height: 1.2 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- AUTOMATIC DATE & DAY (Dynamics) ---
# Ye page open karne par aaj ki date dikhayega
now = datetime.now()
auto_day = now.strftime("%A")  # Example: Friday
auto_date = now.strftime("%d %b %Y") # Example: 27 Mar 2026

# --- SIDEBAR: LOGO, NAME & SETTINGS ---
with st.sidebar:
    st.markdown("<h2 style='text-align:center;'>🏦 Cash Denomination</h2>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=100)
    st.sidebar.header("⚙️ Settings")
    user_name = st.sidebar.text_input("Change Name:", value="Sandeep")
    st.sidebar.divider()
    st.sidebar.info(f"Day: {auto_day}\nDate: {auto_date}")

# --- APP HEADER (Matching your portrait style) ---
st.markdown(f"<h3 style='text-align: center; margin-bottom: 0;'>Name : {user_name}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 18px; color: #666;'>{auto_day} | {auto_date}</p>", unsafe_allow_html=True)
st.divider()

# Reset functionality
if 'res' not in st.session_state:
    st.session_state.res = 0

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- CALCULATION TABLE ---
for n in notes:
    # 5 Tight columns for perfect portrait spacing
    c1, c2, c3, c4, c5 = st.columns([1, 0.4, 1.2, 0.4, 2.3])
    
    with c1:
        st.markdown(f"<p class='row-item'>₹{n}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p class='row-item'>x</p>", unsafe_allow_html=True)
    with c3:
        # number_input without buttons for best focus
        count = st.number_input(f"n_{n}", min_value=0, step=1, value=0, key=f"k_{n}_{st.session_state.res}", label_visibility="collapsed")
        counts[n] = count
    with c4:
        st.markdown("<p class='row-item'>=</p>", unsafe_allow_html=True)
    with c5:
