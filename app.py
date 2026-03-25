import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# Styling for ZERO GAP and NO BUTTONS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; }
    
    /* Remove column padding and gaps completely */
    [data-testid="column"] {
        padding-left: 0px !important;
        padding-right: 0px !important;
        margin-left: 0px !important;
        margin-right: 0px !important;
        flex: unset !important;
        min-width: unset !important;
    }

    /* Remove + and - buttons from number input */
    button[data-testid="step-up"], button[data-testid="step-down"] {
        display: none !important;
    }

    /* Input Box Styling - VERY TIGHT */
    div[data-baseweb="input"] {
        width: 55px !important;
        height: 35px !important;
        background-color: white !important;
        border: 1px solid #999 !important;
        border-radius: 4px !important;
        margin-left: 5px !important;
        margin-right: 5px !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
        padding: 0px !important;
    }
    
    .calc-row { 
        font-family: monospace; 
        font-size: 18px; 
        font-weight: bold; 
        color: #1b5e20;
        margin-top: 8px;
        margin-left: 10px;
    }
    
    p { margin-bottom: 0px !important; }
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

# --- ZERO GAP INPUT SECTION ---
for n in notes:
    # Smallest possible column widths
    c1, c2, c3, c4, c5 = st.columns([0.4, 0.2, 0.6, 0.2, 1.5])
    
    with c1:
        st.markdown(f"<p style='margin-top:8px;'><b>₹{n}</b></p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p style='margin-top:8px;'><b>x</b></p>", unsafe_allow_html=True)
    with c3:
        # number_input with step-buttons hidden by CSS
        count = st.number_input(f"qty_{n}", min_value=0, step=1, value=0, key=f"n_{n}", label_visibility="collapsed")
        counts[n] = count
    with c4:
        st.markdown("<p style='margin-top:8px;'><b>=</b></p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p class='calc-row'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Section (No divider)
cc1, cc2, cc3, cc4, cc5 = st.columns([0.4, 0.2, 0.6, 0.2, 1.5])
with cc1:
    st.markdown("<p style='margin-top:8px;'><b>Coins</b></p>", unsafe_allow_html=True)
with cc2:
    pass # Empty for spacing
with cc3:
    coin_val = st.number_input("coin_v", min_value=0, step=1, value=0, key="coin_input", label_visibility="collapsed")
with cc4:
    st.markdown("<p style='margin-top:8px;'><b>=</b></p>", unsafe_allow_html=True)
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

st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-weight:bold;">📲 WhatsApp Share</button></a>''', unsafe_allow_html=True)

if st.button("🔄 Clear All"):
    st.rerun()
