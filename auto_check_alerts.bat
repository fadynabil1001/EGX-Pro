@echo off
chcp 65001 > nul
title فحص التنبيهات - بورصة الوحيد Pro
cd /d "%~dp0"

echo [%date% %time%] جاري فحص التنبيهات...
python -c "
import sys
sys.path.insert(0, '.')
from concurrent.futures import ThreadPoolExecutor
from data.stocks_db import EGX_STOCKS
from data.fetcher import get_quote
from data.alerts import get_alerts, check_alerts

alerts = get_alerts(active_only=True)
if not alerts:
    print('لا توجد تنبيهات نشطة')
    sys.exit(0)

tickers = set(a['ticker'] for a in alerts)
stocks = [s for s in EGX_STOCKS if s['ticker'] in tickers]
prices = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    fs = {ex.submit(get_quote, s): s['ticker'] for s in stocks}
    for f, t in fs.items():
        try:
            q = f.result(timeout=15)
            prices[t] = q.get('price')
        except Exception:
            pass

triggered = check_alerts(prices)
print(f'تم فحص {len(alerts)} تنبيه — تم تنفيذ {len(triggered)} منها')
for t in triggered:
    print(f'  → {t[\"ticker\"]}: {t[\"current_price\"]:.2f} ج.م')
"
