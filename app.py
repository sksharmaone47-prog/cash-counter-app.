import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG (Hiding Menu) ---
st.set_page_config(page_title="Cash Counter Pro", page_icon="🏦", layout="centered", menu_items=None)

# Professional White Table Styling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #ffffff; }
    
    /* Summary Header Styling */
    .summary-text { font-size: 18px; font-weight: bold; color: #000000; margin-bottom: 5px; }
    .summary-val { float: right; }
    
    /* Table Header Styling */
    .table-header { 
        background-color: #000000; 
        color: #ffffff; 
        padding: 10px; 
        font-weight: bold; 
        display: flex; 
        justify-content: space-between;
        border-radius: 5px 5px 0 0;
    }
    
    /* Monospace for Alignment */
    .calc-row { 
        font-family: 'Courier New', Courier, monospace; 
        font-size: 18px; 
        font-weight: bold; 
        color: #000000;
        white-space: pre;
    }
    input { border-bottom: 1px solid #000 !important; border-top: none !important; border-left: none !important; border-right: none !important; border-radius: 0px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- APP LOGIC ---
st.sidebar.header("Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

# Notes List (As per your new image)
notes = [2000, 500, 200, 100, 50, 20, 10, 5, 2, 1]
counts = {}
totals = []

# Calculation for Top Summary
# We need to run a quick loop first to get totals for the header
for n in notes:
    counts[n] = 0 # Default

# UI - Top Summary Section
st.markdown(f'<div class="summary-text">Date : <span class="summary-val">{report_date.strftime("%a, %d %b %y, %I:%M %p")}</span></div>', unsafe_allow_html=True)
total_notes_placeholder = st.empty()
grand_total_placeholder = st.empty()
words_placeholder = st.empty()

st.divider()

# Table Header
st.markdown("""
<div class="table-header">
    <span>Currency</span>
    <span>Count</span>
    <span style="margin-right: 15px;">Amount</span>
</div>
""", unsafe_allow_html=True)

# --- TABLE ROWS ---
for n in notes:
    col1, col2, col3 = st.columns([1.5, 2, 2.5])
    with col1:
        st.write(f"**₹ {n}**")
    with col2:
        count = st.number_input(f"x {n}", min_value=0, step=1, value=0, key=f"q_{n}", label_visibility="collapsed")
        counts[n] = count
    with col3:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f'<p class="calc-row">  ₹ {subtotal:>5} /-</p>', unsafe_allow_html=True)

# Coin Row
col1, col2, col3 = st.columns([1.5, 2, 2.5])
with col1:
    st.write("**Coin**")
with col2:
    coin_qty = st.number_input("Coin Qty", min_value=0, step=1, value=0, key="coin_q", label_visibility="collapsed")
with col3:
    st.markdown(f'<p class="calc-row">  ₹ {coin_qty:>5} /-</p>', unsafe_allow_html=True)

# Final Totals
grand_total = sum(totals) + coin_qty
total_items = sum(counts.values()) + (1 if coin_qty > 0 else 0)

try:
    words = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words = "Zero Only"

# Updating Top Summary with Real Data
total_notes_placeholder.markdown(f'<div class="summary-text">Total Notes / Coins : <span class="summary-val">{sum(counts.values())}</span></div>', unsafe_allow_html=True)
grand_total_placeholder.markdown(f'<div class="summary-text">Total Amount : <span class="summary-val">₹ {grand_total}</span></div>', unsafe_allow_html=True)
words_placeholder.markdown(f"<h4 style='text-align: center; color: black; margin-top: 10px;'>{words}</h4>", unsafe_allow_html=True)

# --- WHATSAPP BUTTON ---
st.divider()
whatsapp_text = f"Date : {report_date.strftime('%d %b %y')}\nTotal Amount : ₹ {grand_total}\n{words}\n\n"
whatsapp_text += "Currency | Count | Amount\n"
whatsapp_text += "---------------------------\n"
for n in notes:
    if counts[n] > 0:
        whatsapp_text += f"₹{n:<4} | {counts[n]:<3} | ₹{n*counts[n]:>6}\n"
if coin_qty > 0:
    whatsapp_text += f"Coin     | --  | ₹{coin_qty:>6}\n"

whatsapp_url = f"https://wa.me/?text={whatsapp_text.replace(' ', '%20').replace('\n', '%0A')}"

st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; cursor:pointer; font-weight:bold;">📲 Share on WhatsApp</button></a>''', unsafe_allow_html=True)

if st.button("🔄 Reset App"):
    st.rerun()
