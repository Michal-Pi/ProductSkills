# ProductSkills Response: pm-growth

Runtime: Codex. ProductSkills package version: 0.2.1. Skill used: `pm-growth`.

## Growth Model

AtlasBoard is a B2B SaaS product-led plus sales-assist workflow product. The likely growth loop is: import evidence -> synthesize opportunities -> create or review PRD -> run dry-run preview -> share artifact with Product Ops, engineering, or leadership -> invite more collaborators.

This artifact separates assumptions from facts: usage analytics and churn notes are facts from local files; experiment impact and conversion outcomes are assumptions.

## Segment

- Product Ops: 18 workspaces, 78 percent activation, 72 percent week 4 retention, 52 Linear preview runs, 44 Notion preview runs.
- Mid-market PM: 46 workspaces, 63 percent activation, 58 percent week 4 retention.
- Enterprise PMO: 7 workspaces, 57 percent activation, 64 percent week 4 retention, but security/admin evidence is missing.
- SMB founder-led: 34 workspaces, 31 percent activation, 24 percent week 4 retention.

## Bottleneck

The highest-leverage bottleneck is the drop from create/review PRD to run Linear or Notion preview. Funnel conversion from previous step drops to 22 percent at preview run. This matters because Product Ops has the strongest preview usage and highest retention.

## Evidence

- Usage analytics define activation as importing 10 evidence items, creating 3 opportunities, and creating or reviewing 1 PRD within 7 days.
- Product Ops has strongest activation and retention.
- SMB teams rarely use previews and show weak current fit.
- CHURN-004 shows stale synthesis risk: repeated weekly reports without a change log caused churn.
- SUP-002 and SUP-005 show preview structure and admin controls are adoption risks.

## Hypotheses

- If previews preserve PRD section structure, Product Ops preview completion will increase.
- If weekly synthesis marks what changed, week 4 retention will improve.
- If admin-disabled states are clearer, enterprise evaluators will continue evaluations without assuming live sync risk.

## Experiments

| Experiment | Target Metric | Guardrail Metric | Decision Threshold |
| --- | --- | --- | --- |
| Improve Linear preview grouping from SUP-002 | Preview run rate from PRD review | Zero unintended external writes | +10 percentage points preview run conversion |
| Add weekly synthesis change log | Week 4 retention | No increase in stale repeated themes | Product Ops week 4 retention remains above 70 percent and churn complaints decline |
| Add admin-disabled preview state | Enterprise evaluation continuation | No user thinks writes occurred | 80 percent of evaluators can explain preview-only state |

## Metrics

- Activation and retention consideration: activation rate, week 4 retention, PRDs with evidence links, Linear preview runs, Notion preview runs, return in week 4.
- Missing instrumentation: paid conversion, CAC, LTV, long-term retention beyond week 4, expansion, support cost.

## Decision Thresholds

This artifact includes confidence or risk notes and names concrete next actions.

- Proceed with preview quality improvements if preview conversion improves without write-safety confusion.
- Validate monetization before pricing decisions.
- Block paid conversion or revenue claims because no paid conversion data exists.

No external writes were performed.
