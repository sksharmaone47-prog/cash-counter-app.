import streamlit as st
import urllib.parse
from datetime import date

# Page Layout
st.set_page_config(page_title="Cash Memo", page_icon="🏦", layout="centered")

# --- NUMBER TO WORDS FUNCTION ---
def number_to_words(n):
    # Bahut basic conversion logic (Simple way)
    if n == 0: return "Zero Only"
    def units(n):
        words = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", 
                 "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
        return words[n]
    def tens(n):
        words = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
        return words[n]
    
    # Ye function 1 lakh tak handle karega as per standard requirement
    res = ""
    if (n // 100000) > 0:
        res += units(n // 100000) + " Lakh "
        n %= 100000
    if (n // 1000) > 0:
        res += (units(n // 1000) if n//1000 < 20 else tens(n // 10000) + " " + units((n // 1000) % 10)) + " Thousand "
        n %= 1000
    if (n // 100) > 0:
        res += units(n // 100) + " Hundred "
        n %= 100
    if n > 0:
        if res != "": res += "and "
        if n < 20: res += units(n)
        else: res += tens(n // 10) + " " + units(n % 10)
    
    return res.strip() + " Only"

# --- CUSTOM CSS (Buttons Hide aur Table Layout) ---
st.markdown("""
<style>
    /* Sabhi + aur - buttons ko hide karne ke liye */
    button[step-up="true"], button[step-down="true"] {
        display: none !important;
    }
    div[data-testid="stNumberInputStepUp"], div[data-testid="stNumberInputStepDown"] {
        display: none !important;
    }
    /* Input box ke borders aur style */
    .stNumberInput input {
        text-align: center;
        border: 1px solid #ccc !important;
    }
    .bill-box {
        border: 2px solid #000;
        padding: 25px;
        background-color: #fff;
        color: #000;
        border-radius: 5px;
    }
    .header-row {
        display: flex;
        justify-content: space-between;
        font-weight: bold;
        border-bottom: 2px solid #000;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Main App UI
st.markdown('<div class="bill-box">', unsafe_allow_html=True)

# 1. Header: Name Left, Date Right
c1, c2 = st.columns([2,1])
with c1:
    user_name = st.text_input("Name:", value="Sandeep")
with c2:
    user_date = st.text_input("Date:", value=date.today().strftime("%d-%m-%Y"))

st.markdown(f'<div class="header-row"><div>👤 {user_name}</div><div>📅 {user_date}</div></div>', unsafe_allow_html=True)
st.markdown('<h2 style="text-align:center; text-decoration: underline;">CASH DENOMINATION</h2>', unsafe_allow_html=True)

# 2. Denomination Table Layout
notes = [2000, 500, 200, 100, 50, 20, 10]
data = {}
grand_total = 0

# Table Headings
h1, h2, h3 = st.columns([1, 1, 1])
h1.markdown("**Denom.**")
h2.markdown("**Quantity**")
h3.markdown("**Amount**")

for note in notes:
    col_note, col_input, col_total = st.columns([1, 1, 1])
    
    with col_note:
        st.write(f"💵 ₹{note}")
    
    with col_input:
        # label_visibility="collapsed" use kiya hai taaki label na dikhe
        qty = st.number_input(f"q_{note}", min_value=0, step=1, key=f"key_{note}", label_visibility="collapsed")
    
    line_amt = note * (qty if qty else 0)
    grand_total += line_amt
    if qty > 0: data[note] = {"qty": qty, "amt": line_amt}
    
    with col_total:
        st.write(f"**= ₹{line_amt:,}**")

# Coins
col_cn1, col_cn2, col_cn3 = st.columns([1, 1, 1])
col_cn1.write("🪙 Coins")
with col_cn2:
    coins_total = st.number_input("c_total", min_value=0, step=1, key="c_key", label_visibility="collapsed")
col_cn3.write(f"**= ₹{coins_total:,}**")
grand_total += (coins_total if coins_total else 0)

# 3. Total in Words
st.markdown("<br><hr>", unsafe_allow_html=True)
total_words = number_to_words(grand_total)

st.markdown(f"""
    <div style="text-align: right;">
        <h3 style="margin-bottom:0;">Grand Total: ₹{grand_total:,}</h3>
        <p style="font-style: italic; color: #555;">({total_words})</p>
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
            <button style="background-color:#25D366; color:white; border:none; padding:15px 35px; border-radius:50px; font-weight:bold; font-size:18px; cursor:pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
                📲 WhatsApp Par Bhejein
            </button>
        </a>
    </div>
''', unsafe_allow_html=True)
