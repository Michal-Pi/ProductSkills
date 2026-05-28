# Sample Notion Preview

Dry-run only. No Notion pages or databases were created.

## Unresolved Workspace Context

- Notion workspace ID: `UNRESOLVED_NOTION_WORKSPACE_ID`
- Product docs database ID: `UNRESOLVED_NOTION_DATABASE_ID`
- Parent page ID: `UNRESOLVED_NOTION_PARENT_PAGE_ID`

## Page Preview

```json
{
  "dryRun": true,
  "operation": "notion.pageBatchPreview",
  "payloadHash": "sha256:synthetic-notion-preview-001",
  "confirmationRequired": true,
  "parentPageId": "UNRESOLVED_NOTION_PARENT_PAGE_ID",
  "pages": [
    {
      "externalId": "atlasboard-notion-prd-summary-001",
      "title": "AtlasBoard Dry-Run Delivery Preview PRD Summary",
      "properties": {
        "Status": "Preview Only",
        "Owner": "Synthetic Product Ops",
        "Release": "Dry-Run Delivery Preview"
      },
      "sections": [
        "Objective",
        "Evidence",
        "Scope",
        "Non-Goals",
        "Risks",
        "Open Questions"
      ]
    },
    {
      "externalId": "atlasboard-notion-decision-log-001",
      "title": "Decision Log - Dry-Run Preview",
      "properties": {
        "Decision": "Proceed with preview-only release planning",
        "Source": "Synthetic PRD"
      }
    },
    {
      "externalId": "atlasboard-notion-launch-checklist-001",
      "title": "Launch Checklist - Dry-Run Preview",
      "properties": {
        "Launch Status": "Conditional",
        "External Writes": "Disabled"
      }
    }
  ]
}
```

## Future Write Blockers

- Resolve real workspace/database/page IDs.
- Confirm exact payload and hash.
- Verify admin permits external writes.
- Persist external ID map.
- No true rollback is available; prepare manual revert payloads for future writes.
