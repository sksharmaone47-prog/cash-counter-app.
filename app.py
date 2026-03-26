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
