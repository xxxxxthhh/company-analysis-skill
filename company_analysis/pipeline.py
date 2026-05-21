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
from .metric_packs import load_metric_pack


def collect_raw_data(ticker: str) -> dict[str, Any]:
    """Collect public-first raw data.

    This function intentionally returns a transparent raw-data object. Never
    store only LLM summaries; keep source URLs and access dates.
    """
    return {
        "ticker": ticker,
        "access_date": str(date.today()),
        "sec": {},
        "market": {},
        "news": [],
        "earnings_calendar": {},
        "sources": [],
    }


def generate_report_bundle(ticker: str, industry: str, output_dir: Path, allow_placeholder: bool = False) -> dict[str, str]:
    raw_data = collect_raw_data(ticker)
    pack = load_metric_pack(industry)
    analysis = pack.analyze(raw_data)

    payload = {
        "ticker": ticker,
        "industry": industry,
        "raw_data": raw_data,
        "analysis": analysis,
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
    return f"""# Executive Summary: {payload['ticker']}

Generated: {payload['generated_at']}  
Industry pack: {payload['industry']}

## Investment Thesis

TODO: one-sentence thesis after live data collection.

## Key Metrics Snapshot

TODO: fill from metric pack output.

## Key Contradictions / Alpha Hooks

{_bullet_titles(contradictions) or '- TODO: find at least one contradiction or explain why none was found.'}

## Key Risks

{_bullet_titles(risks) or '- TODO: bear case required.'}

## Falsification Triggers

{_bullets(triggers) or '- TODO: at least two required.'}
"""


def render_full_report(payload: dict[str, Any]) -> str:
    return f"""# Full Company Report: {payload['ticker']}

Generated: {payload['generated_at']}

## Conclusion

TODO.

## So What / Alpha View

Every data section must answer:

1. What does this mean?
2. What if this interpretation is wrong?
3. Where is the market consensus likely wrong?

## Company Overview

TODO.

## Industry and Competition

TODO.

## Financial Analysis

TODO.

## Contradiction Hunting

TODO.

## Management Track Record

TODO: compare guidance, capital allocation, buybacks/M&A, and actual outcomes.

## Valuation

TODO.

## Bear Case and Falsification Triggers

TODO.

## Appendix: Sources and Raw Data

See companion JSON payload.
"""


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {x}" for x in items)


def _bullet_titles(items: list[dict[str, Any]]) -> str:
    return "\n".join(f"- {x.get('title') or x.get('observation') or x}" for x in items)
