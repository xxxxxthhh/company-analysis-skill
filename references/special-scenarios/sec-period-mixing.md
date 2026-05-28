# SEC Companyfacts Period Normalization

Lesson from reviewing the company-analysis public repo: SEC `companyfacts` includes multiple facts for the same tag filed on the same date, often mixing quarterly (QTD), year-to-date (YTD), annual FY, restated annual, and instant balance-sheet values.

## Why this matters

Naively sorting facts by `filed` date and taking the first/latest value can produce false investment signals. Example failure mode:

- Latest 10-Q filing includes both QTD and YTD revenue values.
- A metric extractor compares a 6-month/YTD value to a 3-month/QTD or annual value.
- `revenue_growth_yoy` becomes a fake 100%+ growth number.
- The contradiction hunter flags “high growth but deteriorating FCF margin,” but the signal is just period-mixing noise.

## Durable rule

For income-statement and cash-flow trend metrics, do not use generic “latest filed” facts. Normalize periods first.

Preferred default for generic company reports:

1. Use annual `10-K` / `FY` facts for YoY growth, margins, FCF, SBC, and annual trend metrics.
2. Require duration sanity checks when `start`/`end` exist: roughly 300–400 days for annual periods.
3. Dedupe restatements by fiscal year + period end; keep the newest filing for that fiscal-year/end pair.
4. Sort by period end date, not just `filed` date.
5. For margin changes, use the matching prior-period denominator. Example: prior FCF margin = prior FCF / prior revenue, not prior FCF / current revenue.
6. For TTM or quarterly analysis, build explicit TTM/QoQ logic rather than reusing annual YoY names.
7. Label period metadata honestly: `Annual`, `TTM`, `QTD`, or `YTD`; do not call annual values TTM.

## Implementation sketch

```python
def _duration_days(entry):
    start = date.fromisoformat(entry["start"])
    end = date.fromisoformat(entry["end"])
    return (end - start).days


def _sec_annual_history(facts, tag, periods=2):
    candidates = []
    for unit, values in facts["facts"]["us-gaap"][tag]["units"].items():
        for entry in values:
            duration = _duration_days(entry) if entry.get("start") and entry.get("end") else None
            if entry.get("form") == "10-K" and entry.get("fp") == "FY" and duration and 300 <= duration <= 400:
                candidates.append(entry)

    deduped = {}
    for entry in candidates:
        key = (entry.get("fy"), entry.get("end"))
        if key not in deduped or entry.get("filed", "") > deduped[key].get("filed", ""):
            deduped[key] = entry

    return sorted(deduped.values(), key=lambda x: (x.get("end", ""), x.get("filed", "")), reverse=True)[:periods]
```

## Review checklist for metric-pack PRs

- [ ] Revenue growth is not calculated from mixed QTD/YTD/FY facts.
- [ ] Income statement and cash flow use matching periods.
- [ ] Prior margin uses prior denominator.
- [ ] Metric names and period labels match actual data period.
- [ ] Contradiction hunter output is inspected for false positives caused by data normalization.
- [ ] `so_what` and `risk_if_wrong` are populated for key metrics, not only narrative insights.
- [ ] Quality gates cover key metrics as first-class insight objects when they appear in reports.
