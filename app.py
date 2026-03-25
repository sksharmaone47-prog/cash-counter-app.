import streamlit as st
from datetime import date
from num2words import num2words

# --- APP CONFIGURATION & ICON ---
st.set_page_config(page_title="Cash Counter Pro", page_icon="🏦", layout="centered")

# Custom Styling for Professional Look
st.markdown("""
    <style>
    .stApp { background-color: #e8f5e9; }
    .bold-text { font-size: 22px !important; font-weight: bold !important; color: #000000; }
    /* Monospace for Straight Vertical Alignment */
    .calc-row { 
        font-family: 'Courier New', Courier, monospace; 
        font-size: 20px; 
        font-weight: bold; 
        color: #1b5e20; 
        white-space: pre;
    }
    input { font-size: 18px !important; font-weight: bold !important; }
    .spacer { margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Cash Counter Pro")

# Sidebar Settings
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

# Header Section
st.markdown(f'<p class="bold-text">Entry Name : {user_name}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="bold-text">Date : {report_date.strftime("%a, %d %b %Y")}</p>', unsafe_allow_html=True)

st.divider()

# Notes List (2000 included)
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
        # Right aligned numbers with '=' in fixed position
        st.markdown(f'<p class="calc-row"> x {count:<3} = {subtotal:>8}</p>', unsafe_allow_html=True)

# Coins Section
st.divider()
c_col1, c_col2 = st.columns([3.5, 3])
with c_col1:
    coin_val = st.number_input("Coins Value (₹)", min_value=0, step=1, value=0)
with c_col2:
    st.markdown(f'<p class="calc-row">Coins    = {coin_val:>8}</p>', unsafe_allow_html=True)

# Calculations
grand_total = sum(totals) + coin_val
total_items = sum(counts.values())

try:
    # Removed 'And' and kept normal spacing
    words_val = num2words(grand_total, lang='en_IN').title().replace("-", " ").replace(" And ", " ") + " Only"
except:
    words_val = "Zero Only"

# --- SUMMARY SECTION (Double Line & Gaps) ---
st.divider()
st.markdown(f'<p class="calc-row">--------------------------------</p>', unsafe_allow_html=True)
st.markdown(f'<p class="bold-text">Total      = ₹ {grand_total}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="calc-row">--------------------------------</p>', unsafe_allow_html=True)

# Gap between Total and Hindi Words
st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

st.write(f"**{words_val}**")
st.write(f"**Total {total_items} Notes / Coins**")

# --- WHATSAPP SHARE (Perfect Vertical Alignment) ---
st.divider()

whatsapp_text = f"Entry Name : {user_name}\n"
whatsapp_text += f"Date : {report_date.strftime('%a, %d %b %Y')}\n\n"

for n in notes:
    if counts[n] > 0:
        whatsapp_text += f"₹{n:<4} x {counts[n]:<3} = {n*counts[n]:>8}\n"

if coin_val > 0:
    whatsapp_text += f"Coins       = {coin_val:>8}\n"

whatsapp_text += "--------------------------------\n"
whatsapp_text += f"Total       = ₹ {grand_total:>8}\n"
whatsapp_text += "--------------------------------\n\n"
whatsapp_text += f"{words_val}\n"
whatsapp_text += f"Total {total_items} Notes / Coins"

whatsapp_url = f"https://wa.me/?text={whatsapp_text.replace(' ', '%20').replace('\n', '%0A')}"

st.markdown(f'''
    <a href="{whatsapp_url}" target="_blank">
        <button style="width:100%; background-color:#25D366; color:white; border:none; padding:18px; border-radius:15px; cursor:pointer; font-size:20px; font-weight:bold; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
            📲 Share on WhatsApp
        </button>
    </a>
''', unsafe_allow_html=True)

if st.button("🔄 Clear All / Reset"):
    st.rerun()
