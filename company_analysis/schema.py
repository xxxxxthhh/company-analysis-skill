"""Shared schema conventions for company-analysis pipeline.

Keep this lightweight and stdlib-only in v0.1. Production users can replace
these TypedDicts with Pydantic models if they want stricter runtime validation.
"""
from __future__ import annotations

from typing import Any, TypedDict


class Source(TypedDict, total=False):
    title: str
    url: str
    source_type: str
    document_date: str
    access_date: str
    reliability: str


class Metric(TypedDict, total=False):
    name: str
    value: Any
    period: str
    unit: str
    source: Source
    so_what: str
    risk_if_wrong: str


class Insight(TypedDict, total=False):
    title: str
    observation: str
    so_what: str
    risk_if_wrong: str
    evidence: list[Source]
    confidence: str


class MetricPackResult(TypedDict, total=False):
    industry: str
    company: dict[str, Any]
    key_metrics: list[Metric]
    insights: list[Insight]
    contradictions: list[Insight]
    bear_case: list[Insight]
    falsification_triggers: list[str]
    missing_data: list[str]


RawData = dict[str, Any]
