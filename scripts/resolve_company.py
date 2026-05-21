#!/usr/bin/env python3
"""Resolve US ticker to SEC CIK using the public SEC company_tickers.json endpoint.

Usage:
  python scripts/resolve_company.py NVDA

SEC requires a descriptive User-Agent. Set SEC_USER_AGENT, e.g.:
  export SEC_USER_AGENT="Your Name your.email@example.com"
"""
import json
import os
import sys
import urllib.request

SEC_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"


def fetch_json(url: str) -> dict:
    ua = os.environ.get("SEC_USER_AGENT", "company-analysis-skill/0.1 contact@example.com")
    # Do not set Accept-Encoding manually: urllib does not transparently
    # decompress gzip in all environments.
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: resolve_company.py <ticker>", file=sys.stderr)
        return 2
    ticker = sys.argv[1].upper()
    data = fetch_json(SEC_TICKERS_URL)
    for row in data.values():
        if row.get("ticker", "").upper() == ticker:
            cik = str(row["cik_str"]).zfill(10)
            print(json.dumps({"ticker": row["ticker"], "title": row["title"], "cik": cik}, indent=2))
            return 0
    print(f"Ticker not found: {ticker}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
