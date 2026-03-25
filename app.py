import streamlit as st
from datetime import date
from num2words import num2words

# --- PAGE CONFIG ---
st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="centered", menu_items=None)

# CSS for Strict Single Line & Professional Green Theme
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { background-color: #e8f5e9; }
    
    /* Hide +/- Buttons Always */
    button[data-testid="step-up"], button[data-testid="step-down"] {
        display: none !important;
    }
    
    /* Custom Styling for the input box inside our custom row */
    div[data-baseweb="input"] {
        width: 80px !important;
        height: 40px !important;
        background-color: white !important;
        border: 1px solid #999 !important;
        margin: 0px 5px !important;
    }
    input { 
        text-align: center !important; 
        font-weight: bold !important; 
        font-size: 18px !important;
    }

    /* Professional Alignment for the whole row */
    .row-flex {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: flex-start;
        margin-bottom: 12px;
        width: 100%;
    }
    .text-bold { font-weight: bold; font-size: 18px; color: black; min-width: 55px; }
    .sign-bold { font-weight: bold; font-size: 18px; color: black; margin: 0 5px; }
    .total-bold { font-weight: bold; font-size: 19px; color: #1b5e20; font-family: monospace; text-align: right; flex-grow: 1; margin-right: 10px; }
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

# --- NEW STABLE LAYOUT ---
for n in notes:
    # We use a container but put everything in a Flex Row via CSS
    with st.container():
        # Using 3 columns but with FIXED widths via flex-basis
        c1, c2, c3 = st.columns([1, 1, 2])
        
        with c1:
            st.markdown(f"<p class='text-bold' style='margin-top:8px;'>₹{n} &nbsp; x</p>", unsafe_allow_html=True)
        with c2:
            # count input
            count = st.number_input(f"n_{n}", min_value=0, step=1, value=0, key=f"key_{n}", label_visibility="collapsed")
            counts[n] = count
        with c3:
            subtotal = n * count
            totals.append(subtotal)
            st.markdown(f"<p class='total-bold' style='margin-top:8px;'>= &nbsp; {subtotal}</p>", unsafe_allow_html=True)

# Coins Section (Line removed between 10 and Coins)
with st.container():
    cc1, cc2, cc3 = st.columns([1, 1, 2])
    with cc1:
        st.markdown("<p class='text-bold' style='margin-top:8px;'>Coins</p>", unsafe_allow_html=True)
    with cc2:
        coin_val = st.number_input("c_input", min_value=0, step=1, value=0, key="coin_k", label_visibility="collapsed")
    with cc3:
        st.markdown(f"<p class='total-bold' style='margin-top:8px;'>= &nbsp; {coin_val}</p>", unsafe_allow_html=True)

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
