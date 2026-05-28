# ProductSkills Response: pm-strategy

Runtime: Codex. ProductSkills package version: 0.2.1. Skill used: `pm-strategy`.

## Decision Context

AtlasBoard must choose which product opportunities to prioritize from synthetic discovery evidence. The decision should not default to automatic RICE scoring for every scenario because reach, effort, pricing, and implementation estimates are incomplete. The useful choice is a weighted opportunity scorecard grounded in evidence strength, segment fit, strategic alignment, risk, confidence, and effort uncertainty.

This artifact separates assumptions from facts: evidence IDs and analytics are facts from local files; effort, commercial conversion, and pricing implications are assumptions or missing evidence.

## Options

1. Evidence-linked PRD review and opportunity synthesis.
2. Linear/Notion dry-run delivery preview.
3. Support-ticket import quality controls.
4. Enterprise security/admin readiness.
5. GitHub Issues preview.
6. Lightweight founder PRD templates.
7. Automatic live sync to external tools.

## Selected Method

Selected method: weighted scorecard plus Now/Next/Later sequencing.

Method selection rationale: opportunity scoring fits customer-discovered opportunities; weighted scorecards fit strategy-specific tradeoffs. RICE is incomplete because reach and effort are uncertain. WSJF would require cost of delay and job size that are not evidenced. ICE is better for experiment backlogs, not committed roadmap sequencing. MoSCoW is useful later for release-scope negotiation, not portfolio choice.

## Criteria

- Evidence strength and citation quality.
- Segment fit with Product Ops and mid-market B2B SaaS.
- Strategic alignment with evidence-to-PRD-to-delivery continuity.
- Risk and missing evidence.
- Effort uncertainty.
- Commercial signal without inventing pricing or TAM.

## Scores

| Opportunity | Evidence | Segment Fit | Risk | Effort Uncertainty | Recommendation |
| --- | --- | --- | --- | --- | --- |
| Evidence-linked PRD review | High: INT-001, INT-002, INT-005, SUP-001, SUP-003, SUP-008, SUP-009, SALES-001 | High | Medium | Medium | Now |
| Linear/Notion dry-run preview | High: INT-003, SALES-002, SUP-002, SUP-005, usage analytics | High | Medium-high safety risk | Medium-high | Now |
| Support import quality | Medium-high: INT-008, SUP-007, support ARR fields | Medium | Medium data quality risk | Medium | Next |
| Enterprise security/admin | Medium: INT-006, SALES-003, SUP-005, CHURN-002 | High ARR but readiness blocked | High | High | Next after validation/security |
| GitHub Issues preview | Medium: INT-007, SALES-005, SUP-006, CHURN-003 | Low current fit | Medium | Unknown | Later |
| Founder templates | Low-medium: INT-004, SALES-004, SUP-004, CHURN-001 | Low | Low strategic fit | Low | Later |
| Automatic live sync | Risky: INT-003 and SALES-002 explicitly reject blind writes | Poor until safety proven | Critical | High | Block |

## Confidence

Confidence or sensitivity note: confidence is highest for Product Ops / Notion plus Linear because Product Ops analytics show 78 percent activation and 72 percent week 4 retention. Confidence drops for pricing, enterprise procurement, GitHub scope, and founder templates because evidence is incomplete or conflicts with current positioning.

## Recommendation

This artifact names concrete next actions:

Now:
- Evidence-linked PRD review and missing-evidence labels.
- Dry-run Linear/Notion preview payload quality and admin-disabled state.

Next:
- Support-ticket import quality controls.
- Security/admin discovery for enterprise readiness.
- Weekly synthesis change log.

Later:
- GitHub Issues preview.
- Lightweight founder templates.
- Paid conversion instrumentation once pricing research exists.

Next decision step: approve a validation plan for dry-run preview comprehension, admin controls, and Product Ops willingness to keep using previews before live writes.

## Risks

- Do not invent TAM, pricing, paid conversion, procurement timing, or implementation estimates.
- Enterprise upside is blocked by security and admin evidence.
- GitHub Issues demand conflicts with Linear-first strategy.
- Frequency alone must not over-promote SMB template requests or cosmetic asks.

No external writes were performed.
