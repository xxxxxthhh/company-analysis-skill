# Company Analysis Skill

Public-first Hermes skill/playbook for deep company and equity research.

Goal: given a company name or ticker, produce a grounded company research report with citations, financial analysis, competitive context, valuation scenarios, risks, catalysts, and clear investment judgment.

## What this repo contains

- `skills/company-analysis/SKILL.md` — Hermes skill/playbook.
- `company_analysis/` — stdlib-first pipeline skeleton and quality gates.
- `company_analysis/metric_packs/` — industry metric pack interface and v0.1 pack stubs.
- `templates/company-report.md` — full report template.
- `templates/executive_summary.md` — one-page summary template.
- `templates/source-checklist.md` — source coverage checklist.
- `templates/thesis-tracker.md` — living thesis tracker template.
- `docs/metric-pack-interface.md` — metric pack input/output contract.
- `scripts/` — optional public-data connector skeletons.

## Design principles

1. Official sources first: SEC filings and company IR outrank news and third-party summaries.
2. Every important number needs provenance: source URL, document date, and access date where possible.
3. Separate facts, consensus, model assumptions, and analyst judgment.
4. No black-box valuation: expose assumptions and sensitivity.
5. Always include bear case, thesis-breaking risks, and what would change the view.
6. Avoid copyrighted/paid data scraping. Third-party APIs should be optional adapters.

## Quick use

Tell Hermes:

```text
Use the company-analysis skill. Analyze NVIDIA / NVDA and produce a full report.
```

Recommended output order:

1. Conclusion / rating-style view
2. Why the thesis works or fails
3. Key evidence and citations
4. Valuation and scenario analysis
5. Risks / catalysts / open questions

## Status

Initial draft. Built for public-first workflows; production-grade data connectors should add caching, rate limits, and provider-specific compliance.

## Pipeline skeleton

```bash
python -m company_analysis generate AAPL --industry software-platform --output reports/ --allow-placeholder
```

Without `--allow-placeholder`, quality gates reject reports that lack bear case, falsification triggers, or contradiction/alpha hooks.

## v0.1 industry packs

1. SaaS / Cloud
2. Fintech / Crypto Infrastructure
3. Software / Platform
4. Banks
5. E-commerce / Consumer
6. Semiconductors

Deferred: biotech and energy unless a user request needs them.
