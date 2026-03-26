import streamlit as st
import urllib.parse
from datetime import date

# Page ki setting
st.set_page_config(page_title="Cash Counter", page_icon="🏦")

st.title("🏦 Cash Denomination Counter")

# 1. Name aur Date change ka option
col_h1, col_h2 = st.columns(2)
with col_h1:
    user_name = st.text_input("Name", value="Sandeep")
with col_h2:
    user_date = st.text_input("Date", value=date.today().strftime("%d-%m-%Y"))

st.markdown("---")

# Notes list
notes = [2000, 500, 200, 100, 50, 20, 10]
data = {}
grand_total = 0

# UI layout for Notes
st.subheader("💵 Notes Quantity")
for note in notes:
    qty = st.number_input(f"₹ {note} Note", min_value=0, step=1, key=f"note_{note}")
    if qty > 0:
        amt = note * qty
        data[note] = {"qty": qty, "amt": amt}
        grand_total += amt

st.markdown("---")

# Coins Section
st.subheader("🪙 Coins")
coins_total = st.number_input("Sari Coins ka Total Amount bharein", min_value=0, step=1)
grand_total += coins_total

# Grand Total Display
st.markdown(f"## 💰 Grand Total: ₹ {grand_total:,}")

# WhatsApp Report Taiyar Karna
report_text = f"🏦 *CASH REPORT*\n👤 *Name:* {user_name}\n📅 *Date:* {user_date}\n\n"
for n, details in data.items():
    report_text += f"💵 ₹{n} x {details['qty']} = ₹{details['amt']}\n"

if coins_total > 0:
    report_text += f"🪙 Coins Total = ₹{coins_total}\n"

report_text += f"\n*GRAND TOTAL: ₹{grand_total}*"

# WhatsApp Button
encoded_text = urllib.parse.quote(report_text)
whatsapp_url = f"https://wa.me/?text={encoded_text}"

st.markdown(f'''
    <a href="{whatsapp_url}" target="_blank">
        <button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:10px; font-weight:bold; font-size:18px; cursor:pointer;">
            📲 Share on WhatsApp
        </button>
    </a>
    ''', unsafe_allow_html=True)
