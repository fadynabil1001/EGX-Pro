"""
Shared UI Components - مكونات الواجهة المشتركة
"""

import base64
import streamlit as st
from pathlib import Path


def load_css():
    """Inject custom CSS."""
    css_file = Path(__file__).parent / "assets" / "styles.css"
    if css_file.exists():
        css = css_file.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def logo_base64():
    """Return base64 of the logo for embedding."""
    for fname in ("logo.png", "logo.jpg"):
        logo = Path(__file__).parent / "assets" / fname
        if logo.exists():
            return base64.b64encode(logo.read_bytes()).decode(), fname.split(".")[-1]
    return "", "png"


def app_header():
    """Render the header with logo."""
    b64, ext = logo_base64()
    mime = "png" if ext == "png" else "jpeg"
    if b64:
        img_tag = (
            f'<img src="data:image/{mime};base64,{b64}" '
            f'style="width:64px;height:64px;border-radius:12px;'
            f'box-shadow:0 4px 16px rgba(0,200,150,0.3)"/>'
        )
    else:
        img_tag = '<span style="font-size:48px">📈</span>'

    header_html = (
        '<div class="app-header">'
        + img_tag
        + '<div>'
        + '<h1>بورصة الوحيد Pro</h1>'
        + '<div class="tagline">منصة احترافية لتحليل الأسهم المصرية (EGX) — أنت في أمان شديد</div>'
        + '</div>'
        + '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)


def metric_card(label, value, delta="", delta_class="neu"):
    """Build HTML for a custom metric card."""
    return (
        f'<div class="metric-card">'
        f'<div class="label">{label}</div>'
        f'<div class="value">{value}</div>'
        f'<div class="delta delta-{delta_class}">{delta}</div>'
        f'</div>'
    )


def stock_card_html(ticker, name, price, change_pct):
    """Render a single stock card as HTML."""
    if price is None:
        price_str = "—"
        change_str = "—"
        change_cls = "change-neu"
    else:
        price_str = f"{price:,.2f} ج.م"
        try:
            cp = float(change_pct or 0)
            sign = "+" if cp >= 0 else ""
            change_str = f"{sign}{cp:.2f}%"
            change_cls = "change-pos" if cp >= 0 else "change-neg"
        except Exception:
            change_str = "—"
            change_cls = "change-neu"

    return (
        f'<div class="stock-card">'
        f'<div class="ticker">{ticker}</div>'
        f'<div class="name">{name}</div>'
        f'<div class="price-row">'
        f'<span class="price">{price_str}</span>'
        f'<span class="change {change_cls}">{change_str}</span>'
        f'</div>'
        f'</div>'
    )


def tradingview_widget(symbol="EGX:EGX30", height=600):
    """Embed TradingView Advanced Chart widget."""
    config = (
        '{'
        '"autosize": true,'
        f'"symbol": "{symbol}",'
        '"interval": "D",'
        '"timezone": "Africa/Cairo",'
        '"theme": "dark",'
        '"style": "1",'
        '"locale": "ar_AE",'
        '"toolbar_bg": "#0E1117",'
        '"enable_publishing": false,'
        '"withdateranges": true,'
        '"hide_side_toolbar": false,'
        '"allow_symbol_change": true,'
        '"studies": ['
        '"MASimple@tv-basicstudies",'
        '"RSI@tv-basicstudies",'
        '"Volume@tv-basicstudies"'
        '],'
        '"container_id": "tv_chart_container"'
        '}'
    )
    html = (
        '<div class="tradingview-widget-container" '
        f'style="height:{height}px;width:100%">'
        '<div id="tv_chart_container" style="height:100%;width:100%"></div>'
        '<script type="text/javascript" '
        'src="https://s3.tradingview.com/tv.js"></script>'
        '<script type="text/javascript">'
        f'new TradingView.widget({config});'
        '</script>'
        '</div>'
    )
    st.components.v1.html(html, height=height + 20)


def tradingview_mini(symbol="EGX:EGX30", height=220):
    """Compact TradingView mini-chart."""
    config = (
        '{'
        f'"symbol": "{symbol}",'
        '"width": "100%",'
        f'"height": {height},'
        '"locale": "ar_AE",'
        '"dateRange": "12M",'
        '"colorTheme": "dark",'
        '"trendLineColor": "rgba(0,200,150,1)",'
        '"underLineColor": "rgba(0,200,150,0.15)",'
        '"isTransparent": true,'
        '"autosize": true,'
        '"largeChartUrl": ""'
        '}'
    )
    html = (
        '<div class="tradingview-widget-container" '
        f'style="height:{height}px">'
        '<div class="tradingview-widget-container__widget"></div>'
        '<script type="text/javascript" '
        'src="https://s3.tradingview.com/external-embedding/embed-widget-mini-symbol-overview.js" '
        f'async>{config}</script>'
        '</div>'
    )
    st.components.v1.html(html, height=height + 10)


def tradingview_ticker_tape():
    """Top ticker tape showing key EGX symbols."""
    config = (
        '{'
        '"symbols": ['
        '{"description":"EGX 30","proName":"EGX:EGX30"},'
        '{"description":"COMI","proName":"EGX:COMI"},'
        '{"description":"HRHO","proName":"EGX:HRHO"},'
        '{"description":"TMGH","proName":"EGX:TMGH"},'
        '{"description":"ETEL","proName":"EGX:ETEL"},'
        '{"description":"FWRY","proName":"EGX:FWRY"},'
        '{"description":"EFIH","proName":"EGX:EFIH"},'
        '{"description":"ABUK","proName":"EGX:ABUK"},'
        '{"description":"PHDC","proName":"EGX:PHDC"},'
        '{"description":"EAST","proName":"EGX:EAST"}'
        '],'
        '"showSymbolLogo": false,'
        '"colorTheme": "dark",'
        '"isTransparent": true,'
        '"displayMode": "adaptive",'
        '"locale": "ar_AE"'
        '}'
    )
    html = (
        '<div class="tradingview-widget-container">'
        '<div class="tradingview-widget-container__widget"></div>'
        '<script type="text/javascript" '
        'src="https://s3.tradingview.com/external-embedding/embed-widget-ticker-tape.js" '
        f'async>{config}</script>'
        '</div>'
    )
    st.components.v1.html(html, height=80)


def tradingview_heatmap():
    """Market heatmap for EGX sectors."""
    config = (
        '{'
        '"exchanges": ["EGX"],'
        '"dataSource": "AllEgypt",'
        '"grouping": "sector",'
        '"blockSize": "market_cap_basic",'
        '"blockColor": "change",'
        '"locale": "ar_AE",'
        '"symbolUrl": "",'
        '"colorTheme": "dark",'
        '"hasTopBar": true,'
        '"isDataSetEnabled": true,'
        '"isZoomEnabled": true,'
        '"hasSymbolTooltip": true,'
        '"width": "100%",'
        '"height": "500"'
        '}'
    )
    html = (
        '<div class="tradingview-widget-container" style="height:500px">'
        '<div class="tradingview-widget-container__widget"></div>'
        '<script type="text/javascript" '
        'src="https://s3.tradingview.com/external-embedding/embed-widget-stock-heatmap.js" '
        f'async>{config}</script>'
        '</div>'
    )
    st.components.v1.html(html, height=520)
