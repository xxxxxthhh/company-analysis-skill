"""SEC EDGAR public data connector (stdlib-only).

Fetches company facts and recent filings via SEC EDGAR API.
Respects SEC rate limits (10 requests/second).
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from datetime import date
from typing import Any


_TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
_SUBMISSIONS_API = "https://data.sec.gov/submissions"
_COMPANYFACTS_API = "https://data.sec.gov/api/xbrl/companyfacts"

# SEC requires a descriptive User-Agent with contact information. Allow users to
# override it for production runs without editing source.
_HEADERS = {
    "User-Agent": os.environ.get(
        "SEC_USER_AGENT",
        "company-analysis-skill/0.1 contact@example.com (github.com/xxxxxthhh/company-analysis-skill)",
    ),
    "Accept": "application/json",
}


def _fetch_json(url: str, timeout: int = 30) -> dict[str, Any]:
    req = urllib.request.Request(url, headers=_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {}
        raise


def _cik_from_ticker(ticker: str) -> str | None:
    """Lookup CIK from ticker using SEC's company tickers file."""
    data = _fetch_json(_TICKERS_URL)
    for entry in data.values():
        if entry.get("ticker", "").upper() == ticker.upper():
            return str(entry["cik_str"]).zfill(10)
    return None


def fetch_sec_data(ticker: str) -> dict[str, Any]:
    """Return raw SEC data for a ticker with full provenance.

    Connector failures are returned as error fields instead of crashing the
    whole pipeline. A public-data pipeline should degrade gracefully: missing SEC
    data is a quality issue for the report, not a Python traceback.
    """
    access_date = str(date.today())

    try:
        cik = _cik_from_ticker(ticker)
    except urllib.error.HTTPError as exc:
        return {
            "cik": None,
            "company_facts": {},
            "recent_filings": [],
            "sources": [
                {
                    "title": f"SEC ticker lookup: {ticker}",
                    "url": _TICKERS_URL,
                    "source_type": "SEC EDGAR",
                    "access_date": access_date,
                    "reliability": "primary_regulatory",
                }
            ],
            "error": f"SEC ticker lookup failed with HTTP {exc.code}",
        }

    if not cik:
        return {
            "cik": None,
            "company_facts": {},
            "recent_filings": [],
            "sources": [],
            "error": f"Could not resolve CIK for ticker {ticker}",
        }

    # Respect SEC rate limit.
    time.sleep(0.15)

    try:
        facts = _fetch_json(f"{_COMPANYFACTS_API}/CIK{cik}.json")
    except urllib.error.HTTPError as exc:
        facts = {"error": f"SEC companyfacts failed with HTTP {exc.code}"}
    time.sleep(0.15)

    try:
        submissions = _fetch_json(f"{_SUBMISSIONS_API}/CIK{cik}.json")
    except urllib.error.HTTPError as exc:
        submissions = {"error": f"SEC submissions failed with HTTP {exc.code}"}
    time.sleep(0.15)

    recent_filings: list[dict[str, Any]] = []
    filings = submissions.get("filings", {})
    recent = filings.get("recent", {}) if isinstance(filings, dict) else {}
    if recent:
        forms = recent.get("form", [])
        dates = recent.get("filingDate", [])
        accs = recent.get("accessionNumber", [])
        for form, date_str, acc in zip(forms[:10], dates[:10], accs[:10]):
            acc_no_dashes = acc.replace("-", "")
            filing_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_no_dashes}/{acc}-index.html"
            recent_filings.append(
                {
                    "form": form,
                    "filing_date": date_str,
                    "accession_number": acc,
                    "url": filing_url,
                }
            )

    sources = [
        {
            "title": f"SEC Company Facts: {ticker}",
            "url": f"{_COMPANYFACTS_API}/CIK{cik}.json",
            "source_type": "SEC EDGAR",
            "document_date": None,
            "access_date": access_date,
            "reliability": "primary_regulatory",
        },
        {
            "title": f"SEC Submissions: {ticker}",
            "url": f"{_SUBMISSIONS_API}/CIK{cik}.json",
            "source_type": "SEC EDGAR",
            "document_date": None,
            "access_date": access_date,
            "reliability": "primary_regulatory",
        },
    ]

    return {
        "cik": cik,
        "company_facts": facts,
        "recent_filings": recent_filings,
        "sources": sources,
    }
