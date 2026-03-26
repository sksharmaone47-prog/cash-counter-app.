import streamlit as st
import urllib.parse
from datetime import date

# Mobile-friendly Page Config
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

# --- CSS FOR FIXED TABLE LAYOUT ---
st.markdown("""
<style>
    /* Table styling to force single line on mobile */
    .bill-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }
    .bill-table td {
        padding: 5px 2px;
        vertical-align: middle;
        white-space: nowrap; /* Text ko niche girne se rokta hai */
    }
    .stTextInput input {
        text-align: center !important;
        width: 60px !important;
        height: 30px !important;
        padding: 2px !important;
        font-size: 16px !important;
    }
    .bill-box {
        border: 2px solid #000;
        padding: 10px;
        background-color: #fff;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Main Container
st.markdown('<div class="bill-box">', unsafe_allow_html=True)

# 1. Header: Name & Date
col_h1, col_h2 = st.columns([1.5, 1])
with col_h1:
    user_name = st.text_input("Name:", value="Sandeep")
with col_h2:
    sel_date = st.date_input("Date:", date.today())
    user_date = sel_date.strftime("%d-%m-%Y")

st.markdown(f'<div style="display:flex; justify-content:space-between; border-bottom:2px solid #000; padding:5px; font-weight:bold; font-size:14px;"><span>👤 {user_name}</span><span>📅 {user_date}</span></div>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align:center; text-decoration:underline; margin:10px 0;">CASH DENOMINATION</h3>', unsafe_allow_html=True)

# 2. Denomination Table Headers
st.markdown("""
<table class="bill-table">
    <tr style="font-weight:bold; border-bottom:1px solid #ccc; font-size:14px;">
        <td style="width:30%;">Note</td>
        <td style="width:30%; text-align:center;">Qty</td>
        <td style="width:40%; text-align:right;">Amount</td>
    </tr>
</table>
""", unsafe_allow_html=True)

# 3. Denomination Rows
notes = [2000, 500, 200, 100, 50, 20, 10]
data = {}
grand_total = 0

for note in notes:
    # Creating row with HTML and Streamlit input
    c1, c2, c3 = st.columns([1, 1, 1.2]) # Forced row alignment
    
    with c1:
        st.markdown(f'<div style="padding-top:10px; font-weight:bold; font-size:15px;">💵 ₹{note}</div>', unsafe_allow_html=True)
    with c2:
        qty_str = st.text_input("", value="0", key=f"q_{note}", label_visibility="collapsed")
        try:
            qty = int(qty_str) if qty_str else 0
        except:
            qty = 0
    with c3:
        line_amt = note * qty
        grand_total += line_amt
        if qty > 0: data[note] = {"qty": qty, "amt": line_amt}
        st.markdown(f'<div style="padding-top:10px; text-align:right; font-weight:bold; font-size:15px;">= ₹{line_amt:,}</div>', unsafe_allow_html=True)

# Coins
st.markdown('<hr style="margin:5px 0;">', unsafe_allow_html=True)
cc1, cc2, cc3 = st.columns([1, 1, 1.2])
with cc1:
    st.markdown('<div style="padding-top:10px; font-weight:bold;">🪙 Coins</div>', unsafe_allow_html=True)
with cc2:
    coins_str = st.text_input("", value="0", key="coins", label_visibility="collapsed")
    try:
        coins_total = int(coins_str) if coins_str else 0
    except:
        coins_total = 0
with cc3:
    grand_total += coins_total
    st.markdown(f'<div style="padding-top:10px; text-align:right; font-weight:bold;">= ₹{coins_total:,}</div>', unsafe_allow_html=True)

# 4. Final Total
st.markdown("<hr style='border:1px solid #000;'>", unsafe_allow_html=True)
total_words = number_to_words(grand_total)

st.markdown(f"""
    <div style="text-align: right;">
        <h3 style="margin:0;">Grand Total: ₹{grand_total:,}</h3>
        <p style="font-weight:bold; color:#000; font-size:13px;">{total_words}</p>
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
st.markdown(f'''
    <div style="text-align:center; margin-top:20px;">
        <a href="https://wa.me/?text={encoded_msg}" target="_blank">
            <button style="background-color:#25D366; color:white; border:none; padding:15px 30px; border-radius:30px; font-weight:bold; font-size:18px; cursor:pointer; width:100%;">
                📲 WhatsApp Par Bhejein
            </button>
        </a>
    </div>
''', unsafe_allow_html=True)
