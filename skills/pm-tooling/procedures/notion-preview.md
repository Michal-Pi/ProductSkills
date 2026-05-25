# Notion Preview

Use when preparing a Notion page or database update.

## Steps

1. Build payload according to `../../../references/mcp/notion-mcp-contract.md` and `../../../references/methods/tooling-dry-run.md`.
2. Validate against `../../../schemas/notion-page.schema.json` conceptually or with available validators.
3. Show title, target, properties, blocks, and source artifact.
4. Ask for explicit user confirmation tied to the target, idempotency key, and dry-run payload hash before any live write.
5. If writing is confirmed, preserve external IDs for future idempotent updates when available.

## Output

Return dry-run payload, validation notes, dry-run payload hash, confirmation question, and manual fallback.
