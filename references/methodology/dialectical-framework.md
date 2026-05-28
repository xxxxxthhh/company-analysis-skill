---
name: company-deep-research
description: Deep fundamental research and analysis framework for public companies. Triggers when user wants to research a company, analyze business fundamentals, evaluate investment thesis, assess competitive positioning, or generate comprehensive research reports. Use when user mentions "调研公司", "research [company]", "analyze [ticker]", "investment thesis", "公司分析", "基本面研究", or asks about a company's business model, competitive moat, financial health, management quality, or future outlook. Produces objective, dialectical reports with bull/bear cases and explicit risk assessment.
---

# Company Deep Research Framework

Systematic framework for producing **objective, dialectical, and comprehensive** company research reports. Emphasizes intellectual honesty, contrarian thinking, and explicit acknowledgment of uncertainty.

## Core Philosophy

**思辨原则 (Dialectical Thinking):**
- Every bull case deserves a steel-manned bear case
- Every bear case deserves a steel-manned bull case
- Acknowledge what you don't know
- Present conflicting evidence, don't hide it
- Distinguish between facts, inferences, and opinions

## Research Workflow

### Phase 1: Scope Definition

**Before starting research, clarify with user:**

1. **Research Depth**
   - Quick overview (30 min): Key metrics + brief thesis
   - Standard analysis (2 hr): Full framework below
   - Deep dive (4+ hr): Include channel checks, expert calls synthesis

2. **Focus Area**
   - General investment thesis
   - Specific angle (e.g., China recovery, AI monetization, margin expansion)
   - Comparative analysis (vs competitors)

3. **Time Horizon**
   - Near-term catalyst (3-6 months)
   - Medium-term (1-2 years)
   - Long-term secular (3-5+ years)

4. **Output Format**
   - Executive summary only
   - Full research report (recommended)
   - Investment memo style

### Phase 2: Information Gathering

**Mandatory Data Sources (search all):**

```
1. Company Filings
   - Latest 10-K/20-F (annual)
   - Recent 10-Q (quarterly)
   - Earnings call transcripts (last 2-4 quarters)
   - Investor presentations

2. Financial Data
   - web_search: "[TICKER] revenue growth last 5 years"
   - web_search: "[TICKER] operating margin trend"
   - web_search: "[TICKER] free cash flow history"
   - web_search: "[TICKER] balance sheet debt levels"

3. Industry Context
   - web_search: "[INDUSTRY] market size TAM growth"
   - web_search: "[COMPANY] market share vs competitors"
   - web_search: "[INDUSTRY] regulatory changes 2024 2025"

4. Management & Governance
   - web_search: "[COMPANY] CEO background track record"
   - web_search: "[COMPANY] insider buying selling"
   - web_search: "[COMPANY] executive compensation"

5. Sentiment & Controversy
   - web_search: "[COMPANY] short seller report"
   - web_search: "[COMPANY] accounting concerns"
   - web_search: "[COMPANY] lawsuit regulatory investigation"
   - web_search: "[COMPANY] bear case risks"

6. Recent Developments
   - web_search: "[COMPANY] news last 30 days"
   - web_search: "[COMPANY] analyst rating changes"
   - web_search: "[COMPANY] guidance outlook 2025 2026"
```

**Information Quality Standards:**
- Primary sources (filings, transcripts) > Secondary sources (news)
- Quantitative data > Qualitative claims
- Recent data > Historical data
- Multiple confirming sources > Single source

### Phase 3: Analytical Framework

**Apply each module systematically:**

#### Module A: Business Quality Assessment

| Factor | Questions to Answer | Data Sources |
|--------|---------------------|--------------|
| **Moat** | What prevents competition? How durable? | Industry reports, competitor analysis |
| **Unit Economics** | Gross margin, CAC/LTV, payback period | Financials, management commentary |
| **Revenue Quality** | Recurring vs one-time? Concentration risk? | 10-K segment breakdown |
| **Pricing Power** | Can raise prices? Evidence? | Historical pricing, gross margin trend |
| **Capital Intensity** | CapEx needs, working capital | Cash flow statement |

**Moat Classification:**
- 🏰 **Strong**: Network effects, high switching costs, regulatory capture
- 🏠 **Moderate**: Brand, scale economies, patents (time-limited)
- 🏚️ **Weak/None**: Commodity business, low barriers

#### Module B: Financial Health Check

**Quantitative Scorecard:**

```markdown
## Financial Health Matrix

| Metric | Current | 3Y Ago | Trend | vs Peers | Grade |
|--------|---------|--------|-------|----------|-------|
| Revenue Growth (CAGR) | | | | | |
| Gross Margin | | | | | |
| Operating Margin | | | | | |
| ROIC | | | | | |
| FCF Conversion | | | | | |
| Debt/EBITDA | | | | | |
| Interest Coverage | | | | | |

Grade: A (top quartile), B (above average), C (average), D (below), F (concern)
```

**Red Flag Checklist:**
- [ ] Revenue growing faster than cash flow
- [ ] Accounts receivable growing faster than revenue
- [ ] Frequent "one-time" adjustments
- [ ] Declining audit quality or auditor changes
- [ ] Related party transactions
- [ ] Excessive stock-based compensation
- [ ] Goodwill > 30% of assets

#### Module C: Management Quality

**Assessment Framework:**

1. **Track Record**
   - Previous company performance
   - Execution vs prior guidance
   - Capital allocation history

2. **Alignment**
   - Insider ownership %
   - Compensation structure (vs value created)
   - Recent buying/selling patterns

3. **Communication**
   - Transparency in bad times
   - Consistency of messaging
   - Acknowledgment of challenges

**Management Grade: A/B/C/D/F with justification**

#### Module D: Valuation Context

**Multi-Method Approach:**

```markdown
## Valuation Summary

| Method | Value/Share | Assumptions | Confidence |
|--------|-------------|-------------|------------|
| DCF (Base) | $ | [Key inputs] | Medium |
| DCF (Bull) | $ | [Optimistic] | Low |
| DCF (Bear) | $ | [Conservative] | Medium |
| Comps (P/E) | $ | vs [peers] | High |
| Comps (EV/Sales) | $ | vs [peers] | Medium |
| Historical | $ | [range] | Medium |

Current Price: $
Implied Upside/Downside: % to base case
```

**DO NOT give price targets as recommendations.** Present valuation as context, not conviction.

### Phase 4: Dialectical Synthesis

**This is the most important section. Be intellectually honest.**

#### Bull Case (Steel-Manned)

```markdown
## 🐂 Bull Case

**Core Thesis:** [One sentence]

**Supporting Evidence:**
1. [Strongest argument with data]
2. [Second strongest with data]
3. [Third strongest with data]

**Key Assumptions:**
- [What must be true for this to work]
- [Market conditions required]
- [Execution milestones]

**Upside Scenario:** [Quantified if possible]
```

#### Bear Case (Steel-Manned)

```markdown
## 🐻 Bear Case

**Core Thesis:** [One sentence]

**Supporting Evidence:**
1. [Strongest bearish argument with data]
2. [Second strongest with data]
3. [Third strongest with data]

**Key Concerns:**
- [What could go wrong]
- [Structural risks]
- [Competitive threats]

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

### Phase 5: Synthesis & Framework Output

**Final Report Structure:**

```markdown
# [Company Name] ([TICKER]) Deep Research Report

**Date:** [Date]
**Analyst:** Claude AI (assisted research)
**Disclaimer:** This is not investment advice. Do your own due diligence.

---

## Executive Summary

**One-Line Thesis:** [Concise summary]

**Investment Verdict:** 
- Bull/Bear/Neutral with conviction level (High/Medium/Low)
- Key catalyst or timeline

**Quick Stats:**
| Metric | Value |
|--------|-------|
| Market Cap | |
| P/E (TTM) | |
| P/E (Forward) | |
| Revenue Growth | |
| FCF Yield | |

---

## 1. Business Overview
[What they do, how they make money, key segments]

## 2. Industry & Competitive Position
[TAM, market share, competitors, moat assessment]

## 3. Financial Analysis
[Financial health matrix, trends, red flags]

## 4. Management Assessment
[Track record, alignment, grade]

## 5. Bull Case
[Steel-manned optimistic thesis]

## 6. Bear Case
[Steel-manned pessimistic thesis]

## 7. Key Uncertainties
[What we don't know, thesis-breakers]

## 8. Valuation Context
[Multiple methods, NOT a recommendation]

## 9. Catalysts & Timeline
[Near-term: 0-6mo, Medium: 6-18mo, Long: 18mo+]

## 10. Conclusion
[Balanced synthesis, explicit about confidence level]

---

## Appendix
- Data sources
- Key assumptions
- Peer comparison table
```

## Quality Standards

### What Makes a GOOD Research Report

✅ **Objective:** Presents both sides fairly  
✅ **Data-Driven:** Claims backed by numbers  
✅ **Honest:** Acknowledges uncertainty and limitations  
✅ **Structured:** Easy to navigate and reference  
✅ **Actionable:** Clear on what to watch and when  

### What Makes a BAD Research Report

❌ **One-sided:** Only bull or only bear  
❌ **Vague:** "The company has potential" without specifics  
❌ **Overconfident:** "Will definitely" or "guaranteed"  
❌ **Stale:** Uses outdated data without noting it  
❌ **Copied:** Regurgitates press releases without analysis  

## Special Considerations

### For 2025/2026 Outlook Questions

When asked about future trajectory:

1. **Identify Key Drivers**
   - Macro factors (rates, GDP, sector rotation)
   - Company-specific catalysts (product launches, expansion)
   - Regulatory changes

2. **Scenario Analysis**
   - Base case (50% probability): [Outcome]
   - Bull case (25%): [Outcome]
   - Bear case (25%): [Outcome]

3. **Leading Indicators to Watch**
   - [Metric 1]: Why it matters, where to track
   - [Metric 2]: Why it matters, where to track

### For China/Singapore Companies

**Additional considerations:**
- VIE structure risks (for China ADRs)
- Currency exposure
- Geopolitical factors
- Regulatory environment differences
- Accounting standard differences (IFRS vs GAAP)

### For Tech/Growth Companies

**Adjust framework for:**
- Revenue growth > profitability (early stage)
- TAM expansion potential
- Network effects assessment
- Unit economics trajectory
- Path to profitability timeline

## Common Pitfalls to Avoid

1. **Confirmation Bias**
   - If user seems bullish, still present bear case fairly
   - If user seems bearish, still present bull case fairly

2. **Recency Bias**
   - Don't over-weight latest quarter
   - Look at multi-year trends

3. **Authority Bias**
   - Analyst ratings are inputs, not conclusions
   - Management is not always truthful

4. **Narrative Fallacy**
   - Good story ≠ Good investment
   - Focus on numbers over narratives

## Resources

See `references/` for:
- `financial-metrics.md`: Detailed calculation formulas
- `red-flags-checklist.md`: Expanded warning signs
- `industry-frameworks.md`: Sector-specific considerations
- `valuation-methods.md`: DCF and comps methodology
