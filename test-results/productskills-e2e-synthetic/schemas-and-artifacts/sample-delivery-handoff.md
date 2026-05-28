# Sample Delivery Handoff

## Source PRD

`productskills-e2e-synthetic/product/existing-prd-approved.md`

## Epic 1 - Structured Linear Preview

Objective: Generate a dry-run Linear issue tree that preserves PRD sections.

Stories:
- As a Product Ops lead, I can preview epics grouped by PRD scope area so that delivery structure reflects product intent.
- As a PM, I can inspect story acceptance criteria before any issue is created.
- As an engineering lead, I can see dependencies and unresolved IDs before confirming future sync.

Acceptance Criteria:
- Preview includes epics, stories, acceptance criteria, labels, dependencies, and owners.
- Every item has a stable synthetic external ID.
- Preview labels all unresolved Linear team, state, and label IDs.
- No live Linear write is performed.

## Epic 2 - Structured Notion Preview

Objective: Generate dry-run Notion page previews for PRD summary, decision log, and launch checklist.

Stories:
- As a PM, I can preview the Notion PRD summary page before publishing.
- As a Product Ops lead, I can inspect decision-log entries and source evidence links.
- As a launch owner, I can preview launch-readiness checklist pages.

Acceptance Criteria:
- Preview includes page hierarchy, properties, source links, and payload hashes.
- Missing database/page IDs are marked unresolved.
- No live Notion write is performed.

## Epic 3 - Tooling Safety and Admin Controls

Objective: Make dry-run status and future write requirements explicit.

Stories:
- As an admin, I can disable external write actions for the workspace.
- As a user, I can see that previews are not synced records.
- As a reviewer, I can see confirmation requirements and idempotency keys.

Acceptance Criteria:
- Admin-disabled state blocks write actions.
- UI copy says dry-run preview in every preview export.
- Manual revert language is used; no true rollback is promised.

## Open Engineering Questions

- What payload hash function will be stable enough for idempotency checks?
- Should labels be resolved during preview or only after explicit workspace discovery?
- Where should external ID maps be stored in repo-scope tests?
