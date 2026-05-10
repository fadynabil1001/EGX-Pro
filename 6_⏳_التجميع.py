"""
اكتشاف الأسهم التي تتحرك في نفس الـ price range لفترة طويلة (التجميع)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from components import load_css, app_header
from data.stocks_db import EGX_STOCKS
from data.fetcher import get_historical, get_quote
from analysis.technical import detect_consolidation, PERIOD_MAP

st.set_page_config(page_title="⏳ التجميع", page_icon="⏳", layout="wide")
load_css()
app_header()

st.markdown("## ⏳ كشف الأسهم التي تجمّع (Accumulation/Consolidation)")
st.caption("الأسهم التي تتحرك في نفس النطاق السعري لفترة طويلة — مؤشر على تجميع المؤسسات")

c1, c2 = st.columns(2)
with c1:
    period_name = st.selectbox(
        "📅 الفترة:",
        options=list(PERIOD_MAP.keys()),
        index=2  # شهر default
    )
with c2:
    max_range = st.slider(
        "🎯 الحد الأقصى لاتساع النطاق (%)",
        min_value=3.0, max_value=30.0, value=10.0, step=1.0,
        help="كلما قل الرقم كلما كان السهم أكثر تجميعاً"
    )

period_days = PERIOD_MAP[period_name]

@st.cache_data(ttl=300, show_spinner=False)
def find_consolidating(_period_days: int, _max_range: float):
    results = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        def process(stock):
            df = get_historical(stock, period="2y")
            if df is None or df.empty:
                return None
            res = detect_consolidation(df, _period_days, _max_range)
            if res.get("is_consolidating"):
                quote = get_quote(stock)
                return {**stock, **res, "current_price": quote.get("price")}
            return None

        futures = [ex.submit(process, s) for s in EGX_STOCKS]
        for fut in futures:
            try:
                r = fut.result(timeout=30)
                if r:
                    results.append(r)
            except Exception:
                pass
    return results


with st.spinner(f"⏳ جاري تحليل {len(EGX_STOCKS)} سهم لمدة {period_name}..."):
    results = find_consolidating(period_days, max_range)

st.markdown(f"### 🎯 وجدت **{len(results)}** سهم في وضع تجميع")
st.caption(f"خلال آخر **{period_name}** ({period_days} يوم تداول) — تتحرك ضمن نطاق ≤ **{max_range}%**")

if not results:
    st.info("💡 جرب فترة أطول أو زيادة الحد الأقصى لاتساع النطاق")
else:
    # Sort by tightness (smaller range = better)
    results.sort(key=lambda x: x["range_pct"])

    rows = []
    for s in results:
        rows.append({
            "الرمز": s["ticker"],
            "الاسم": s["name_ar"],
            "السعر الحالي": f"{s.get('current_price', s['current_price']):.2f}" if s.get("current_price") else f"{s['current_price']:.2f}",
            "أعلى سعر": f"{s['high']:.2f}",
            "أدنى سعر": f"{s['low']:.2f}",
            "نطاق %": f"{s['range_pct']:.2f}%",
            "القطاع": s["sector"],
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, height=600)

    st.markdown("### 📊 توزيع الأسهم المجمعة حسب القطاع")
    sectors = pd.Series([s["sector"] for s in results]).value_counts()
    st.bar_chart(sectors)
