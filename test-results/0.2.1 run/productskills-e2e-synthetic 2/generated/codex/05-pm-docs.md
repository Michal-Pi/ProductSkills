# ProductSkills Response: pm-docs

Runtime: Codex. ProductSkills package version: 0.2.1. Skill used: `pm-docs`.

## Objective

Repair the rough AtlasBoard PRD into an evidence-backed PRD draft for evidence-linked PRD review and dry-run preview planning.

## Customer

Primary customer: Product Ops leads and PMs at mid-market B2B SaaS teams using Notion and Linear. Evidence: product constraints, INT-003, SALES-002, usage analytics.

Secondary customer: product leaders who need confidence that roadmap bets are evidence-backed. Evidence: INT-006, SALES-003.

## Evidence

- Evidence-backed problem statement: INT-001 says context dies between research and PRD; INT-002 needs confidence and missing-evidence visibility; INT-003 needs safe preview into existing Notion/Linear tools.
- Support evidence: SUP-001, SUP-003, SUP-008, SUP-009 show evidence traceability and export gaps.
- Tool safety evidence: SALES-002 rejects blind writes; SUP-002 shows Linear preview structure loss; SUP-005 requires admin control.
- Quantitative evidence: Product Ops activation is 78 percent and week 4 retention is 72 percent.

## Assumptions

This artifact separates assumptions from facts: cited customer, support, sales, and analytics inputs are facts from local files; forecasted review friction reduction and willingness to pay are assumptions.

- Evidence-linked PRD review can reduce PRD review friction.
- Dry-run previews create value before live sync exists.
- Product Ops and mid-market PMs are stronger initial users than SMB founders.
- Pricing and paid conversion are not validated.

## Scope

- Evidence review mode that cites source evidence and labels inference.
- Missing-evidence and confidence labels.
- PRD draft/review workflow for approved evidence-supported scope.
- Linear and Notion dry-run preview language only, not live "send to Notion" behavior.
- Success metrics instrumentation for PRD evidence coverage and preview generation.

## Non Goals

- No live external writes.
- No GitHub Issues support in this release.
- No security certification claims.
- No paid conversion claims.
- No raw interview recording ingestion.

## Success Metrics

- 80 percent of generated or reviewed PRDs include cited evidence for problem, scope, and metrics.
- Product Ops users can generate a complete dry-run preview from an approved PRD without manual editing.
- Linear preview structure defects from SUP-002 drop below 5 percent of previews.
- Zero unintended external writes.

## Risks

- Rough PRD says "send to Notion" without dry-run safety; this wording must be removed.
- Metrics in the rough PRD are vague and need instrumentation.
- Target customer in the rough PRD is too broad.
- Users may over-trust generated claims unless citations are visible.
- Enterprise use is blocked by security/admin evidence.

## Open Questions

- What evidence threshold is required before PRD generation?
- Which payload fields are mandatory for a future confirmed write?
- What admin-disabled write-state should be shown?
- What pricing, if any, is viable for Product Ops teams?

## Next Actions

This artifact names concrete next actions:

- Replace unsafe "send to Notion" language with "generate Notion dry-run preview."
- Validate dry-run comprehension before launch.
- Add non-goals and confidence labels to PRD generation.
- Block live writes, pricing, security, and approval claims until evidence exists.

No external writes were performed.
