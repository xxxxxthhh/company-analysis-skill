---
name: company-deep-research
description: "Deep fundamental research and analysis framework for public companies. Use when user wants to research a company, analyze business fundamentals, evaluate investment thesis, assess competitive positioning, or generate comprehensive research reports. Triggers on: 调研公司, research [company], analyze [ticker], investment thesis, 公司分析, 基本面研究, or questions about business model, competitive moat, financial health, management quality, or future outlook. Produces bilingual (中文/EN), dialectical reports with bull/bear cases and explicit risk assessment."
version: 2.0.0
author: UltraMan & BoJack
license: MIT
metadata:
  hermes:
    tags: [company-research, equity-analysis, fundamental-research, valuation, sec-filings, investment-thesis, bilingual]
    related_skills: [arxiv, blogwatcher, ocr-and-documents, youtube-content]
---

# Company Deep Research

## Overview

Systematic framework for producing **objective, dialectical, and comprehensive** company research reports. This skill absorbs the nanoclaw-company-research-core methodology — replacing the earlier linear analysis flow with a five-phase dialectical process.

**Core philosophy:** Every bull case deserves a steel-manned bear case. Every bear case deserves a steel-manned bull case. Acknowledge what you don't know. Separate facts, inferences, and opinions.

This is **not** a trading-execution skill. It supports fundamental research and decision-making. Do NOT use as the sole source for trade execution, legal advice, tax advice, or accounting decisions.

## When to Use

Use when the user asks for:
- "Analyze company X / ticker Y" → Research Report (default)
- "深入研究 CRCL" / "deep dive NVDA" → Investment Memo
- "快速看一眼 NVDA" / "pulse check AAPL" → Pulse Check
- A full company report, investment memo, or stock pitch
- Earnings preview / earnings update
- Competitive landscape or moat analysis
- Valuation work: DCF, comps, bull/base/bear
- Thesis tracker, catalyst calendar, or risk review

### Report Depth Tiers

| Tier | Trigger words | Output | Token budget | Use case |
|---|---|---|---|---|
| **Pulse Check** | 快看, quick look, pulse | ~30 lines / 2K tokens | One-sentence thesis, key numbers, 2-line bull/bear, next catalyst | Quick orientation before deeper work |
| **Research Report** | 分析, research, analyze (default) | 200-300 lines / 8K tokens | Full 10-section report with sources and quality gates | Standard company analysis |
| **Investment Memo** | 深入研究, deep dive, investment memo | 500+ lines / 15K+ tokens | Full report + detailed sensitivity analysis + full peer comps table + extended contradiction hunting | Investment decision support |

**Phase 1 (Scope Definition) sets the tier.** Do not default to deep dive unless explicitly requested. Default to Research Report.

## Five-Phase Research Workflow

### Phase 1: Scope Definition

Before starting research, clarify with user (if ambiguous):

1. **Research Depth** — Pulse Check / Research Report / Investment Memo
2. **Focus Area** — General investment thesis, specific angle, or comparative analysis
3. **Time Horizon** — Near-term catalyst (3-6 mo), medium-term (1-2 yr), long-term (3-5+ yr)
4. **Output Format** — Executive summary only / full report / investment memo style

If the user gives no guidance, default to **Research Report, general thesis, medium-term horizon**.

### Phase 2: Information Gathering

**Priority order of sources:**
1. SEC/regulator filings: 10-K, 10-Q, 8-K, DEF 14A, S-1/F-1
2. Company IR: earnings release, investor presentation, annual report, webcast transcript
3. Exchange/regulator notices
4. Reputable news and industry sources
5. Social/alternative data → only as weak signals

**Data Collection — Two Paths:**

- **Preferred path** (automated): Run `scripts/sec_xbrl_parser.py` and `scripts/yahoo_connector.py` via `execute_code` for structured SEC/Yahoo data with fiscal-year alignment. Then run `scripts/contradiction_hunter.py` for automated red-flag detection.
- **Fallback path** (manual): Use `web_search` and `browser_navigate` to SEC EDGAR and Yahoo Finance directly. Manually apply L1 hard gates from `rules/l1-hard-gate.yaml` and contradictions from `rules/contradictions/`.

Scripts are accelerators, not dependencies. If unavailable or failing, proceed with manual search — but apply the same fiscal-year alignment rules documented in `references/special-scenarios/sec-period-mixing.md`.

**Mandatory search coverage:**
- Latest 10-K/20-F (annual), recent 10-Q (quarterly)
- Earnings call transcripts (last 2-4 quarters)
- Industry: market size, TAM, growth trends
- Management: CEO track record, insider buying/selling, executive compensation
- Sentiment: short seller reports, accounting concerns, lawsuits, regulatory investigations
- Recent developments: news last 30 days, analyst rating changes, guidance outlook

**Information Quality Standards:**
- Primary sources (filings, transcripts) > Secondary sources (news)
- Quantitative data > Qualitative claims
- Recent data > Historical data
- Multiple confirming sources > Single source
- Every number must have a source URL, document date, and access date

### Phase 3: Analytical Framework

Apply each module systematically:

#### Module A: Business Quality Assessment

| Factor | Key Questions |
|---|---|
| Moat | What prevents competition? How durable? Switching costs, network effects, brand, cost advantage, scale, data, distribution, regulatory, IP. State whether moat is expanding, stable, or eroding. |
| Unit Economics | Gross margin, CAC/LTV, payback period |
| Revenue Quality | Recurring vs one-time? Concentration risk? |
| Pricing Power | Can they raise prices? Evidence? |
| Capital Intensity | CapEx needs, working capital |

**Moat Classification:**
- 🏰 Strong: Network effects, high switching costs, regulatory capture
- 🏠 Moderate: Brand, scale economies, patents (time-limited)
- 🏚️ Weak/None: Commodity business, low barriers

#### Module B: Financial Health Check

**Quantitative Scorecard (fill for every report):**

| Metric | Current | 3Y Ago | Trend | Grade (A/B/C/D/F) |
|---|---|---|---|---|
| Revenue Growth (CAGR) | | | | |
| Gross Margin | | | | |
| Operating Margin | | | | |
| ROIC | | | | |
| FCF Conversion | | | | |
| Debt/EBITDA | | | | |
| Interest Coverage | | | | |

Extract and assess:
- Revenue by segment/product/geography
- Gross margin, operating margin, net margin
- Free cash flow and FCF conversion quality
- Capex, R&D, SBC, working capital
- Debt, cash, leases, maturities
- Share count, dilution, buybacks/dividends
- Customer concentration, backlog/RPO
- Industry-specific KPIs (see `references/industry-frameworks.md`)

Mark unavailable metrics as `unknown`; do NOT invent them.

**Run Red Flag Checklist** (from `checks/red-flags-checklist.md`):
- 🔴 Critical: Auditor resignation, SEC investigation, accounting restatement, fraud allegations
- 🟠 Serious: Multiple red flags, material internal control weakness, CFO departure, covenant violations
- 🟡 Caution: Single flag, declining metrics, management credibility concerns

**Run Contradiction Hunter** (from `rules/contradictions/`):
- Automated via `scripts/contradiction_hunter.py` (scripts path) or manual YAML checklist (fallback path)
- Key checks: growth vs FCF quality, gross margin vs operating leverage, SBC dilution, inventory vs revenue trends, goodwill concentration

#### Module C: Management Quality

Assessment framework:
1. **Track Record** — Previous company performance, execution vs prior guidance, capital allocation history
2. **Alignment** — Insider ownership %, compensation structure, recent buying/selling patterns
3. **Communication** — Transparency in bad times, consistency of messaging, acknowledgment of challenges

**Management Grade: A/B/C/D/F with justification.**

#### Module D: Valuation Context

Use at least two lenses when possible:
- Trading comps / historical multiple range
- DCF or reverse DCF
- Sum-of-the-parts for multi-segment businesses
- Bull/base/bear scenario table

**Always expose assumptions:** Revenue CAGR, terminal margin, tax rate, WACC, terminal growth or exit multiple, net debt/cash, diluted share count.

**State what the current price implies.** This is more useful than a single target price.

**DO NOT give price targets as recommendations.** Present valuation as context, not conviction.

### Phase 4: Dialectical Synthesis

This is the most important phase. Be intellectually honest.

#### Bull Case (Steel-Manned)

```markdown
## 🐂 Bull Case

**Core Thesis:** [One sentence]

**Supporting Evidence:**
1. [Strongest argument with data and source]
2. [Second strongest]
3. [Third strongest]

**Key Assumptions:**
- [What must be true for this to work]

**Upside Scenario:** [Quantified if possible]
```

#### Bear Case (Steel-Manned)

```markdown
## 🐻 Bear Case

**Core Thesis:** [One sentence]

**Supporting Evidence:**
1. [Strongest bearish argument with data and source]
2. [Second strongest]
3. [Third strongest]

**Key Concerns:**
- [What could go wrong, structural risks, competitive threats]

**Downside Scenario:** [Quantified if possible]
```

#### Key Uncertainties

```markdown
## ❓ What We Don't Know

1. **[Uncertainty 1]**: Why it matters, when we'll know more
2. **[Uncertainty 2]**: Why it matters, when we'll know more
3. **[Uncertainty 3]**: Why it matters, when we'll know more

**Thesis-Breaking Events:**
- If [X] happens, bull case invalid
- If [Y] happens, bear case invalid
```

### Phase 5: Synthesis & Output

## Output Contract

**Default output order (老大 preference):**
1. **Conclusion** — rating-style view, one-line thesis, upside/downside
2. **Why** — thesis pillars with evidence
3. **Risks** — strong bear case, not token objections
4. **Recommended action / next checks**

**Full 10-section report structure:**
1. Executive Summary (one-line thesis + investment verdict + quick stats)
2. Business Overview (what they do, how they make money, key segments)
3. Industry & Competitive Position (TAM, market share, moat assessment)
4. Financial Analysis (financial health matrix + red flag check + contradiction flags)
5. Management Assessment (track record, alignment, grade)
6. Bull Case (steel-manned)
7. Bear Case (steel-manned)
8. Key Uncertainties (thesis-breakers)
9. Valuation Context (multiple methods, NOT a recommendation)
10. Catalysts & Timeline (near: 0-6 mo, medium: 6-18 mo, long: 18+ mo)

**Appendix:** Sources, key assumptions, peer comparison table.

## Alpha / So What Enforcement

A report is useful because it explains **what matters and where consensus may be wrong**.

Hard rules:
- Every major data section must include **So What** and **What If Wrong**.
- Hunt contradictions: growth vs FCF, gross margin vs operating margin, management guidance vs actual delivery, reported earnings vs per-share dilution.
- Time series beats snapshot: show trend, inflection, and deterioration/improvement.
- Compare management words with actions: guidance hit rate, capital allocation, buybacks, M&A, dilution.
- State current market consensus and how the report differs. **No differentiated view means no alpha claim.**
- Missing bear case or fewer than two thesis-breaking events → **BLOCK publication.**

## Quality Gates

### L1: Hard Publication Gates (REJECT if ANY fail)

These are **mandatory**. Command-tone enforcement:
- ❌ Missing bear case → REJECT, do not publish.
- ❌ Fewer than 2 thesis-breaking events (falsification triggers) → REJECT.
- ❌ Key financial numbers without source provenance → REJECT.
- ❌ Company identity not resolved (name, ticker, exchange) → REJECT.
- ❌ Latest filing period not stated → REJECT.
- ❌ Facts, estimates, assumptions, judgments not separated → REJECT.
- ❌ Bull/base/bear or scenario thinking absent → REJECT.
- ❌ Bear case is weak/token (only 1-2 sentences without data) → REJECT.
- ❌ No differentiated view vs market consensus → downgrade, flag as incomplete.

### L2: Industry-Specific Checks

See `rules/l2-industry-checks.yaml` for industry-specific quality checks. Load the relevant industry rules based on company classification.

### L3: Style Constraints

See `rules/l3-style-guide.yaml` for report tone and style requirements.

## Industry-Specific Metrics

### Data Availability Annotation

Every industry metric carries a three-tier annotation:

| Icon | Meaning | Action |
|---|---|---|
| ✅ | Automatically available | Extract from SEC XBRL or Yahoo Finance |
| 🔍 | Requires search | Find in 10-K management discussion, IR presentations, or earnings transcripts |
| ❌ | Data unavailable | Mark as `est.` (estimate with basis) or `N/A (based on management guidance)`. **NEVER invent numbers when data is unavailable.** |

### v1.0 Industry Packs

**SaaS / Cloud:**
- ✅ Revenue growth, gross margin, operating margin, FCF → SEC XBRL
- 🔍 ARR/MRR, NRR/GRR → 10-K MD&A, IR presentations
- 🔍 CAC payback, LTV/CAC → IR presentations, S-1 filings
- ✅ Rule of 40 = Revenue Growth% + FCF Margin% → Computable from SEC data
- ✅ SBC as % of revenue → SEC cash flow statement

**Fintech / Crypto Infrastructure:**
- ✅ Revenue growth, margins, FCF → SEC XBRL
- 🔍 Transaction volume, take rate → IR presentations, earnings calls
- 🔍 AUM/assets, user metrics → IR materials
- 🔍 Custody/regulatory exposure → 10-K risk factors

**Semiconductors:**
- ✅ Revenue growth, gross margin, R&D % → SEC XBRL
- 🔍 Inventory turnover, design wins → 10-K MD&A
- 🔍 Customer concentration → 10-K segment reporting
- 🔍 Supply/node/capex cycle → Industry reports, IR materials
- ✅ CapEx/revenue ratio → SEC cash flow statement

**Banks:**
- ✅ NIM, ROE, CET1 → Earnings releases
- 🔍 Loan book composition, credit quality → 10-K MD&A, regulatory filings
- 🔍 Deposit stability → IR materials

**E-commerce / Consumer:**
- ✅ Revenue growth, margins → SEC XBRL
- 🔍 GMV, take rate, active buyers → IR materials
- 🔍 AOV, fulfillment cost → 10-K MD&A

**Generic (fallback for uncovered industries):**
- ✅ Revenue growth, margins, FCF, ROIC, leverage, dilution → SEC XBRL
- 🔍 Industry-specific KPIs → Manual search

### Data Availability Annotation (per metric)

| Metric | Source | Reliability |
|---|---|---|
| Revenue growth | ✅ SEC XBRL | High — official filing |
| NRR/GRR (SaaS) | 🔍 10-K MD&A / IR | Medium — company-reported |
| CAC Payback (SaaS) | ❌ Often undisclosed | Low — estimate from S-1 or third-party |
| Market consensus P/E | ✅ Yahoo Finance | Medium — aggregated estimate |

## Scripts Usage

Scripts live in `scripts/` and are optional accelerators. SKILL_ROOT auto-discovery is built into each script.

**Available scripts:**
- `scripts/sec_xbrl_parser.py` — SEC EDGAR XBRL parsing with fiscal-year alignment
- `scripts/yahoo_connector.py` — Yahoo Finance market data
- `scripts/contradiction_hunter.py` — YAML rule-based contradiction detection
- `scripts/utils.py` — Shared utilities (fiscal-year alignment helpers)

**Usage pattern in SKILL.md:**
```
# Attempt automated path first:
execute_code(code that imports and runs sec_xbrl_parser + yahoo_connector)

# If script path fails, fall back to manual web_search:
web_search: "[TICKER] 10-K FY2025 revenue operating margin"
```

## Special Scenarios

### 13F Filings

When analyzing hedge fund/institutional 13F filings, apply rules from `references/special-scenarios/13f-options.md`:
- Option table value ≠ AUM. Large put/call entries may represent notional-style exposure, not premium paid.
- Do not infer "the fund spent $X" from option value alone.
- 13F is a delayed Q4 snapshot. Anchor analysis to report period, filing date, and intervening events.
- Label all 13F data as: date, filing date, caveats about unknown delta/strike/expiry.

### SEC Period-Mixing

SEC company facts may contain QTD, YTD, and FY entries filed on the same date. A contradiction flag may be a data-normalization bug, not alpha.

See `references/special-scenarios/sec-period-mixing.md` for full rules. Core principle: check the underlying SEC fact periods before trusting automated contradiction flags.

### Foreign / Small-Cap Theme Stocks

For non-US small-cap stocks with home listings and OTC lines, apply rules from `references/special-scenarios/foreign-small-cap.md`:
- Primary vs OTC venue judgment
- ADT filtering, VIE structure risks (China ADRs)
- Dilution/runway checks, currency exposure
- Separate policy/theme fit from priced-in expectations

## Report Maintenance Rules

### UPDATE HISTORY Format

Every report must include in its Appendix:

```markdown
## Report Metadata
- **Initial Date:** YYYY-MM-DD (first generation)
- **Last Updated:** YYYY-MM-DD
- **Update History:**
  - YYYY-MM-DD: [What changed, why, impact on thesis]. [Source: Q4 20XX Earnings Release, URL]
```

Write an UPDATE HISTORY entry ONLY when:
- New quarterly/annual financials are released
- Management guidance changes materially
- A major catalyst occurs (M&A, regulatory action, product launch, CEO change)
- New data invalidates or strengthens a bull/bear case pillar

Do NOT log minor corrections (typos, formatting).

### Re-Analyzing a Previously Covered Company

1. Read the old report in full
2. Identify chapters with stale data → mark `[STALE: based on Q1 20XX data]`
3. Target-update financial data and management discussion
4. Run contradiction hunter against new data → check if old flags resolved or new flags emerged
5. Check whether bull/bear case pillars still hold
6. Append UPDATE HISTORY entry
7. Preserve unchanged chapters; do NOT regenerate the entire report from scratch

## Common Pitfalls

1. **Pretty report, weak evidence.** Professional tone ≠ citations. Every key number needs a source.
2. **Confusing company story with investment thesis.** A good company can be a bad stock at the wrong price.
3. **Ignoring market expectations.** The key question is often what is already priced in.
4. **Single-source dependence.** Cross-check filings, IR, and external sources.
5. **No falsification triggers.** Every thesis needs conditions that would make it wrong.
6. **Generic industry analysis.** Use industry-specific metrics and value drivers.
7. **Black-box DCF.** If assumptions are hidden, the valuation is not useful.
8. **Overweighting recent news.** Distinguish durable drivers from noise.
9. **SEC period-mixing false positives.** A contradiction flag may be a data-normalization bug. Verify underlying periods.
10. **Metrics without judgment.** Every key metric needs `so_what` and `risk_if_wrong`.
11. **Misreading 13F option table value as real AUM.** Option notional ≠ true exposure.
12. **Over-interpreting delayed snapshots.** Q4 13F after a shock may show panic hedges, not conviction.
13. **Confirmation bias.** If user seems bullish, still present bear case fairly. Vice versa.
14. **Recency bias.** Don't over-weight latest quarter. Look at multi-year trends.
15. **Narrative fallacy.** Good story ≠ Good investment. Focus on numbers over narratives.

## Pulse Check Template (Hard — 30 lines max)

When generating a Pulse Check, use this exact structure:

```markdown
# [Company] ([TICKER]) Pulse Check
**Date:** YYYY-MM-DD | **Price:** $X | **Market Cap:** $XB | **Industry:** [sector]

## Thesis (1 line)
[One-sentence investment thesis]

## Key Numbers
| Metric | Value | YoY | Source |
|---|---|---|---|
| Revenue | $XB | +X% | 10-K FY20XX |
| Op Margin | X% | +/-Xpp | 10-K FY20XX |
| FCF | $XB | +X% | 10-K FY20XX |
| P/E (TTM) | Xx | | Yahoo Finance |

## Bull Case (2 lines)
[Key reason + catalyst]

## Bear Case (2 lines)
[Key risk + what would break thesis]

## Next Catalyst
[Event + rough timing]

## Monitor
- [Metric 1]: [threshold to watch]
- [Metric 2]: [threshold to watch]
```

## Research Report Template

See `templates/research-report.md` for the full 10-section template.

## Investment Memo Template

See `templates/investment-memo.md` for the deep-dive template with sensitivity analysis and full peer comps.

## References

Load relevant references during research:
- `references/methodology/dialectical-framework.md` — Phase 1-5 detailed process
- `references/metrics/financial-metrics.md` — Formula reference and thresholds
- `references/metrics/saas-metrics.md` — SaaS-specific KPIs
- `references/valuation/valuation-methods.md` — DCF, comps, SOTP methodology
- `references/special-scenarios/13f-options.md` — 13F option table interpretation
- `references/special-scenarios/sec-period-mixing.md` — SEC data normalization traps
- `references/special-scenarios/foreign-small-cap.md` — Non-US small-cap analysis
- `references/examples/` — 4 annotated example reports (Coinbase, SK Hynix, 金盘科技, Salesforce)
- `checks/red-flags-checklist.md` — Three-tier red flag checklist
- `docs/update-guide.md` — Report maintenance and UPDATE HISTORY format
- `rules/l1-hard-gate.yaml` — Mandatory publication gates
- `rules/l2-industry-checks.yaml` — Industry-specific quality checks
- `rules/l3-style-guide.yaml` — Report style constraints
- `rules/contradictions/generic.yaml` — Cross-industry contradiction rules
- `rules/contradictions/saas.yaml` — SaaS-specific contradiction rules
