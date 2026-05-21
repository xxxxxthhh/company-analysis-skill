"""Rule-based contradiction hunter.

The goal is not to be clever; it is to force the analyst to look where alpha
usually lives: data that does not fit the easy story.
"""
from __future__ import annotations

from typing import Any


def find_contradictions(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    flags: list[dict[str, Any]] = []

    revenue_growth = metrics.get("revenue_growth_yoy")
    fcf_margin_change = metrics.get("fcf_margin_change_yoy")
    gross_margin_change = metrics.get("gross_margin_change_yoy")
    operating_margin_change = metrics.get("operating_margin_change_yoy")
    sbc_as_revenue = metrics.get("sbc_as_revenue")

    if _gt(revenue_growth, 0.30) and _lt(fcf_margin_change, 0):
        flags.append(_flag(
            "High growth but deteriorating FCF margin",
            "Revenue growth is strong, but cash conversion is weakening.",
            "Growth may be lower quality than headline revenue suggests.",
            "If working-capital timing or one-off investment explains the FCF decline, this may be noise rather than thesis risk.",
        ))
    if _gt(gross_margin_change, 0) and operating_margin_change is not None and operating_margin_change <= 0:
        flags.append(_flag(
            "Gross margin up but operating leverage absent",
            "Product/unit economics improved, but operating margin did not follow.",
            "Opex intensity may be absorbing product-level gains; check sales efficiency, R&D, SBC, and restructuring.",
            "If opex is front-loaded for durable growth, the margin lag may be acceptable.",
        ))
    if _gt(sbc_as_revenue, 0.10):
        flags.append(_flag(
            "SBC dilution may offset operating progress",
            "Stock-based compensation is high relative to revenue.",
            "Per-share economics may lag company-level growth.",
            "If SBC is rapidly declining or already reflected in diluted shares, the dilution concern may be overstated.",
        ))
    return flags


def _flag(title: str, observation: str, so_what: str, risk_if_wrong: str) -> dict[str, str]:
    return {"title": title, "observation": observation, "so_what": so_what, "risk_if_wrong": risk_if_wrong, "confidence": "medium"}


def _gt(value: Any, threshold: float) -> bool:
    return isinstance(value, (int, float)) and value > threshold


def _lt(value: Any, threshold: float) -> bool:
    return isinstance(value, (int, float)) and value < threshold
