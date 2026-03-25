import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# Styling: Hiding extra elements and fixing alignment
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; }
    .bold-text { font-size: 22px !important; font-weight: bold !important; color: #000000; }
    .calc-row { 
        font-family: 'Courier New', Courier, monospace; 
        font-size: 20px; 
        font-weight: bold; 
        color: #1b5e20; 
        white-space: pre;
        display: flex;
        align-items: center;
    }
    /* Input box styling to look like part of the line */
    div[data-baseweb="input"] {
        width: 80px !important;
        background-color: white !important;
        border: 1px solid #ccc !important;
    }
    input { font-size: 18px !important; font-weight: bold !important; text-align: center !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Cash Denomination")

# Sidebar
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

# Header BOLD
st.markdown(f'<p class="bold-text">Entry Name : {user_name}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="bold-text">Date : {report_date.strftime("%a, %d %b %Y")}</p>', unsafe_allow_html=True)

st.divider()

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

st.subheader("Enter Quantities")

# --- CLEAN INPUT SECTION (Only 2000 x 5 = 10000) ---
for n in notes:
    col1, col2, col3, col4 = st.columns([1, 0.5, 1, 2])
    with col1:
        st.write(f"**₹{n}**")
    with col2:
        st.write("**x**")
    with col3:
        # Ab yahi main input hai, bada box hat gaya hai
        count = st.number_input(f"qty_{n}", min_value=0, step=1, value=0, key=f"q_{n}", label_visibility="collapsed")
        counts[n] = count
    with col4:
        subtotal = n * count
        totals.append(subtotal)
        # Seedhi line mein calculation
        st.markdown(f'<p class="calc-row"> =  {subtotal:>7}</p>', unsafe_allow_html=True)

# Coins Section
st.divider()
col_c1, col_c2, col_c3 = st.columns([1.5, 1, 2])
with col_c1:
    st.write("**Coins**")
with col_c2:
    coin_val = st.number_input("coin_v", min_value=0, step=1, value=0, key="coin_v", label_visibility="collapsed")
with col_c3:
    st.markdown(f'<p class="calc-row"> =  {coin_val:>7}</p>', unsafe_allow_html=True)

# Final Calculations
grand_total = sum(totals) + coin_val
total_items = sum(counts.values())

try:
    words_val = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words_val = "Zero Only"

# --- SUMMARY ---
st.divider()
st.markdown(f'<p class="calc-row">------------------------------</p>', unsafe_allow_html=True)
st.markdown(f'<p class="bold-text">Total      = ₹ {grand_total}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="calc-row">------------------------------</p>', unsafe_allow_html=True)
st.markdown(f"<p style='font-weight: bold;'>{words_val}</p>", unsafe_allow_html=True)
st.write(f"**Total {total_items} Notes / Coins**")

# --- WHATSAPP TEXT ---
st.divider()
whatsapp_text = f"Entry Name : {user_name}\nDate : {report_date.strftime('%a, %d %b %Y')}\n\n"
for n in notes:
    if counts[n] > 0:
        whatsapp_text += f"₹{n:<4} x {counts[n]:<2} = {n*counts[n]:>7}\n"
if coin_val > 0:
    whatsapp_text += f"Coins      = {coin_val:>7}\n"
whatsapp_text += "------------------------------\n"
whatsapp_text += f"Total      = ₹ {grand_total:>7}\n"
whatsapp_text += "------------------------------\n\n"
whatsapp_text += f"{words_val}\n"
whatsapp_text += f"Total {total_items} Notes / Coins"

whatsapp_url = f"https://wa.me/?text={whatsapp_text.replace(' ', '%20').replace('\n', '%0A')}"

st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-size:18px; font-weight:bold;">📲 Share on WhatsApp</button></a>''', unsafe_allow_html=True)

if st.button("🔄 Reset App"):
    st.rerun()
