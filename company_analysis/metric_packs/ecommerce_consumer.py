"""Metric pack: E-commerce / Consumer."""
from __future__ import annotations

from typing import Any

from company_analysis.analysts.contradiction_hunter import find_contradictions

KEY_METRICS = "GMV, take rate, MAU/buyers, AOV, fulfillment cost, retention, inventory"


def analyze(raw_data: dict[str, Any]) -> dict[str, Any]:
    # v0.1 interface contract. Real implementations should map connector
    # outputs into normalized metric values, each with source provenance.
    normalized_metrics: dict[str, Any] = {}
    contradictions = find_contradictions(normalized_metrics)
    return {
        "industry": "E-commerce / Consumer",
        "company": {"ticker": raw_data.get("ticker")},
        "key_metric_definitions": KEY_METRICS,
        "key_metrics": [],
        "insights": [],
        "contradictions": contradictions,
        "bear_case": [],
        "falsification_triggers": [],
        "missing_data": [
            "Populate E-commerce / Consumer metrics from SEC/company IR/market data connectors",
            "Add peer comparison matrix",
            "Add management track record evidence",
        ],
    }
