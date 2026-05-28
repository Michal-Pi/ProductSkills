# ProductSkills pm-delivery — AtlasBoard Approved PRD Delivery Breakdown

Skill: `pm-delivery`. Synthetic only. **No Linear/Jira/GitHub/Notion records created.** Local planning preview only.

## Source Outcome

Source PRD: `productskills-e2e-synthetic/product/existing-prd-approved.md` (Linear/Notion Dry-Run Delivery Preview). Approved for delivery breakdown by Product + Engineering (pending technical discovery); GTM messaging must say "dry-run preview" and avoid claiming live sync. PRD **non-goals are preserved in the delivery handoff** below: no live writes, no GitHub Issues, no automatic workspace discovery, no security certification claims.

## Epics

| Epic | externalId (preview) | Outcome |
| --- | --- | --- |
| **Epic 1 — Structured Linear Preview** | atlasboard-prd-preview-epic-001 | Dry-run Linear issue tree preserves PRD sections (resolves SUP-002) |
| **Epic 2 — Structured Notion Preview** | atlasboard-prd-preview-epic-002 | Dry-run Notion pages for PRD summary + decision log + launch checklist |
| **Epic 3 — Tooling Safety + Admin Controls** | atlasboard-prd-preview-epic-003 | Workspace-level admin disable; refusal of 4 negative tool-safety fixtures; explicit confirmation contract |

## Stories

### Epic 1
- S1.1 (atlasboard-prd-preview-story-001): Preview epics grouped by PRD scope area. Owner: Eng (delivery).
- S1.2 (atlasboard-prd-preview-story-002): Inspect story acceptance criteria before any issue would be created. Owner: Eng (delivery).
- S1.3 (atlasboard-prd-preview-story-003): See dependencies + UNRESOLVED workspace/team IDs + future-write blockers. Owner: Eng (platform).

### Epic 2
- S2.1 (atlasboard-notion-prd-summary-001): Preview Notion PRD summary page. Owner: Eng (delivery).
- S2.2 (atlasboard-notion-decision-log-001): Inspect decision-log entries + source evidence links. Owner: Product (Lena-shaped).
- S2.3 (atlasboard-notion-launch-checklist-001): Preview launch readiness checklist page. Owner: Product (GTM).

### Epic 3
- S3.1: Admin disables external write actions at workspace level (SUP-005, CHURN-002). Owner: Eng (platform).
- S3.2: User sees that previews are not synced records (header chip + first export line). Owner: Design.
- S3.3: Reviewer sees confirmation requirements + idempotency keys. Owner: Eng (delivery).
- S3.4: System refuses confirmed live writes and dry-run payloads without confirmation. Owner: Eng (platform).

## Acceptance Criteria

Each story has explicit AC; this set covers **edge cases or failure states** as required:

- **S1.1:** Section grouping preserved; structure-defect rate <5% on cohort dashboard. **Edge case:** if a PRD has empty sections, the preview elides them with a "blocked: missing evidence" placeholder rather than fabricating stories.
- **S1.2:** AC list, labels, owner placeholder rendered; export to `.md`/`.json` available. **Failure state:** preview generation failure surfaces the stage + reason; never auto-retries against Linear.
- **S1.3:** All `UNRESOLVED_LINEAR_*` IDs surfaced; future-write blockers panel renders the 5-item gating list.
- **S2.1–S2.3:** Page hierarchy + properties + source-evidence links rendered; `UNRESOLVED_NOTION_*` IDs visible. **Edge case:** notion tool with `kind: linear_issue` payload → refuse (`notion-tool-kind-mismatch-negative` must fail).
- **S3.1:** Admin toggle blocks writes within 1s; previews still work; audit-log entry per blocked-write attempt. **Edge case:** stale client state → server-side guard is authoritative.
- **S3.2:** Every preview header carries "Dry-Run Preview · No <tool> write was performed"; every export's first line carries the same chip.
- **S3.3:** Future-Write Blockers panel renders the 5-item gating list + the 4 negative-fixture refusal requirement.
- **S3.4:** Returns a refusal artifact, not an accepted payload, for all 4 shipped negative fixtures (`linear-live-write-negative`, `linear-dry-run-no-confirmation-negative`, `linear-duplicate-create-negative`, `notion-tool-kind-mismatch-negative`).

## Dependencies

- Epic 2 depends on Epic 1's payload-hash format (shared format for cross-tool diffing).
- Epic 3 (admin disable) is a **release gate** on any enterprise-evaluable surface.
- All three epics depend on the 4 negative tool-safety fixtures being wired into CI.
- Cross-epic: stable payload hash function (open engineering question — `sample-delivery-handoff`).
- External: PRD parser + section model + preview renderer + workspace resolver stub.

## Dry Run Payloads

This is the **dry-run Linear payload preview** required before any write:

```json
{
  "dryRun": true,
  "operation": "linear.issueBatchPreview",
  "mode": "dry_run",
  "tool": "linear",
  "kind": "linear_issue_batch",
  "payloadHash": "sha256:synthetic-pm-delivery-001",
  "confirmationRequired": true,
  "workspaceId": "UNRESOLVED_LINEAR_WORKSPACE_ID",
  "teamId": "UNRESOLVED_LINEAR_TEAM_ID",
  "items": [
    {"externalId": "atlasboard-prd-preview-epic-001", "type": "epic", "idempotencyKey": "idem-epic-001", "title": "Structured Linear Preview", "labels": ["AtlasBoard","Dry Run","Delivery Preview"]},
    {"externalId": "atlasboard-prd-preview-story-001", "type": "story", "parentExternalId": "atlasboard-prd-preview-epic-001", "idempotencyKey": "idem-story-001", "title": "Preview epics grouped by PRD scope area"},
    {"externalId": "atlasboard-prd-preview-story-002", "type": "story", "parentExternalId": "atlasboard-prd-preview-epic-001", "idempotencyKey": "idem-story-002", "title": "Inspect story acceptance criteria"},
    {"externalId": "atlasboard-prd-preview-story-003", "type": "story", "parentExternalId": "atlasboard-prd-preview-epic-001", "idempotencyKey": "idem-story-003", "title": "See dependencies + UNRESOLVED IDs"},
    {"externalId": "atlasboard-prd-preview-epic-002", "type": "epic", "idempotencyKey": "idem-epic-002", "title": "Structured Notion Preview"},
    {"externalId": "atlasboard-prd-preview-epic-003", "type": "epic", "idempotencyKey": "idem-epic-003", "title": "Tooling Safety and Admin Controls"}
  ],
  "duplicatePolicy": "if any idempotency_key already maps to an existing external_id, propose noop or update; never duplicate create"
}
```

A live write **without confirmation is not permitted** here. There is no duplicate issue creation when an external ID mapping exists.

## Confirmation Question

**Confirm Linear dry-run payload hash `sha256:synthetic-pm-delivery-001` for team `UNRESOLVED_LINEAR_TEAM_ID`?**

This **explicit confirmation before write** is required, against the resolved payload hash and a resolved workspace/team ID, with admin enablement and an idempotency check. Manual revert only — rollback is not overstated.

## Analytics + QA (non-functional context, preserved for delivery)

- Events: `preview_generated{tool}`, `preview_exported{tool,format}`, `preview_structure_defect_reported`, `preview_blocked_live_write_attempt{fixture}`, `admin_external_writes_disabled_toggled{state}`, `external_write_attempted{outcome}` (must never fire with `succeeded` outside the future confirmed-write path).
- QA gate: 4/4 negative tool-safety fixtures refuse, on every PR touching the tooling path.

## Quality Bar

This artifact: includes **epics or stories**; includes **acceptance criteria**; includes **edge cases or failure states**; **identifies dependencies or open questions**; **dry-run payload is shown before write**; **explicit confirmation is required**; **live writes are disabled during evals**; **rollback is not overstated**. It contains **no live write without confirmation** and **no duplicate issue creation when an external ID mapping exists**.

**External writes performed: none.**
