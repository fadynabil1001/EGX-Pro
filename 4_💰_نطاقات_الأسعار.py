"""
نطاقات الأسعار - Price Range Categories
- أقل من 1 جنيه
- 1 - 10 جنيه
- 10 - 50 جنيه
- 51 - 100 جنيه
- أعلى من 100 جنيه
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from components import load_css, app_header, stock_card_html
from data.stocks_db import EGX_STOCKS
from data.fetcher import get_quote
from analysis.technical import classify_by_price, PRICE_BUCKETS

st.set_page_config(page_title="💰 نطاقات الأسعار", page_icon="💰", layout="wide")
load_css()
app_header()

st.markdown("## 💰 الأسهم حسب نطاقات الأسعار")
st.caption("تصنيف الأسهم بناءً على سعر السهم الحالي")

@st.cache_data(ttl=120, show_spinner=False)
def fetch_all_quotes():
    quotes = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futures = [ex.submit(get_quote, s) for s in EGX_STOCKS]
        for s, fut in zip(EGX_STOCKS, futures):
            try:
                q = fut.result(timeout=20)
                quotes.append({**s, **q})
            except Exception:
                quotes.append({**s, "price": None, "change": 0, "change_pct": 0})
    return quotes


with st.spinner("⏳ جاري جلب الأسعار وتصنيفها..."):
    quotes = fetch_all_quotes()

# Classify each
for q in quotes:
    q["bucket"] = classify_by_price(q.get("price"))

# Stats per bucket
bucket_counts = {b: 0 for b in PRICE_BUCKETS}
for q in quotes:
    if q["bucket"] in bucket_counts:
        bucket_counts[q["bucket"]] += 1

# Top metrics
mc = st.columns(len(PRICE_BUCKETS))
emojis = ["💎", "🪙", "💵", "💰", "🏆"]
for i, b in enumerate(PRICE_BUCKETS):
    with mc[i]:
        st.markdown(f"""<div class="metric-card">
            <div class="label">{emojis[i]} {b}</div>
            <div class="value">{bucket_counts[b]}</div>
            <div class="delta delta-neu">سهم</div>
        </div>""", unsafe_allow_html=True)

st.divider()

# Tabs per bucket
tabs = st.tabs([f"{emojis[i]} {b}" for i, b in enumerate(PRICE_BUCKETS)])
for tab, bucket in zip(tabs, PRICE_BUCKETS):
    with tab:
        st.markdown(f"### الأسهم في نطاق: **{bucket}**")
        bucket_stocks = [q for q in quotes if q["bucket"] == bucket]
        if not bucket_stocks:
            st.info("لا توجد أسهم في هذا النطاق حالياً")
            continue

        # Sort by change %
        bucket_stocks.sort(key=lambda x: x.get("change_pct", 0), reverse=True)

        # Build table
        rows = []
        for s in bucket_stocks:
            rows.append({
                "الرمز": s["ticker"],
                "الاسم": s["name_ar"],
                "السعر (ج.م)": s.get("price"),
                "النسبة %": s.get("change_pct", 0),
                "القطاع": s["sector"],
            })
        df_bucket = pd.DataFrame(rows)

        st.dataframe(
            df_bucket.style.format({
                "السعر (ج.م)": "{:.2f}",
                "النسبة %": "{:+.2f}%"
            }, na_rep="—"),
            use_container_width=True,
            height=min(420, len(rows) * 40 + 50)
        )

        # Show as cards too
        st.markdown("#### 💳 عرض كبطاقات")
        cols = st.columns(3)
        for i, s in enumerate(bucket_stocks[:12]):
            with cols[i % 3]:
                st.markdown(
                    stock_card_html(s["ticker"], s["name_ar"], s.get("price"), s.get("change_pct")),
                    unsafe_allow_html=True
                )
