import streamlit as st
import urllib.parse
from datetime import date

# Mobile Friendly Config
st.set_page_config(page_title="Cash Memo", page_icon="🏦", layout="centered")

# --- NUMBER TO WORDS (NO 'AND') ---
def number_to_words(n):
    if n == 0: return "Zero Only"
    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", 
             "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    res = ""
    if (n // 100000) > 0:
        res += units[n // 100000] + " Lakh "
        n %= 100000
    if (n // 1000) > 0:
        val = n // 1000
        res += (units[val] if val < 20 else tens[val // 10] + " " + units[val % 10]) + " Thousand "
        n %= 1000
    if (n // 100) > 0:
        res += units[n // 100] + " Hundred "
        n %= 100
    if n > 0:
        if n < 20: res += units[n]
        else: res += tens[n // 10] + " " + units[n % 10]
    return res.strip() + " Only"

# --- CSS FOR FORCED SIDE-BY-SIDE ALIGNMENT ---
st.markdown("""
<style>
    /* Mobile par columns ko tutne se rokne ke liye */
    [data-testid="column"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        width: 100% !important;
        min-width: 100% !important;
    }
    .main-container {
        border: 1px solid #000;
        padding: 10px;
        background-color: #fff;
        border-radius: 5px;
    }
    /* Input box setting */
    input {
        text-align: center !important;
        width: 70px !important;
        height: 35px !important;
        border: 1px solid #ccc !important;
    }
</style>
""", unsafe_allow_html=True)

# 1. Header Section
st.markdown('<div class="main-container">', unsafe_allow_html=True)
col_h1, col_h2 = st.columns([1, 1])
with col_h1:
    user_name = st.text_input("Name:", value="Sandeep")
with col_h2:
    sel_date = st.date_input("Date:", date.today())
    user_date = sel_date.strftime("%d-%m-%Y")

st.markdown(f'<div style="display:flex; justify-content:space-between; border-bottom:2px solid #000; padding:5px; font-weight:bold;"><span>👤 {user_name}</span><span>📅 {user_date}</span></div>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align:center; text-decoration:underline;">CASH DENOMINATION</h3>', unsafe_allow_html=True)

# 2. Denomination Table (Custom HTML-like Rows)
notes = [2000, 500, 200, 100, 50, 20, 10]
data = {}
grand_total = 0

# Header Label
st.markdown('<div style="display:flex; justify-content:space-between; font-weight:bold; font-size:14px; margin-bottom:10px;">'
            '<span style="width:30%;">Note</span>'
            '<span style="width:30%; text-align:center;">Qty</span>'
            '<span style="width:40%; text-align:right;">Amount</span></div>', unsafe_allow_html=True)

for note in notes:
    # We use a single column to force them to stay together
    col = st.columns(1)[0]
    with col:
        # Note Label
        st.markdown(f'<span style="width:30%; font-weight:bold;">💵 ₹{note}</span>', unsafe_allow_html=True)
        
        # Qty Input (No Plus/Minus)
        qty_str = st.text_input("", value="0", key=f"q_{note}", label_visibility="collapsed")
        try:
            qty = int(qty_str) if qty_str else 0
        except:
            qty = 0
            
        line_amt = note * qty
        grand_total += line_amt
        if qty > 0: data[note] = {"qty": qty, "amt": line_amt}
        
        # Amount Label
        st.markdown(f'<span style="width:40%; text-align:right; font-weight:bold;">= ₹{line_amt:,}</span>', unsafe_allow_html=True)

# Coins Row
st.markdown('<hr style="margin:5px 0;">', unsafe_allow_html=True)
c_col = st.columns(1)[0]
with c_col:
    st.markdown('<span style="width:30%; font-weight:bold;">🪙 Coins</span>', unsafe_allow_html=True)
    coins_str = st.text_input("", value="0", key="coins", label_visibility="collapsed")
    try:
        coins_total = int(coins_str) if coins_str else 0
    except:
        coins_total = 0
    st.markdown(f'<span style="width:40%; text-align:right; font-weight:bold;">= ₹{coins_total:,}</span>', unsafe_allow_html=True)
    grand_total += coins_total

# 3. Total & Words
st.markdown("<hr style='border:1px solid #000;'>", unsafe_allow_html=True)
total_words = number_to_words(grand_total)

st.markdown(f"""
    <div style="text-align: right;">
        <h3 style="margin:0;">Grand Total: ₹{grand_total:,}</h3>
        <p style="font-weight:bold; color:#000;">{total_words}</p>
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# WhatsApp Button
report_text = f"📜 *CASH MEMO*\n👤 *Name:* {user_name}\n📅 *Date:* {user_date}\n"
report_text += f"━━━━━━━━━━━━━━\n"
for n, d in data.items():
    report_text += f"💵 ₹{n} x {d['qty']} = ₹{d['amt']:,}\n"
if coins_total > 0:
    report_text += f"🪙 Coins = ₹{coins_total:,}\n"
report_text += f"━━━━━━━━━━━━━━\n"
report_text += f"*TOTAL: ₹{grand_total:,}*\n*{total_words}*"

encoded_msg = urllib.parse.quote(report_text)
st.markdown(f'<br><a href="https://wa.me/?text={encoded_msg}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:30px; font-weight:bold; font-size:18px;">📲 WhatsApp Share</button></a>', unsafe_allow_html=True)
