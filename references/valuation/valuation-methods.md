# Valuation Methods Reference

## DCF (Discounted Cash Flow)

### Basic Formula
```
Enterprise Value = Σ (FCFt / (1 + WACC)^t) + Terminal Value / (1 + WACC)^n
```

### Key Inputs

**Free Cash Flow Projection:**
```
FCF = EBIT × (1 - Tax Rate) + D&A - CapEx - Δ Working Capital
```

**WACC Calculation:**
```
WACC = (E/V × Re) + (D/V × Rd × (1 - Tax Rate))

Where:
Re = Risk-free rate + β × Equity Risk Premium
Rd = Cost of debt (yield on existing debt)
E/V = Equity weight
D/V = Debt weight
```

**Terminal Value Methods:**

1. **Perpetuity Growth:**
```
TV = FCF_final × (1 + g) / (WACC - g)
```
g = Long-term growth rate (typically 2-3%)

2. **Exit Multiple:**
```
TV = EBITDA_final × Exit Multiple
```

### Sensitivity Analysis

Always run scenarios on:
- Revenue growth rate (±2%)
- Operating margin (±2%)
- WACC (±1%)
- Terminal growth rate (±1%)

Present as a matrix showing value range.

### DCF Limitations

- Highly sensitive to assumptions
- Garbage in, garbage out
- Less useful for:
  - Early-stage companies (negative FCF)
  - Highly cyclical businesses
  - Distressed situations

---

## Comparable Company Analysis ("Comps")

### Process

1. **Select peer group** (5-10 companies)
   - Same industry
   - Similar business model
   - Comparable size and geography
   - Similar growth profile

2. **Calculate trading multiples:**
   - P/E (Price/Earnings)
   - EV/EBITDA
   - EV/Revenue
   - EV/EBIT
   - P/B (Price/Book)

3. **Apply to target company:**
```
Implied Value = Target Metric × Peer Multiple
```

### Multiple Selection Guide

| Situation | Preferred Multiple |
|-----------|-------------------|
| Profitable, stable | P/E, EV/EBITDA |
| High growth | EV/Revenue, PEG |
| Asset-heavy | P/B, EV/IC |
| Cyclical | Normalized P/E |
| Pre-profit | EV/Revenue, EV/Users |
| Banks | P/B, P/TBV |
| REITs | P/FFO, P/NAV |

### Adjustments

Apply premium/discount for:
- Growth differential (+/- 10-30%)
- Margin differential (+/- 5-15%)
- Scale advantage (+/- 5-10%)
- Geographic risk (+/- 10-20%)

---

## Precedent Transactions

### When to Use
- M&A scenarios
- Sum-of-parts valuation
- Private company valuation

### Key Metrics
- EV/Revenue at acquisition
- EV/EBITDA at acquisition
- Premium to unaffected price

### Considerations
- Control premium (20-40% typical)
- Synergy assumptions
- Market conditions at time of deal
- Strategic vs financial buyer

---

## Sum-of-Parts (SOTP)

### Application
Companies with distinct business segments that could be valued separately.

### Process
1. Identify separable segments
2. Value each segment independently
3. Apply segment-appropriate multiples
4. Sum values
5. Subtract holding company discount (10-20%)
6. Add/subtract net cash/debt

### Example Structure
```markdown
| Segment | EBITDA | Multiple | EV |
|---------|--------|----------|-----|
| Segment A | $100M | 10x | $1,000M |
| Segment B | $50M | 8x | $400M |
| Segment C | $30M | 12x | $360M |
| **Total** | | | **$1,760M** |
| Holding discount | | -15% | ($264M) |
| Net cash | | | $200M |
| **Equity Value** | | | **$1,696M** |
```

---

## Growth-Adjusted Metrics

### PEG Ratio
```
PEG = P/E / EPS Growth Rate
```
Interpretation:
- <1: Potentially undervalued
- 1-2: Fair
- >2: Potentially expensive

### Rule of 40 (SaaS)
```
Rule of 40 Score = Revenue Growth % + FCF Margin %
```
- >40%: Efficient growth
- <40%: Needs improvement

### EV/Revenue to Growth
```
EV/Revenue / Revenue Growth Rate
```
Useful for high-growth, pre-profit companies

---

## Sector-Specific Valuation

### Technology/SaaS
- EV/ARR (5-20x depending on growth)
- EV/Revenue (3-15x)
- Customer lifetime value analysis

### Banks
- P/B (0.5-2.0x)
- P/TBV (Tangible Book)
- P/E with ROE adjustment

### REITs
- P/FFO
- P/AFFO
- NAV premium/discount

### Biotech
- Pipeline NPV
- Risk-adjusted probability
- Sum of pipeline values

### Commodity/Cyclical
- Normalized earnings P/E
- Through-the-cycle multiples
- Replacement cost

---

## Valuation Sanity Checks

### Implied Assumptions Test
Work backwards from current price:
- What growth is implied?
- What margin is implied?
- What terminal value is implied?

Ask: Are these assumptions reasonable?

### Historical Context
- Where is current valuation vs 5-year range?
- What drove prior highs/lows?
- Is current situation comparable?

### Cross-Method Consistency
If DCF and comps give wildly different values:
- Investigate the discrepancy
- One method may be more appropriate
- Adjust assumptions or peer selection

---

## Presenting Valuation

### Do's
✅ Show a range, not a point estimate
✅ Disclose key assumptions
✅ Show sensitivity analysis
✅ Acknowledge limitations
✅ Present multiple methods

### Don'ts
❌ Imply false precision
❌ Cherry-pick favorable multiples
❌ Ignore contradictory data points
❌ Present as investment recommendation

### Output Format
```markdown
## Valuation Summary

| Method | Bear Case | Base Case | Bull Case |
|--------|-----------|-----------|-----------|
| DCF | $X | $Y | $Z |
| Comps (P/E) | $A | $B | $C |
| Comps (EV/EBITDA) | $D | $E | $F |

Current Price: $[Current]
Implied Upside to Base: [%]
Implied Downside to Bear: [%]

**Key Assumptions:**
- [List critical inputs]

**Primary Uncertainty:**
- [What most affects the range]
```
