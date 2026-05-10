"""
بحث وتحليل سهم - Stock Search & Analysis Page
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from components import load_css, app_header, tradingview_widget
from data.stocks_db import EGX_STOCKS, search_stocks, get_stock_by_ticker
from data.fetcher import get_quote, get_historical
from data.alerts import add_alert, get_alerts
from analysis.technical import (
    full_analysis, find_swing_high_low, fibonacci_levels, fib_position,
    compute_moving_averages, ma_position, get_volume_table, daily_liquidity_summary
)

st.set_page_config(
    page_title="🔍 بحث - بورصة الوحيد Pro",
    page_icon="🔍",
    layout="wide"
)
load_css()
app_header()

st.markdown("## 🔍 بحث وتحليل سهم")
st.caption("ابحث عن أي سهم بالاسم العربي أو الإنجليزي أو رمز الـ Ticker")

# ====================================================================
# Search Bar
# ====================================================================
col_search, col_btn = st.columns([5, 1])
with col_search:
    query = st.text_input(
        "🔎 اكتب اسم السهم أو الرمز:",
        placeholder="مثال: COMI أو البنك التجاري الدولي",
        label_visibility="collapsed"
    )

# Quick select from popular stocks
st.caption("**أو اختر من الأسهم الشائعة:**")
popular = ["COMI", "HRHO", "TMGH", "FWRY", "ETEL", "EAST", "EFIH", "ABUK", "PHDC"]
pop_cols = st.columns(len(popular))
selected_quick = None
for i, t in enumerate(popular):
    with pop_cols[i]:
        if st.button(t, key=f"pop_{t}", use_container_width=True):
            selected_quick = t

# Determine selected stock
selected_stock = None
if selected_quick:
    selected_stock = get_stock_by_ticker(selected_quick)
elif query:
    results = search_stocks(query)
    if results:
        if len(results) == 1:
            selected_stock = results[0]
        else:
            st.write(f"وجدت **{len(results)}** نتيجة:")
            options = {f"{s['ticker']} — {s['name_ar']}": s for s in results}
            choice = st.selectbox("اختر سهماً:", list(options.keys()))
            selected_stock = options[choice]
    else:
        st.warning("⚠️ لم يتم العثور على نتائج. جرب رمز مختلف.")

# ====================================================================
# Display Stock Analysis
# ====================================================================
if selected_stock:
    st.divider()
    ticker = selected_stock["ticker"]
    st.markdown(f"## 📊 {selected_stock['name_ar']} ({ticker})")
    st.caption(f"**{selected_stock['name_en']}** — قطاع: {selected_stock['sector']}")

    # Fetch quote and historical data
    with st.spinner("⏳ جاري جلب الأسعار من المصادر..."):
        quote = get_quote(selected_stock)
        df = get_historical(selected_stock, period="2y")

    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    price = quote.get("price")
    change = quote.get("change", 0)
    change_pct = quote.get("change_pct", 0)
    source = quote.get("source", "N/A")

    with col1:
        if price is not None:
            delta_cls = "delta-pos" if change >= 0 else "delta-neg"
            sign = "+" if change >= 0 else ""
            st.markdown(f"""<div class="metric-card">
                <div class="label">السعر الحالي</div>
                <div class="value">{price:,.2f} ج.م</div>
                <div class="delta {delta_cls}">{sign}{change:.2f} ({sign}{change_pct:.2f}%)</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.warning("⚠️ السعر غير متاح حالياً")

    with col2:
        st.markdown(f"""<div class="metric-card">
            <div class="label">المصدر</div>
            <div class="value">📡 {source}</div>
            <div class="delta delta-neu">بيانات حقيقية</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        if quote.get("prev_close"):
            st.markdown(f"""<div class="metric-card">
                <div class="label">إغلاق سابق</div>
                <div class="value">{quote['prev_close']:,.2f} ج.م</div>
                <div class="delta delta-neu">آخر جلسة</div>
            </div>""", unsafe_allow_html=True)

    with col4:
        if df is not None and not df.empty:
            high_52w = df["High"].tail(252).max() if "High" in df.columns else df["Close"].tail(252).max()
            low_52w = df["Low"].tail(252).min() if "Low" in df.columns else df["Close"].tail(252).min()
            st.markdown(f"""<div class="metric-card">
                <div class="label">نطاق 52 أسبوع</div>
                <div class="value">{low_52w:.2f} - {high_52w:.2f}</div>
                <div class="delta delta-neu">قاع وقمة العام</div>
            </div>""", unsafe_allow_html=True)

    # TABS for detailed analysis
    tabs = st.tabs([
        "📈 شارت TradingView",
        "📊 المتوسطات المتحركة",
        "🌀 فيبوناتشي",
        "💧 السيولة والحجم",
        "📑 معلومات الشركة",
        "🔔 إضافة تنبيه"
    ])

    # ===== Tab 1: TradingView Chart =====
    with tabs[0]:
        st.markdown(f"### 📈 شارت {ticker} - TradingView")
        st.caption("شارت تفاعلي مع كل أدوات التحليل الفني")
        tradingview_widget(symbol=selected_stock["tv"], height=620)

    # ===== Tab 2: Moving Averages =====
    with tabs[1]:
        st.markdown("### 📊 موقع السعر بالنسبة للمتوسطات المتحركة")
        if df is None or df.empty or price is None:
            st.warning("⚠️ بيانات تاريخية غير متاحة لحساب المتوسطات")
        else:
            mas = compute_moving_averages(df, periods=(21, 50, 100, 200))
            ma_cols = st.columns(4)
            for idx, p in enumerate([21, 50, 100, 200]):
                pos = ma_position(price, mas[p])
                with ma_cols[idx]:
                    if pos["position"] == "N/A":
                        st.markdown(f"""<div class="metric-card">
                            <div class="label">MA {p}</div>
                            <div class="value">—</div>
                            <div class="delta delta-neu">بيانات غير كافية</div>
                        </div>""", unsafe_allow_html=True)
                    else:
                        cls = "delta-pos" if pos["position"] == "فوق" else "delta-neg"
                        sign = "+" if pos["diff_pct"] >= 0 else ""
                        st.markdown(f"""<div class="metric-card">
                            <div class="label">MA {p} يوم</div>
                            <div class="value">{pos['ma_value']:.2f}</div>
                            <div class="delta {cls}">
                                {'📈' if pos['position'] == 'فوق' else '📉'} السعر {pos['position']} المتوسط ({sign}{pos['diff_pct']:.2f}%)
                            </div>
                        </div>""", unsafe_allow_html=True)

            # Plot price with MAs
            st.markdown("#### 📉 شارت السعر مع المتوسطات")
            fig = go.Figure()
            df_chart = df.tail(300)
            fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart["Close"],
                                     name="السعر", line=dict(color="#FFD700", width=2)))
            colors = ["#00C896", "#4A90E2", "#FF8C00", "#FF4757"]
            for i, p in enumerate([21, 50, 100, 200]):
                if len(df) >= p:
                    ma_series = df["Close"].rolling(window=p).mean().tail(300)
                    fig.add_trace(go.Scatter(x=ma_series.index, y=ma_series,
                                             name=f"MA{p}",
                                             line=dict(color=colors[i], width=1.5, dash="dot")))
            fig.update_layout(
                template="plotly_dark",
                height=480,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(22,27,38,0.5)",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                xaxis_title="التاريخ",
                yaxis_title="السعر (ج.م)",
            )
            st.plotly_chart(fig, use_container_width=True)

    # ===== Tab 3: Fibonacci =====
    with tabs[2]:
        st.markdown("### 🌀 مستويات فيبوناتشي - من آخر قاع وقمة")
        if df is None or df.empty or price is None:
            st.warning("⚠️ بيانات تاريخية غير متاحة")
        else:
            # Lookback choice
            lookback = st.select_slider(
                "اختر فترة البحث عن القاع والقمة:",
                options=[60, 90, 120, 180, 252, 504],
                value=180,
                format_func=lambda x: f"{x//22} شهر" if x <= 252 else f"{x//252} سنة"
            )
            swing = find_swing_high_low(df, lookback_days=lookback)
            fib = fibonacci_levels(swing["high"], swing["low"])
            fib_pos_info = fib_position(price, fib)

            colsw1, colsw2, colsw3 = st.columns(3)
            with colsw1:
                st.metric("🔴 القمة", f"{swing['high']:.2f} ج.م", swing['high_date'])
            with colsw2:
                st.metric("🟢 القاع", f"{swing['low']:.2f} ج.م", swing['low_date'])
            with colsw3:
                st.metric("📍 الموقع الحالي", fib_pos_info.get("zone", "—"),
                         f"الأقرب: {fib_pos_info.get('nearest', '—')}")

            # Show all Fibonacci levels
            st.markdown("#### مستويات فيبوناتشي")
            for level_name, level_val in sorted(fib.items(), key=lambda x: -x[1]):
                is_current = level_name == fib_pos_info.get("nearest")
                cls = "fib-level fib-current" if is_current else "fib-level"
                indicator = "⭐ السعر الحالي قريب من هذا المستوى" if is_current else ""
                st.markdown(f"""
                <div class="{cls}">
                    <strong>{level_name}</strong>
                    <span>{level_val:.2f} ج.م {indicator}</span>
                </div>
                """, unsafe_allow_html=True)

            # Plot
            fig = go.Figure()
            df_chart = df.tail(min(lookback + 30, len(df)))
            fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart["Close"],
                                     name="السعر", line=dict(color="#FFD700", width=2)))
            fib_colors = ["#FF4757", "#FF8C00", "#FFD700", "#FFFFFF", "#00C896", "#4A90E2", "#7B61FF"]
            for i, (name, val) in enumerate(sorted(fib.items(), key=lambda x: x[1])):
                fig.add_hline(y=val, line_dash="dash",
                             annotation_text=f"{name} = {val:.2f}",
                             annotation_position="right",
                             line_color=fib_colors[i % len(fib_colors)],
                             line_width=1)
            fig.update_layout(template="plotly_dark", height=500,
                              paper_bgcolor="rgba(0,0,0,0)",
                              plot_bgcolor="rgba(22,27,38,0.5)")
            st.plotly_chart(fig, use_container_width=True)

    # ===== Tab 4: Volume / Liquidity =====
    with tabs[3]:
        st.markdown("### 💧 مراقب السيولة والحجم")
        if df is None or df.empty:
            st.warning("⚠️ بيانات غير متاحة")
        else:
            # Volume table (last 20 sessions)
            st.markdown("#### آخر 20 جلسة")
            vol_table = get_volume_table(df, days=20)
            if not vol_table.empty:
                st.dataframe(vol_table, use_container_width=True, height=420)

            # Daily liquidity summary (last 30 days)
            st.markdown("#### ملخص السيولة لآخر 30 يوم")
            summary = daily_liquidity_summary(df, days=30)
            sc1, sc2, sc3, sc4 = st.columns(4)
            with sc1:
                st.metric("📈 أيام إيجابية", summary["positive_days"])
            with sc2:
                st.metric("📉 أيام سلبية", summary["negative_days"])
            with sc3:
                st.metric("📊 متوسط الحجم اليومي", f"{summary['avg_daily']:,.0f}")
            with sc4:
                st.metric("💼 إجمالي الحجم", f"{summary['total_volume']:,.0f}")

            # Volume bar chart
            recent = df.tail(30)
            colors = ["#00C896" if recent["Close"].iloc[i] >= (recent["Close"].iloc[i-1] if i > 0 else recent["Close"].iloc[i])
                     else "#FF4757" for i in range(len(recent))]
            fig = go.Figure(data=[go.Bar(
                x=recent.index, y=recent["Volume"],
                marker_color=colors, name="الحجم اليومي"
            )])
            fig.update_layout(template="plotly_dark", height=380,
                              paper_bgcolor="rgba(0,0,0,0)",
                              plot_bgcolor="rgba(22,27,38,0.5)",
                              title="حجم التداول اليومي - 30 يوم")
            st.plotly_chart(fig, use_container_width=True)

    # ===== Tab 5: Company Info =====
    with tabs[4]:
        st.markdown("### 📑 معلومات الشركة")
        info_data = {
            "الرمز (Ticker)": selected_stock["ticker"],
            "الاسم بالعربية": selected_stock["name_ar"],
            "الاسم بالإنجليزية": selected_stock["name_en"],
            "القطاع": selected_stock["sector"],
            "رمز Yahoo": selected_stock["yahoo"],
            "رمز TradingView": selected_stock["tv"],
        }
        st.table(pd.DataFrame(info_data.items(), columns=["البند", "القيمة"]))

        st.markdown("#### 🔗 روابط مفيدة")
        ticker = selected_stock["ticker"]
        slug = selected_stock.get("investing_slug", "")
        st.markdown(f"""
        - 📊 [صفحة السهم على البورصة المصرية](https://www.egx.com.eg/ar/listedcompanies.aspx?Sector=0&type=1&Letter=A) — ابحث عن `{ticker}`
        - 📈 [صفحة Investing.com](https://www.investing.com/equities/{slug})
        - 📰 [أخبار {ticker} على Mubasher](https://www.mubasher.info/markets/EGX/stocks/{ticker})
        - 📊 [شارت TradingView](https://www.tradingview.com/symbols/{selected_stock['tv'].replace(':', '-')}/)
        """)

        st.info("💡 **التقارير المالية والميزانيات:** متاحة على الموقع الرسمي للبورصة المصرية في قسم \"إفصاحات الشركات المقيدة\" - egx.com.eg")

    # ===== Tab 6: Add Alert =====
    with tabs[5]:
        st.markdown("### 🔔 إضافة تنبيه سعري")
        st.caption(f"السعر الحالي: **{price:.2f} ج.م**" if price else "—")

        with st.form("add_alert_form"):
            ac1, ac2 = st.columns(2)
            with ac1:
                target = st.number_input(
                    "السعر المستهدف:",
                    min_value=0.01, value=float(price) if price else 1.0,
                    step=0.1, format="%.2f"
                )
            with ac2:
                direction = st.selectbox(
                    "الاتجاه:",
                    options=["above", "below"],
                    format_func=lambda x: "📈 عندما يصل السعر فوق المستهدف" if x == "above" else "📉 عندما ينخفض السعر تحت المستهدف"
                )
            note = st.text_input("ملاحظة (اختياري):", placeholder="مثل: مقاومة، دعم، شراء...")
            submitted = st.form_submit_button("➕ إضافة التنبيه", use_container_width=True)
            if submitted:
                alert = add_alert(
                    ticker=ticker, name=selected_stock["name_ar"],
                    target_price=target, direction=direction, note=note
                )
                st.success(f"✅ تم إضافة التنبيه! سيتم إعلامك عندما يصل {ticker} إلى {target:.2f} ج.م")
                st.balloons()

        # Show existing alerts for this stock
        all_alerts = get_alerts(active_only=True)
        my_alerts = [a for a in all_alerts if a["ticker"] == ticker]
        if my_alerts:
            st.markdown("#### تنبيهاتك النشطة على هذا السهم:")
            for a in my_alerts:
                dir_text = "فوق" if a["direction"] == "above" else "تحت"
                st.info(f"🔔 تنبيه عند {a['target_price']:.2f} ج.م ({dir_text}) — {a.get('note', '')}")
else:
    # Empty state
    st.info("👆 ابدأ بالبحث أعلاه أو اختر سهماً من الأسهم الشائعة")
