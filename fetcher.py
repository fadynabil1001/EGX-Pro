"""
وحدة جلب البيانات من مصادر متعددة - Multi-Source Data Fetcher
يحاول جلب البيانات من:
1. Investing.com (الأدق للأسعار الحقيقية)
2. Mubasher (للأسعار العربية والأخبار)
3. Yahoo Finance (احتياطي / للبيانات التاريخية)
4. EGX الموقع الرسمي
"""

import time
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import requests
from typing import Optional, Dict, Any, List

try:
    import yfinance as yf
    YF_AVAILABLE = True
except ImportError:
    YF_AVAILABLE = False

# Cache directory
CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


# ====================================================================
# Cache Helpers
# ====================================================================
def cache_get(key: str, max_age_seconds: int = 300):
    """Get cached value if not expired."""
    f = CACHE_DIR / f"{key}.json"
    if not f.exists():
        return None
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        if time.time() - data.get("_ts", 0) > max_age_seconds:
            return None
        return data.get("data")
    except Exception:
        return None


def cache_set(key: str, data: Any):
    """Save value to cache."""
    f = CACHE_DIR / f"{key}.json"
    try:
        payload = {"_ts": time.time(), "data": data}
        f.write_text(json.dumps(payload, ensure_ascii=False, default=str),
                    encoding="utf-8")
    except Exception:
        pass


# ====================================================================
# Investing.com Source (Most Accurate for EGX)
# ====================================================================
def fetch_investing_quote(slug: str) -> Optional[Dict[str, Any]]:
    """Fetch quote from investing.com for a given slug."""
    if not slug:
        return None

    cache_key = f"inv_quote_{slug}"
    cached = cache_get(cache_key, max_age_seconds=60)
    if cached:
        return cached

    url = f"https://www.investing.com/equities/{slug}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return None
        html = resp.text

        # Extract last price
        price_match = re.search(
            r'data-test="instrument-price-last"[^>]*>([\d,\.]+)', html
        )
        change_match = re.search(
            r'data-test="instrument-price-change"[^>]*>([\-\+\d,\.]+)', html
        )
        pct_match = re.search(
            r'data-test="instrument-price-change-percent"[^>]*>\(?([\-\+\d,\.]+%)\)?', html
        )
        prev_close_match = re.search(
            r'data-test="prevClose"[^>]*>([\d,\.]+)', html
        )

        if not price_match:
            return None

        def clean_num(s):
            return float(s.replace(",", "").replace("+", "").replace("%", "").strip())

        data = {
            "price": clean_num(price_match.group(1)),
            "change": clean_num(change_match.group(1)) if change_match else 0.0,
            "change_pct": clean_num(pct_match.group(1)) if pct_match else 0.0,
            "prev_close": clean_num(prev_close_match.group(1)) if prev_close_match else None,
            "source": "Investing.com",
            "ts": datetime.utcnow().isoformat()
        }
        cache_set(cache_key, data)
        return data
    except Exception:
        return None


# ====================================================================
# Mubasher Source
# ====================================================================
def fetch_mubasher_quote(ticker: str) -> Optional[Dict[str, Any]]:
    """Fetch quote from mubasher.info."""
    if not ticker:
        return None

    cache_key = f"mub_{ticker}"
    cached = cache_get(cache_key, max_age_seconds=60)
    if cached:
        return cached

    # Mubasher URL pattern (English)
    url = f"https://english.mubasher.info/markets/EGX/stocks/{ticker}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return None
        html = resp.text

        # Mubasher uses different selectors - try multiple patterns
        price_patterns = [
            r'"lastPrice"\s*:\s*"?([\d\.]+)"?',
            r'class="last-price"[^>]*>([\d\.,]+)',
            r'data-last-price="([\d\.]+)"',
            r'<span[^>]*price[^>]*>([\d\.,]+)</span>',
        ]
        price = None
        for pattern in price_patterns:
            m = re.search(pattern, html, re.IGNORECASE)
            if m:
                try:
                    price = float(m.group(1).replace(",", ""))
                    break
                except (ValueError, IndexError):
                    continue

        change_patterns = [
            r'"change"\s*:\s*"?([\-\d\.]+)"?',
            r'data-change="([\-\d\.]+)"',
        ]
        change = 0.0
        for pattern in change_patterns:
            m = re.search(pattern, html)
            if m:
                try:
                    change = float(m.group(1))
                    break
                except (ValueError, IndexError):
                    continue

        pct_patterns = [
            r'"changePercent"\s*:\s*"?([\-\d\.]+)"?',
            r'data-change-percent="([\-\d\.]+)"',
        ]
        change_pct = 0.0
        for pattern in pct_patterns:
            m = re.search(pattern, html)
            if m:
                try:
                    change_pct = float(m.group(1))
                    break
                except (ValueError, IndexError):
                    continue

        if price is None:
            return None

        data = {
            "price": price,
            "change": change,
            "change_pct": change_pct,
            "prev_close": price - change if change else None,
            "source": "Mubasher",
            "ts": datetime.utcnow().isoformat()
        }
        cache_set(cache_key, data)
        return data
    except Exception:
        return None


# ====================================================================
# Yahoo Finance Source (Fallback - includes historical)
# ====================================================================
def fetch_yahoo_data(yahoo_symbol: str, period: str = "2y") -> Optional[pd.DataFrame]:
    """Fetch historical OHLCV data from Yahoo Finance."""
    if not YF_AVAILABLE or not yahoo_symbol:
        return None

    cache_key = f"yf_{yahoo_symbol}_{period}".replace(".", "_")
    cached = cache_get(cache_key, max_age_seconds=600)
    if cached:
        try:
            df = pd.DataFrame(cached)
            df.index = pd.to_datetime(df.index)
            return df
        except Exception:
            pass

    try:
        ticker = yf.Ticker(yahoo_symbol)
        df = ticker.history(period=period, auto_adjust=True)
        if df is None or df.empty:
            return None

        # Cache it
        df_for_cache = df.copy()
        df_for_cache.index = df_for_cache.index.astype(str)
        cache_set(cache_key, df_for_cache.to_dict())
        return df
    except Exception:
        return None


def fetch_yahoo_quote(yahoo_symbol: str) -> Optional[Dict[str, Any]]:
    """Get latest price from Yahoo Finance."""
    if not YF_AVAILABLE:
        return None
    df = fetch_yahoo_data(yahoo_symbol, period="5d")
    if df is None or df.empty:
        return None

    last_close = float(df["Close"].iloc[-1])
    prev_close = float(df["Close"].iloc[-2]) if len(df) > 1 else last_close
    change = last_close - prev_close
    change_pct = (change / prev_close * 100) if prev_close else 0.0

    return {
        "price": last_close,
        "change": change,
        "change_pct": change_pct,
        "prev_close": prev_close,
        "source": "Yahoo Finance",
        "ts": datetime.utcnow().isoformat()
    }


# ====================================================================
# Unified Quote Function (Multi-Source with Fallback)
# ====================================================================
def get_quote(stock: dict) -> Dict[str, Any]:
    """
    Get the most accurate quote available for a stock.
    Tries: Investing.com → Mubasher → Yahoo Finance
    """
    # 1. Try Investing.com (most accurate for EGX)
    quote = fetch_investing_quote(stock.get("investing_slug", ""))
    if quote and quote.get("price"):
        return quote

    # 2. Try Mubasher
    quote = fetch_mubasher_quote(stock.get("ticker", ""))
    if quote and quote.get("price"):
        return quote

    # 3. Fallback: Yahoo Finance
    quote = fetch_yahoo_quote(stock.get("yahoo", ""))
    if quote and quote.get("price"):
        return quote

    # Return placeholder
    return {
        "price": None,
        "change": 0.0,
        "change_pct": 0.0,
        "prev_close": None,
        "source": "N/A",
        "ts": datetime.utcnow().isoformat()
    }


def get_historical(stock: dict, period: str = "2y") -> Optional[pd.DataFrame]:
    """Get historical OHLCV data."""
    return fetch_yahoo_data(stock.get("yahoo", ""), period=period)


# ====================================================================
# Batch Operations
# ====================================================================
def get_quotes_batch(stocks: List[dict], use_cache: bool = True) -> List[dict]:
    """Get quotes for a list of stocks."""
    results = []
    for stock in stocks:
        quote = get_quote(stock)
        results.append({
            **stock,
            **quote
        })
    return results


# ====================================================================
# Investing.com Search (for autocompletion of stock names)
# ====================================================================
def investing_search(query: str) -> List[dict]:
    """Search investing.com for a stock (returns matches)."""
    if not query or len(query) < 2:
        return []

    cache_key = f"inv_search_{query.lower()}"
    cached = cache_get(cache_key, max_age_seconds=3600)
    if cached is not None:
        return cached

    url = "https://www.investing.com/search/service/search"
    try:
        resp = requests.post(
            url,
            data={"search_text": query, "tab": "quotes"},
            headers={**HEADERS, "X-Requested-With": "XMLHttpRequest"},
            timeout=10
        )
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("quotes", [])[:10]
            cache_set(cache_key, results)
            return results
    except Exception:
        pass
    return []


if __name__ == "__main__":
    # Test
    test_stock = {
        "ticker": "COMI", "yahoo": "COMI.CA", "tv": "EGX:COMI",
        "name_en": "Commercial International Bank",
        "investing_slug": "com-intl-bk"
    }
    print("Quote:", get_quote(test_stock))
