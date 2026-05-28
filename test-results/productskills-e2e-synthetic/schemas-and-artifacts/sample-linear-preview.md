# Sample Linear Preview

Dry-run only. No Linear issues were created.

## Unresolved Workspace Context

- Linear workspace ID: `UNRESOLVED_LINEAR_WORKSPACE_ID`
- Linear team ID: `UNRESOLVED_LINEAR_TEAM_ID`
- Linear project ID: `UNRESOLVED_LINEAR_PROJECT_ID`
- Default state ID: `UNRESOLVED_LINEAR_STATE_ID`

## External ID Map Preview

| External ID | Object Type | Source |
| --- | --- | --- |
| atlasboard-prd-preview-epic-001 | Linear epic/project | Approved PRD scope: Structured Linear Preview |
| atlasboard-prd-preview-story-001 | Linear issue | Preview preserves PRD sections |
| atlasboard-prd-preview-story-002 | Linear issue | Inspect acceptance criteria |
| atlasboard-prd-preview-epic-002 | Linear epic/project | Structured Notion Preview |
| atlasboard-prd-preview-epic-003 | Linear epic/project | Tooling Safety and Admin Controls |

## Payload Preview

```json
{
  "dryRun": true,
  "operation": "linear.issueBatchPreview",
  "payloadHash": "sha256:synthetic-linear-preview-001",
  "confirmationRequired": true,
  "workspaceId": "UNRESOLVED_LINEAR_WORKSPACE_ID",
  "teamId": "UNRESOLVED_LINEAR_TEAM_ID",
  "items": [
    {
      "externalId": "atlasboard-prd-preview-epic-001",
      "type": "epic",
      "title": "Structured Linear Preview",
      "description": "Generate a dry-run Linear issue tree that preserves PRD sections.",
      "labels": ["AtlasBoard", "Dry Run", "Delivery Preview"]
    },
    {
      "externalId": "atlasboard-prd-preview-story-001",
      "type": "story",
      "parentExternalId": "atlasboard-prd-preview-epic-001",
      "title": "Preview epics grouped by PRD scope area",
      "acceptanceCriteria": [
        "Preview includes epics, stories, acceptance criteria, labels, dependencies, and owners.",
        "Every item has a stable synthetic external ID.",
        "No live Linear write is performed."
      ]
    }
  ]
}
```

## Future Write Blockers

- Resolve real workspace/team/state/label IDs.
- Confirm exact payload and hash.
- Confirm admin permits external writes.
- Persist external ID map.
- Run idempotency check.
