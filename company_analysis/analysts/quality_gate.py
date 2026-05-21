"""Hard quality gates for useful company reports."""
from __future__ import annotations

from typing import Any


class QualityGateError(ValueError):
    """Raised when a report is not decision-useful enough to publish."""


def validate_report_payload(payload: dict[str, Any], allow_placeholder: bool = False) -> None:
    analysis = payload.get("analysis", {})
    bear_case = analysis.get("bear_case") or []
    triggers = analysis.get("falsification_triggers") or []
    contradictions = analysis.get("contradictions") or []

    errors: list[str] = []
    if not bear_case:
        errors.append("missing bear_case")
    if len(triggers) < 2:
        errors.append("need at least two falsification_triggers")
    if not contradictions:
        errors.append("no contradictions / alpha hooks found")

    # Each insight-like object should have So What and risk-if-wrong fields.
    for section in ("insights", "contradictions", "bear_case"):
        for idx, item in enumerate(analysis.get(section) or []):
            if not item.get("so_what"):
                errors.append(f"{section}[{idx}] missing so_what")
            if not item.get("risk_if_wrong"):
                errors.append(f"{section}[{idx}] missing risk_if_wrong")

    if errors and not allow_placeholder:
        raise QualityGateError("; ".join(errors))
