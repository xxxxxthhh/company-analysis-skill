---
name: company-analysis
description: "Use when the user gives a company name or ticker and wants deep company/equity research. Produces grounded reports with source discovery, SEC/IR review, financial analysis, competitive positioning, valuation scenarios, risks, catalysts, and a clear investment view."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [company-analysis, equity-research, sec, filings, valuation, investing]
    related_skills: [arxiv, blogwatcher, ocr-and-documents]
---

# Company Analysis

## Overview

Use this skill to analyze a public or private company deeply enough to support an investment memo, stock pitch, competitive intelligence brief, or thesis update.

The default behavior is **evidence-first**: collect official disclosures before making claims, cite sources for key numbers, separate facts from judgment, and produce a conclusion with clear risks and falsification triggers.

This is not a real-time trading signal skill. It is for fundamental research and decision support.

## When to Use

Use when the user asks for:

- “Analyze company X / ticker Y.”
- A full company report, investment memo, or stock pitch.
- Earnings preview / earnings update.
- Competitive landscape or moat analysis.
- Valuation work: DCF, comps, bull/base/bear.
- Thesis tracker, catalyst calendar, or risk review.

Do **not** use as the only source for:

- Trade execution decisions.
- Legal, tax, or accounting advice.
- Companies with material non-public information requirements.
- Reports that require proprietary data unless the user provides access.

## Output Contract

Default report order:

1. **Conclusion** — rating-style view, one-line thesis, key upside/downside.
2. **Why** — 3-5 thesis pillars with evidence.
3. **Company Overview** — business model, segments, customers, geography.
4. **Industry / Competition** — market structure, peers, moat, substitutes.
5. **Financials** — revenue, margins, FCF, ROIC, leverage, share count.
6. **Management / Filings** — MD&A, guidance, risk factors, accounting notes.
7. **Valuation** — multiples, DCF/scenarios, implied expectations.
8. **Catalysts** — what can change market perception and when.
9. **Risks / Bear Case** — thesis-breaking risks and what would prove the view wrong.
10. **Open Questions** — missing data and next checks.
11. **Sources** — citations with document date and access date.

For shorter requests, compress but keep: conclusion, evidence, valuation/risk, sources.


## Alpha / So What Enforcement

A report is not useful because it is complete; it is useful because it explains what matters and where consensus may be wrong. Enforce these rules:

- Every major data section must include **So What** and **What If Wrong**.
- Hunt contradictions: growth vs FCF, gross margin vs operating margin, management guidance vs actual delivery, reported earnings vs per-share dilution.
- Time series beats snapshot. Show trend, inflection, and deterioration/improvement.
- Compare management words with actions: guidance hit rate, capital allocation, buybacks, M&A, dilution.
- State current market consensus and how the report differs. No differentiated view means no alpha claim.
- Missing bear case or fewer than two falsification triggers should block final publication.

## v0.1 Industry Metric Pack Priority

Prioritize packs most relevant to the user workflow:

1. **SaaS / Cloud:** ARR, NRR/GRR, RPO, CAC payback, Rule of 40, SBC.
2. **Fintech / Crypto Infrastructure:** transaction volume, take rate, AUM/assets, users, custody/regulatory exposure.
3. **Software / Platform:** subscription migration, ecosystem lock-in, operating leverage, ROIC, capital return.
4. **Banks:** NIM, deposits, CET1, ROE, provisions, reserve coverage.
5. **E-commerce / Consumer:** GMV, take rate, active buyers, AOV, fulfillment cost, retention.
6. **Semiconductors:** inventory, gross margin cycle, design wins, customer concentration, supply/node/capex cycle.

Defer biotech and energy unless explicitly requested.

## Research Workflow

### 1. Resolve the company

Identify:

- Legal name, ticker, exchange, CIK if US-listed.
- Fiscal year-end and reporting currency.
- Industry / GICS / peer group.
- Latest available reporting period.

If ambiguous, list candidates and choose the most likely based on user context.

### 2. Collect official sources first

Priority order:

1. SEC / regulator filings: 10-K, 10-Q, 8-K, DEF 14A, S-1/F-1 when relevant.
2. Company IR: earnings release, investor presentation, annual report, webcast/transcript.
3. Exchange / regulator notices.
4. Reputable news and industry sources.
5. Social or alternative data only as weak signals.

Capture for each source:

- Title
- URL
- Document date
- Access date
- Source type
- Relevant excerpt or table reference

### 3. Build the fact base

Extract:

- Revenue by segment/product/geography where available.
- Gross margin, operating margin, net margin.
- Free cash flow and FCF conversion.
- Capex, R&D, SBC, working capital.
- Debt, cash, leases, maturities.
- Share count, dilution, buybacks/dividends.
- Customer concentration, backlog/RPO, ARR/NRR for SaaS, same-store sales for retail, etc.

Mark unavailable metrics as `unknown`; do not invent them.

### 4. Analyze the business

Answer:

- What does the company actually sell?
- Who pays, why do they buy, and why now?
- What drives volume, price, retention, and margin?
- What is cyclical vs structural?
- What could make the business better or worse over 3-5 years?

### 5. Analyze moat and competition

Evaluate:

- Switching costs
- Network effects
- Brand
- Cost advantage
- Scale economies
- Data advantage
- Distribution advantage
- Regulatory barriers
- IP / patents / technical lead

For each moat claim, state whether it is expanding, stable, or eroding.

### 6. Analyze financial quality

Look for:

- Growth durability
- Margin structure and operating leverage
- FCF quality vs accounting earnings
- ROIC and reinvestment runway
- Balance sheet resilience
- Dilution and SBC drag
- Revenue concentration or one-off items
- Accounting red flags

### 7. Valuation and expectations

Use at least two lenses when possible:

- Trading comps / historical multiple range.
- DCF or reverse DCF.
- Sum-of-the-parts for multi-segment businesses.
- Scenario table: bull / base / bear.

Always expose assumptions:

- Revenue CAGR
- Terminal margin
- Tax rate
- WACC / discount rate
- Terminal growth or exit multiple
- Net debt / cash
- Diluted share count

State what the current price implies. This is often more useful than a single target price.

### 8. Devil’s advocate

Before finalizing, write the strongest opposing case:

- What are bulls/bears probably missing?
- What evidence would invalidate the thesis?
- Which numbers are most fragile?
- What could management be over-optimistic about?
- What could the market already price in?

### 9. Final report

Prefer the user’s default structure:

- Conclusion
- Why
- Risks
- Recommended action / next checks

For investment reports, include an explicit “not financial advice” caveat only when public distribution or regulatory context makes it necessary; do not bury the analysis under boilerplate.

## Source Quality Rules

- SEC / company filings outrank news.
- Company IR claims are useful but promotional; cross-check with filings.
- News is event context, not proof of financial impact.
- Analyst consensus is an input, not truth.
- Social media is weak evidence unless measuring sentiment or product complaints.
- If a number lacks source provenance, downgrade confidence.

## Citation Style

Use compact citations:

```text
Revenue grew X% YoY to $Y in FY2025 [10-K FY2025, filed YYYY-MM-DD, URL].
Management guided to ... [Q4 FY2025 earnings release, YYYY-MM-DD, URL].
```

At the end include a source table:

| Source | Type | Date | Used for | URL |
|---|---|---:|---|---|

## Industry Metric Packs

Adjust metrics by industry:

- **SaaS:** ARR, NRR/GRR, CAC payback, Rule of 40, RPO, churn, SBC.
- **Semiconductors:** wafer supply, node, design wins, inventory, gross margin cycle, customer concentration.
- **Retail:** comps, traffic, ticket, store count, inventory turns, shrink, lease obligations.
- **Banks:** NIM, deposits, loan growth, CET1, NPLs, duration risk.
- **Insurance:** combined ratio, float, reserve development, investment yield.
- **Energy:** production, reserves, lifting cost, decline rates, commodity sensitivity.
- **Biotech:** pipeline stage, trial endpoints, cash runway, patent life, regulatory calendar.
- **Consumer internet:** MAU/DAU, ARPU, engagement, take rate, CAC, cohort retention.

If no pack fits, define the company-specific value drivers explicitly.

## Quality Gates

Before final answer, verify:

- [ ] Company identity resolved correctly.
- [ ] Latest filing period and price/market data date are stated.
- [ ] Key financial numbers have sources.
- [ ] Facts, estimates, assumptions, and judgments are separated.
- [ ] Bull/base/bear or equivalent scenario thinking is included.
- [ ] Bear case is strong, not token.
- [ ] Valuation assumptions are visible.
- [ ] Missing data is disclosed.
- [ ] Recommended next checks are actionable.

## Common Pitfalls

1. **Pretty report, weak evidence.** A professional tone is not a substitute for citations.
2. **Confusing company story with investment thesis.** A good company can be a bad stock at the wrong price.
3. **Ignoring market expectations.** The key question is often what is already priced in.
4. **Single-source dependence.** Cross-check filings, IR, and external sources.
5. **No falsification triggers.** Every thesis needs conditions that would make it wrong.
6. **Generic industry analysis.** Use industry-specific metrics and value drivers.
7. **Black-box DCF.** If assumptions are hidden, the valuation is not useful.
8. **Overweighting recent news.** Distinguish durable drivers from noise.

## One-Shot Prompt

```text
Use company-analysis. Analyze <COMPANY/TICKER>. Produce a full report with conclusion first, source-backed facts, financial trends, moat/competition, valuation scenarios, risks, catalysts, and open questions. Separate facts, assumptions, and judgment. Cite sources and state missing data.
```
