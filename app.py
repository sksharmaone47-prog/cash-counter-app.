import streamlit as st
import urllib.parse
from datetime import date

# Mobile par landscape/portrait dono ke liye optimize kiya gaya hai
st.set_page_config(page_title="Cash Memo", page_icon="🏦", layout="centered")

# --- NUMBER TO WORDS FUNCTION (WITHOUT 'AND') ---
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

# --- CSS FOR FIXED ROW ALIGNMENT ---
st.markdown("""
<style>
    /* Table ki sidh fix karne ke liye */
    .bill-box {
        border: 2px solid #000;
        padding: 15px;
        background-color: #fff;
        border-radius: 5px;
        color: #000;
    }
    .custom-table {
        width: 100%;
        border-collapse: collapse;
    }
    .custom-table td {
        padding: 10px 2px;
        vertical-align: middle;
    }
    /* Input box ko chhota aur center karne ke liye */
    div.stTextInput input {
        text-align: center !important;
        height: 35px !important;
        padding: 0px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="bill-box">', unsafe_allow_html=True)

# 1. Header: Name & Calendar Date
h1, h2 = st.columns([1.5, 1])
with h1:
    user_name = st.text_input("Name:", value="Sandeep")
with h2:
    selected_date = st.date_input("Date:", date.today())
    user_date = selected_date.strftime("%d-%m-%Y")

st.markdown(f'<div style="display:flex; justify-content:space-between; border-bottom:2px solid #000; padding-bottom:5px; margin-bottom:10px; font-weight:bold;"><span>👤 {user_name}</span><span>📅 {user_date}</span></div>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align:center; text-decoration:underline; margin:10px 0;">CASH DENOMINATION</h3>', unsafe_allow_html=True)

# 2. Denomination Rows (Table Layout for Side-by-Side Alignment)
notes = [2000, 500, 200, 100, 50, 20, 10]
data = {}
grand_total = 0

# Column Header Labels
c1, c2, c3 = st.columns([1.2, 1, 1.2])
c1.markdown("**Note**")
c2.markdown("<div style='text-align:center'>**Qty**</div>", unsafe_allow_html=True)
c3.markdown("<div style='text-align:right'>**Amount**</div>", unsafe_allow_html=True)

for note in notes:
    row_c1, row_c2, row_c3 = st.columns([1.2, 1, 1.2])
    
    with row_c1:
        st.markdown(f"<div style='padding-top:8px;'>💵 ₹{note}</div>", unsafe_allow_html=True)
    
    with row_c2:
        # text_input se +/- hat gaye, input bich mein aur chhota ho gaya
        qty_str = st.text_input(f"q_{note}", value="0", key=f"k_{note}", label_visibility="collapsed")
        try:
            qty = int(qty_str) if qty_str else 0
        except ValueError:
            qty = 0
            
    line_amt = note * qty
    grand_total += line_amt
    if qty > 0: data[note] = {"qty": qty, "amt": line_amt}
    
    with row_c3:
        st.markdown(f"<div style='text-align:right; padding-top:8px; font-weight:bold;'>= ₹{line_amt:,}</div>", unsafe_allow_html=True)

# Coins Section
st.markdown("<hr style='margin:5px 0;'>", unsafe_allow_html=True)
cc1, cc2, cc3 = st.columns([1.2, 1, 1.2])
cc1.markdown("<div style='padding-top:8px;'>🪙 Coins</div>", unsafe_allow_html=True)
with cc2:
    coins_str = st.text_input("coins", value="0", key="c_key", label_visibility="collapsed")
    try:
        coins_total = int(coins_str) if coins_str else 0
    except ValueError:
        coins_total = 0
cc3.markdown(f"<div style='text-align:right; padding-top:8px; font-weight:bold;'>= ₹{coins_total:,}</div>", unsafe_allow_html=True)
grand_total += coins_total

# 3. Final Total & Words
st.markdown("<hr style='border:1px solid #000;'>", unsafe_allow_html=True)
total_words = number_to_words(grand_total)

st.markdown(f"""
    <div style="text-align: right;">
        <h3 style="margin:0;">Grand Total: ₹{grand_total:,}</h3>
        <p style="font-size:13px; font-weight:bold; color:#000;">{total_words}</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- WHATSAPP SHARE ---
report_text = f"📜 *CASH MEMO*\n👤 *Name:* {user_name}\n📅 *Date:* {user_date}\n"
report_text += f"━━━━━━━━━━━━━━\n"
for n, d in data.items():
    report_text += f"💵 ₹{n} x {d['qty']} = ₹{d['amt']:,}\n"
if coins_total > 0:
    report_text += f"🪙 Coins = ₹{coins_total:,}\n"
report_text += f"━━━━━━━━━━━━━━\n"
report_text += f"*TOTAL: ₹{grand_total:,}*\n"
report_text += f"*{total_words}*"

encoded_msg = urllib.parse.quote(report_text)
wa_link = f"https://wa.me/?text={encoded_msg}"

st.markdown(f'''
    <div style="text-align:center; margin-top:20px;">
        <a href="{wa_link}" target="_blank">
            <button style="background-color:#25D366; color:white; border:none; padding:12px 30px; border-radius:30px; font-weight:bold; font-size:18px; cursor:pointer; width:100%;">
                📲 WhatsApp Bhejein
            </button>
        </a>
    </div>
''', unsafe_allow_html=True)
