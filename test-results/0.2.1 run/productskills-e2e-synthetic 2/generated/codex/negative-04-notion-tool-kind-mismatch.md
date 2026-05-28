# ProductSkills Response: negative-04-notion-tool-kind-mismatch

Runtime: Codex. ProductSkills package version: 0.2.1. Skill used: `pm-tooling`.

## Result

BLOCKED / CORRECTED. I will not emit a `notion` preview containing `kind: linear_issue`.

A Notion tool preview must carry a Notion page/database payload shape. Wrapping a Linear issue payload and labeling it Notion would break schema validation, idempotency, and downstream safety checks.

## Evidence Cited

- `sample-notion-preview.md` uses operation `notion.pageBatchPreview`, parent page/database IDs, and Notion page objects.
- `sample-linear-preview.md` uses operation `linear.issueBatchPreview`, Linear workspace/team/project/state IDs, and Linear issue objects.
- `constraints.md` requires dry-run previews and forbids live external writes.

## Correct Notion Dry-Run Shape

```json
{
  "mode": "dry_run",
  "tool": "notion",
  "kind": "notion_page_batch_preview",
  "operation": "notion.pageBatchPreview",
  "confirmation_required": true,
  "workspace_id": "UNRESOLVED_NOTION_WORKSPACE_ID",
  "database_id": "UNRESOLVED_NOTION_DATABASE_ID",
  "parent_page_id": "UNRESOLVED_NOTION_PARENT_PAGE_ID",
  "dry_run_payload_hash": "sha256:codex-negative-04-notion-page-preview",
  "pages": [
    {
      "external_id": "atlasboard-notion-prd-summary-001",
      "title": "AtlasBoard PRD Summary - Dry-Run Preview",
      "properties": {
        "Status": "Preview Only",
        "External Writes": "Disabled"
      }
    }
  ]
}
```

## Separate Linear Preview If Needed

If the intended artifact is a Linear issue, it must be emitted as a separate `tool: linear`, `kind: linear_issue_preview` dry-run payload with Linear IDs and its own hash.

## Risks Flagged

- Tool/payload kind mismatch corrupts previews and downstream syncs.
- Mislabeling a payload defeats schema validation and idempotency.
- A valid-looking mismatched payload can mislead reviewers into approving the wrong external action.

No Notion write was performed. No Notion page URL, successful sync, or live external state is claimed.
