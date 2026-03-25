import streamlit as st
from datetime import date
from num2words import num2words

st.set_page_config(page_title="Cash Denomination", page_icon="🏦", layout="wide")

# ---- CLEAN CSS ----
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}

.stApp {background-color:#f1f8e9;}

/* Make inputs ultra compact */
div[data-baseweb="input"] {
    width:70px !important;
}
input {
    text-align:center !important;
    font-weight:bold !important;
    font-size:16px !important;
}

/* Force no wrapping EVER */
.row {
    display:flex;
    align-items:center;
    gap:10px;
    white-space:nowrap;
}

/* Right side result */
.result {
    margin-left:auto;
    font-weight:bold;
    color:#1b5e20;
    font-size:18px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏦 Cash Denomination")

# Sidebar
user_name = st.sidebar.text_input("Entry Name:", "Sandeep")
report_date = st.sidebar.date_input("Date:", date.today())

st.write(f"**{user_name} | {report_date.strftime('%d %b %Y')}**")
st.divider()

notes = [2000, 500, 200, 100, 50, 20, 10]
counts = {}
totals = []

# ---- PERFECT SINGLE LINE ROW ----
for n in notes:
    cols = st.columns([1.2, 1, 0.5, 2])

    with cols[0]:
        st.markdown(f"**₹{n} x**")

    with cols[1]:
        val = st.text_input("", value="0", key=f"k_{n}")
        count = int(val) if val.isdigit() else 0
        counts[n] = count

    with cols[2]:
        st.markdown("**=**")

    with cols[3]:
        subtotal = n * count
        totals.append(subtotal)
        st.markdown(f"<div class='result'>{subtotal}</div>", unsafe_allow_html=True)

# ---- COINS ----
st.divider()

cols = st.columns([1.2, 1, 0.5, 2])

with cols[0]:
    st.markdown("**Coins**")

with cols[1]:
    c_val = st.text_input("", value="0", key="coins")
    coin_val = int(c_val) if c_val.isdigit() else 0

with cols[2]:
    st.markdown("**=**")

with cols[3]:
    st.markdown(f"<div class='result'>{coin_val}</div>", unsafe_allow_html=True)

# ---- TOTAL ----
grand_total = sum(totals) + coin_val
total_items = sum(counts.values())

try:
    words = num2words(grand_total, lang='en_IN').title() + " Only"
except:
    words = "Zero Only"

st.divider()
st.markdown(f"### Total = ₹ {grand_total}")
st.write(words)
st.write(f"Total Items: {total_items}")

# ---- RESET ----
if st.button("🔄 Reset"):
    st.rerun()
