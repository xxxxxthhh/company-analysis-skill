"""Yahoo Finance public data connector (stdlib-only).

Mirrors the approach in the yahoo-finance-stdlib skill: urllib + json, zero deps.
Fetches summary stats, price history, and financials via Yahoo Finance API endpoints.
"""
from __future__ import annotations

import json
import urllib.request
from typing import Any


def _yf_api(ticker: str, module: str) -> dict[str, Any]:
    url = (
        f"https://query1.finance.yahoo.com/v10/finance/"
        f"quoteSummary/{ticker}?modules={module}"
    )
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; company-analysis-skill/0.1)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            result = data.get("quoteSummary", {}).get("result", [{}])[0]
            return result.get(module, {})
    except Exception:
        return {}


def _yf_chart(ticker: str, range_: str = "1y", interval: str = "1d") -> dict[str, Any]:
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/"
        f"chart/{ticker}?range={range_}&interval={interval}"
    )
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; company-analysis-skill/0.1)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return {}


def fetch_yahoo_data(ticker: str) -> dict[str, Any]:
    """Return raw market data with provenance.

    Returns:
        {
            "summary": {...},
            "financials": {...},
            "balance_sheet": {...},
            "cash_flow": {...},
            "price_history": {...},
            "sources": [...],
        }
    """
    summary = _yf_api(ticker, "summaryDetail")
    default_stats = _yf_api(ticker, "defaultKeyStatistics")
    financials = _yf_api(ticker, "financialData")
    earnings = _yf_api(ticker, "earnings")
    income = _yf_api(ticker, "incomeStatementHistory")
    balance = _yf_api(ticker, "balanceSheetHistory")
    cash = _yf_api(ticker, "cashflowStatementHistory")
    chart = _yf_chart(ticker)

    # Merge summary with default stats for richer view
    combined_summary = {**summary, **default_stats}

    sources = [
        {
            "title": f"Yahoo Finance Summary: {ticker}",
            "url": f"https://finance.yahoo.com/quote/{ticker}",
            "source_type": "market_data",
            "reliability": "secondary_aggregated",
        },
        {
            "title": f"Yahoo Finance Chart: {ticker}",
            "url": f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}",
            "source_type": "market_data",
            "reliability": "secondary_aggregated",
        },
    ]

    return {
        "summary": combined_summary,
        "financials": financials,
        "income_statement": income,
        "balance_sheet": balance,
        "cash_flow": cash,
        "earnings_history": earnings,
        "price_history": chart,
        "sources": sources,
    }
