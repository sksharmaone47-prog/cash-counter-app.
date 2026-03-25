import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# Styling for rigid one-line layout even on slim mobile screens
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; }
    
    /* Force row to stay in one line and not wrap */
    .custom-row {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        gap: 8px;
        margin-bottom: 10px;
        width: 100%;
    }
    
    .label-txt { min-width: 50px; font-weight: bold; font-size: 16px; }
    .sign-txt { min-width: 15px; font-weight: bold; font-size: 16px; }
    .total-txt { min-width: 80px; font-weight: bold; font-size: 16px; text-align: right; color: #1b5e20; font-family: monospace; }

    /* Small Input Box styling */
    div[data-baseweb="input"] {
        width: 65px !important;
        height: 35px !important;
        background-color: white !important;
        border: 1px solid #999 !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 16px !important;
        padding: 5px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Cash Denomination")

# Sidebar Settings
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

st.markdown(f"**Entry Name :** {user_name}")
st.markdown(f"**Date :** {report_date.strftime('%a, %d %b %Y')}")
st.divider()

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- RIGID LAYOUT FOR NOTES ---
for n in notes:
    # Using a single container for each row to prevent wrapping
    row_container = st.container()
    with row_container:
        col1, col2, col3, col4, col5 = st.columns([1, 0.4, 1.2, 0.4, 2])
        with col1:
            st.markdown(f"<p style='margin-top:8px;'><b>₹{n}</b></p>", unsafe_allow_html=True)
        with col2:
            st.markdown("<p style='margin-top:8px;'><b>x</b></p>", unsafe_allow_html=True)
        with col3:
            val = st.text_input(f"q_{n}", value="", placeholder="0", key=f"k_{n}", label_visibility="collapsed")
            count = int(val) if val.isdigit() else 0
            counts[n] = count
        with col4:
            st.markdown("<p style='margin-top:8px;'><b>=</b></p>", unsafe_allow_html=True)
        with col5:
            subtotal = n * count
            totals.append(subtotal)
            st.markdown(f"<p style='margin-top:8px; font-family:monospace; text-align:right;'><b>{subtotal}</b></p>", unsafe_allow_html=True)

# --- COINS SECTION (No Divider between 10 and Coins) ---
row_coin = st.container()
with row_coin:
    c1, c2, c3, c4, c5 = st.columns([1, 0.4, 1.2, 0.4, 2])
    with c1:
        st.markdown("<p style='margin-top:8px;'><b>Coins</b></p>", unsafe_allow_html=True)
    with col2: # spacing
        pass
    with c3:
        c_str = st.text_input("c_v", value="", placeholder="0", key="c_k", label_visibility="collapsed")
        coin_val = int(c_str) if c_str.isdigit() else 0
    with c4:
        st.markdown("<p style='margin-top:8px;'><b>=</b></p>", unsafe_allow_html=True)
    with c5:
        st.markdown(f"<p style='margin-top:8px; font-family:monospace; text-align:right;'><b>{coin_val}</b></p>", unsafe_allow_html=True)

# Final Calculations
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

if st.button("🔄 Reset"):
    st.rerun()
