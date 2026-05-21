#!/usr/bin/env python3
"""Fetch lightweight Google News RSS results for a company query.

Usage:
  python scripts/fetch_news_rss.py "NVIDIA earnings"
"""
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: fetch_news_rss.py <query>", file=sys.stderr)
        return 2
    query = " ".join(sys.argv[1:])
    url = "https://news.google.com/rss/search?q=" + urllib.parse.quote(query) + "&hl=en-US&gl=US&ceid=US:en"
    req = urllib.request.Request(url, headers={"User-Agent": "company-analysis-skill/0.1"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        xml = resp.read()
    root = ET.fromstring(xml)
    items = []
    for item in root.findall(".//item")[:20]:
        items.append({
            "title": item.findtext("title"),
            "link": item.findtext("link"),
            "published": item.findtext("pubDate"),
            "source": item.findtext("source"),
        })
    print(json.dumps(items, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
