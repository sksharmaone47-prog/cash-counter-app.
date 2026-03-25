import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# Styling for perfect single line alignment
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; }
    .bold-text { font-size: 20px !important; font-weight: bold !important; color: #000000; }
    
    /* Chrome/Safari se arrows hatane ke liye */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    
    .calc-row { 
        font-family: 'Courier New', Courier, monospace; 
        font-size: 20px; 
        font-weight: bold; 
        color: #1b5e20; 
        display: flex;
        align-items: center;
    }
    
    /* Input box ko chota aur clean banane ke liye */
    div[data-baseweb="input"] {
        width: 70px !important;
        min-height: 35px !important;
        background-color: white !important;
        border: 1px solid #999 !important;
        padding: 0px !important;
    }
    input { 
        padding: 5px !important; 
        text-align: center !important; 
        font-weight: bold !important;
        font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Cash Denomination")

# Sidebar
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

# Header
st.markdown(f'<p class="bold-text">Entry Name : {user_name}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="bold-text">Date : {report_date.strftime("%a, %d %b %Y")}</p>', unsafe_allow_html=True)

st.divider()
st.subheader("Enter Quantities")

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- SINGLE LINE INPUT SECTION ---
for n in notes:
    # columns for: ₹2000 | x | [Input] | = | Total
    c1, c2, c3, c4, c5 = st.columns([1, 0.4, 1, 0.4, 2])
    
    with c1:
        st.markdown(f"<p style='margin-top:10px; font-weight:bold;'>₹{n}</p>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p style='margin-top:10px; font-weight:bold;'>x</p>", unsafe_allow_html=True)
    with c3:
        # text_input use kiya hai taki + - buttons na dikhein
        val = st.text_input(f"q_{n}", value="0", key=f"key_{n}", label_visibility="collapsed")
        # Check if input is a number
        count = int(val) if val.isdigit() else 0
        counts[n] = count
    with c4:
        st.markdown("<p style='margin-top:10px; font-weight:bold;'>=</p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p class='calc-row' style='margin-top:10px;'>{subtotal:>7}</p>", unsafe_allow_html=True)

# Coins Section
st.divider()
cc1, cc2, cc3 = st.columns([1.4, 1, 2])
with cc1:
    st.markdown("<p style='margin-top:10px; font-weight:bold;'>Coins</p>", unsafe_allow_html=True)
with cc2:
    c_val_str = st.text_input("coin_v", value="0", key="c_key", label_visibility="collapsed")
    coin_val = int(c_val_str) if c_val_str.isdigit() else 0
with cc3:
    st.markdown(f"<p class='calc-row' style='margin-top:10px;'>= {coin_val:>7}</p>", unsafe_allow_html=True)

# Calculations
grand_total = sum(totals) + coin_val
total_items = sum(counts.values())

try:
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words = "Zero Only"

# --- SUMMARY ---
st.divider()
st.markdown(f"**Total = ₹ {grand_total}**")
st.write(f"*{words}*")
st.write(f"Total {total_items} Notes / Coins")

# --- WHATSAPP ---
whatsapp_text = f"Entry Name : {user_name}\nDate : {report_date.strftime('%d %b %y')}\n\n"
for n in notes:
    if counts[n] > 0:
        whatsapp_text += f"₹{n:<4} x {counts[n]:<2} = {n*counts[n]:>7}\n"
if coin_val > 0:
    whatsapp_text += f"Coins      = {coin_val:>7}\n"
whatsapp_text += "------------------------------\n"
whatsapp_text += f"Total      = ₹ {grand_total:>7}\n"
whatsapp_text += f"{words}\n"

whatsapp_url = f"https://wa.me/?text={whatsapp_text.replace(' ', '%20').replace('\n', '%0A')}"

st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; cursor:pointer; font-weight:bold;">📲 Share on WhatsApp</button></a>''', unsafe_allow_html=True)

if st.button("🔄 Reset"):
    st.rerun()
    
