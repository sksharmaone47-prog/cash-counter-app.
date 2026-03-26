import streamlit as st
import urllib.parse
from datetime import date

# Page Layout (Mobile Friendly)
st.set_page_config(page_title="Cash Memo", page_icon="🏦", layout="centered")

# --- NUMBER TO WORDS FUNCTION ---
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
        if res != "": res += "and "
        if n < 20: res += units[n]
        else: res += tens[n // 10] + " " + units[n % 10]
    return res.strip() + " Only"

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Input boxes ko chhota aur compact karne ke liye */
    .stTextInput input {
        padding: 5px !important;
        height: 35px !important;
        text-align: center !important;
        font-size: 14px !important;
    }
    .bill-box {
        border: 1px solid #000;
        padding: 15px;
        background-color: #fff;
        border-radius: 8px;
    }
    /* Mobile screen par columns ke bich ki space kam karne ke liye */
    [data-testid="column"] {
        padding: 0px 5px !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="bill-box">', unsafe_allow_html=True)

# 1. Header: Name & Calendar Date
c1, c2 = st.columns([1.5, 1])
with c1:
    user_name = st.text_input("Customer Name:", value="Sandeep")
with c2:
    # date_input se ab Calendar open hoga
    selected_date = st.date_input("Select Date:", date.today())
    user_date = selected_date.strftime("%d-%m-%Y")

st.markdown(f'<div style="display:flex; justify-content:space-between; font-weight:bold; border-bottom:1px solid #000; padding-bottom:5px; margin-bottom:10px;"><div>👤 {user_name}</div><div>📅 {user_date}</div></div>', unsafe_allow_html=True)
st.markdown('<h4 style="text-align:center; text-decoration:underline; margin-top:0;">CASH DENOMINATION</h4>', unsafe_allow_html=True)

# 2. Denomination Table
notes = [2000, 500, 200, 100, 50, 20, 10]
data = {}
grand_total = 0

# Table Headings (Small Fonts)
h1, h2, h3 = st.columns([1, 0.8, 1.2])
h1.caption("**Note**")
h2.caption("**Qty**")
h3.caption("**Amount**")

for note in notes:
    col_n, col_q, col_a = st.columns([1, 0.8, 1.2])
    
    with col_n:
        st.write(f"💵 ₹{note}")
    
    with col_q:
        # text_input use kiya hai taaki +/- buttons na aayein
        qty_str = st.text_input(f"q_{note}", value="0", key=f"k_{note}", label_visibility="collapsed")
        try:
            qty = int(qty_str) if qty_str else 0
        except ValueError:
            qty = 0
            
    line_amt = note * qty
    grand_total += line_amt
    if qty > 0: data[note] = {"qty": qty, "amt": line_amt}
    
    with col_a:
        st.write(f"**= ₹{line_amt:,}**")

# Coins Section
st.markdown("---")
cc1, cc2, cc3 = st.columns([1, 0.8, 1.2])
cc1.write("🪙 Coins")
with cc2:
    coins_str = st.text_input("coins", value="0", key="c_key", label_visibility="collapsed")
    try:
        coins_total = int(coins_str) if coins_str else 0
    except ValueError:
        coins_total = 0
cc3.write(f"**= ₹{coins_total:,}**")
grand_total += coins_total

# 3. Final Total
total_words = number_to_words(grand_total)
st.markdown(f"""
    <div style="text-align: right; border-top: 1px solid #000; margin-top:10px; padding-top:10px;">
        <h3 style="margin:0;">Grand Total: ₹{grand_total:,}</h3>
        <p style="font-size:12px; font-style:italic;">({total_words})</p>
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
report_text += f"_{total_words}_"

encoded_msg = urllib.parse.quote(report_text)
wa_link = f"https://wa.me/?text={encoded_msg}"

st.markdown(f'''
    <div style="text-align:center; margin-top:20px;">
        <a href="{wa_link}" target="_blank">
            <button style="background-color:#25D366; color:white; border:none; padding:12px 25px; border-radius:30px; font-weight:bold; font-size:16px; cursor:pointer;">
                📲 WhatsApp Share
            </button>
        </a>
    </div>
''', unsafe_allow_html=True)
