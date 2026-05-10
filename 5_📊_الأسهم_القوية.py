"""
الأسهم القوية - Strong Stocks (Gainers/Losers)
- أسهم قوية مالياً ارتفعت بنسبة كبيرة
- أسهم قوية مالياً انخفضت بنسبة كبيرة
- مع السعر قبل وبعد
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from components import load_css, app_header
from data.stocks_db import EGX_STOCKS, get_egx30_tickers
from data.fetcher import get_quote, get_historical
from analysis.technical import calculate_movement

st.set_page_config(page_title="📊 الأسهم القوية", page_icon="📊", layout="wide")
load_css()
app_header()

st.markdown("## 📊 الأسهم القوية - الصاعدة والهابطة بنسبة كبيرة")
st.caption("يتم تصفية الأسهم القوية مالياً (من EGX 30) وتحديد الحركات السعرية الكبيرة")

# Controls
c1, c2, c3 = st.columns(3)
with c1:
    period_days = st.selectbox(
        "📅 الفترة الزمنية:",
        options=[5, 10, 22, 66, 132],
        format_func=lambda x: {5: "أسبوع", 10: "أسبوعين", 22: "شهر",
                                66: "3 شهور", 132: "6 شهور"}.get(x, f"{x} يوم"),
        index=2
    )
with c2:
    threshold = st.slider("🎯 الحد الأدنى للنسبة %:", min_value=2.0, max_value=50.0, value=10.0, step=1.0)
with c3:
    universe = st.radio("نطاق البحث:",
                        ["EGX 30 (الأقوى مالياً)", "كل الأسهم"],
                        horizontal=True)

# Filter universe
if "30" in universe:
    universe_stocks = [s for s in EGX_STOCKS if s["ticker"] in get_egx30_tickers()]
else:
    universe_stocks = EGX_STOCKS

# Fetch quotes + historical
@st.cache_data(ttl=300, show_spinner=False)
def compute_movements(_tickers: tuple, days: int):
    """Compute movements for the given tickers over N days."""
    stocks = [s for s in EGX_STOCKS if s["ticker"] in _tickers]
    results = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        def process(stock):
            df = get_historical(stock, period="1y" if days <= 132 else "2y")
            if df is None or df.empty:
                return None
            mov = calculate_movement(df, days=days)
            quote = get_quote(stock)
            return {**stock, **mov, **{"current_price": quote.get("price")}}

        futures = [ex.submit(process, s) for s in stocks]
        for fut in futures:
            try:
                r = fut.result(timeout=30)
                if r:
                    results.append(r)
            except Exception:
                pass
    return results


with st.spinner(f"⏳ جاري حساب الحركات السعرية لـ {len(universe_stocks)} سهم..."):
    results = compute_movements(tuple(s["ticker"] for s in universe_stocks), period_days)

# Separate gainers / losers
gainers = [r for r in results if r.get("change_pct", 0) >= threshold]
losers = [r for r in results if r.get("change_pct", 0) <= -threshold]

gainers.sort(key=lambda x: x["change_pct"], reverse=True)
losers.sort(key=lambda x: x["change_pct"])

# Stats
sc1, sc2 = st.columns(2)
with sc1:
    st.metric(f"🚀 صاعدة (≥ +{threshold}%)", len(gainers))
with sc2:
    st.metric(f"📉 هابطة (≤ -{threshold}%)", len(losers))

# Two tabs
g_tab, l_tab = st.tabs([f"🚀 صاعدة بقوة ({len(gainers)})",
                        f"📉 هابطة بقوة ({len(losers)})"])

with g_tab:
    if not gainers:
        st.info(f"لا توجد أسهم صعدت أكثر من {threshold}% خلال هذه الفترة")
    else:
        st.markdown(f"### الأسهم التي ارتفعت أكثر من **{threshold}%** خلال {period_days} يوم")
        rows = []
        for s in gainers:
            rows.append({
                "الرمز": s["ticker"],
                "الاسم": s["name_ar"],
                "السعر قبل": f"{s.get('price_before', 0):.2f}",
                "السعر بعد": f"{s.get('price_after', 0):.2f}",
                "السعر الحالي": f"{s.get('current_price', 0):.2f}" if s.get('current_price') else "—",
                "التغيير المطلق": f"{s.get('abs_change', 0):+.2f}",
                "النسبة %": f"+{s['change_pct']:.2f}%",
                "القطاع": s["sector"],
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, height=520)

with l_tab:
    if not losers:
        st.info(f"لا توجد أسهم انخفضت أكثر من {threshold}% خلال هذه الفترة")
    else:
        st.markdown(f"### الأسهم التي انخفضت أكثر من **{threshold}%** خلال {period_days} يوم")
        rows = []
        for s in losers:
            rows.append({
                "الرمز": s["ticker"],
                "الاسم": s["name_ar"],
                "السعر قبل": f"{s.get('price_before', 0):.2f}",
                "السعر بعد": f"{s.get('price_after', 0):.2f}",
                "السعر الحالي": f"{s.get('current_price', 0):.2f}" if s.get('current_price') else "—",
                "التغيير المطلق": f"{s.get('abs_change', 0):.2f}",
                "النسبة %": f"{s['change_pct']:.2f}%",
                "القطاع": s["sector"],
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, height=520)
