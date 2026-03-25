import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Counter Pro", page_icon="🏦")

# Styling for perfect vertical alignment
st.markdown("""
    <style>
    .stApp { background-color: #e8f5e9; }
    .bold-text { font-size: 22px !important; font-weight: bold !important; color: #000000; }
    /* Monospace for perfect column alignment */
    .calc-row { 
        font-family: 'Courier New', Courier, monospace; 
        font-size: 20px; 
        font-weight: bold; 
        color: #1b5e20; 
        white-space: pre;
    }
    input { font-size: 18px !important; font-weight: bold !important; }
    .gap-line { margin-top: 20px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Cash Counter Pro")

# Sidebar
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

# Header
st.markdown(f'<p class="bold-text">Entry Name : {user_name}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="bold-text">Date : {report_date.strftime("%a, %d %b %Y")}</p>', unsafe_allow_html=True)

st.divider()

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

st.subheader("Enter Quantities")

# --- ALIGNED INPUT SECTION ---
for n in notes:
    col1, col2, col3 = st.columns([1.5, 2, 3])
    with col1:
        st.write(f"**₹{n}**")
    with col2:
        count = st.number_input(f"x {n}", min_value=0, step=1, value=0, key=f"q_{n}", label_visibility="collapsed")
        counts[n] = count
    with col3:
        subtotal = n * count
        totals.append(subtotal)
        # Right aligned numbers with '=' in a fixed position
        st.markdown(f'<p class="calc-row"> x {count:<2} = {subtotal:>7}</p>', unsafe_allow_html=True)

# Coins
st.divider()
c_col1, c_col2 = st.columns([3.5, 3])
with c_col1:
    coin_val = st.number_input("Coins Value (₹)", min_value=0, step=1, value=0)
with c_col2:
    st.markdown(f'<p class="calc-row">Coins   = {coin_val:>7}</p>', unsafe_allow_html=True)

# Calculations
grand_total = sum(totals) + coin_val
total_items = sum(counts.values())

try:
    # 'And' hatakar normal spacing
    words_hi = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words_hi = "Zero Only"

# --- SUMMARY SECTION (With Gap and Lines) ---
st.divider()
st.markdown(f'<p class="calc-row">------------------------------</p>', unsafe_allow_html=True)
st.markdown(f'<p class="bold-text">Total      = ₹ {grand_total}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="calc-row">------------------------------</p>', unsafe_allow_html=True)

# Adding gap between Total line and Hindi words
st.markdown('<div class="gap-line"></div>', unsafe_allow_html=True)

st.write(f"**{words_hi}**")
st.write(f"**Total {total_items} Notes / Coins**")

# --- WHATSAPP TEXT (Perfect Straight Alignment) ---
st.divider()

# WhatsApp logic for straight vertical lines
whatsapp_text = f"Entry Name : {user_name}\n"
whatsapp_text += f"Date : {report_date.strftime('%a, %d %b %Y')}\n\n"

for n in notes:
    if counts[n] > 0:
        # alignment logic (Right align subtotal)
        whatsapp_text += f"₹{n:<4} x {counts[n]:<2} = {n*counts[n]:>7}\n"

if coin_val > 0:
    whatsapp_text += f"Coins      = {coin_val:>7}\n"

whatsapp_text += "------------------------------\n"
whatsapp_text += f"Total      = ₹ {grand_total:>7}\n"
whatsapp_text += "------------------------------\n\n" # Double enter for gap
whatsapp_text += f"{words_hi}\n"
whatsapp_text += f"Total {total_items} Notes / Coins"

whatsapp_url = f"https://wa.me/?text={whatsapp_text.replace(' ', '%20').replace('\n', '%0A')}"

st.markdown(f'''
    <a href="{whatsapp_url}" target="_blank">
        <button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-size:18px; font-weight:bold;">
            📲 Share on WhatsApp
        </button>
    </a>
''', unsafe_allow_html=True)

if st.button("🔄 Reset App"):
    st.rerun()
