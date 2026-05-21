#!/usr/bin/env python3
"""Fetch SEC XBRL companyfacts for a CIK.

Usage:
  python scripts/fetch_companyfacts.py 0001045810 > nvda-companyfacts.json
"""
import json
import os
import sys
import urllib.request


def fetch_companyfacts(cik: str) -> dict:
    cik = str(cik).zfill(10)
    ua = os.environ.get("SEC_USER_AGENT", "company-analysis-skill/0.1 contact@example.com")
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    # Do not set Accept-Encoding manually: urllib does not transparently
    # decompress gzip in all environments.
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: fetch_companyfacts.py <CIK>", file=sys.stderr)
        return 2
    print(json.dumps(fetch_companyfacts(sys.argv[1]), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
