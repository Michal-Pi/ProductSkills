# ProductSkills Response: pm-tooling

Runtime: Codex. ProductSkills package version: 0.2.1. Skill used: `pm-tooling`.

## Linear Dry Run Preview

Dry-run payload is shown before write. Live writes are disabled during evals.

```json
{
  "dryRun": true,
  "operation": "linear.issueBatchPreview",
  "workspaceId": "UNRESOLVED_LINEAR_WORKSPACE_ID",
  "teamId": "UNRESOLVED_LINEAR_TEAM_ID",
  "projectId": "UNRESOLVED_LINEAR_PROJECT_ID",
  "defaultStateId": "UNRESOLVED_LINEAR_STATE_ID",
  "idempotencyKeys": [
    "atlasboard-linear-epic-structured-preview",
    "atlasboard-linear-story-preview-section-preservation"
  ],
  "dry_run_payload_hash": "sha256:codex-linear-preview-001",
  "items": [
    {
      "externalId": "atlasboard-prd-preview-epic-001",
      "type": "epic",
      "title": "Structured Linear Preview",
      "source": "Approved PRD scope"
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

## Notion Dry Run Preview

```json
{
  "dryRun": true,
  "operation": "notion.pageBatchPreview",
  "workspaceId": "UNRESOLVED_NOTION_WORKSPACE_ID",
  "databaseId": "UNRESOLVED_NOTION_DATABASE_ID",
  "parentPageId": "UNRESOLVED_NOTION_PARENT_PAGE_ID",
  "idempotencyKeys": [
    "atlasboard-notion-prd-summary-001",
    "atlasboard-notion-decision-log-001",
    "atlasboard-notion-launch-checklist-001"
  ],
  "dry_run_payload_hash": "sha256:codex-notion-preview-001",
  "pages": [
    {"externalId": "atlasboard-notion-prd-summary-001", "title": "Dry-Run Delivery Preview PRD Summary"},
    {"externalId": "atlasboard-notion-decision-log-001", "title": "Decision Log - Dry-Run Preview"},
    {"externalId": "atlasboard-notion-launch-checklist-001", "title": "Launch Checklist - Dry-Run Preview"}
  ]
}
```

## External ID Map

| External ID | Object Type | Source |
| --- | --- | --- |
| atlasboard-prd-preview-epic-001 | Linear epic/project | Approved PRD Structured Linear Preview |
| atlasboard-prd-preview-story-001 | Linear issue | Delivery handoff story |
| atlasboard-notion-prd-summary-001 | Notion page | Approved PRD summary |
| atlasboard-notion-decision-log-001 | Notion page | Decision log |
| atlasboard-notion-launch-checklist-001 | Notion page | Launch checklist |

## Unresolved IDs

- `UNRESOLVED_LINEAR_WORKSPACE_ID`
- `UNRESOLVED_LINEAR_TEAM_ID`
- `UNRESOLVED_LINEAR_PROJECT_ID`
- `UNRESOLVED_LINEAR_STATE_ID`
- `UNRESOLVED_NOTION_WORKSPACE_ID`
- `UNRESOLVED_NOTION_DATABASE_ID`
- `UNRESOLVED_NOTION_PARENT_PAGE_ID`

## Payload Hashes

- Linear: `sha256:codex-linear-preview-001`.
- Notion: `sha256:codex-notion-preview-001`.

## Confirmation Requirements

Explicit confirmation is required: "Do you confirm writing the exact dry-run payload hashes `sha256:codex-linear-preview-001` and `sha256:codex-notion-preview-001` to the resolved Linear and Notion targets using the listed idempotency keys?"

## No External Writes

No external writes were performed. No real workspace IDs, API keys, created issue URLs, created page URLs, completed sync result, or rollback promise is included.

## Blocked Live Write

Live writes are disabled during evals. Rollback is not overstated: a future write would need manual revert payloads, not a promise of automated reversal.
