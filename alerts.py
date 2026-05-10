"""
نظام التنبيهات السعرية - Price Alerts System
- إضافة وإدارة التنبيهات
- فحص التنبيهات وإطلاق الإشعارات
- يدعم إشعارات Windows + إشعارات للهاتف عبر ntfy.sh / Pushover (اختياري)
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

import requests

ALERTS_FILE = Path(__file__).parent / "alerts.json"
SETTINGS_FILE = Path(__file__).parent / "settings.json"


def _load_alerts() -> List[Dict]:
    if not ALERTS_FILE.exists():
        return []
    try:
        return json.loads(ALERTS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save_alerts(alerts: List[Dict]):
    ALERTS_FILE.write_text(
        json.dumps(alerts, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8"
    )


def get_settings() -> Dict:
    """Get user settings (notification channels)."""
    if not SETTINGS_FILE.exists():
        return {
            "ntfy_topic": "",      # ntfy.sh topic (set by user for phone notifications)
            "ntfy_server": "https://ntfy.sh",
            "windows_notifications": True,
            "sound": True,
        }
    try:
        return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_settings(settings: Dict):
    SETTINGS_FILE.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


# ====================================================================
# Alert Management
# ====================================================================
def add_alert(ticker: str, name: str, target_price: float, direction: str,
              note: str = "") -> Dict:
    """
    Add a new price alert.
    direction: 'above' (sell/breakout) or 'below' (buy/support)
    """
    alerts = _load_alerts()
    alert = {
        "id": int(time.time() * 1000),
        "ticker": ticker.upper(),
        "name": name,
        "target_price": float(target_price),
        "direction": direction,  # 'above' or 'below'
        "note": note,
        "created_at": datetime.utcnow().isoformat(),
        "triggered": False,
        "triggered_at": None,
        "active": True,
    }
    alerts.append(alert)
    _save_alerts(alerts)
    return alert


def get_alerts(active_only: bool = False) -> List[Dict]:
    alerts = _load_alerts()
    if active_only:
        return [a for a in alerts if a.get("active") and not a.get("triggered")]
    return alerts


def delete_alert(alert_id: int) -> bool:
    alerts = _load_alerts()
    new = [a for a in alerts if a.get("id") != alert_id]
    if len(new) < len(alerts):
        _save_alerts(new)
        return True
    return False


def toggle_alert(alert_id: int) -> bool:
    alerts = _load_alerts()
    for a in alerts:
        if a.get("id") == alert_id:
            a["active"] = not a.get("active", True)
            a["triggered"] = False  # Reset trigger when re-enabling
            _save_alerts(alerts)
            return True
    return False


def mark_triggered(alert_id: int):
    alerts = _load_alerts()
    for a in alerts:
        if a.get("id") == alert_id:
            a["triggered"] = True
            a["triggered_at"] = datetime.utcnow().isoformat()
            _save_alerts(alerts)
            return


# ====================================================================
# Notification Channels
# ====================================================================
def send_ntfy_notification(title: str, message: str) -> bool:
    """Send notification via ntfy.sh - user installs ntfy app on phone."""
    settings = get_settings()
    topic = settings.get("ntfy_topic", "").strip()
    if not topic:
        return False
    server = settings.get("ntfy_server", "https://ntfy.sh")
    url = f"{server}/{topic}"
    try:
        resp = requests.post(
            url,
            data=message.encode("utf-8"),
            headers={
                "Title": title.encode("utf-8"),
                "Priority": "high",
                "Tags": "chart_with_upwards_trend,bell",
            },
            timeout=10
        )
        return resp.status_code == 200
    except Exception:
        return False


def send_windows_notification(title: str, message: str) -> bool:
    """Send Windows toast notification (best-effort)."""
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            timeout=10,
            app_name="بورصة الوحيد Pro"
        )
        return True
    except Exception:
        try:
            # Fallback: use win10toast
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=10, threaded=True)
            return True
        except Exception:
            return False


def notify(title: str, message: str):
    """Send notification through all enabled channels."""
    settings = get_settings()
    if settings.get("windows_notifications", True):
        send_windows_notification(title, message)
    if settings.get("ntfy_topic"):
        send_ntfy_notification(title, message)


# ====================================================================
# Alert Checker
# ====================================================================
def check_alerts(current_prices: Dict[str, float]) -> List[Dict]:
    """
    Check active alerts against current prices.
    Returns list of triggered alerts.
    current_prices: {ticker: price}
    """
    triggered = []
    alerts = get_alerts(active_only=True)
    for alert in alerts:
        ticker = alert["ticker"]
        if ticker not in current_prices:
            continue
        price = current_prices[ticker]
        if price is None:
            continue

        target = alert["target_price"]
        direction = alert["direction"]

        hit = False
        if direction == "above" and price >= target:
            hit = True
        elif direction == "below" and price <= target:
            hit = True

        if hit:
            # Send notification
            title = f"🔔 تنبيه: {alert['name']}"
            msg = (
                f"السهم {ticker} وصل للسعر المستهدف!\n"
                f"السعر الحالي: {price:.2f} جنيه\n"
                f"المستهدف: {target:.2f} جنيه ({'فوق' if direction == 'above' else 'تحت'})"
            )
            if alert.get("note"):
                msg += f"\nملاحظة: {alert['note']}"
            notify(title, msg)
            mark_triggered(alert["id"])
            triggered.append({**alert, "current_price": price})

    return triggered


if __name__ == "__main__":
    print("Active alerts:", get_alerts(active_only=True))
