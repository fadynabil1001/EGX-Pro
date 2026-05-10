"""
بورصة الوحيد Pro - EGX Stock Analysis Platform
==============================================
المنصة الرئيسية للتحليل الفني والأساسي لأسهم البورصة المصرية
"""

import streamlit as st
from pathlib import Path

# Local imports
from components import (
    load_css, app_header, tradingview_widget, tradingview_ticker_tape
)

# ====================================================================
# Page Config
# ====================================================================
LOGO_PATH = Path(__file__).parent / "assets" / "logo.png"

st.set_page_config(
    page_title="بورصة الوحيد Pro - منصة الأسهم المصرية",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "بورصة الوحيد Pro — منصة احترافية لتحليل أسهم البورصة المصرية."
    },
)

load_css()
app_header()

# ====================================================================
# Sidebar Navigation Info
# ====================================================================
with st.sidebar:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=160)
    st.markdown("### 🧭 التنقل")
    st.markdown(
        """
        اختر أحد الأقسام من القائمة:
        - 🏠 **الرئيسية** (هذه الصفحة)
        - 🔍 **بحث وتحليل سهم**
        - 📊 **EGX Top 30**
        - 📈 **EGX Top 100**
        - 💰 **نطاقات الأسعار**
        - 📊 **الأسهم القوية**
        - ⏳ **اكتشاف التجميع**
        - 📰 **أخبار البورصة**
        - 🔔 **التنبيهات**
        """
    )
    st.divider()
    st.caption("💡 مصادر البيانات: Investing.com، Mubasher، Yahoo Finance، TradingView")
    st.caption("⏱️ آخر تحديث: لحظي")

# ====================================================================
# Main Content - Home / Market Overview
# ====================================================================
st.markdown("### 📡 شريط السوق المباشر")
tradingview_ticker_tape()

st.markdown("### 📈 شارت السوق المصري - EGX 30")
st.caption("شارت TradingView التفاعلي مع كافة الأدوات الفنية")
tradingview_widget(symbol="EGX:EGX30", height=620)

# Quick Statistics Cards
st.markdown("### 🎯 نقاط الوصول السريع")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """<div class="metric-card">
        <div class="label">🔍 بحث وتحليل</div>
        <div class="value">ابحث عن أي سهم</div>
        <div class="delta delta-neu">بالاسم العربي أو الرمز الإنجليزي</div>
        </div>""", unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """<div class="metric-card">
        <div class="label">📊 EGX Top 30</div>
        <div class="value">أهم 30 سهم</div>
        <div class="delta delta-pos">أعلى السيولة</div>
        </div>""", unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """<div class="metric-card">
        <div class="label">⏳ التجميع</div>
        <div class="value">اكتشف الفرص</div>
        <div class="delta delta-neu">أسهم تتحرك في نفس النطاق</div>
        </div>""", unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """<div class="metric-card">
        <div class="label">🔔 تنبيهات</div>
        <div class="value">احصل على إشعارات</div>
        <div class="delta delta-pos">عند وصول السعر للهدف</div>
        </div>""", unsafe_allow_html=True
    )

st.divider()

# Market Heatmap from TradingView
st.markdown("### 🌡️ خريطة السوق الحرارية (EGX 30)")
heatmap_html = """
<div class="tradingview-widget-container" style="height:500px">
  <div class="tradingview-widget-container__widget"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js" async>
  {
  "exchanges": ["EGX"],
  "dataSource": "AllEgypt",
  "grouping": "sector",
  "blockSize": "market_cap_basic",
  "blockColor": "change",
  "locale": "ar_AE",
  "symbolUrl": "",
  "colorTheme": "dark",
  "hasTopBar": true,
  "isDataSetEnabled": true,
  "isZoomEnabled": true,
  "hasSymbolTooltip": true,
  "width": "100%",
  "height": "500"
  }
  </script>
</div>
"""
st.components.v1.html(heatmap_html, height=520)

st.divider()

# Quick News Preview
from data.news import get_all_news
st.markdown("### 📰 أحدث الأخبار")
try:
    news = get_all_news(limit_per_source=5)
    if news:
        for n in news[:8]:
            st.markdown(
                f"""<div class="news-card">
                <div class="news-source">{n['source']}</div>
                <a href="{n['url']}" target="_blank">{n['title']}</a>
                </div>""",
                unsafe_allow_html=True
            )
    else:
        st.info("⚠️ تعذر جلب الأخبار حالياً. حاول مرة أخرى لاحقاً.")
except Exception as e:
    st.info(f"⚠️ خطأ في جلب الأخبار: {e}")

st.divider()

# Footer
st.markdown(
    """
    <div style="text-align:center;padding:20px;color:#8A92A6;font-size:0.85rem">
        بورصة الوحيد Pro © 2026 | بيانات للأغراض التعليمية فقط - ليست توصية استثمارية
        <br>
        📊 EGX | 📈 TradingView | 💼 Investing.com | 📰 Mubasher
    </div>
    """,
    unsafe_allow_html=True
)
