import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# CSS for Strict Single Line & Hide Buttons
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; }
    
    /* Hide +/- Buttons */
    button[data-testid="step-up"], button[data-testid="step-down"] {
        display: none !important;
    }
    
    /* Force Columns to stay tight and not wrap */
    [data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
        width: fit-content !important;
        flex: unset !important;
    }

    /* Input Box size */
    div[data-baseweb="input"] {
        width: 75px !important;
        height: 38px !important;
        background-color: white !important;
        border: 1px solid #999 !important;
        margin: 0 5px !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
    }

    .row-text {
        font-weight: bold;
        font-size: 18px;
        margin-top: 8px;
        white-space: nowrap;
    }
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

# --- FIXED SINGLE LINE LAYOUT ---
for n in notes:
    # Manual row with very tight columns
    c1, c2, c3, c4, c5 = st.columns([0.5, 0.2, 0.8, 0.2, 1.5])
    
    with c1:
        st.markdown(f"<p class='row-text'>₹{n}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p class='row-text'>x</p>", unsafe_allow_html=True)
    with c3:
        # number_input used for 'Enter/Next' key support
        count = st.number_input(f"n_{n}", min_value=0, step=1, value=0, key=f"key_{n}", label_visibility="collapsed")
        counts[n] = count
    with c4:
        st.markdown("<p class='row-text'>=</p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p class='row-text' style='color:#1b5e20; padding-left:10px;'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Row (No Divider)
cc1, cc2, cc3, cc4, cc5 = st.columns([0.5, 0.2, 0.8, 0.2, 1.5])
with cc1:
    st.markdown("<p class='row-text'>Coins</p>", unsafe_allow_html=True)
with cc2:
    pass
with cc3:
    coin_val = st.number_input("c_input", min_value=0, step=1, value=0, key="coin_k", label_visibility="collapsed")
with cc4:
    st.markdown("<p class='row-text'>=</p>", unsafe_allow_html=True)
with cc5:
    st.markdown(f"<p class='row-text' style='color:#1b5e20; padding-left:10px;'>{coin_val}</p>", unsafe_allow_html=True)

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
