"""Peer comparison module.

Loads curated peer manifest, fetches summary stats for peers,
and produces a raw comparable table.
"""
from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Any


_MANIFEST_PATH = Path(__file__).parent.parent.parent / "peers" / "manifest.json"


def _yf_summary(ticker: str) -> dict[str, Any]:
    """Fetch Yahoo Finance summary for a single ticker."""
    url = (
        f"https://query1.finance.yahoo.com/v10/finance/"
        f"quoteSummary/{ticker}?modules=summaryDetail,defaultKeyStatistics"
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
            summary = result.get("summaryDetail", {})
            stats = result.get("defaultKeyStatistics", {})
            return {**summary, **stats}
    except Exception:
        return {}


def _extract_peer_row(raw: dict[str, Any], ticker: str) -> dict[str, Any]:
    """Extract comparable fields from Yahoo summary."""
    def _raw(key: str) -> Any:
        v = raw.get(key)
        if isinstance(v, dict) and "raw" in v:
            return v["raw"]
        return v

    return {
        "ticker": ticker,
        "market_cap": _raw("marketCap"),
        "trailing_pe": _raw("trailingPE"),
        "forward_pe": _raw("forwardPE"),
        "price_to_sales": _raw("priceToSalesTrailing12Months"),
        "price_to_book": _raw("priceToBook"),
        "ev_ebitda": _raw("enterpriseToEbitda"),
        "beta": _raw("beta"),
        "dividend_yield": _raw("dividendYield"),
        "revenue_growth": _raw("revenueGrowth"),
        "profit_margins": _raw("profitMargins"),
        "operating_margins": _raw("operatingMargins"),
        "return_on_equity": _raw("returnOnEquity"),
        "debt_to_equity": _raw("debtToEquity"),
        "current_ratio": _raw("currentRatio"),
        "quick_ratio": _raw("quickRatio"),
        "total_cash": _raw("totalCash"),
        "total_debt": _raw("totalDebt"),
        "shares_outstanding": _raw("sharesOutstanding"),
        "float_shares": _raw("floatShares"),
        "held_by_insiders": _raw("heldPercentInsiders"),
        "held_by_institutions": _raw("heldPercentInstitutions"),
    }


def load_manifest() -> dict[str, Any]:
    """Load the curated peer manifest."""
    if not _MANIFEST_PATH.exists():
        return {}
    return json.loads(_MANIFEST_PATH.read_text())


def get_peers_for(ticker: str) -> dict[str, Any]:
    """Return peer group info for a ticker."""
    manifest = load_manifest()
    return manifest.get(ticker.upper(), {})


def build_peer_table(ticker: str) -> dict[str, Any]:
    """Build a raw comparable table for a ticker and its peers.

    Returns:
        {
            "subject": {...},
            "peers": [{...}, ...],
            "rationale": "...",
            "missing_peers": ["..."],
        }
    """
    info = get_peers_for(ticker)
    if not info:
        return {
            "subject": _extract_peer_row(_yf_summary(ticker), ticker),
            "peers": [],
            "rationale": "No curated peer mapping found. Add to peers/manifest.json.",
            "missing_peers": [],
        }

    peers = info.get("peers", [])
    rationale = info.get("rationale", "")

    subject = _extract_peer_row(_yf_summary(ticker), ticker)
    peer_rows = []
    missing = []

    for peer in peers:
        raw = _yf_summary(peer)
        if not raw:
            missing.append(peer)
            # Still include peer with N/A values so table structure is visible
            peer_rows.append(_extract_peer_row({}, peer))
            continue
        peer_rows.append(_extract_peer_row(raw, peer))

    return {
        "subject": subject,
        "peers": peer_rows,
        "rationale": rationale,
        "missing_peers": missing,
    }
