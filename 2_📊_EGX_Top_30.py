"""
EGX Top 30 - أكبر 30 سهم
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from components import load_css, app_header, stock_card_html
from data.stocks_db import EGX_STOCKS, get_egx30_tickers
from data.fetcher import get_quote

st.set_page_config(page_title="📊 EGX Top 30", page_icon="📊", layout="wide")
load_css()
app_header()

st.markdown("## 📊 EGX Top 30 - أهم 30 سهم في البورصة المصرية")
st.caption("الأسهم الأعلى سيولة في السوق المصري — يتم تحديث الأسعار من Investing.com / Mubasher")

# Embed TradingView screener for EGX
screener_html = """
<div class="tradingview-widget-container" style="height:600px">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-screener.js" async>
  {
  "width": "100%",
  "height": 600,
  "defaultColumn": "overview",
  "defaultScreen": "general",
  "market": "egypt",
  "showToolbar": true,
  "colorTheme": "dark",
  "locale": "ar_AE",
  "isTransparent": true
  }
  </script>
</div>
"""
st.components.v1.html(screener_html, height=620)

st.divider()

# Top 30 Live Quotes
st.markdown("### 💹 الأسعار الحية - Top 30")

@st.cache_data(ttl=120, show_spinner=False)
def fetch_top30_quotes():
    """Fetch quotes for top 30 stocks in parallel."""
    tickers = get_egx30_tickers()
    stocks = [s for s in EGX_STOCKS if s["ticker"] in tickers][:30]
    quotes = []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(get_quote, s): s for s in stocks}
        for fut, s in futures.items():
            try:
                q = fut.result(timeout=20)
                quotes.append({**s, **q})
            except Exception:
                quotes.append({**s, "price": None, "change": 0, "change_pct": 0, "source": "N/A"})
    return quotes


with st.spinner("⏳ جاري جلب الأسعار..."):
    quotes = fetch_top30_quotes()

# Convert to DataFrame for display
rows = []
for q in quotes:
    rows.append({
        "الرمز": q["ticker"],
        "الاسم": q["name_ar"],
        "السعر (ج.م)": f"{q['price']:.2f}" if q.get("price") else "—",
        "التغيير": f"{q.get('change', 0):+.2f}",
        "النسبة %": f"{q.get('change_pct', 0):+.2f}%",
        "القطاع": q["sector"],
        "المصدر": q.get("source", "N/A"),
    })
df = pd.DataFrame(rows)

# Sort selector
sort_col = st.selectbox("ترتيب حسب:", ["الرمز", "النسبة %", "السعر (ج.م)"], index=1)
if sort_col == "النسبة %":
    df["_sort"] = df["النسبة %"].str.replace("%", "").str.replace("+", "").astype(float)
    df = df.sort_values("_sort", ascending=False).drop(columns="_sort")
elif sort_col == "السعر (ج.م)":
    df["_sort"] = pd.to_numeric(df["السعر (ج.م)"].replace("—", "0"), errors="coerce")
    df = df.sort_values("_sort", ascending=False).drop(columns="_sort")

# Style: color the percentage column
def color_pct(val):
    try:
        n = float(val.replace("%", "").replace("+", ""))
        if n > 0:
            return "color: #00C896; font-weight: bold"
        elif n < 0:
            return "color: #FF4757; font-weight: bold"
    except Exception:
        pass
    return "color: #8A92A6"

styled = df.style.applymap(color_pct, subset=["النسبة %", "التغيير"])
st.dataframe(styled, use_container_width=True, height=520)

# Stats summary
st.markdown("### 📈 ملخص الأداء")
gainers = [q for q in quotes if q.get("change_pct", 0) > 0]
losers = [q for q in quotes if q.get("change_pct", 0) < 0]
unchanged = [q for q in quotes if q.get("change_pct", 0) == 0]

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("📈 أسهم رابحة", len(gainers))
with c2:
    st.metric("📉 أسهم خاسرة", len(losers))
with c3:
    st.metric("➖ ثابتة", len(unchanged))
with c4:
    if gainers:
        best = max(gainers, key=lambda x: x.get("change_pct", 0))
        st.metric("🏆 الأعلى صعوداً", best["ticker"], f"+{best['change_pct']:.2f}%")

# Top gainers/losers cards
gc, lc = st.columns(2)
with gc:
    st.markdown("#### 🚀 الأعلى صعوداً")
    top_gainers = sorted(quotes, key=lambda x: x.get("change_pct", 0), reverse=True)[:5]
    for s in top_gainers:
        st.markdown(stock_card_html(s["ticker"], s["name_ar"],
                                     s.get("price"), s.get("change_pct")), unsafe_allow_html=True)

with lc:
    st.markdown("#### 📉 الأعلى هبوطاً")
    top_losers = sorted(quotes, key=lambda x: x.get("change_pct", 0))[:5]
    for s in top_losers:
        st.markdown(stock_card_html(s["ticker"], s["name_ar"],
                                     s.get("price"), s.get("change_pct")), unsafe_allow_html=True)
