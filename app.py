import streamlit as st
import urllib.parse
from datetime import date

# Page Layout
st.set_page_config(page_title="Cash Memo", page_icon="🏦", layout="centered")

# Custom CSS for Clean Look
st.markdown("""
<style>
    /* Hide Plus/Minus Buttons from Number Input */
    button.step-up, button.step-down {
        display: none !important;
    }
    input[type=number] {
        -moz-appearance: textfield;
    }
    
    .bill-box {
        border: 2px solid #333;
        padding: 20px;
        background-color: white;
        border-radius: 10px;
        color: black;
    }
    
    .bill-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
    }

    .center-title {
        text-align: center;
        font-weight: bold;
        font-size: 22px;
        text-decoration: underline;
        margin-bottom: 20px;
    }

    .grand-total-section {
        border-top: 2px solid #333;
        margin-top: 20px;
        padding-top: 10px;
        text-align: right;
        color: #d32f2f;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="bill-box">', unsafe_allow_html=True)

# --- HEADER (Name Left, Date Right) ---
c_left, c_right = st.columns([2, 1])
with c_left:
    user_name = st.text_input("Name:", value="Sandeep")
with c_right:
    user_date = st.text_input("Date:", value=date.today().strftime("%d-%m-%Y"))

st.markdown(f'''
    <div class="bill-header">
        <div style="font-weight:bold;">👤 {user_name}</div>
        <div style="font-weight:bold;">📅 {user_date}</div>
    </div>
''', unsafe_allow_html=True)

# --- CENTER TITLE ---
st.markdown('<div class="center-title">CASH DENOMINATION</div>', unsafe_allow_html=True)

# --- CALCULATION SECTION ---
notes = [2000, 500, 200, 100, 50, 20, 10]
data = {}
grand_total = 0

for note in notes:
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.write(f"💵 ₹{note}") # Sirf Symbol aur Value
    
    with col2:
        # label_visibility="collapsed" se extra text gayab ho jayega
        qty = st.number_input(f"qty_{note}", min_value=0, step=1, key=f"n_{note}", label_visibility="collapsed")
    
    amt = note * (qty if qty else 0)
    if qty > 0:
        data[note] = {"qty": qty, "amt": amt}
        grand_total += amt
    
    with col3:
        st.write(f"**= ₹{amt:,}**")

st.markdown("---")

# Coins Section
col_c1, col_c2, col_c3 = st.columns([1, 1, 1])
with col_c1:
    st.write("🪙 Coins")
with col_c2:
    coins_total = st.number_input("coins", min_value=0, step=1, key="coins_in", label_visibility="collapsed")
with col_c3:
    st.write(f"**= ₹{coins_total:,}**")

grand_total += (coins_total if coins_total else 0)

# --- HINDI TOTAL ---
st.markdown('<div class="grand-total-section">', unsafe_allow_html=True)
st.markdown(f"### कुल योग (Grand Total): ₹{grand_total:,}")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- WHATSAPP SHARE ---
report_text = f"📜 *CASH MEMO*\n"
report_text += f"📅 *Date:* {user_date}\n"
report_text += f"👤 *Name:* {user_name}\n"
report_text += f"━━━━━━━━━━━━━━\n"

for n, details in data.items():
    report_text += f"💵 ₹{n} x {details['qty']} = ₹{details['amt']:,}\n"

if coins_total > 0:
    report_text += f"🪙 Coins = ₹{coins_total:,}\n"

report_text += f"━━━━━━━━━━━━━━\n"
report_text += f"*कुल योग: ₹{grand_total:,}*"

encoded_text = urllib.parse.quote(report_text)
whatsapp_url = f"https://wa.me/?text={encoded_text}"

st.markdown(f'''
    <div style="text-align:center; margin-top:20px;">
        <a href="{whatsapp_url}" target="_blank">
            <button style="background-color:#25D366; color:white; border:none; padding:15px 30px; border-radius:30px; font-weight:bold; font-size:18px; cursor:pointer;">
                📲 WhatsApp Par Bhejein
            </button>
        </a>
    </div>
''', unsafe_allow_html=True)
