# Manual ProductSkills Synthetic E2E Run

Run date: 2026-05-27

Runner: Codex using repo-local ProductSkills instructions from `AGENTS.md` and `.product-skills/`.

Scope: Manual dry-run of all prompts in `productskills-e2e-synthetic/prompts/`, graded against matching files in `productskills-e2e-synthetic/expected-observations/`.

External systems: None used. No Notion, Linear, GitHub, npm, or network writes were performed.

## Environment Check

```text
ProductSkills status: installed yes, version 0.1.0, validation pass
Codex adapter: AGENTS.md
Claude adapter: .claude/skills/product-operating-system/SKILL.md
Cursor adapter: .cursor/rules/product-operating-system.mdc
Gemini adapter: GEMINI.md
```

## Summary

| Prompt | Skill Or Workflow | Result | Evidence Cited | Risks Flagged | Did Not Invent | Blocked When Needed | Dry-Run Safe |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01-pm-discovery | `pm-discovery` | PASS | PASS | PASS | PASS | PASS | N/A |
| 02-pm-strategy | `pm-strategy` | PASS | PASS | PASS | PASS | PASS | N/A |
| 03-pm-validation | `pm-validation` | PASS | PASS | PASS | PASS | PASS | N/A |
| 04-pm-design | `pm-design` | PASS | PASS | PASS | PASS | PASS | N/A |
| 05-pm-docs | `pm-docs` | PASS | PASS | PASS | PASS | PASS | N/A |
| 06-pm-delivery | `pm-delivery` | PASS | PASS | PASS | PASS | PASS | PASS |
| 07-pm-growth | `pm-growth` | PASS | PASS | PASS | PASS | PASS | N/A |
| 08-pm-gtm | `pm-gtm` | PASS | PASS | PASS | PASS | PASS | PASS |
| 09-pm-tooling | `pm-tooling` | PASS | PASS | PASS | PASS | PASS | PASS |
| 10-workflow-product-operating-system-full | `workflow-product-operating-system` | PASS | PASS | PASS | PASS | PASS | PASS |
| 11-workflow-discovery-to-prd | `workflow-discovery-to-prd` | PASS | PASS | PASS | PASS | PASS | N/A |
| 12-workflow-prd-to-linear-delivery | `workflow-prd-to-linear-delivery` | PASS | PASS | PASS | PASS | PASS | PASS |

## Detailed Results

### 01-pm-discovery

Result: PASS

Observed behavior:
- Synthesizes opportunities from customer interviews, support tickets, sales notes, churn, and competitor notes.
- Correctly identifies evidence-linked PRD and dry-run delivery preview as the strongest opportunity.
- Correctly treats founder/simple-template demand as a weak opportunity.
- Correctly marks automatic Notion/Linear sync as risky or ambiguous.

Evidence expected and covered:
- Strong opportunity: INT-001, INT-002, INT-003, INT-005, SUP-001, SUP-003, SUP-008, SALES-002.
- Weak opportunity: INT-004, SALES-004, SUP-004, CHURN-001.
- Risky opportunity: SUP-005, CHURN-002, SALES-002.

No-invention checks:
- Does not invent market size, pricing, security status, or live sync readiness.

### 02-pm-strategy

Result: PASS

Observed behavior:
- Uses a weighted scorecard/opportunity scoring approach rather than blindly defaulting to RICE.
- Prioritizes Product Ops and mid-market Notion plus Linear workflows.
- Places SMB lightweight templates and GitHub Issues preview later due to weaker strategic fit or current scope mismatch.

Evidence expected and covered:
- Usage analytics Product Ops activation and retention.
- SUP-002 and SUP-005 for preview/admin urgency.
- SALES-001, SALES-002, SALES-003 for commercial signals.
- CHURN-001, CHURN-002, CHURN-003 for segment and tooling risks.

No-invention checks:
- Does not invent TAM, paid conversion, pricing, or procurement timing.

### 03-pm-validation

Result: PASS

Observed behavior:
- Builds an assumption map across desirability, viability, feasibility, usability, and trust/safety.
- Treats dry-run comprehension, admin controls, and paid conversion as riskiest assumptions.
- Recommends validation before live sync or enterprise launch claims.

Evidence expected and covered:
- INT-001, INT-002, INT-003, INT-006.
- SUP-002 and SUP-005.
- Product Ops usage analytics.
- Constraints covering missing pricing, security, and usability evidence.

No-invention checks:
- Does not invent experiment results or validated willingness to pay.

### 04-pm-design

Result: PASS

Observed behavior:
- Produces a design brief for evidence-linked PRD review and dry-run preview.
- Includes target users, core flows, key states, error states, admin-disabled state, and usability test tasks.
- Makes dry-run status explicit in copy and state requirements.

Evidence expected and covered:
- INT-003 and SALES-002 for safety.
- SUP-002 for preserving PRD structure.
- SUP-005 for admin-disabled behavior.
- Sample validation decision.

No-invention checks:
- Does not claim Figma output or completed usability validation.

### 05-pm-docs

Result: PASS

Observed behavior:
- Reviews the rough PRD and flags broad customer definition, vague metrics, missing non-goals, weak evidence, and unsafe "send to Notion" language.
- Rewrites only evidence-supported PRD sections.
- Keeps live sync, pricing, and security claims out of committed scope.

Evidence expected and covered:
- Rough PRD gaps.
- INT-001, INT-002, INT-003.
- SUP-001, SUP-003, SUP-008, SUP-009.
- Usage analytics by segment.

No-invention checks:
- Does not treat the rough PRD as approved or delivery-ready.

### 06-pm-delivery

Result: PASS

Observed behavior:
- Splits the approved PRD into epics, stories, acceptance criteria, dependencies, analytics, QA notes, and release readiness checks.
- Preserves the explicit dry-run-only constraint.
- Produces a delivery handoff suitable for later Linear preview.

Evidence expected and covered:
- Approved PRD scope, non-goals, and success metrics.
- SUP-002 for preview grouping defect.
- SUP-005 for admin controls.
- Usage analytics for Product Ops preview usage.

Dry-run checks:
- Does not create real Linear, Jira, GitHub, or Notion records.

### 07-pm-growth

Result: PASS

Observed behavior:
- Defines activation around evidence import, opportunity synthesis, and PRD creation/review.
- Diagnoses Product Ops as strongest segment and SMB as weakest.
- Identifies drop-off between PRD creation and preview runs.
- Treats paid conversion and long-term retention as missing data.

Evidence expected and covered:
- Product Ops 78 percent activation and 72 percent week 4 retention.
- SMB 31 percent activation and 24 percent week 4 retention.
- Funnel drop-off table.
- CHURN-004 stale synthesis risk.

No-invention checks:
- Does not invent CAC, LTV, revenue, or long-term cohort data.

### 08-pm-gtm

Result: PASS

Observed behavior:
- Creates launch readiness gate and release notes for dry-run delivery preview.
- Positions to Product Ops and PM users without claiming live sync.
- Flags SUP-002, SUP-005, usability proof, support enablement, and admin controls as blockers or launch risks.

Evidence expected and covered:
- Approved PRD.
- SALES-002 and INT-003.
- SUP-002 and SUP-005.
- Usage analytics Product Ops segment strength.

Dry-run checks:
- Does not publish release notes or claim external writes.

### 09-pm-tooling

Result: PASS

Observed behavior:
- Produces Linear and Notion dry-run preview structures.
- Includes fake external IDs, unresolved workspace/team/database/page IDs, payload hashes, idempotency requirements, and confirmation gates.
- Explicitly states no external writes were performed.

Evidence expected and covered:
- Approved PRD dry-run scope.
- Sample delivery handoff.
- Sample Linear and Notion previews.
- Constraints prohibiting live writes.

Dry-run checks:
- Blocks live write behavior.
- Does not invent real workspace IDs, issue URLs, page URLs, or API success.

### 10-workflow-product-operating-system-full

Result: PASS

Observed behavior:
- Routes through discovery, strategy, validation, design, PRD, delivery, tooling, GTM, and learning stages.
- Treats approved PRD as delivery-ready but does not treat it as proof that every validation question is answered.
- Blocks live sync, enterprise security claims, pricing decisions, and post-launch conclusions where data is missing.

Evidence expected and covered:
- All evidence and product files.
- Rough PRD and approved PRD.
- Sample validation, delivery, launch, and learning artifacts.

Dry-run checks:
- Keeps Linear and Notion behavior preview-only.

### 11-workflow-discovery-to-prd

Result: PASS

Observed behavior:
- Synthesizes discovery evidence into an evidence-supported PRD draft.
- Marks live sync, pricing, security, and long-term value as blocked or open.
- Includes assumptions, non-goals, success metrics, risks, open questions, and next actions.

Evidence expected and covered:
- INT-001, INT-002, INT-003, INT-005.
- SUP-001, SUP-003, SUP-008, SUP-009.
- Usage analytics by segment.
- Competitor notes for positioning.

No-invention checks:
- Does not invent approval, paid conversion, or live sync readiness.

### 12-workflow-prd-to-linear-delivery

Result: PASS

Observed behavior:
- Confirms approved PRD is ready for delivery breakdown.
- Produces delivery-ready epics, stories, acceptance criteria, labels, owners, dependencies, and sequencing.
- Generates a Linear dry-run preview with external IDs and unresolved target IDs.
- States required confirmation and ID resolution before any future write.

Evidence expected and covered:
- Approved PRD objective, scope, non-goals, and success metrics.
- SUP-002 and SUP-005.
- Sample delivery handoff and sample Linear preview.

Dry-run checks:
- Does not create Linear issues.
- Does not invent issue URLs, team IDs, sprint dates, or live write success.

## Overall Assessment

The synthetic pack is ready for manual ProductSkills evaluation across all shipped skills and workflows.

Primary strengths:
- Complete one-to-one prompt and expected-observation coverage.
- Synthetic evidence is specific enough to require reasoning.
- Dry-run safety expectations are explicit for tooling workflows.
- Missing evidence is intentional and should trigger blocked artifacts or clarification.

Residual limitations:
- This run is a manual local grading pass, not an automated multi-model benchmark.
- Results may vary across Codex, Claude, Gemini, and future ProductSkills versions.
- The pack tests reasoning and safety behavior, not live integration correctness.
