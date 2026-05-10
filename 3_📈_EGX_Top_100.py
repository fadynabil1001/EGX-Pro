"""
EGX Top 100 - كل الأسهم في قاعدة البيانات
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from components import load_css, app_header
from data.stocks_db import EGX_STOCKS
from data.fetcher import get_quote

st.set_page_config(page_title="📈 EGX Top 100", page_icon="📈", layout="wide")
load_css()
app_header()

st.markdown("## 📈 EGX Top 100 - شامل أسهم البورصة المصرية")
st.caption("قائمة موسعة بأسهم EGX 100 + قائمة أكبر الشركات المتداولة")

@st.cache_data(ttl=120, show_spinner=False)
def fetch_all_quotes():
    """Fetch quotes for all stocks."""
    quotes = []
    with ThreadPoolExecutor(max_workers=12) as ex:
        futures = [ex.submit(get_quote, s) for s in EGX_STOCKS]
        for s, fut in zip(EGX_STOCKS, futures):
            try:
                q = fut.result(timeout=20)
                quotes.append({**s, **q})
            except Exception:
                quotes.append({**s, "price": None, "change": 0, "change_pct": 0, "source": "N/A"})
    return quotes


with st.spinner("⏳ جاري جلب الأسعار لـ 100 سهم..."):
    quotes = fetch_all_quotes()

# Filter controls
fc1, fc2, fc3 = st.columns(3)
with fc1:
    sectors = sorted(set(q["sector"] for q in quotes))
    sector_filter = st.multiselect("🏷️ القطاع:", sectors, default=[])
with fc2:
    sort_by = st.selectbox("ترتيب حسب:", ["الرمز", "السعر (تنازلي)", "النسبة % (تنازلي)", "النسبة % (تصاعدي)"])
with fc3:
    search = st.text_input("🔍 ابحث:", placeholder="رمز أو اسم")

# Apply filters
filtered = quotes
if sector_filter:
    filtered = [q for q in filtered if q["sector"] in sector_filter]
if search:
    s_lower = search.lower()
    filtered = [q for q in filtered
                if s_lower in q["ticker"].lower()
                or s_lower in q["name_en"].lower()
                or search in q["name_ar"]]

# Build dataframe
rows = []
for q in filtered:
    rows.append({
        "الرمز": q["ticker"],
        "الاسم العربي": q["name_ar"],
        "الاسم الإنجليزي": q["name_en"],
        "السعر": q.get("price"),
        "التغيير": q.get("change", 0),
        "النسبة %": q.get("change_pct", 0),
        "القطاع": q["sector"],
        "المصدر": q.get("source", "N/A"),
    })
df = pd.DataFrame(rows)

# Sorting
if sort_by == "السعر (تنازلي)":
    df = df.sort_values("السعر", ascending=False, na_position="last")
elif sort_by == "النسبة % (تنازلي)":
    df = df.sort_values("النسبة %", ascending=False)
elif sort_by == "النسبة % (تصاعدي)":
    df = df.sort_values("النسبة %", ascending=True)
else:
    df = df.sort_values("الرمز")

st.markdown(f"### عدد الأسهم: **{len(df)}**")
st.dataframe(
    df.style.format({
        "السعر": "{:.2f}",
        "التغيير": "{:+.2f}",
        "النسبة %": "{:+.2f}%"
    }, na_rep="—"),
    use_container_width=True,
    height=600,
)

# Quick visual: distribution by sector
st.markdown("### 🏷️ توزيع الأسهم حسب القطاع")
sector_counts = pd.Series([q["sector"] for q in quotes]).value_counts()
st.bar_chart(sector_counts)
