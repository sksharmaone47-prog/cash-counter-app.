import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# CSS for Strict Single Line Table & Green Theme
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; }
    
    /* Table Styling for Absolute Alignment */
    table { width: 100%; border-collapse: collapse; table-layout: fixed; }
    td { padding: 5px 2px; vertical-align: middle; }
    .label-cell { font-weight: bold; font-size: 16px; width: 25%; }
    .input-cell { width: 30%; }
    .sign-cell { font-weight: bold; font-size: 16px; width: 10%; text-align: center; }
    .total-cell { font-weight: bold; font-size: 18px; text-align: right; width: 35%; font-family: monospace; color: #1b5e20; }
    
    /* Input Styling - Removing all default Streamlit decoration */
    div[data-baseweb="input"] {
        width: 75px !important;
        height: 38px !important;
        background-color: white !important;
        border: 1px solid #999 !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
    }

    /* Hide +/- Buttons */
    button[data-testid="step-up"], button[data-testid="step-down"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏦 Cash Denomination")

# Sidebar
st.sidebar.header("📋 Settings")
user_name = st.sidebar.text_input("Entry Name:", value="Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

st.markdown(f"**Entry Name :** {user_name} | **Date :** {report_date.strftime('%d %b %y')}")
st.divider()

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# --- FAST INPUT TABLE ---
for n in notes:
    # Using 3 tight columns for a clean row
    col_l, col_i, col_t = st.columns([1, 1, 2])
    
    with col_l:
        st.markdown(f"<p style='margin-top:10px; font-weight:bold; font-size:18px;'>₹{n} &nbsp; x</p>", unsafe_allow_html=True)
    with col_i:
        # number_input used for 'Enter/Next' support, CSS hides buttons
        count = st.number_input(f"qty_{n}", min_value=0, step=1, value=0, key=f"k_{n}", label_visibility="collapsed")
        counts[n] = count
    with col_t:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<p style='margin-top:10px; font-weight:bold; font-size:19px; text-align:right; font-family:monospace; color:#1b5e20;'>= &nbsp; {subtotal}</p>", unsafe_allow_html=True)

# Coins Row (No divider line here)
c_l, c_i, c_t = st.columns([1, 1, 2])
with c_l:
    st.markdown("<p style='margin-top:10px; font-weight:bold; font-size:18px;'>Coins</p>", unsafe_allow_html=True)
with c_i:
    coin_val = st.number_input("coin_v", min_value=0, step=1, value=0, key="c_k", label_visibility="collapsed")
with c_t:
    st.markdown(f"<p style='margin-top:10px; font-weight:bold; font-size:19px; text-align:right; font-family:monospace; color:#1b5e20;'>= &nbsp; {coin_val}</p>", unsafe_allow_html=True)

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
st.write(f"Total {total_items} Notes / Coins")

# --- WHATSAPP SHARE ---
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

st.markdown(f'''<a href="{whatsapp_url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:12px; cursor:pointer; font-weight:bold; font-size:18px;">📲 Share on WhatsApp</button></a>''', unsafe_allow_html=True)

if st.button("🔄 Reset App"):
    st.rerun()
