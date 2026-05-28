# ProductSkills Response: workflow-prd-to-linear-delivery

Runtime: Codex. ProductSkills package version: 0.2.1. Workflow used: `workflow-prd-to-linear-delivery`.

## PRD Readiness Review

Source PRD: approved Linear/Notion Dry-Run Delivery Preview.

Readiness: passes delivery breakdown because it includes objective, customer, evidence, scope, non-goals, success metrics, risks, open questions, and approval. Validation-not-required rationale: the artifact is approved for delivery planning, but unresolved assumptions remain in the handoff.

## Scope Map

- Structured Linear preview with epics, stories, acceptance criteria, labels, owners, dependencies, and external IDs.
- Structured Notion preview with PRD summary, decision log, launch checklist, source evidence links, and page hierarchy.
- Tooling safety with payload hashes, idempotency keys, unresolved IDs, confirmation requirements, and admin-disabled state.
- Non-goals preserved in delivery handoff: no live writes, no GitHub Issues support, no automatic workspace discovery, no security certification claims.

## Epic Map

1. Structured Linear Preview.
2. Structured Notion Preview.
3. Tooling Safety and Admin Controls.

## Story Set

- As a Product Ops lead, I can preview epics grouped by PRD scope area.
- As a PM, I can inspect story acceptance criteria before issue creation.
- As an engineering lead, I can see unresolved IDs and dependencies before future sync.
- As an admin, I can disable external write actions.
- As a reviewer, I can export preview artifacts for review.

## Acceptance Criteria

- Preview includes epics or stories, acceptance criteria, labels, dependencies, and owners.
- Edge cases and failure states include unresolved workspace/team/state IDs, admin-disabled writes, duplicate external IDs, malformed payloads, export failure, and user attempts to write without confirmation.
- Existing external IDs use update preview for existing external IDs rather than duplicate issue creation.
- No implementation-only tasks without user value are included.

## Dependencies

- Payload hash stability decision.
- External ID map storage and idempotency design.
- Admin-disabled write-state behavior.
- QA coverage for SUP-002 preview section preservation and SUP-005 admin controls.

## Linear Dry Run Payloads

```json
{
  "dryRun": true,
  "operation": "linear.issueBatchPreview",
  "workspaceId": "UNRESOLVED_LINEAR_WORKSPACE_ID",
  "teamId": "UNRESOLVED_LINEAR_TEAM_ID",
  "stateId": "UNRESOLVED_LINEAR_STATE_ID",
  "idempotencyKey": "atlasboard-prd-to-linear-preview-001",
  "dry_run_payload_hash": "sha256:codex-prd-to-linear-001",
  "items": [
    {
      "externalId": "atlasboard-prd-preview-epic-001",
      "type": "epic",
      "title": "Structured Linear Preview"
    },
    {
      "externalId": "atlasboard-prd-preview-story-001",
      "type": "story",
      "parentExternalId": "atlasboard-prd-preview-epic-001",
      "title": "Preview epics grouped by PRD scope area"
    }
  ]
}
```

## Approval Gates

- Explicit Linear confirmation question before any future write.
- Resolve real Linear workspace/team/state IDs.
- Confirm admin permits external writes.
- Confirm exact dry-run payload hash and idempotency key.
- Persist external ID map.

## Open Questions

- Which payload fields are mandatory for a future write?
- Should labels be resolved during preview or only after workspace discovery?
- What hash format remains stable across minor edits?

## Next Actions

Generate local preview artifacts, run QA for structure preservation, and keep all Linear behavior dry-run only.

Explicit Linear confirmation question: "Do you confirm writing dry-run payload `sha256:codex-prd-to-linear-001` to the resolved Linear target using idempotency key `atlasboard-prd-to-linear-preview-001`?"

Rollback is not overstated: future writes would require manual revert payloads, not a true rollback promise.

No external writes were performed.
