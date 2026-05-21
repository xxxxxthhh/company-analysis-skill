"""Earnings calendar connector (stdlib-only).

Fetches upcoming and past earnings dates via Yahoo Finance API.
Critical for Theta Gang / options catalyst tracking.
"""
from __future__ import annotations

import json
import urllib.request
from datetime import datetime
from typing import Any


def fetch_earnings_calendar(ticker: str) -> dict[str, Any]:
    """Return earnings calendar data with provenance.

    Returns:
        {
            "earnings_date": "YYYY-MM-DD" or None,
            "earnings_history": [{"date": "...", "eps_actual": ..., "eps_estimate": ...}],
            "sources": [...],
        }
    """
    # Yahoo Finance calendar module
    url = (
        f"https://query1.finance.yahoo.com/v10/finance/"
        f"quoteSummary/{ticker}?modules=calendarEvents,earningsHistory"
    )
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; company-analysis-skill/0.1)",
        },
    )

    calendar = {}
    history = []
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            result = data.get("quoteSummary", {}).get("result", [{}])[0]

            cal = result.get("calendarEvents", {})
            earnings = cal.get("earnings", {})
            if earnings:
                earnings_date = earnings.get("earningsDate", [])
                if earnings_date:
                    # Yahoo returns epoch ms
                    ts = earnings_date[0].get("raw")
                    if ts:
                        calendar["next_earnings_date"] = datetime.utcfromtimestamp(ts).strftime("%Y-%m-%d")
                    else:
                        calendar["next_earnings_date"] = None
                else:
                    calendar["next_earnings_date"] = None
                calendar["earnings_average"] = earnings.get("earningsAverage", {}).get("raw")
                calendar["earnings_low"] = earnings.get("earningsLow", {}).get("raw")
                calendar["earnings_high"] = earnings.get("earningsHigh", {}).get("raw")
                calendar["revenue_average"] = earnings.get("revenueAverage", {}).get("raw")
                calendar["revenue_low"] = earnings.get("revenueLow", {}).get("raw")
                calendar["revenue_high"] = earnings.get("revenueHigh", {}).get("raw")

            hist = result.get("earningsHistory", {}).get("history", [])
            for entry in hist:
                history.append({
                    "date": entry.get("quarter", {}).get("fmt"),
                    "eps_actual": entry.get("epsActual", {}).get("raw"),
                    "eps_estimate": entry.get("epsEstimate", {}).get("raw"),
                    "eps_difference": entry.get("epsDifference", {}).get("raw"),
                    "surprise_percent": entry.get("surprisePercent", {}).get("raw"),
                })
    except Exception:
        pass

    sources = [
        {
            "title": f"Yahoo Finance Earnings Calendar: {ticker}",
            "url": f"https://finance.yahoo.com/quote/{ticker}/calendar/",
            "source_type": "market_data",
            "reliability": "secondary_aggregated",
        }
    ]

    return {
        "calendar": calendar,
        "earnings_history": history,
        "sources": sources,
    }
