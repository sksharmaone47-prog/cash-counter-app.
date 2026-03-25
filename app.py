import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# Styling for ZERO GAP and CLEAN INPUT (No Buttons)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; }
    
    /* Strict Column Alignment - No Gaps */
    [data-testid="column"] {
        padding-left: 0px !important;
        padding-right: 0px !important;
        margin-left: 0px !important;
        margin-right: 0px !important;
        flex: unset !important;
        min-width: unset !important;
    }

    /* Input Box Styling (Using text_input to avoid +/- buttons) */
    div[data-baseweb="input"] {
        width: 60px !important;
        height: 35px !important;
        background-color: white !important;
        border: 1px solid #999 !important;
        border-radius: 4px !important;
        margin-left: 2px !important;
        margin-right: 2px !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
        padding: 0px !important;
    }
    
    .calc-row { 
        font-family: monospace; 
        font-size: 19px; 
        font-weight: bold; 
        color: #1b5e20;
        margin-top: 7px;
        margin-left: 5px;
    }
    
    p { margin-bottom: 0px !important; line-height: 1.2 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Cash Denomination")

# Sidebar
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

st.divider()

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- ZERO GAP LAYOUT ---
for n in notes:
    # Tightest possible column layout
    c1, c2, c3, c4, c5 = st.columns([0.45, 0.2, 0.7, 0.2, 1.8])
    
    with c1:
        st.markdown(f"<p style='margin-top:7px;'><b>₹{n}</b></p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p style='margin-top:7px;'><b>x</b></p>", unsafe_allow_html=True)
    with c3:
        # text_input use karne se +/- buttons kabhi nahi aayenge
        val = st.text_input(f"qty_{n}", value="0", key=f"k_{n}", label_visibility="collapsed")
        # Ensure only numbers are used
        count = int(val) if val.isdigit() else 0
        counts[n] = count
    with c4:
        st.markdown("<p style='margin-top:7px;'><b>=</b></p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p class='calc-row'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Row
st.divider()
cc1, cc2, cc3, cc4, cc5 = st.columns([0.45, 0.2, 0.7, 0.2, 1.8])
with cc1:
    st.markdown("<p style='margin-top:7px;'><b>Coins</b></p>", unsafe_allow_html=True)
with cc2:
    pass
with cc3:
    c_val_str = st.text_input("c_v", value="0", key="c_key", label_visibility="collapsed")
    coin_val = int(c_val_str) if c_val_str.isdigit() else 0
with cc4:
    st.markdown("<p style='margin-top:7px;'><b>=</b></p>", unsafe_allow_html=True)
with cc5:
    st.markdown(f"<p class='calc-row'>{coin_val}</p>", unsafe_allow_html=True)

# Calculations
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

st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-weight:bold;">📲 Share on WhatsApp</button></a>''', unsafe_allow_html=True)

if st.button("🔄 Reset App"):
    st.rerun()
