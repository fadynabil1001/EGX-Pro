"""
وحدة جلب الأخبار - News Fetcher
المصادر:
- البورصة المصرية الرسمية (egx.com.eg)
- مباشر (mubasher.info)
- Investing.com
"""

import re
import time
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

CACHE_DIR = Path(__file__).parent / "cache"
CACHE_DIR.mkdir(exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
}


def _cache_get(key: str, max_age: int = 600):
    f = CACHE_DIR / f"{key}.json"
    if not f.exists():
        return None
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        if time.time() - data.get("_ts", 0) > max_age:
            return None
        return data.get("data")
    except Exception:
        return None


def _cache_set(key: str, data):
    f = CACHE_DIR / f"{key}.json"
    try:
        f.write_text(
            json.dumps({"_ts": time.time(), "data": data},
                       ensure_ascii=False, default=str),
            encoding="utf-8"
        )
    except Exception:
        pass


# ====================================================================
# Mubasher News
# ====================================================================
def get_mubasher_news(limit: int = 20) -> List[Dict[str, Any]]:
    """Scrape latest news headlines from mubasher.info."""
    cached = _cache_get("mubasher_news", max_age=600)
    if cached:
        return cached

    url = "https://www.mubasher.info/markets/EGX/news"
    news = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return []
        html = resp.text

        # Try to find news items - look for common patterns
        patterns = [
            r'<a[^>]*href="(/news/[^"]+)"[^>]*>([^<]+)</a>',
            r'<a[^>]*class="[^"]*news[^"]*"[^>]*href="([^"]+)"[^>]*>([^<]+)</a>',
            r'<h\d[^>]*><a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>',
        ]

        seen = set()
        for pattern in patterns:
            for match in re.finditer(pattern, html, re.IGNORECASE):
                link = match.group(1).strip()
                title = re.sub(r'\s+', ' ', match.group(2).strip())
                if not title or len(title) < 10:
                    continue
                if link in seen:
                    continue
                seen.add(link)

                if link.startswith("/"):
                    link = "https://www.mubasher.info" + link

                news.append({
                    "title": title,
                    "url": link,
                    "source": "مباشر",
                    "ts": datetime.utcnow().isoformat()
                })
                if len(news) >= limit:
                    break
            if len(news) >= limit:
                break

        _cache_set("mubasher_news", news)
    except Exception:
        pass
    return news


# ====================================================================
# EGX Official News
# ====================================================================
def get_egx_news(limit: int = 20) -> List[Dict[str, Any]]:
    """Scrape latest news/announcements from egx.com.eg."""
    cached = _cache_get("egx_news", max_age=600)
    if cached:
        return cached

    # EGX has news on multiple pages
    urls = [
        "https://www.egx.com.eg/ar/News.aspx",
        "https://www.egx.com.eg/en/News.aspx",
    ]
    news = []
    seen = set()

    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code != 200:
                continue
            html = resp.text

            # Generic news link pattern
            patterns = [
                r'<a[^>]*href="(News_Details\.aspx[^"]+)"[^>]*>([^<]+)</a>',
                r'<a[^>]*href="([^"]+NewsId[^"]+)"[^>]*>([^<]+)</a>',
                r'<a[^>]*href="(/[^"]*news[^"]*)"[^>]*>([^<]{20,200})</a>',
            ]

            for pattern in patterns:
                for m in re.finditer(pattern, html, re.IGNORECASE):
                    link = m.group(1).strip()
                    title = re.sub(r"<[^>]+>|\s+", " ", m.group(2)).strip()
                    if not title or len(title) < 15:
                        continue
                    if link in seen:
                        continue
                    seen.add(link)

                    if link.startswith("/"):
                        link = "https://www.egx.com.eg" + link
                    elif not link.startswith("http"):
                        link = "https://www.egx.com.eg/ar/" + link

                    news.append({
                        "title": title,
                        "url": link,
                        "source": "البورصة المصرية",
                        "ts": datetime.utcnow().isoformat()
                    })
                    if len(news) >= limit:
                        break
                if len(news) >= limit:
                    break
            if len(news) >= limit:
                break
        except Exception:
            continue

    _cache_set("egx_news", news)
    return news


# ====================================================================
# Investing.com EGX News
# ====================================================================
def get_investing_egx_news(limit: int = 20) -> List[Dict[str, Any]]:
    """Get EGX 30 news from investing.com."""
    cached = _cache_get("inv_egx_news", max_age=600)
    if cached:
        return cached

    url = "https://www.investing.com/indices/egx30-news"
    news = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return []
        html = resp.text

        # Investing.com news structure
        article_pattern = r'<a[^>]*href="(/news/[^"]+)"[^>]*data-test="article-title-link"[^>]*>([^<]+)</a>'
        for m in re.finditer(article_pattern, html):
            link = m.group(1)
            title = re.sub(r'\s+', ' ', m.group(2).strip())
            if not title or len(title) < 15:
                continue
            news.append({
                "title": title,
                "url": "https://www.investing.com" + link,
                "source": "Investing.com",
                "ts": datetime.utcnow().isoformat()
            })
            if len(news) >= limit:
                break

        # Fallback pattern
        if not news:
            fallback = r'<a[^>]*href="(/news/[^"]+)"[^>]*>([^<]{20,200})</a>'
            seen = set()
            for m in re.finditer(fallback, html):
                link = m.group(1)
                title = re.sub(r'<[^>]+>|\s+', ' ', m.group(2)).strip()
                if not title or len(title) < 15:
                    continue
                if link in seen:
                    continue
                seen.add(link)
                news.append({
                    "title": title,
                    "url": "https://www.investing.com" + link,
                    "source": "Investing.com",
                    "ts": datetime.utcnow().isoformat()
                })
                if len(news) >= limit:
                    break

        _cache_set("inv_egx_news", news)
    except Exception:
        pass
    return news


# ====================================================================
# Aggregator
# ====================================================================
def get_all_news(limit_per_source: int = 15) -> List[Dict[str, Any]]:
    """Aggregate news from all sources."""
    all_news = []
    all_news.extend(get_mubasher_news(limit_per_source))
    all_news.extend(get_investing_egx_news(limit_per_source))
    all_news.extend(get_egx_news(limit_per_source))
    return all_news


if __name__ == "__main__":
    for n in get_all_news()[:10]:
        print(f"[{n['source']}] {n['title']}")
        print(f"  → {n['url']}")
