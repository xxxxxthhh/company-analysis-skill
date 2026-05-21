# Metric Pack Interface

Metric packs convert raw connector outputs into decision-useful, industry-aware analysis.

## Input

```python
raw_data = {
  "ticker": "AAPL",
  "access_date": "YYYY-MM-DD",
  "sec": {},
  "market": {},
  "news": [],
  "earnings_calendar": {},
  "sources": []
}
```

## Output

Each pack exposes:

```python
def analyze(raw_data: dict) -> dict:
    return {
      "industry": "SaaS / Cloud",
      "company": {"ticker": "..."},
      "key_metrics": [
        {
          "name": "net revenue retention",
          "value": 1.18,
          "period": "FY2025",
          "unit": "ratio",
          "source": {"title": "FY2025 10-K", "url": "..."},
          "so_what": "...",
          "risk_if_wrong": "..."
        }
      ],
      "insights": [],
      "contradictions": [],
      "bear_case": [],
      "falsification_triggers": [],
      "missing_data": []
    }
```

## Hard requirements

- Every key metric needs source provenance.
- Every insight needs `so_what` and `risk_if_wrong`.
- At least one bear case item is required.
- At least two falsification triggers are required.
- Contradictions are preferred; if none exist, explicitly explain why.

## v0.1 Priority Packs

1. SaaS / Cloud
2. Fintech / Crypto Infrastructure
3. Software / Platform
4. Banks
5. E-commerce / Consumer
6. Semiconductors

Biotech and energy are deferred to v0.2 unless the user explicitly needs them.
