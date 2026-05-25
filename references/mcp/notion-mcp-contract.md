# Notion MCP Contract

Notion integration is optional and must be safe by default.

## Default Flow

1. Discover or receive the target workspace, database, or page.
2. Build a dry-run payload.
3. Validate the payload shape against `schemas/notion-page.schema.json`.
4. Show the user the proposed write.
5. Ask for explicit confirmation tied to the idempotency key or target page/database.
6. Write only after confirmation.
7. Record external IDs for idempotent updates when available.

## Payload Expectations

- `mode`: `dry_run` or `confirmed_write`
- `target`: workspace, database, or parent page identifier
- `title`: page title
- `properties`: database properties or page metadata
- `blocks`: ordered content blocks
- `source_artifact`: local artifact or source summary
- `idempotency_key`: stable key for reruns
- `dry_run_payload_hash`: required for confirmed writes and must match the previewed payload
- `confirmation_required`: true for dry-run previews
- `confirmation_evidence`: required for confirmed writes; summarize the user's exact approval

## Guardrails

- Never make live Notion writes during evals.
- Never infer a workspace ID when multiple targets are plausible.
- Never claim rollback. Provide a manual revert plan instead.
- If the MCP tool is unavailable, return the validated payload for manual use.
- Never set `mode: confirmed_write` without explicit user approval for the exact payload.
