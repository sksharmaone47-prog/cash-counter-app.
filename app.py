import streamlit as st
import urllib.parse
from datetime import date

# Page Layout - Ye apne aap mobile screen ke hisaab se adjust hoga
st.set_page_config(page_title="Cash Memo", page_icon="🏦", layout="wide")

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
        # 'and' hata diya gaya hai
        if n < 20: res += units[n]
        else: res += tens[n // 10] + " " + units[n % 10]
    return res.strip() + " Only"

# --- CUSTOM CSS FOR PERFECT ALIGNMENT ---
st.markdown("""
<style>
    /* Responsive Box */
    .bill-box {
        border: 1px solid #000;
        padding: 10px;
        background-color: #fff;
        border-radius: 5px;
        max-width: 500px;
        margin: auto;
    }
    /* Alignment Fix for Rows */
    .row-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    .col-note { width: 30%; font-weight: bold; text-align: left; }
    .col-qty { width: 30%; text-align: center; }
    .col-amt { width: 40%; text-align: right; font-weight: bold; }
    
    /* Input Styling */
    .stTextInput input {
        text-align: center !important;
        padding: 2px !important;
        height: 30px !important;
    }
    /* Hide extra padding on mobile */
    [data-testid="column"] { padding: 0px !important; }
</style>
""", unsafe_allow_html=True)

# Container start
st.markdown('<div class="bill-box">', unsafe_allow_html=True)

# 1. Header: Name & Date Picker
h_col1, h_col2 = st.columns(2)
with h_col1:
    user_name = st.text_input("Name:", value="Sandeep")
with h_col2:
    selected_date = st.date_input("Date:", date.today())
    user_date = selected_date.strftime("%d-%m-%Y")

st.markdown(f'<div style="display:flex; justify-content:space-between; border-bottom:2px solid #000; padding:5px; margin-bottom:10px;"><span>👤 {user_name}</span><span>📅 {user_date}</span></div>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align:center; text-decoration:underline; margin:0 0 15px 0;">CASH DENOMINATION</h3>', unsafe_allow_html=True)

# 2. Table Headers
st.markdown('<div class="row-container" style="border-bottom:1px solid #ccc; font-size:12px;">'
            '<div class="col-note">Note</div>'
            '<div class="col-qty">Quantity</div>'
            '<div class="col-amt">Amount</div>'
            '</div>', unsafe_allow_html=True)

# 3. Denomination Rows
notes = [2000, 500, 200, 100, 50, 20, 10]
data = {}
grand_total = 0

for note in notes:
    # Creating custom row with 3 columns for perfect alignment
    c1, c2, c3 = st.columns([1, 1, 1.2])
    
    with c1:
        st.markdown(f'<div style="padding-top:5px;">💵 ₹{note}</div>', unsafe_allow_html=True)
    
    with c2:
        qty_str = st.text_input(f"q_{note}", value="0", key=f"k_{note}", label_visibility="collapsed")
        try:
            qty = int(qty_str) if qty_str else 0
        except ValueError:
            qty = 0
            
    line_amt = note * qty
    grand_total += line_amt
    if qty > 0: data[note] = {"qty": qty, "amt": line_amt}
    
    with c3:
        st.markdown(f'<div style="text-align:right; padding-top:5px;">= ₹{line_amt:,}</div>', unsafe_allow_html=True)

# Coins Row
st.markdown("<br>", unsafe_allow_html=True)
cc1, cc2, cc3 = st.columns([1, 1, 1.2])
with cc1:
    st.markdown('<div style="padding-top:5px;">🪙 Coins</div>', unsafe_allow_html=True)
with cc2:
    coins_str = st.text_input("coins", value="0", key="c_key", label_visibility="collapsed")
    try:
        coins_total = int(coins_str) if coins_str else 0
    except ValueError:
        coins_total = 0
with cc3:
    st.markdown(f'<div style="text-align:right; padding-top:5px;">= ₹{coins_total:,}</div>', unsafe_allow_html=True)

grand_total += coins_total

# 4. Final Total & Words
st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)
total_words = number_to_words(grand_total)

st.markdown(f"""
    <div style="text-align: right;">
        <h3 style="margin:0;">Grand Total: ₹{grand_total:,}</h3>
        <p style="font-size:13px; font-weight:bold; color:#444;">{total_words}</p>
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
            <button style="background-color:#25D366; color:white; border:none; padding:12px 30px; border-radius:30px; font-weight:bold; font-size:18px; cursor:pointer; width:100%; max-width:400px;">
                📲 WhatsApp Par Bhejein
            </button>
        </a>
    </div>
''', unsafe_allow_html=True)
    
