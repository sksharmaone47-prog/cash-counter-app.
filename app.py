import streamlit as st
from datetime import datetime
import pytz
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered")

# CSS for Zero Gap, No Buttons & Green Theme
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; }
    
    [data-testid="column"] {
        padding: 0px !important;
        margin: 0px !important;
        width: fit-content !important;
        flex: unset !important;
    }

    button[data-testid="step-up"], button[data-testid="step-down"] {
        display: none !important;
    }

    div[data-baseweb="input"] {
        width: 65px !important;
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
    }
    
    .calc-text { font-family: monospace; font-size: 18px; font-weight: bold; color: #1b5e20; margin-top: 8px; margin-left: 10px; }
    .label-text { font-weight: bold; font-size: 18px; margin-top: 8px; min-width: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- SETTINGS SECTION (Sidebar) ---
IST = pytz.timezone('Asia/Kolkata')
default_date = datetime.now(IST)

with st.sidebar:
    st.markdown("## ⚙️ App Settings")
    user_name = st.text_input("Edit Name:", value="Sandeep")
    selected_date = st.date_input("Edit Date:", value=default_date)
    
    display_day = selected_date.strftime("%A")
    display_date = selected_date.strftime("%d %b %Y")
    st.divider()
    st.success(f"Settings Active:\n{display_day}\n{display_date}")

# --- MAIN HEADER ---
st.title("🏦 Cash Denomination")
st.markdown(f"<p style='text-align: center; font-size: 22px; font-weight: bold; color: #000; margin-bottom:0;'>Name : {user_name}</p>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-size: 18px; font-weight: bold; color: #1b5e20;'>{display_day} | {display_date}</p>", unsafe_allow_html=True)
st.divider()

if 'rid' not in st.session_state:
    st.session_state.rid = 0

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- CALCULATION ROWS ---
for n in notes:
    c1, c2, c3, c4, c5 = st.columns([0.6, 0.3, 1, 0.3, 2])
    with c1: st.markdown(f"<p class='label-text'>₹{n}</p>", unsafe_allow_html=True)
    with c2: st.markdown("<p class='label-text'>x</p>", unsafe_allow_html=True)
    with c3:
        count = st.number_input(f"q_{n}", min_value=0, step=1, value=0, key=f"n_{n}_{st.session_state.rid}", label_visibility="collapsed")
        counts[n] = count
    with c4: st.markdown("<p class='label-text'>=</p>", unsafe_allow_html=True)
    with c5:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p class='calc-text'>{subtotal}</p>", unsafe_allow_html=True)

# Coins Row
cc1, cc2, cc3, cc4, cc5 = st.columns([0.6, 0.3, 1, 0.3, 2])
with cc1: st.markdown("<p class='label-text'>Coins</p>", unsafe_allow_html=True)
with cc2: st.markdown("<p class='label-text'>+</p>", unsafe_allow_html=True)
with cc3:
    coin_val = st.number_input("c_v", min_value=0, step=1, value=0, key=f"c_{st.session_state.rid}", label_visibility="collapsed")
with cc4: st.markdown("<p class='label-text'>=</p>", unsafe_allow_html=True)
with cc5: st.markdown(f"<p class='calc-text'>{coin_val}</p>", unsafe_allow_html=True)

# Total Logic
grand_total = sum(totals) + coin_val
try:
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words = "Zero Only"

st.divider()
st.markdown(f"<h2 style='text-align: center; color: #1b5e20;'>Total = ₹ {grand_total}</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 18px;'>{words}</p>", unsafe_allow_html=True)

# --- REPORT GENERATION ---
report_text = f"--- CASH DENOMINATION REPORT ---\n"
report_text += f"Name: {user_name}\n"
report_text += f"Date: {display_date} ({display_day})\n"
report_text += f"--------------------------------\n"
for n in notes:
    if counts[n] > 0:
        report_text += f"₹{n:<4} x {counts[n]:<3} = {n*counts[n]:>10}\n"
if coin_val > 0:
    report_text += f"Coins      = {coin_val:>10}\n"
report_text += f"--------------------------------\n"
report_text += f"GRAND TOTAL: ₹ {grand_total}\n"
report_text += f"In Words: {words}\n"
report_text += f"--------------------------------"

# --- ACTION BUTTONS ---
st.divider()

# 1. WhatsApp Share
whatsapp_msg = f"*Cash Denomination Report*\nName: {user_name}\nDate: {display_date}\n\n"
for n in notes:
    if counts[n] > 0:
        whatsapp_msg += f"₹{n:<4} x {counts[n]:<2} = {n*counts[n]:>7}\n"
if coin_val > 0:
    whatsapp_msg += f"Coins      = {coin_val:>7}\n"
whatsapp_msg += "------------------------------\n"
whatsapp_msg += f"Total      = ₹ {grand_total:>7}\n"
whatsapp_msg += f"{words}"

wa_url = f"https://wa.me/?text={whatsapp_msg.replace(' ', '%20').replace('\n', '%0A')}"
st.markdown(f'''<a href="{wa_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-weight:bold; font-size:18px; margin-bottom:10px;">📲 Share on WhatsApp</button></a>''', unsafe_allow_html=True)

# 2. Download Link (Text File)
st.download_button(
    label="📥 Download Report (.txt)",
    data=report_text,
    file_name=f"Cash_Report_{display_date.replace(' ', '_')}.txt",
    mime="text/plain",
    use_container_width=True
)

# 3. Reset Button
st.write("") # Padding
if st.button("🔄 Clear All", use_container_width=True):
    st.session_state.rid += 1
    st.rerun()
    
