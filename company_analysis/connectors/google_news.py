"""Google News RSS connector (stdlib-only).

Fetches recent news via Google News RSS feeds. No API key required.
Returns raw RSS items with provenance.
"""
from __future__ import annotations

import html
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any


def _fetch_rss(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; company-analysis-skill/0.1)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return ""


def fetch_news(ticker: str, company_name: str | None = None, max_items: int = 10) -> dict[str, Any]:
    """Return recent news items with provenance.

    Args:
        ticker: e.g. "AAPL"
        company_name: optional human name for broader search
        max_items: max RSS items to return

    Returns:
        {
            "items": [
                {"title": "...", "link": "...", "pub_date": "...", "source": "..."},
            ],
            "sources": [...],
        }
    """
    # Try ticker-specific RSS first, then company name
    queries = [f"{ticker}+stock"]
    if company_name:
        queries.append(f"{company_name.replace(' ', '+')}")

    items: list[dict[str, str]] = []
    seen_links: set[str] = set()

    for query in queries:
        rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        body = _fetch_rss(rss_url)
        if not body:
            continue

        try:
            root = ET.fromstring(body)
        except ET.ParseError:
            continue

        # RSS 2.0 namespace
        ns = {"rss": "http://purl.org/dc/elements/1.1/"}
        channel = root.find("channel")
        if channel is None:
            continue

        for item in channel.findall("item"):
            title_el = item.find("title")
            link_el = item.find("link")
            pub_el = item.find("pubDate")
            source_el = item.find("source")

            title = html.unescape(title_el.text) if title_el is not None and title_el.text else ""
            link = link_el.text if link_el is not None and link_el.text else ""
            pub_date = pub_el.text if pub_el is not None and pub_el.text else ""
            source = source_el.text if source_el is not None and source_el.text else ""

            if not link or link in seen_links:
                continue
            seen_links.add(link)
            items.append({
                "title": title,
                "link": link,
                "pub_date": pub_date,
                "source": source,
            })
            if len(items) >= max_items:
                break

        if len(items) >= max_items:
            break

    sources = [
        {
            "title": f"Google News RSS: {ticker}",
            "url": f"https://news.google.com/rss/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en",
            "source_type": "news_aggregator",
            "reliability": "secondary_aggregated",
        }
    ]

    return {
        "items": items,
        "sources": sources,
    }
