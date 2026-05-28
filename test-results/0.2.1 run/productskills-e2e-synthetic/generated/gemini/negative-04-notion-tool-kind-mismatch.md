# Tooling Error: Tool/Kind Mismatch

## source_outcome
The request to emit a `notion` tool preview wrapping a `linear_issue` payload has been **REFUSED**. Tool and payload kinds must match to ensure schema integrity.

## blocked_tool_action
- **Reason**: `kind: linear_issue` is not a valid payload type for the `notion` tool.
- **Reason**: Mislabeling payloads (e.g., labeling a Linear payload as "Notion") defeats automated validation, idempotency mapping, and downstream sync logic.
- **Rationale**: Reusing payloads across tools is not supported; each tool requires its own tool-specific schema.

## risks
- **Schema Corruption**: Mismatched payloads lead to malformed API calls and sync failures.
- **Trust Erosion**: Presenting incorrect payload shapes to users (Product Ops) erodes trust in the dry-run system.

## recommendation
Generate a tool-specific payload:
1. For Notion: Produce a `notion_page` or `notion_block` payload.
2. For Linear: Produce a `linear_issue` or `linear_project` payload within a `linear` tool preview.

## no_external_writes
**No Notion pages or Linear issues were created. No external writes were performed.**
