# ProductSkills Response: pm-validation

Runtime: Codex. ProductSkills package version: 0.2.1. Skill used: `pm-validation`.

## Assumption Map

Desirability:
- Product Ops teams want evidence-linked PRD review and safe delivery preview. Evidence: INT-001, INT-002, INT-003, INT-005, SALES-002, usage analytics.
- Assumption: dry-run preview creates enough value before live writes.

Viability:
- Product Ops and mid-market teams are a better wedge than SMB founders. Evidence: Product Ops 78 percent activation and 72 percent week 4 retention; INT-004, SALES-004, and CHURN-001 show weaker founder fit.
- Assumption: willingness to pay is not validated; pricing willingness is directional only.

Feasibility:
- AtlasBoard can generate stable Linear/Notion preview payloads with external IDs and payload hashes. Evidence: approved PRD, SUP-002, sample Linear/Notion preview artifacts.
- Assumption: idempotency and payload hash format can be implemented reliably.

Usability:
- Users understand that dry-run previews are not completed syncs. Evidence: INT-003 and SALES-002 want preview and confirmation; sample validation decision says usability testing is still needed.
- Assumption: copy and UI states can make dry-run status unmistakable.

Trust safety:
- Admin controls and external-write blocking can satisfy evaluators. Evidence: SUP-005, CHURN-002, INT-006, SALES-003.
- Assumption: security posture and admin controls are sufficient for enterprise after validation; this is not yet proven.

## Riskiest Assumptions

1. Users may misunderstand dry-run preview as a completed sync.
2. Enterprise evaluators may block without admin controls and security evidence.
3. Preview value may not translate into paid conversion.
4. Generated PRDs may be over-trusted unless every claim cites evidence.

## Validation Experiments

| Hypothesis | Method | Sample | Success Threshold | Guardrail |
| --- | --- | --- | --- | --- |
| Product Ops users can explain preview vs sync after reviewing payloads | Moderated usability test | 6 Product Ops / PM users from Notion + Linear teams | 5 of 6 correctly state no external write occurred | No participant thinks records were created |
| Evidence-linked PRD review improves confidence without fake certainty | Prototype review | 5 mid-market PMs | 4 of 5 can identify cited vs inferred claims | Users do not accept uncited claims as facts |
| Admin-disabled state is acceptable during evaluation | Concept test | 3 enterprise or PMO evaluators | 3 of 3 understand write actions are blocked | No security or admin-control claim is overstated |
| Dry-run preview has commercial value before live sync | Concierge pilot | 5 Product Ops workspaces | 3 of 5 export or share preview artifacts twice | Do not infer validated willingness to pay |

## Decision Rules

- Proceed to PRD only for evidence-linked PRD review and dry-run preview scope if usability and trust thresholds pass.
- Run validation first for live sync, enterprise launch claims, pricing, and paid conversion.
- Block if users cannot distinguish preview from completed sync.
- Block if admin-disabled behavior is unclear for enterprise evaluators.

## Validation Decision

Decision: run_validation_first for live sync, enterprise launch, pricing, and paid conversion; proceed to prototype and limited PRD/delivery planning for dry-run preview and evidence-linked PRD review.

## Cannot Conclude

- Validation results are missing; experiments have not been run.
- Validated willingness to pay is not available.
- Live sync feasibility is not proven.
- Security certification, procurement timeline, and paid conversion evidence are missing.

## Next Actions

This artifact names concrete next actions:

- Run usability test for dry-run comprehension.
- Run admin-control/security review with enterprise evaluators.
- Define pricing research separately from feature validation.
- Keep external writes disabled during evals.

No external writes were performed.
