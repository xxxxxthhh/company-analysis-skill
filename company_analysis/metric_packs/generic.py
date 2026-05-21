"""Metric pack: generic."""
from __future__ import annotations

from typing import Any

from company_analysis.analysts.contradiction_hunter import find_contradictions

KEY_METRICS = "Revenue growth, margin trend, FCF quality, leverage, dilution, valuation"


def analyze(raw_data: dict[str, Any]) -> dict[str, Any]:
    # v0.1 interface contract. Real implementations should map connector
    # outputs into normalized metric values, each with source provenance.
    normalized_metrics: dict[str, Any] = {}
    contradictions = find_contradictions(normalized_metrics)
    return {
        "industry": "generic",
        "company": {"ticker": raw_data.get("ticker")},
        "key_metric_definitions": KEY_METRICS,
        "key_metrics": [],
        "insights": [],
        "contradictions": contradictions,
        "bear_case": [],
        "falsification_triggers": [],
        "missing_data": [
            "Populate generic metrics from SEC/company IR/market data connectors",
            "Add peer comparison matrix",
            "Add management track record evidence",
        ],
    }
