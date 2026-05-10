"""
وحدة التحليل الفني - Technical Analysis Module
- المتوسطات المتحركة (21, 50, 100, 200)
- مستويات فيبوناتشي (38.2%, 50%, 61.8%)
- مراقب السيولة (Volume)
- اكتشاف التجميع (Consolidation Detection)
- تحديد القاع والقمة الحقيقيين
"""

import numpy as np
import pandas as pd
from typing import Optional, Dict, List, Any


# ====================================================================
# Moving Averages
# ====================================================================
def compute_moving_averages(df: pd.DataFrame, periods=(21, 50, 100, 200)) -> Dict[int, float]:
    """Compute moving averages for given periods using the close price."""
    if df is None or df.empty:
        return {p: None for p in periods}

    close = df["Close"] if "Close" in df.columns else df.iloc[:, -1]
    result = {}
    for p in periods:
        if len(close) >= p:
            result[p] = float(close.rolling(window=p).mean().iloc[-1])
        else:
            result[p] = None
    return result


def ma_position(current_price: float, ma_value: Optional[float]) -> Dict[str, Any]:
    """Determine if price is above or below a moving average."""
    if ma_value is None or current_price is None:
        return {"position": "N/A", "diff": None, "diff_pct": None}

    diff = current_price - ma_value
    diff_pct = (diff / ma_value * 100) if ma_value else 0.0

    return {
        "position": "فوق" if diff > 0 else "تحت",
        "position_en": "Above" if diff > 0 else "Below",
        "diff": diff,
        "diff_pct": diff_pct,
        "ma_value": ma_value
    }


def analyze_mas(df: pd.DataFrame, current_price: float) -> Dict[int, Dict]:
    """Full MA analysis: returns position relative to each MA."""
    mas = compute_moving_averages(df)
    return {p: ma_position(current_price, v) for p, v in mas.items()}


# ====================================================================
# Fibonacci Retracement Levels
# ====================================================================
def find_swing_high_low(df: pd.DataFrame, lookback_days: int = 180) -> Dict[str, Any]:
    """
    Find the real swing high and low in the lookback period.
    Uses a smoothed approach to identify significant peaks/troughs.
    """
    if df is None or df.empty:
        return {"high": None, "low": None, "high_date": None, "low_date": None}

    recent = df.tail(lookback_days) if len(df) > lookback_days else df

    high_idx = recent["High"].idxmax() if "High" in recent.columns else recent["Close"].idxmax()
    low_idx = recent["Low"].idxmin() if "Low" in recent.columns else recent["Close"].idxmin()

    high_val = float(recent["High"].max() if "High" in recent.columns else recent["Close"].max())
    low_val = float(recent["Low"].min() if "Low" in recent.columns else recent["Close"].min())

    return {
        "high": high_val,
        "low": low_val,
        "high_date": str(high_idx)[:10] if hasattr(high_idx, 'strftime') else str(high_idx)[:10],
        "low_date": str(low_idx)[:10] if hasattr(low_idx, 'strftime') else str(low_idx)[:10],
    }


def fibonacci_levels(high: float, low: float) -> Dict[str, float]:
    """Calculate the key Fibonacci retracement levels."""
    if high is None or low is None or high <= low:
        return {}

    diff = high - low
    return {
        "0%": low,
        "23.6%": low + diff * 0.236,
        "38.2%": low + diff * 0.382,
        "50%": low + diff * 0.500,
        "61.8%": low + diff * 0.618,
        "78.6%": low + diff * 0.786,
        "100%": high,
    }


def fib_position(current_price: float, levels: Dict[str, float]) -> Dict[str, Any]:
    """Determine which Fibonacci zone the current price is in."""
    if not levels or current_price is None:
        return {"zone": "N/A", "nearest": None, "nearest_level": None}

    sorted_levels = sorted(levels.items(), key=lambda x: x[1])

    # Find which zone
    zone = "Above 100%"
    for i in range(len(sorted_levels) - 1):
        lvl_name, lvl_val = sorted_levels[i]
        next_name, next_val = sorted_levels[i + 1]
        if lvl_val <= current_price <= next_val:
            zone = f"بين {lvl_name} و {next_name}"
            break
    if current_price < sorted_levels[0][1]:
        zone = "تحت 0%"

    # Find nearest level
    nearest = min(levels.items(), key=lambda x: abs(x[1] - current_price))

    return {
        "zone": zone,
        "nearest": nearest[0],
        "nearest_level": nearest[1],
        "distance": current_price - nearest[1],
        "distance_pct": ((current_price - nearest[1]) / nearest[1] * 100) if nearest[1] else 0
    }


# ====================================================================
# Volume / Liquidity Monitor
# ====================================================================
def get_volume_table(df: pd.DataFrame, days: int = 20) -> pd.DataFrame:
    """Get the volume table for the last N days with positive/negative sentiment."""
    if df is None or df.empty:
        return pd.DataFrame()

    recent = df.tail(days).copy()
    if "Volume" not in recent.columns:
        return pd.DataFrame()

    recent["السعر"] = recent["Close"].round(2)
    recent["السيولة"] = (recent["Volume"] * recent["Close"]).round(0)
    recent["الحجم"] = recent["Volume"]
    recent["التغيير"] = recent["Close"].diff()
    recent["الاتجاه"] = recent["التغيير"].apply(
        lambda x: "📈 إيجابي" if pd.notna(x) and x > 0 else ("📉 سلبي" if pd.notna(x) and x < 0 else "➖ ثابت")
    )

    out = recent[["السعر", "الحجم", "السيولة", "التغيير", "الاتجاه"]].copy()
    out.index = [d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)[:10]
                 for d in out.index]
    out.index.name = "التاريخ"
    return out.iloc[::-1]  # Most recent first


def daily_liquidity_summary(df: pd.DataFrame, days: int = 30) -> Dict:
    """Daily liquidity summary for the past month (positive/negative)."""
    if df is None or df.empty or "Volume" not in df.columns:
        return {"positive_days": 0, "negative_days": 0, "total_volume": 0, "avg_daily": 0}

    recent = df.tail(days).copy()
    recent["change"] = recent["Close"].diff()
    positive = int((recent["change"] > 0).sum())
    negative = int((recent["change"] < 0).sum())
    total_vol = float(recent["Volume"].sum())
    avg_daily = float(recent["Volume"].mean())

    return {
        "positive_days": positive,
        "negative_days": negative,
        "neutral_days": days - positive - negative,
        "total_volume": total_vol,
        "avg_daily": avg_daily,
        "positive_volume": float(recent.loc[recent["change"] > 0, "Volume"].sum()),
        "negative_volume": float(recent.loc[recent["change"] < 0, "Volume"].sum())
    }


# ====================================================================
# Consolidation Detection (الأسهم التي تتحرك في نفس الـ price range)
# ====================================================================
PERIOD_MAP = {
    "أسبوع": 5,
    "أسبوعين": 10,
    "شهر": 22,
    "3 شهور": 66,
    "6 شهور": 132,
    "سنة": 252,
    "أكثر من سنة": 400,
}


def detect_consolidation(df: pd.DataFrame, period_days: int,
                         max_range_pct: float = 15.0) -> Dict[str, Any]:
    """
    Detect if a stock is consolidating within a price range over a period.
    Returns dict with is_consolidating, range_pct, high, low, etc.
    """
    if df is None or df.empty or len(df) < period_days:
        return {"is_consolidating": False, "reason": "Insufficient data"}

    recent = df.tail(period_days)
    high = float(recent["High"].max() if "High" in recent.columns else recent["Close"].max())
    low = float(recent["Low"].min() if "Low" in recent.columns else recent["Close"].min())

    if low <= 0:
        return {"is_consolidating": False, "reason": "Invalid prices"}

    range_pct = ((high - low) / low) * 100

    return {
        "is_consolidating": range_pct <= max_range_pct,
        "range_pct": range_pct,
        "high": high,
        "low": low,
        "current_price": float(recent["Close"].iloc[-1]),
        "period_days": period_days,
    }


# ====================================================================
# Price Range Classification
# ====================================================================
def classify_by_price(price: float) -> str:
    """Classify stock into price range buckets."""
    if price is None:
        return "غير محدد"
    if price < 1:
        return "أقل من 1 جنيه"
    elif price < 10:
        return "1 - 10 جنيه"
    elif price < 50:
        return "10 - 50 جنيه"
    elif price <= 100:
        return "51 - 100 جنيه"
    else:
        return "أعلى من 100 جنيه"


PRICE_BUCKETS = [
    "أقل من 1 جنيه",
    "1 - 10 جنيه",
    "10 - 50 جنيه",
    "51 - 100 جنيه",
    "أعلى من 100 جنيه",
]


# ====================================================================
# Movement Detection (Strong Gainers/Losers)
# ====================================================================
def calculate_movement(df: pd.DataFrame, days: int = 30) -> Dict[str, Any]:
    """Calculate price movement over N days (for finding strong gainers/losers)."""
    if df is None or df.empty or len(df) < days:
        return {"change_pct": 0, "price_before": None, "price_after": None}

    recent = df.tail(days)
    price_before = float(recent["Close"].iloc[0])
    price_after = float(recent["Close"].iloc[-1])
    change_pct = ((price_after - price_before) / price_before * 100) if price_before else 0

    return {
        "change_pct": change_pct,
        "price_before": price_before,
        "price_after": price_after,
        "abs_change": price_after - price_before,
        "period_days": days,
    }


# ====================================================================
# Full Analysis Report (for a single stock)
# ====================================================================
def full_analysis(df: pd.DataFrame, current_price: Optional[float] = None) -> Dict[str, Any]:
    """Run a complete technical analysis on a stock's historical data."""
    if df is None or df.empty:
        return {"error": "No data available"}

    if current_price is None:
        current_price = float(df["Close"].iloc[-1])

    # Moving Averages
    mas = compute_moving_averages(df)
    ma_analysis = {p: ma_position(current_price, v) for p, v in mas.items()}

    # Fibonacci
    swing = find_swing_high_low(df, lookback_days=180)
    fib = fibonacci_levels(swing["high"], swing["low"])
    fib_pos = fib_position(current_price, fib)

    # Volume
    vol_table = get_volume_table(df, days=20)
    liquidity = daily_liquidity_summary(df, days=30)

    return {
        "current_price": current_price,
        "moving_averages": ma_analysis,
        "swing": swing,
        "fibonacci": fib,
        "fib_position": fib_pos,
        "volume_table": vol_table,
        "liquidity_summary": liquidity,
    }


if __name__ == "__main__":
    # Test with dummy data
    import numpy as np
    dates = pd.date_range(end=pd.Timestamp.today(), periods=300, freq="B")
    prices = 50 + np.cumsum(np.random.randn(300) * 0.5)
    df = pd.DataFrame({
        "Open": prices,
        "High": prices + 1,
        "Low": prices - 1,
        "Close": prices,
        "Volume": np.random.randint(100000, 1000000, 300)
    }, index=dates)
    print(full_analysis(df))
