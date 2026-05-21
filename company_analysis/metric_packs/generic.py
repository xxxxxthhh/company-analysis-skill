"""Metric pack: generic.

Extracts fundamental metrics from public connector data (Yahoo Finance + SEC)
and feeds them into the contradiction hunter. Works for any ticker with
standard financial statements.

SEC company facts (XBRL) are prioritized over Yahoo Finance because they are
primary regulatory filings. Yahoo Finance is used as fallback and for market
multiples.
"""
from __future__ import annotations

from datetime import date
from typing import Any

from company_analysis.analysts.contradiction_hunter import find_contradictions

KEY_METRICS = "Revenue growth, margin trend, FCF quality, leverage, dilution, valuation"


def _get(data: dict[str, Any], *path: str) -> Any:
    """Safely navigate nested dict; Yahoo returns {raw: N, fmt: '...'} structs."""
    node = data
    for key in path:
        if not isinstance(node, dict):
            return None
        node = node.get(key)
        if node is None:
            return None
    # Yahoo Finance wraps numbers in {"raw": N, "fmt": "..."}
    if isinstance(node, dict) and "raw" in node:
        return node["raw"]
    return node


# ── SEC XBRL helpers ────────────────────────────────────────────────────────

def _sec_latest(facts: dict[str, Any], tag: str) -> float | None:
    """Get the most recent value for a US-GAAP XBRL tag from SEC company facts."""
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    if tag not in us_gaap:
        return None
    units = us_gaap[tag].get("units", {})
    for unit_name, values in units.items():
        if not values:
            continue
        # Sort by filed date descending, take latest
        sorted_vals = sorted(values, key=lambda x: x.get("filed", ""), reverse=True)
        latest = sorted_vals[0]
        return latest.get("val")
    return None


def _sec_history(facts: dict[str, Any], tag: str, periods: int = 2) -> list[dict[str, Any]]:
    """Get recent history for a US-GAAP tag, newest first."""
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    if tag not in us_gaap:
        return []
    units = us_gaap[tag].get("units", {})
    for _unit_name, values in units.items():
        if not values:
            continue
        sorted_vals = sorted(values, key=lambda x: x.get("filed", ""), reverse=True)
        return sorted_vals[:periods]
    return []


def _duration_days(entry: dict[str, Any]) -> int | None:
    """Return statement duration in days when start/end are available."""
    try:
        start = date.fromisoformat(entry.get("start", ""))
        end = date.fromisoformat(entry.get("end", ""))
        return (end - start).days
    except ValueError:
        return None


def _sec_annual_history(facts: dict[str, Any], tag: str, periods: int = 2) -> list[dict[str, Any]]:
    """Get annual 10-K values, newest first, avoiding mixed QTD/YTD comparisons.

    SEC companyfacts often includes multiple entries filed on the same date: QTD,
    YTD, restated annuals, and instant values. For growth/margin calculations,
    mixing a quarter with a year creates false signals. Prefer 10-K/FY entries
    with roughly annual durations and dedupe by fiscal year/end date.
    """
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    if tag not in us_gaap:
        return []

    candidates: list[dict[str, Any]] = []
    for _unit_name, values in us_gaap[tag].get("units", {}).items():
        for entry in values:
            duration = _duration_days(entry)
            if entry.get("form") == "10-K" and entry.get("fp") == "FY" and duration and 300 <= duration <= 400:
                candidates.append(entry)

    # Dedupe restatements / duplicate frames by fiscal year + period end. Keep
    # the newest filing for each fiscal-year/end combination.
    deduped: dict[tuple[Any, Any], dict[str, Any]] = {}
    for entry in candidates:
        key = (entry.get("fy"), entry.get("end"))
        if key not in deduped or entry.get("filed", "") > deduped[key].get("filed", ""):
            deduped[key] = entry

    sorted_vals = sorted(deduped.values(), key=lambda x: (x.get("end", ""), x.get("filed", "")), reverse=True)
    return sorted_vals[:periods]


# ── Metric extractors ───────────────────────────────────────────────────────

def _extract_sec_income_metrics(sec_facts: dict[str, Any]) -> dict[str, Any]:
    """Extract annual income statement metrics from SEC XBRL.

    Use annual 10-K values to avoid false comparisons between QTD/YTD and FY
    periods. Names keep the original public interface, but period metadata below
    marks them as annual.
    """
    rev_history = _sec_annual_history(sec_facts, "RevenueFromContractWithCustomerExcludingAssessedTax", 2)
    if len(rev_history) < 2:
        rev_history = _sec_annual_history(sec_facts, "Revenues", 2)
    gp_history = _sec_annual_history(sec_facts, "GrossProfit", 2)
    oi_history = _sec_annual_history(sec_facts, "OperatingIncomeLoss", 2)

    revenue = rev_history[0].get("val") if rev_history else None
    prior_revenue = rev_history[1].get("val") if len(rev_history) > 1 else None
    gross_profit = gp_history[0].get("val") if gp_history else None
    prior_gross_profit = gp_history[1].get("val") if len(gp_history) > 1 else None
    operating_income = oi_history[0].get("val") if oi_history else None
    prior_operating_income = oi_history[1].get("val") if len(oi_history) > 1 else None

    revenue_growth = None
    if revenue and prior_revenue and prior_revenue != 0:
        revenue_growth = (revenue - prior_revenue) / abs(prior_revenue)

    gross_margin = gross_profit / revenue if revenue and gross_profit is not None else None
    operating_margin = operating_income / revenue if revenue and operating_income is not None else None

    gross_margin_prior = None
    if prior_revenue and prior_gross_profit is not None:
        gross_margin_prior = prior_gross_profit / prior_revenue
    operating_margin_prior = None
    if prior_revenue and prior_operating_income is not None:
        operating_margin_prior = prior_operating_income / prior_revenue

    gross_margin_change = None
    operating_margin_change = None
    if gross_margin is not None and gross_margin_prior is not None:
        gross_margin_change = gross_margin - gross_margin_prior
    if operating_margin is not None and operating_margin_prior is not None:
        operating_margin_change = operating_margin - operating_margin_prior

    return {
        "revenue_growth_yoy": revenue_growth,
        "gross_margin_ttm": gross_margin,
        "operating_margin_ttm": operating_margin,
        "gross_margin_change_yoy": gross_margin_change,
        "operating_margin_change_yoy": operating_margin_change,
    }


def _extract_sec_cashflow_metrics(sec_facts: dict[str, Any]) -> dict[str, Any]:
    """Extract annual cash flow metrics from SEC XBRL."""
    ocf_history = _sec_annual_history(sec_facts, "NetCashProvidedByUsedInOperatingActivities", 2)
    capex_history = _sec_annual_history(sec_facts, "PaymentsToAcquirePropertyPlantAndEquipment", 2)
    sbc_history = _sec_annual_history(sec_facts, "ShareBasedCompensation", 1)

    ocf = ocf_history[0].get("val") if ocf_history else None
    capex = capex_history[0].get("val") if capex_history else None
    fcf = ocf - abs(capex) if ocf is not None and capex is not None else None

    fcf_prior = None
    if len(ocf_history) >= 2 and len(capex_history) >= 2:
        ocf_prior = ocf_history[1].get("val")
        capex_prior = capex_history[1].get("val")
        if ocf_prior is not None and capex_prior is not None:
            fcf_prior = ocf_prior - abs(capex_prior)

    sbc = sbc_history[0].get("val") if sbc_history else None

    return {
        "fcf_ttm": fcf,
        "fcf_prior": fcf_prior,
        "fcf_margin_ttm": None,
        "fcf_margin_change_yoy": None,
        "sbc_ttm": sbc,
        "sbc_as_revenue": None,
    }


def _extract_sec_balance_metrics(sec_facts: dict[str, Any]) -> dict[str, Any]:
    """Extract balance sheet metrics from SEC XBRL."""
    total_debt = _sec_latest(sec_facts, "LongTermDebtAndCapitalLeaseObligations")
    if total_debt is None:
        total_debt = _sec_latest(sec_facts, "LongTermDebtNoncurrent")

    total_equity = _sec_latest(sec_facts, "StockholdersEquity")
    if total_equity is None:
        total_equity = _sec_latest(sec_facts, "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest")

    debt_to_equity = None
    if total_debt and total_equity and total_equity != 0:
        debt_to_equity = total_debt / total_equity

    cash = _sec_latest(sec_facts, "CashAndCashEquivalentsAtCarryingValue")
    if cash is None:
        cash = _sec_latest(sec_facts, "CashCashEquivalentsAndShortTermInvestments")

    current_assets = _sec_latest(sec_facts, "AssetsCurrent")
    current_liabilities = _sec_latest(sec_facts, "LiabilitiesCurrent")
    current_ratio = None
    if current_assets and current_liabilities and current_liabilities != 0:
        current_ratio = current_assets / current_liabilities

    return {
        "debt_to_equity": debt_to_equity,
        "current_ratio": current_ratio,
        "cash": cash,
    }


# ── Yahoo fallback extractors (kept for reference) ──────────────────────────

def _extract_yahoo_income_metrics(income_stmt: dict[str, Any]) -> dict[str, Any]:
    history = income_stmt.get("incomeStatementHistory", [])
    if not history or len(history) < 2:
        return {}
    ttm = history[0].get("incomeStatementHistory", [{}])[0]
    prior = history[1].get("incomeStatementHistory", [{}])[0] if len(history) > 1 else {}
    total_revenue_ttm = _get(ttm, "totalRevenue")
    total_revenue_prior = _get(prior, "totalRevenue")
    revenue_growth = None
    if total_revenue_ttm and total_revenue_prior and total_revenue_prior != 0:
        revenue_growth = (total_revenue_ttm - total_revenue_prior) / abs(total_revenue_prior)
    # ... (truncated for brevity, not used when SEC data available)
    return {"revenue_growth_yoy": revenue_growth}


def _extract_yahoo_summary_metrics(summary: dict[str, Any]) -> dict[str, Any]:
    pe = _get(summary, "trailingPE")
    forward_pe = _get(summary, "forwardPE")
    ps = _get(summary, "priceToSalesTrailing12Months")
    pb = _get(summary, "priceToBook")
    ev_ebitda = _get(summary, "enterpriseToEbitda")
    market_cap = _get(summary, "marketCap")
    beta = _get(summary, "beta")
    return {
        "pe_trailing": pe,
        "pe_forward": forward_pe,
        "price_to_sales": ps,
        "price_to_book": pb,
        "ev_to_ebitda": ev_ebitda,
        "market_cap": market_cap,
        "beta": beta,
    }


# ── Main analyze function ───────────────────────────────────────────────────

def analyze(raw_data: dict[str, Any]) -> dict[str, Any]:
    market = raw_data.get("market", {})
    sec = raw_data.get("sec", {})
    sec_facts = sec.get("company_facts", {})
    summary = market.get("summary", {})

    # Try SEC XBRL first (primary source), then Yahoo fallback
    if sec_facts and sec_facts.get("facts"):
        income_metrics = _extract_sec_income_metrics(sec_facts)
        cash_metrics = _extract_sec_cashflow_metrics(sec_facts)
        balance_metrics = _extract_sec_balance_metrics(sec_facts)
    else:
        income_stmt = market.get("income_statement", {})
        cash = market.get("cash_flow", {})
        balance = market.get("balance_sheet", {})
        income_metrics = _extract_yahoo_income_metrics(income_stmt)
        cash_metrics = {}  # Yahoo cash flow extraction omitted for brevity
        balance_metrics = {}  # Yahoo balance extraction omitted for brevity

    summary_metrics = _extract_yahoo_summary_metrics(summary)

    # Cross-link: need annual revenue for FCF margin and SBC %.
    revenue = None
    prior_revenue = None
    if sec_facts:
        rev_history = _sec_annual_history(sec_facts, "RevenueFromContractWithCustomerExcludingAssessedTax", 2)
        if len(rev_history) < 2:
            rev_history = _sec_annual_history(sec_facts, "Revenues", 2)
        revenue = rev_history[0].get("val") if rev_history else None
        prior_revenue = rev_history[1].get("val") if len(rev_history) > 1 else None
    if revenue is None:
        income_history = market.get("income_statement", {}).get("incomeStatementHistory", [])
        if income_history:
            ttm_stmt = income_history[0].get("incomeStatementHistory", [{}])[0]
            revenue = _get(ttm_stmt, "totalRevenue")

    if revenue and revenue != 0:
        if cash_metrics.get("fcf_ttm") is not None:
            cash_metrics["fcf_margin_ttm"] = cash_metrics["fcf_ttm"] / revenue
        if cash_metrics.get("fcf_prior") is not None and prior_revenue:
            fcf_margin_prior = cash_metrics["fcf_prior"] / prior_revenue
            if cash_metrics.get("fcf_margin_ttm") is not None:
                cash_metrics["fcf_margin_change_yoy"] = cash_metrics["fcf_margin_ttm"] - fcf_margin_prior
        if cash_metrics.get("sbc_ttm") is not None:
            cash_metrics["sbc_as_revenue"] = cash_metrics["sbc_ttm"] / revenue

    normalized_metrics = {
        **income_metrics,
        **cash_metrics,
        **balance_metrics,
        **summary_metrics,
    }

    contradictions = find_contradictions(normalized_metrics)

    # Build key_metrics list for report rendering.
    ratio_metrics = {
        "pe_trailing", "pe_forward", "price_to_sales", "price_to_book",
        "ev_to_ebitda", "beta", "debt_to_equity", "sbc_as_revenue",
    }
    key_metrics = []
    for name, value in normalized_metrics.items():
        if value is not None:
            is_ratio = "margin" in name or "growth" in name or "ratio" in name or name in ratio_metrics
            key_metrics.append({
                "name": name,
                "value": value,
                "period": "Annual / latest filing",
                "unit": "ratio" if is_ratio else "USD",
                "source": {"source_type": "SEC EDGAR / Yahoo Finance", "url": f"https://finance.yahoo.com/quote/{raw_data.get('ticker')}"},
                "so_what": "Use this metric to test business quality, cash conversion, balance-sheet risk, or market expectations.",
                "risk_if_wrong": "If the metric is distorted by period mixing, restatement, one-off working capital, or missing data, the derived thesis may be unreliable.",
            })

    # Generate bear case and falsification triggers
    bear_case = []
    falsification_triggers = []

    if not contradictions:
        bear_case.append({
            "title": "Placeholder bear case",
            "observation": "No contradictions detected with available data.",
            "so_what": "This may mean the company is executing cleanly, or data coverage is insufficient to surface risks.",
            "risk_if_wrong": "If material risks exist but aren't captured in standard financials, the analysis will be incomplete.",
            "confidence": "low",
        })
        falsification_triggers.append("Revenue growth decelerates below 10% for two consecutive quarters")
        falsification_triggers.append("Operating margin contracts by >200bps in a single quarter")
    else:
        for c in contradictions:
            bear_case.append({
                "title": f"Bear case: {c['title']}",
                "observation": c["observation"],
                "so_what": c["so_what"],
                "risk_if_wrong": c["risk_if_wrong"],
                "confidence": c.get("confidence", "medium"),
            })
        falsification_triggers.append("FCF margin continues to decline despite revenue growth >20%")
        falsification_triggers.append("Gross margin expansion stalls while opex accelerates")

    while len(falsification_triggers) < 2:
        falsification_triggers.append("Management guidance miss on next earnings call")

    missing_data = []
    if not sec_facts or not sec_facts.get("facts"):
        missing_data.append("SEC company facts unavailable")
    if not summary:
        missing_data.append("Yahoo Finance summary unavailable (market multiples may be missing)")

    return {
        "industry": "generic",
        "company": {"ticker": raw_data.get("ticker")},
        "key_metric_definitions": KEY_METRICS,
        "key_metrics": key_metrics,
        "insights": [],
        "contradictions": contradictions,
        "bear_case": bear_case,
        "falsification_triggers": falsification_triggers,
        "missing_data": missing_data,
    }
