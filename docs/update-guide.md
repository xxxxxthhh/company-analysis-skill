# Report Maintenance & UPDATE HISTORY Guide

## UPDATE HISTORY Convention

Every report generated with this skill must include metadata for traceability and freshness assessment. This is not optional — it's part of the report's credibility.

### Metadata Block Format

```markdown
### Report Metadata
- **Initial Date:** YYYY-MM-DD (date of first generation)
- **Last Updated:** YYYY-MM-DD (date of most recent substantive update)
- **Update History:**
  - YYYY-MM-DD: [What changed, why, impact on thesis]. [Source: e.g., Q4 20XX Earnings Release, URL]
  - YYYY-MM-DD: [Earlier entry if applicable]
```

### When to Write an UPDATE HISTORY Entry

**DO write an entry when:**
- New quarterly/annual financials are released
- Management guidance changes materially
- A major catalyst occurs (M&A announcement, regulatory action, product launch, CEO change)
- New data invalidates or strengthens a bull/bear case pillar

**Do NOT write an entry for:**
- Minor corrections (typos, formatting fixes)
- Re-wording without substantive change
- Adding a source you missed on first pass (unless the new source changes the conclusion)

### Marking Stale Data

When updating a previously published report:

1. **DO** mark old data with `~~strikethrough~~` and follow with the updated value
2. **Example:** `~~Q4 2025 Revenue: $1.87B~~ → Q1 2026 Revenue (Actual): $2.1B`
3. **DO** add a banner at the top summarizing what was updated:
   ```
   **[YYYY-MM-DD Update]** Key changes: Q1 2026 earnings released — beat estimates on revenue (+15% vs consensus), new product launch announced. Previous data marked with ~~strikethrough~~.
   ```
4. **Do NOT** silently replace old data without evidence of the change

### Re-Analyzing a Previously Covered Company

Follow this workflow:

1. **Read the old report in full** (use `read_file` if the report is on disk)
2. **Identify stale chapters** — mark `[STALE: based on QX 20XX data]` at chapter level
3. **Target-update** financial data and management discussion for newly reported periods
4. **Run contradiction hunter** against new data — check if old flags resolved or new flags emerged
5. **Re-evaluate bull/bear case pillars** — check if any have been invalidated or strengthened
6. **Append UPDATE HISTORY entry** (see format above)
7. **Preserve unchanged chapters** — do NOT regenerate the entire report from scratch

## File Naming Convention

```
{Company}_{ReportType}_{YYYY-MM-DD}.md

Examples:
- Coinbase_Research_Report_2026-02-11.md
- SK_Hynix_Investment_Memo_2026-02-25.md
- Salesforce_Pulse_Check_2026-05-29.md
```

For bilingual outputs:
```
- {Company}_深度研究报告_{YYYY-MM}.md      (中文)
- {Company}_Deep_Research_Report_{YYYY-MM}.md (English)
```

Both language versions must be complete reports with all sections. Do not split content between languages.

## Staleness Thresholds

A report is considered **stale** when:
- A new quarterly filing (10-Q) is available and not reflected → flag as `[STALE]`
- Price/market data is > 30 days old → flag the valuation section
- A material catalyst has occurred (earnings, M&A, regulatory action) → flag as `[OUTDATED THESIS]`
- Management guidance has been revised → flag the catalysts section

A report is considered **outdated** when:
- A new annual filing (10-K) is available → full refresh recommended
- Two or more quarters have passed since last update → full refresh recommended
- A thesis-breaking event has occurred → full rewrite needed

## Example: Coinbase UPDATE HISTORY

From the Coinbase 2026 report (see `references/examples/Coinbase_Report.md`):

```
**[2026-02-14 Update] Additional Q4 2025 details: cash $11.3B (previously $8B+), Q4 FCF $3.07B, combined derivatives volume ~$1.25T, net loss breakdown (crypto unrealized loss $718M + strategic investment loss $395M). Stock rebounded +13-18% on 2/13. Old data marked with ~~strikethrough~~.**

**[2026-02-13 Update] Updated with Q4 2025 earnings data (released 2/12 after market close). Q4 revenue $1.78B missed estimates; net loss of $667M ended 8-quarter profitability streak. FY2025 revenue confirmed at $7.18B.**

**Date:** February 11, 2026 (Updated: February 14, 2026)
```

Key lessons from this example:
- Updates are at the TOP, chronologically newest first
- Each entry says WHAT changed, WHY (new data source), and IMPACT on thesis
- Old data is preserved with strikethrough, not deleted
- The reader can trace the evolution of the analysis over time
