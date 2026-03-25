import streamlit as st
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Cash Denomination", 
    page_icon="🏦", 
    layout="centered"
)

# CSS for ZERO GAP, No Buttons, and No Date Display
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; }
    
    /* Remove all column gaps completely */
    [data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
        width: fit-content !important;
        flex: unset !important;
    }

    /* Hide +/- Buttons Always */
    button[data-testid="step-up"], button[data-testid="step-down"] {
        display: none !important;
    }

    /* Input Box Styling - VERY TIGHT */
    div[data-baseweb="input"] {
        width: 60px !important;
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
    
    .calc-text { 
        font-family: monospace; 
        font-size: 18px; 
        font-weight: bold; 
        color: #1b5e20;
        margin-top: 8px;
        margin-left: 10px;
    }
    
    .label-text { font-weight: bold; font-size: 18px; margin-top: 8px; min-width: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- SETTINGS IN SIDEBAR ---
with st.sidebar:
    st.markdown("## ⚙️ App Settings")
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=80)
    user_name = st.text_input("Entry Name:", value="Sandeep")
    st.divider()
    st.info("Date & Day are now hidden from the main screen.")

# --- MAIN HEADER ---
st.title("🏦 Cash Denomination")
st.markdown(f"<h3 style='text-align: center; color: #000;'>Name : {user_name}</h3>", unsafe_allow_html=True)
st.divider()

# Reset state
if 'reset_id' not in st.session_state:
    st.session_state.reset_id = 0

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- ZERO GAP CALCULATION SECTION ---
for n in notes:
    # 5 Very tight columns to bring elements close
    c1, c2, c3, c4, c5 = st.columns([0.6, 0.3, 1, 0.3, 2])
    
    with c1:
        st.markdown(f"<p class='label-text'>₹{n}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p class='label-text'>x</p>", unsafe_allow_html=True)
    with c3:
        # number_input without buttons for best focus and Next key
        count = st.number_input(f"q_{n}", min_value=0, step=1, value=0, key=f"n_{n}_{st.session_state.reset_id}", label_visibility="collapsed")
        counts[n] = count
    with c4:
        st.markdown("<p class='label-text'>=</p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p class='calc-text'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Row
cc1, cc2, cc3, cc4, cc5 = st.columns([0.6, 0.3, 1, 0.3, 2])
with cc1:
    st.markdown("<p class='label-text'>Coins</p>", unsafe_allow_html=True)
with cc2:
    st.markdown("<p class='label-text'>+</p>", unsafe_allow_html=True)
with cc3:
    coin_val = st.number_input("c_v", min_value=0, step=1, value=0, key=f"c_{st.session_state.reset_id}", label_visibility="collapsed")
with cc4:
    st.markdown("<p class='label-text'>=</p>", unsafe_allow_html=True)
with cc5:
    st.markdown(f"<p class='calc-text'>{coin_val}</p>", unsafe_allow_html=True)

# Calculations
grand_total = sum
