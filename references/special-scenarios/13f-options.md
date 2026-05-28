# 13F Options, Notional Artifacts, and Timing Pitfalls

Use this note when analyzing institutional 13F filings with options or when a user asks to interpret a manager's portfolio changes.

## Core pitfall: option `value` is not premium/AUM

Form 13F information tables include listed options, but the reported `value` for puts/calls is tied to the underlying security exposure/reporting convention, not the option premium paid or true economic risk.

Implications:

- Do **not** describe total 13F table value as true AUM when large options positions are present.
- Do **not** say "puts are X% of the portfolio" without labeling it as **13F table value / underlying notional-style exposure**, not premium or delta exposure.
- A large put/call table value may represent a hedge overlay, volatility structure, spread, or paired options trade. 13F does not disclose strike, expiry, premium, delta, or whether offsetting short options/swaps exist.
- Phrase carefully: "reported put exposure / 13F table value" rather than "spent $X on puts" or "has $X short exposure."

## Required interpretation steps

1. Split common/ADR, calls, and puts.
2. State that option values are 13F-reported values and may overstate economic exposure.
3. Avoid inferring net delta from 13F alone.
4. If possible, compare both:
   - reported 13F table value, and
   - qualitative economic interpretation: hedge overlay vs directional short vs volatility trade.
5. Check for duplicated filings across affiliated managers/advisers before double-counting.
6. Look for 13D/13G/Form 4 only for specific security-level timing clues; absence means timing remains unknown.

## Timing / snapshot caution

13F is a delayed quarter-end snapshot. For fast-moving themes, anchor the interpretation to the report date and the disclosure date.

Questions to ask:

- What major market events occurred during the quarter before the report date?
- Could the filing be a post-event hedge rather than a long-term thesis?
- Did subsequent earnings/guidance/capex data confirm or reverse the event narrative?
- Are exits/additions explainable as panic hedge, risk management, or portfolio overlay rather than conviction?

If timing cannot be resolved, say so explicitly: "Public 13F data cannot determine whether this was built before or after event X."

## Output language examples

Prefer:

- "The filing shows a large reported semis put overlay, but true premium/delta exposure is unknown."
- "This may be a hedge against a long AI-infrastructure basket, not a pure directional short."
- "The 13F cannot tell us strike, expiry, premium, or build date."

Avoid:

- "The fund spent $8B buying puts."
- "Puts are 60% of the real portfolio."
- "AUM rose from $5B to $13B" when the change is largely option table value.
