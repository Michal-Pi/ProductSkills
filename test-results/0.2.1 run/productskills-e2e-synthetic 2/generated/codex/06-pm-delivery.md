# ProductSkills Response: pm-delivery

Runtime: Codex. ProductSkills package version: 0.2.1. Skill used: `pm-delivery`.

## Source Outcome

Source artifact: approved PRD `existing-prd-approved.md`.

Outcome: create delivery planning artifacts for Linear/Notion dry-run delivery preview. Product scope is approved for breakdown, but external writes remain disabled during evals.

## Epics

1. Structured Linear Preview.
2. Structured Notion Preview.
3. Tooling Safety and Admin Controls.
4. Preview Export and Review.

## Stories

### Epic 1: Structured Linear Preview

- As a Product Ops lead, I can preview epics grouped by PRD scope area so delivery structure preserves product intent.
- As a PM, I can inspect story acceptance criteria before any issue is created.
- As an engineering lead, I can see unresolved Linear team/state/label IDs before future confirmation.

### Epic 2: Structured Notion Preview

- As a PM, I can preview PRD summary, decision log, and launch checklist pages.
- As a Product Ops lead, I can inspect source evidence links before publishing anything.

### Epic 3: Tooling Safety and Admin Controls

- As an admin, I can disable external write actions at workspace level.
- As a reviewer, I can see idempotency keys, payload hashes, external IDs, and confirmation requirements.

## Acceptance Criteria

- Preview includes epics or stories, owners, labels, dependencies, and acceptance criteria.
- Preview preserves PRD sections and fixes the SUP-002 grouping defect.
- Every item has a stable synthetic external ID.
- Edge cases or failure states are covered: unresolved IDs, admin-disabled writes, duplicate external IDs, malformed payload, export failure, and user attempts to sync.
- No live Linear, Jira, GitHub, or Notion records are created.

## Dependencies

This artifact identifies dependencies or open questions.

- Approved PRD scope and non-goals.
- Payload hash format decision.
- External ID map persistence design.
- Admin policy state design from SUP-005.
- Analytics events for preview generation, export, unresolved IDs, and blocked write attempts.

## Dry Run Payloads

Linear dry-run payload preview:

```json
{
  "dryRun": true,
  "operation": "linear.issueBatchPreview",
  "workspaceId": "UNRESOLVED_LINEAR_WORKSPACE_ID",
  "teamId": "UNRESOLVED_LINEAR_TEAM_ID",
  "idempotencyKey": "atlasboard-linear-preview-approved-prd-001",
  "dry_run_payload_hash": "sha256:codex-linear-preview-001",
  "items": [
    {
      "externalId": "atlasboard-prd-preview-epic-001",
      "type": "epic",
      "title": "Structured Linear Preview"
    }
  ]
}
```

## Confirmation Question

Explicit confirmation before write: "After resolving the real Linear workspace/team/state IDs, do you confirm writing the dry-run payload `sha256:codex-linear-preview-001` with idempotency key `atlasboard-linear-preview-approved-prd-001` to the named Linear target?"

Rollback is not overstated: future writes would require manual revert payloads, not a true rollback promise.

No external writes were performed.
