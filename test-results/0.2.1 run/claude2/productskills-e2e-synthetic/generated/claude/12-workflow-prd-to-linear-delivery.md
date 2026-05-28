# ProductSkills workflow-prd-to-linear-delivery — AtlasBoard Approved PRD → Linear Dry-Run Delivery

Workflow skill: `workflow-prd-to-linear-delivery`. Synthetic only. **No Linear issues created. Dry-run preview only.**

Source PRD: `productskills-e2e-synthetic/product/existing-prd-approved.md`.

## PRD Readiness Review

**PRD completeness review** against the pack's quality bar:

| Check | Status | Evidence |
| --- | --- | --- |
| Objective concrete + customer-bound | ✅ | "Enable Product Ops and PM teams to generate safe, reviewable Linear and Notion dry-run previews from an approved PRD." |
| Primary customer named | ✅ | Mid-market B2B SaaS Product Ops + PMs on Notion + Linear |
| Evidence cited with IDs | ✅ | INT-003, SALES-002, SUP-002, SUP-005, USAGE Product Ops 78%/72% |
| Scope bounded, shippable | ✅ | 3 epics: Linear preview, Notion preview, Tooling Safety + Admin |
| Non-goals explicit | ✅ | No live writes; no GitHub; no auto-workspace discovery; no security cert claims |
| Success metrics instrumented + threshold-defined | ✅ | 80% preview-without-edits; <5% structure defects; ≥60% stable external IDs; 0 unintended writes |
| Risks + open questions named | ✅ | Confusion with live sync; missing workspace IDs; sensitive text risk; payload hash format open |
| Approval recorded | ✅ | Product approved; Engineering approved pending technical discovery; GTM requires dry-run framing |

**Readiness verdict: READY for delivery breakdown.** **Non-goals preserved in delivery handoff** below (no live writes; no GitHub; no auto-workspace discovery; no security certification claims).

## Scope Map

| PRD scope area | Delivery epic | Notes |
| --- | --- | --- |
| "Generate Linear dry-run preview…preserve PRD sections" | Epic 1 — Structured Linear Preview | Resolves SUP-002 |
| "Generate Notion dry-run preview…PRD summary / decision log / launch checklist" | Epic 2 — Structured Notion Preview | Mirrors `sample-notion-preview.md` shape |
| "Admin-disabled state…blocks writes…still allows preview generation" | Epic 3 — Tooling Safety + Admin Controls | Release gate; closes CHURN-002 root cause at the control level |
| "Show payload hash, idempotency keys, unresolved target IDs, confirmation requirements" | Epic 3 stories S3.2 / S3.3 / S3.4 + cross-cutting Linear/Notion payload work | Mirrors `sample-linear-preview.md` / `sample-notion-preview.md` Future Write Blockers |

## Epic Map

| Epic | externalId (preview) | Owner |
| --- | --- | --- |
| Epic 1 — Structured Linear Preview | atlasboard-prd-preview-epic-001 | Eng (delivery) |
| Epic 2 — Structured Notion Preview | atlasboard-prd-preview-epic-002 | Eng (delivery) |
| Epic 3 — Tooling Safety + Admin Controls | atlasboard-prd-preview-epic-003 | Eng (platform) |

## Story Set

### Epic 1
- S1.1 (atlasboard-prd-preview-story-001): Preview epics grouped by PRD scope area.
- S1.2 (atlasboard-prd-preview-story-002): Inspect story acceptance criteria before any issue would be created.
- S1.3 (atlasboard-prd-preview-story-003): See dependencies + UNRESOLVED workspace/team/state IDs + future-write blockers.

### Epic 2
- S2.1 (atlasboard-notion-prd-summary-001): Preview Notion PRD summary page.
- S2.2 (atlasboard-notion-decision-log-001): Inspect decision-log entries + source evidence links.
- S2.3 (atlasboard-notion-launch-checklist-001): Preview launch readiness checklist page.

### Epic 3
- S3.1: Admin disable external write actions at workspace.
- S3.2: User sees that previews are not synced records (header chip + first export line).
- S3.3: Reviewer sees confirmation requirements + idempotency keys.
- S3.4: System refuses confirmed live writes + dry-run payloads without confirmation.

## Acceptance Criteria

Includes **edge cases and failure states** explicitly:

- **S1.1:** Section grouping preserved; defect rate <5% on cohort dashboard. *Edge case:* PRDs with empty sections → preview elides them with "blocked: missing evidence" placeholder (no fabrication).
- **S1.2:** AC list, labels, owner placeholder rendered; export `.md`/`.json`. *Failure state:* preview generation failure surfaces stage + reason; never auto-retries against Linear.
- **S1.3:** All `UNRESOLVED_LINEAR_*` IDs surfaced; future-write blockers panel renders.
- **S2.1–S2.3:** Page hierarchy + properties + source-evidence links rendered; `UNRESOLVED_NOTION_*` IDs visible. *Edge case:* `notion` tool with `kind: linear_issue` payload → refuse (`notion-tool-kind-mismatch-negative` must fail).
- **S3.1:** Admin toggle blocks writes within 1s; previews still work; audit-log entry per blocked-write attempt. *Edge case:* stale client → server-side guard authoritative.
- **S3.2:** Every preview header carries "Dry-Run Preview · No <tool> write was performed"; every export's first line carries the same chip.
- **S3.3:** Future-Write Blockers panel renders the 5-item gating list + the 4 negative-fixture refusal requirement.
- **S3.4:** Returns a refusal artifact (not an accepted payload) for all 4 shipped negative fixtures (`linear-live-write-negative`, `linear-dry-run-no-confirmation-negative`, `linear-duplicate-create-negative`, `notion-tool-kind-mismatch-negative`).

Cross-cutting AC: **update preview for existing external IDs** — if an `idempotency_key` already maps, the preview shows an `update` (or `noop`) against the existing external_id, never a duplicate `create`. There is no duplicate issue creation when external ID mapping exists.

## Dependencies

- Epic 2 depends on Epic 1's payload-hash format (shared format for cross-tool diffing).
- Epic 3 (admin disable) is a release gate on any enterprise-evaluable surface.
- All three epics depend on the 4 negative tool-safety fixtures being wired into CI.
- Cross-epic: stable payload hash function (open engineering question — `sample-delivery-handoff`).
- External: PRD parser + section model + preview renderer + workspace resolver stub.

## Linear Dry Run Payloads

```json
{
  "dryRun": true,
  "operation": "linear.issueBatchPreview",
  "mode": "dry_run",
  "tool": "linear",
  "kind": "linear_issue_batch",
  "payloadHash": "sha256:synthetic-workflow-prd-to-linear-001",
  "confirmationRequired": true,
  "workspaceId": "UNRESOLVED_LINEAR_WORKSPACE_ID",
  "teamId": "UNRESOLVED_LINEAR_TEAM_ID",
  "projectId": "UNRESOLVED_LINEAR_PROJECT_ID",
  "stateId": "UNRESOLVED_LINEAR_STATE_ID",
  "labelIds": "UNRESOLVED_LINEAR_LABEL_IDS",
  "externalIdMap": [
    {"localId": "epic-1", "externalId": "atlasboard-prd-preview-epic-001", "operation": "create", "idempotencyKey": "idem-epic-001"},
    {"localId": "story-1.1", "externalId": "atlasboard-prd-preview-story-001", "operation": "create", "idempotencyKey": "idem-story-001"},
    {"localId": "story-1.2", "externalId": "atlasboard-prd-preview-story-002", "operation": "create", "idempotencyKey": "idem-story-002"},
    {"localId": "story-1.3", "externalId": "atlasboard-prd-preview-story-003", "operation": "create", "idempotencyKey": "idem-story-003"},
    {"localId": "epic-2", "externalId": "atlasboard-prd-preview-epic-002", "operation": "create", "idempotencyKey": "idem-epic-002"},
    {"localId": "epic-3", "externalId": "atlasboard-prd-preview-epic-003", "operation": "create", "idempotencyKey": "idem-epic-003"}
  ],
  "duplicatePolicy": "If any idempotency_key already maps to an existing external_id, propose update or noop — never duplicate create.",
  "confirmationQuestion": "Confirm Linear dry-run payload hash sha256:synthetic-workflow-prd-to-linear-001 for team UNRESOLVED_LINEAR_TEAM_ID?"
}
```

This is the **explicit Linear confirmation question** required before any future write. Manual revert only — rollback is not overstated.

## Approval Gates

- **PRD scope additions:** evidence + approval required before requirements.
- **Live external write path:** admin enablement + idempotency check + **explicit Linear confirmation question** answered yes against the **resolved** payload hash; 4/4 negative tool-safety fixtures refuse in CI; manual revert prepared.
- **Enterprise commit:** require V-5 + security package.
- **Pricing commit:** require V-4 result.

## Open Questions

- Stable payload hash format across minor PRD edits (open engineering question — `sample-delivery-handoff`).
- External ID map storage scope for non-test workspaces (workspace vs repo).
- Label/state resolution policy: during preview vs after explicit workspace discovery.

## Next Actions

1. Land SUP-002 fix + cohort defect dashboard.
2. Ship SUP-005 admin disable + audit log entries.
3. Wire 4 negative tool-safety fixtures into CI; assert refusal artifact return.
4. Define canonical payload normalization rule + add regression tests.
5. Hold any "live write" surface until all gates above close.

## Quality Bar

This artifact: provides **PRD completeness review**; preserves **non-goals preserved in delivery handoff**; covers **edge cases and failure states**; includes **update preview for existing external IDs** (no duplicate create when an external ID mapping exists); ends with an **explicit Linear confirmation question**. It includes epics or stories, acceptance criteria, dependencies/open questions, dry-run payloads, and approval gates. Manual revert language only — rollback is not overstated. There are **no implementation-only tasks without user value**, **no unauthorized external mutation**, and **no live Linear write without confirmation**.

**External writes performed: none.**
