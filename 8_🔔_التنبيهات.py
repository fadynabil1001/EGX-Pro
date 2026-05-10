"""
التنبيهات السعرية - Price Alerts Management
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

from components import load_css, app_header
from data.stocks_db import EGX_STOCKS, get_stock_by_ticker, search_stocks
from data.fetcher import get_quote
from data.alerts import (
    add_alert, get_alerts, delete_alert, toggle_alert,
    check_alerts, get_settings, save_settings
)

st.set_page_config(page_title="🔔 التنبيهات", page_icon="🔔", layout="wide")
load_css()
app_header()

st.markdown("## 🔔 التنبيهات السعرية")
st.caption("احصل على إشعارات عندما تصل الأسهم لأسعار محددة - على الكمبيوتر وعلى هاتفك!")

# ============== Tabs ==============
tabs = st.tabs(["➕ إضافة تنبيه", "📋 تنبيهاتي", "⚙️ إعدادات الإشعارات", "🔄 فحص الآن"])

# ===== Tab 1: Add Alert =====
with tabs[0]:
    st.markdown("### ➕ إضافة تنبيه جديد")

    # Search for stock
    query = st.text_input("🔍 ابحث عن السهم:", placeholder="COMI أو البنك التجاري الدولي")
    selected_stock = None
    if query:
        results = search_stocks(query)
        if results:
            options = {f"{s['ticker']} — {s['name_ar']}": s for s in results}
            choice = st.selectbox("اختر السهم:", list(options.keys()))
            selected_stock = options[choice]

    if selected_stock:
        ticker = selected_stock["ticker"]
        # Get current price
        with st.spinner("⏳ جلب السعر الحالي..."):
            quote = get_quote(selected_stock)
        current = quote.get("price")
        if current:
            st.info(f"💵 السعر الحالي لـ **{ticker}**: **{current:.2f} ج.م**")

        with st.form("alert_form"):
            ac1, ac2 = st.columns(2)
            with ac1:
                target = st.number_input(
                    "🎯 السعر المستهدف (ج.م):",
                    min_value=0.01, max_value=10000.0,
                    value=float(current) if current else 1.0,
                    step=0.1, format="%.2f"
                )
            with ac2:
                direction = st.selectbox(
                    "📊 الاتجاه:",
                    options=["above", "below"],
                    format_func=lambda x: "📈 السعر يصل فوق المستهدف (مقاومة/بيع)" if x == "above" else "📉 السعر ينخفض تحت المستهدف (دعم/شراء)"
                )
            note = st.text_area("📝 ملاحظة (اختياري):",
                                placeholder="مثال: نقطة مقاومة قوية - بيع جزئي")

            submitted = st.form_submit_button("💾 حفظ التنبيه", use_container_width=True, type="primary")
            if submitted:
                alert = add_alert(
                    ticker=ticker,
                    name=selected_stock["name_ar"],
                    target_price=target,
                    direction=direction,
                    note=note
                )
                st.success(f"✅ تم إضافة التنبيه! ستصلك إشعارات عندما يصل **{ticker}** إلى **{target:.2f} ج.م**")
                st.balloons()

# ===== Tab 2: My Alerts =====
with tabs[1]:
    st.markdown("### 📋 تنبيهاتي")
    all_alerts = get_alerts(active_only=False)

    active = [a for a in all_alerts if a.get("active") and not a.get("triggered")]
    triggered = [a for a in all_alerts if a.get("triggered")]
    inactive = [a for a in all_alerts if not a.get("active")]

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("🟢 نشطة", len(active))
    with m2:
        st.metric("✅ تم تنفيذها", len(triggered))
    with m3:
        st.metric("⏸️ معطلة", len(inactive))

    if not all_alerts:
        st.info("💡 لا توجد تنبيهات محفوظة. أضف تنبيهات من علامة التبويب \"إضافة تنبيه\".")
    else:
        st.markdown("#### 🟢 التنبيهات النشطة")
        for a in active:
            with st.container():
                c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
                dir_txt = "📈 فوق" if a["direction"] == "above" else "📉 تحت"
                with c1:
                    st.markdown(f"**{a['ticker']}** — {a['name']}")
                    if a.get("note"):
                        st.caption(f"💬 {a['note']}")
                with c2:
                    st.markdown(f"🎯 **{a['target_price']:.2f} ج.م** {dir_txt}")
                with c3:
                    if st.button("⏸️", key=f"pause_{a['id']}", help="تعطيل"):
                        toggle_alert(a["id"])
                        st.rerun()
                with c4:
                    if st.button("🗑️", key=f"del_{a['id']}", help="حذف"):
                        delete_alert(a["id"])
                        st.rerun()
                st.divider()

        if triggered:
            st.markdown("#### ✅ التنبيهات التي تم تنفيذها")
            for a in triggered:
                st.success(f"✅ **{a['ticker']}** — وصل للسعر **{a['target_price']:.2f} ج.م** ({a.get('triggered_at', '')[:10]})")
                if st.button("🗑️ حذف", key=f"del_trig_{a['id']}"):
                    delete_alert(a["id"])
                    st.rerun()

        if inactive:
            st.markdown("#### ⏸️ التنبيهات المعطلة")
            for a in inactive:
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"⏸️ **{a['ticker']}** — {a['name']} عند {a['target_price']:.2f} ج.م")
                with c2:
                    if st.button("▶️ تفعيل", key=f"act_{a['id']}"):
                        toggle_alert(a["id"])
                        st.rerun()

# ===== Tab 3: Settings =====
with tabs[2]:
    st.markdown("### ⚙️ إعدادات الإشعارات")
    settings = get_settings()

    st.markdown("#### 💻 إشعارات Windows")
    win_enabled = st.checkbox("✅ تفعيل إشعارات سطح المكتب",
                               value=settings.get("windows_notifications", True))

    st.divider()
    st.markdown("#### 📱 إشعارات الهاتف (عبر ntfy.sh)")
    st.markdown("""
    **خطوات إعداد إشعارات الهاتف:**
    1. ⬇️ حمّل تطبيق **ntfy** من [Google Play](https://play.google.com/store/apps/details?id=io.heckel.ntfy) أو [App Store](https://apps.apple.com/us/app/ntfy/id1625396347)
    2. ✏️ ابتكر اسم موضوع فريد (مثلاً: `borsat-alwaheed-yourname-2026`)
    3. 📲 اشترك في هذا الموضوع داخل التطبيق
    4. 💾 اكتب نفس الاسم هنا واحفظ
    5. ✅ ستصلك إشعارات على الهاتف فوراً عند تنفيذ التنبيهات!
    """)

    ntfy_topic = st.text_input(
        "🔑 اسم موضوع ntfy (Topic):",
        value=settings.get("ntfy_topic", ""),
        placeholder="example: my-borsa-alerts-12345"
    )

    if st.button("💾 حفظ الإعدادات", type="primary"):
        new_settings = {
            **settings,
            "windows_notifications": win_enabled,
            "ntfy_topic": ntfy_topic.strip(),
        }
        save_settings(new_settings)
        st.success("✅ تم حفظ الإعدادات!")

    # Test notification
    st.divider()
    if st.button("🧪 اختبر إرسال إشعار"):
        from data.alerts import notify
        notify("🔔 اختبار - بورصة الوحيد Pro",
               "هذا اختبار للتأكد من وصول الإشعارات بنجاح!")
        st.success("📨 تم إرسال إشعار تجريبي - تحقق من الكمبيوتر/الهاتف")

# ===== Tab 4: Check Now =====
with tabs[3]:
    st.markdown("### 🔄 فحص يدوي للتنبيهات")
    st.caption("اضغط أدناه لفحص كل التنبيهات الآن - سيتم إطلاق إشعارات للتنبيهات التي تحقق شروطها")

    if st.button("🔍 فحص جميع التنبيهات الآن", type="primary"):
        active_alerts = get_alerts(active_only=True)
        if not active_alerts:
            st.info("لا توجد تنبيهات نشطة")
        else:
            with st.spinner(f"⏳ فحص {len(active_alerts)} تنبيه..."):
                # Get prices for all unique tickers
                tickers_needed = set(a["ticker"] for a in active_alerts)
                stocks_needed = [s for s in EGX_STOCKS if s["ticker"] in tickers_needed]
                prices = {}
                with ThreadPoolExecutor(max_workers=8) as ex:
                    futures = {ex.submit(get_quote, s): s["ticker"] for s in stocks_needed}
                    for fut, ticker in futures.items():
                        try:
                            q = fut.result(timeout=15)
                            prices[ticker] = q.get("price")
                        except Exception:
                            prices[ticker] = None

                triggered = check_alerts(prices)

            if triggered:
                st.success(f"🎉 تم تنفيذ **{len(triggered)}** تنبيه!")
                for t in triggered:
                    dir_text = "فوق" if t["direction"] == "above" else "تحت"
                    st.info(f"🔔 **{t['ticker']}** — السعر الحالي {t['current_price']:.2f} ج.م ({dir_text} المستهدف {t['target_price']:.2f})")
            else:
                st.info("لم يتم تنفيذ أي تنبيهات - الأسعار لم تصل المستهدفات بعد")

    st.divider()
    st.markdown("#### 💡 تشغيل الفحص التلقائي")
    st.info("""
    لتشغيل الفحص التلقائي في الخلفية، يمكنك:
    - 🕐 تشغيل المنبه كل 15 دقيقة (في Windows: Task Scheduler)
    - 🔁 ترك Streamlit يعمل والضغط على "فحص" كل فترة
    - 📂 ملف `auto_check.bat` المرفق مع المشروع يقوم بذلك تلقائياً
    """)
