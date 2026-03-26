import streamlit as st
import urllib.parse
from datetime import date

# Page ki setting
st.set_page_config(page_title="Cash Memo", page_icon="🏦", layout="centered")

# Custom CSS Bill Jaisa Dikhane Ke Liye
st.markdown("""
<style>
    /* Bill ki outer body */
    .bill-box {
        border: 2px solid #333;
        padding: 20px;
        background-color: white;
        border-radius: 10px;
        font-family: 'Courier New', Courier, monospace; /* Bill jaisa font */
    }
    
    /* Header (Name aur Date) */
    .bill-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        border-bottom: 2px solid #333;
        padding-bottom: 10px;
    }
    
    /* Center Title */
    .center-title {
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        color: black;
        text-decoration: underline;
        margin-bottom: 20px;
    }

    /* Input rows ke bich spacing */
    .stNumberInput {
        margin-bottom: 10px;
    }
    
    /* Grand Total Hindi mein */
    .grand-total-hindi {
        border-top: 2px solid #333;
        margin-top: 20px;
        padding-top: 10px;
        font-weight: bold;
        color: #d32f2f; /* Reddish Color */
        text-align: right;
    }
    
    /* WhatsApp Button Styles */
    .share-container {
        display: flex;
        justify-content: center;
        margin-top: 25px;
    }
    .wa-btn {
        background-color: #25D366;
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 50px;
        cursor: pointer;
        text-decoration: none;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Main container starting
st.markdown('<div class="bill-box">', unsafe_allow_html=True)

# --- BILL HEADER (Name & Date) ---
col_name, col_date = st.columns([2, 1])
with col_name:
    # Text input for Name
    user_name = st.text_input("Grahak ka Naam (Customer Name)", value="Sandeep")
with col_date:
    # Text input for Date
    user_date = st.text_input("Tareekh (Date)", value=date.today().strftime("%d-%m-%Y"))

# Displaying in Bill Format (HTML)
st.markdown(f'''
    <div class="bill-header">
        <div><strong>👤 Name:</strong> {user_name}</div>
        <div><strong>📅 Date:</strong> {user_date}</div>
    </div>
''', unsafe_allow_html=True)


# --- CENTER TITLE ---
st.markdown('<div class="center-title">CASH DENOMINATION</div>', unsafe_allow_html=True)

# --- CALCULATIONS ---
notes = [2000, 500, 200, 100, 50, 20, 10]
data = {}
grand_total = 0

# Storing formatting to display
calculation_display = []

st.write("### Noto ki Ginti (Notes Quantity):")

for note in notes:
    # Horizontal columns per note
    # Column 1: Note name, Column 2: Quantity Input, Column 3: Amount Display
    c1, c2, c3 = st.columns([1, 1, 1.5])
    
    with c1:
        st.write(f"💵 ₹{note} x")
    
    with c2:
        qty = st.number_input(f"Qty for {note}", min_value=0, step=1, key=f"note_{note}", label_visibility="collapsed")
    
    if qty > 0:
        amt = note * qty
        data[note] = {"qty": qty, "amt": amt}
        grand_total += amt
        
        with c3:
            st.markdown(f"**= ₹{amt:,}**")
        
        calculation_display.append(f"₹{note} x {qty} = ₹{amt}")
    else:
        with c3:
            st.markdown("= ₹0")

st.markdown("---")

# Coins Section
st.write("### Coins Total:")
coins_total = st.number_input("Sari Coins ka milakar total bharein", min_value=0, step=1)
if coins_total > 0:
    grand_total += coins_total
    calculation_display.append(f"Coins Total = ₹{coins_total}")

st.markdown("---")

# --- HINDI GRAND TOTAL ---
st.markdown('<div class="grand-total-hindi">', unsafe_allow_html=True)
st.markdown(f"## **कुल योग (Grand Total): ₹{grand_total:,}**")
st.markdown('</div>', unsafe_allow_html=True)

# Container closing
st.markdown('</div>', unsafe_allow_html=True)


# --- WHATSAPP SHARING ---

# WhatsApp formatted text (Bill Jaisa)
report_text = f"📜 *CASH MEMO / receipt*\n"
report_text += f"━━━━━━━━━━━━━━━━━━━━\n"
report_text += f"📅 *Tareekh (Date):* {user_date}\n"
report_text += f"👤 *Grahak (Name):* {user_name}\n"
report_text += f"━━━━━━━━━━━━━━━━━━━━\n"
report_text += f"         *DENOMINATION*\n"
report_text += f"------------------------------------\n"

if not data and coins_total == 0:
    report_text += "    (Koi cash entry nahi hai)\n"
else:
    for n, details in data.items():
        # Padding spaces for alignment
        note_str = f"₹{n}".ljust(6)
        qty_str = f"{details['qty']}".rjust(3)
        amt_str = f"₹{details['amt']:,}".rjust(12)
        report_text += f"{note_str} x {qty_str} = {amt_str}\n"

    if coins_total > 0:
        coins_str = f"₹{coins_total:,}".rjust(12)
        report_text += f"------------------------------------\n"
        report_text += f"Coins Total   = {coins_str}\n"

report_text += f"━━━━━━━━━━━━━━━━━━━━\n"
report_text += f"*कुल योग (Grand Total): ₹{grand_total:,}*\n"
report_text += f"━━━━━━━━━━━━━━━━━━━━\n"
report_text += f"🇮🇳 Shukriya! Wapas aayein."

# WhatsApp Button
encoded_text = urllib.parse.quote(report_text)
whatsapp_url = f"https://wa.me/?text={encoded_text}"

st.markdown(f'''
    <div class="share-container">
        <a href="{whatsapp_url}" target="_blank" class="wa-btn">
            📲 Share on WhatsApp (as Bill)
        </a
    </div>
    ''', unsafe_allow_html=True)
