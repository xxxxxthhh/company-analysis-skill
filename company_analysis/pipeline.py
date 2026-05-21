"""End-to-end report generation skeleton.

v0.1 goal: define the public interface and quality gates. Connectors are kept
small and replaceable; paid data providers should be optional adapters.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from .analysts.quality_gate import validate_report_payload
from .connectors import fetch_earnings_calendar, fetch_news, fetch_sec_data, fetch_yahoo_data
from .metric_packs import load_metric_pack
from .peers import build_peer_table


def collect_raw_data(ticker: str) -> dict[str, Any]:
    """Collect public-first raw data from multiple connectors.

    This function returns a transparent raw-data object with full provenance.
    Never store only LLM summaries; keep source URLs and access dates.
    """
    access_date = str(date.today())

    sec_data = fetch_sec_data(ticker)
    yahoo_data = fetch_yahoo_data(ticker)
    news_data = fetch_news(ticker)
    earnings_data = fetch_earnings_calendar(ticker)

    # Merge all sources for traceability
    all_sources = []
    all_sources.extend(sec_data.get("sources", []))
    all_sources.extend(yahoo_data.get("sources", []))
    all_sources.extend(news_data.get("sources", []))
    all_sources.extend(earnings_data.get("sources", []))

    return {
        "ticker": ticker,
        "access_date": access_date,
        "sec": {
            "cik": sec_data.get("cik"),
            "company_facts": sec_data.get("company_facts", {}),
            "recent_filings": sec_data.get("recent_filings", []),
        },
        "market": {
            "summary": yahoo_data.get("summary", {}),
            "financials": yahoo_data.get("financials", {}),
            "income_statement": yahoo_data.get("income_statement", {}),
            "balance_sheet": yahoo_data.get("balance_sheet", {}),
            "cash_flow": yahoo_data.get("cash_flow", {}),
            "earnings_history": yahoo_data.get("earnings_history", {}),
            "price_history": yahoo_data.get("price_history", {}),
        },
        "news": news_data.get("items", []),
        "earnings_calendar": {
            "next_date": earnings_data.get("calendar", {}).get("next_earnings_date"),
            "history": earnings_data.get("earnings_history", []),
            "consensus": {
                "eps_average": earnings_data.get("calendar", {}).get("earnings_average"),
                "eps_low": earnings_data.get("calendar", {}).get("earnings_low"),
                "eps_high": earnings_data.get("calendar", {}).get("earnings_high"),
                "revenue_average": earnings_data.get("calendar", {}).get("revenue_average"),
                "revenue_low": earnings_data.get("calendar", {}).get("revenue_low"),
                "revenue_high": earnings_data.get("calendar", {}).get("revenue_high"),
            },
        },
        "sources": all_sources,
    }


def generate_report_bundle(ticker: str, industry: str, output_dir: Path, allow_placeholder: bool = False) -> dict[str, str]:
    raw_data = collect_raw_data(ticker)
    pack = load_metric_pack(industry)
    analysis = pack.analyze(raw_data)
    peer_table = build_peer_table(ticker)

    payload = {
        "ticker": ticker,
        "industry": industry,
        "raw_data": raw_data,
        "analysis": analysis,
        "peer_table": peer_table,
        "generated_at": str(date.today()),
    }

    validate_report_payload(payload, allow_placeholder=allow_placeholder)

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{ticker}_{date.today().isoformat()}"
    data_path = output_dir / f"{stem}_data.json"
    summary_path = output_dir / f"{stem}_executive_summary.md"
    report_path = output_dir / f"{stem}_full_report.md"

    data_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    summary_path.write_text(render_executive_summary(payload))
    report_path.write_text(render_full_report(payload))

    return {
        "data": str(data_path),
        "executive_summary": str(summary_path),
        "full_report": str(report_path),
    }


def render_executive_summary(payload: dict[str, Any]) -> str:
    analysis = payload["analysis"]
    triggers = analysis.get("falsification_triggers", [])
    risks = analysis.get("bear_case", [])
    contradictions = analysis.get("contradictions", [])
    key_metrics = analysis.get("key_metrics", [])
    ticker = payload["ticker"]

    # Key metrics snapshot
    metrics_lines = []
    for m in key_metrics[:10]:
        val = m.get("value")
        name = m.get("name", "")
        if val is not None:
            if isinstance(val, float):
                val_str = f"{val:.3f}"
            else:
                val_str = str(val)
            metrics_lines.append(f"- **{name}**: {val_str}")

    return f"""# Executive Summary: {ticker}

Generated: {payload['generated_at']}  
Industry pack: {payload['industry']}

## Investment Thesis

TODO: one-sentence thesis after deeper analysis.

## Key Metrics Snapshot

{chr(10).join(metrics_lines) or '- Data collection in progress.'}

## Key Contradictions / Alpha Hooks

{_bullet_titles(contradictions) or '- No contradictions detected with available data.'}

## Key Risks

{_bullet_titles(risks) or '- TODO: bear case required.'}

## Falsification Triggers

{_bullets(triggers) or '- TODO: at least two required.'}
"""


def render_full_report(payload: dict[str, Any]) -> str:
    analysis = payload["analysis"]
    peer_table = payload.get("peer_table", {})
    ticker = payload["ticker"]

    # Build peer table markdown
    peer_md = _render_peer_table(peer_table)

    # Build key metrics section
    metrics_md = _render_key_metrics(analysis.get("key_metrics", []))

    # Build contradictions section
    contradictions_md = _render_contradictions(analysis.get("contradictions", []))

    # Build bear case section
    bear_md = _render_bear_case(analysis.get("bear_case", []))

    # Build falsification triggers
    triggers = analysis.get("falsification_triggers", [])
    triggers_md = _bullets(triggers) or "- TODO"

    return f"""# Full Company Report: {ticker}

Generated: {payload['generated_at']}

## Executive Summary

See companion executive summary file.

## Key Metrics

{metrics_md}

## Peer Comparison

{peer_md}

## Contradiction Hunting

{contradictions_md}

## Bear Case and Falsification Triggers

### Bear Case

{bear_md}

### Falsification Triggers

{triggers_md}

## So What / Alpha View

Every data section must answer:

1. What does this mean?
2. What if this interpretation is wrong?
3. Where is the market consensus likely wrong?

## Company Overview

TODO: populate from SEC company facts and news analysis.

## Industry and Competition

TODO: add industry pack-specific analysis.

## Financial Analysis

TODO: deep-dive into SEC filings and financial trends.

## Management Track Record

TODO: compare guidance, capital allocation, buybacks/M&A, and actual outcomes.

## Valuation

TODO: DCF / comparable / precedent analysis.

## Appendix: Sources and Raw Data

See companion JSON payload for full source provenance.
"""


def _render_key_metrics(metrics: list[dict[str, Any]]) -> str:
    if not metrics:
        return "No metrics extracted from data sources."
    lines = []
    for m in metrics:
        val = m.get("value")
        name = m.get("name", "")
        unit = m.get("unit", "")
        period = m.get("period", "")
        if val is not None:
            if isinstance(val, float):
                val_str = f"{val:.3f}"
            else:
                val_str = str(val)
            lines.append(f"- **{name}** ({period}, {unit}): {val_str}")
    return "\n".join(lines)


def _render_peer_table(peer_table: dict[str, Any]) -> str:
    subject = peer_table.get("subject", {})
    peers = peer_table.get("peers", [])
    rationale = peer_table.get("rationale", "")
    missing = peer_table.get("missing_peers", [])

    if not peers:
        return "No peer mapping available. Add ticker to peers/manifest.json."

    # Comparable fields
    fields = [
        ("ticker", "Ticker"),
        ("market_cap", "Market Cap"),
        ("trailing_pe", "Trailing P/E"),
        ("forward_pe", "Forward P/E"),
        ("price_to_sales", "P/S"),
        ("price_to_book", "P/B"),
        ("ev_ebitda", "EV/EBITDA"),
        ("beta", "Beta"),
        ("revenue_growth", "Rev Growth"),
        ("profit_margins", "Profit Margin"),
        ("operating_margins", "Op Margin"),
        ("return_on_equity", "ROE"),
        ("debt_to_equity", "D/E"),
        ("current_ratio", "Current Ratio"),
    ]

    lines = []
    if rationale:
        lines.append(f"> **Rationale**: {rationale}")
        lines.append("")

    # Warning if peer data couldn't be fetched
    if missing:
        lines.append(f"> ⚠️ **Note**: Peer data for {', '.join(missing)} could not be fetched (Yahoo Finance API limit).")
        lines.append("")

    # Header
    header = " | ".join(label for _, label in fields)
    lines.append(f"| {header} |")
    lines.append("|" + "|".join([" --- " for _ in fields]) + "|")

    # Subject row (bold ticker)
    row = []
    for key, _ in fields:
        v = subject.get(key)
        if v is None:
            row.append("N/A")
        elif isinstance(v, float):
            row.append(f"{v:.2f}")
        else:
            row.append(str(v))
    # Bold the ticker cell
    row[0] = f"**{row[0]}**"
    lines.append(f"| {' | '.join(row)} |")

    # Peer rows
    for peer in peers:
        row = []
        for key, _ in fields:
            v = peer.get(key)
            if v is None:
                row.append("N/A")
            elif isinstance(v, float):
                row.append(f"{v:.2f}")
            else:
                row.append(str(v))
        lines.append(f"| {' | '.join(row)} |")

    return "\n".join(lines)


def _render_contradictions(contradictions: list[dict[str, Any]]) -> str:
    if not contradictions:
        return "No contradictions detected with available data."
    lines = []
    for c in contradictions:
        title = c.get("title", "")
        obs = c.get("observation", "")
        so_what = c.get("so_what", "")
        risk = c.get("risk_if_wrong", "")
        confidence = c.get("confidence", "medium")
        lines.append(f"### {title}")
        lines.append(f"- **Observation**: {obs}")
        lines.append(f"- **So What**: {so_what}")
        lines.append(f"- **Risk If Wrong**: {risk}")
        lines.append(f"- **Confidence**: {confidence}")
        lines.append("")
    return "\n".join(lines)


def _render_bear_case(bear_cases: list[dict[str, Any]]) -> str:
    if not bear_cases:
        return "TODO: populate bear case from contradiction analysis and qualitative risks."
    lines = []
    for b in bear_cases:
        title = b.get("title", "")
        obs = b.get("observation", "")
        so_what = b.get("so_what", "")
        risk = b.get("risk_if_wrong", "")
        lines.append(f"- **{title}**: {obs} | So what: {so_what} | Risk if wrong: {risk}")
    return "\n".join(lines)


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {x}" for x in items)


def _bullet_titles(items: list[dict[str, Any]]) -> str:
    return "\n".join(f"- {x.get('title') or x.get('observation') or x}" for x in items)
