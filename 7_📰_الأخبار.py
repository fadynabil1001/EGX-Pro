"""
أخبار البورصة المصرية - من مصادر متعددة
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st

from components import load_css, app_header
from data.news import get_mubasher_news, get_egx_news, get_investing_egx_news, get_all_news

st.set_page_config(page_title="📰 الأخبار", page_icon="📰", layout="wide")
load_css()
app_header()

st.markdown("## 📰 أخبار البورصة المصرية")
st.caption("أحدث الأخبار والإفصاحات من المصادر الرسمية")

if st.button("🔄 تحديث الأخبار", use_container_width=False):
    st.cache_data.clear()
    st.rerun()

# Tabs by source
tabs = st.tabs(["📡 كل المصادر", "🏛️ البورصة المصرية", "📊 مباشر", "📈 Investing.com"])

with tabs[0]:
    st.markdown("### كل الأخبار من جميع المصادر")
    with st.spinner("⏳ جاري جلب الأخبار..."):
        news = get_all_news(limit_per_source=20)
    if not news:
        st.warning("⚠️ تعذر جلب الأخبار. حاول مرة أخرى.")
    else:
        for n in news:
            st.markdown(
                f"""<div class="news-card">
                <div class="news-source">{n['source']}</div>
                <a href="{n['url']}" target="_blank">{n['title']}</a>
                </div>""",
                unsafe_allow_html=True
            )

with tabs[1]:
    st.markdown("### 🏛️ أخبار البورصة المصرية (الموقع الرسمي)")
    st.caption("المصدر: egx.com.eg")
    with st.spinner("⏳ جاري جلب الأخبار..."):
        news = get_egx_news(30)
    if not news:
        st.info("📍 يمكنك الذهاب مباشرة إلى: [egx.com.eg](https://www.egx.com.eg/ar/News.aspx)")
    else:
        for n in news:
            st.markdown(
                f"""<div class="news-card">
                <div class="news-source">{n['source']}</div>
                <a href="{n['url']}" target="_blank">{n['title']}</a>
                </div>""",
                unsafe_allow_html=True
            )

with tabs[2]:
    st.markdown("### 📊 أخبار مباشر")
    st.caption("المصدر: mubasher.info")
    with st.spinner("⏳ جاري جلب الأخبار..."):
        news = get_mubasher_news(30)
    if not news:
        st.info("📍 [zugzwang إلى Mubasher مباشرة](https://www.mubasher.info/markets/EGX/news)")
    else:
        for n in news:
            st.markdown(
                f"""<div class="news-card">
                <div class="news-source">{n['source']}</div>
                <a href="{n['url']}" target="_blank">{n['title']}</a>
                </div>""",
                unsafe_allow_html=True
            )

with tabs[3]:
    st.markdown("### 📈 أخبار Investing.com - EGX 30")
    with st.spinner("⏳ جاري جلب الأخبار..."):
        news = get_investing_egx_news(30)
    if not news:
        st.info("📍 [الذهاب إلى Investing.com مباشرة](https://www.investing.com/indices/egx30-news)")
    else:
        for n in news:
            st.markdown(
                f"""<div class="news-card">
                <div class="news-source">{n['source']}</div>
                <a href="{n['url']}" target="_blank">{n['title']}</a>
                </div>""",
                unsafe_allow_html=True
            )

st.divider()
st.markdown("### 🔗 روابط مفيدة")
st.markdown("""
- 🏛️ [البورصة المصرية الرسمية](https://www.egx.com.eg/ar/)
- 📊 [مباشر](https://www.mubasher.info/markets/EGX)
- 📈 [Investing.com EGX 30](https://www.investing.com/indices/egx30)
- 📰 [Reuters Egypt](https://www.reuters.com/markets/quotes/EGX30/)
- 📊 [TradingView EGX](https://www.tradingview.com/markets/stocks-egypt/)
""")
