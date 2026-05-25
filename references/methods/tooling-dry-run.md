# Tooling Dry-Run Conventions

Use dry-run payloads for any Notion, Linear, roadmap, sprint, or external tool workflow.

## Required Dry-Run Fields

- `mode`: `dry_run`
- `source_artifact`
- `target`
- `operation`: create, update, archive, link, or no-op
- `payload`
- `validation`
- `idempotency_key`
- `dry_run_payload_hash`
- `confirmation_required`: true

## Confirmed Write Fields

Only after the user approves the exact preview, a write payload may use:

- `mode`: `confirmed_write`
- `confirmation_required`: false
- `confirmation_evidence`: concise record of the user's approval
- `dry_run_payload_hash`: hash or stable identifier for the previewed payload

## Preview Standard

Before any write, show:

- Target workspace, database, team, project, or parent object
- Objects to create or update
- Fields that will change
- Missing required identifiers
- Validation warnings
- Manual fallback
- Confirmation question

## Idempotency

Use stable local IDs from artifact title, source path, or explicit artifact ID. If `.product-os/external-id-map.json` has a mapping, preview an update instead of a create.

Store workspace conventions in `.product-os/workspace.json` using `schemas/product-os-workspace.schema.json`. Store external mappings in `.product-os/external-id-map.json` using `schemas/external-id-map.schema.json`. Never store API tokens, secrets, or credentials in either file.

## Batch Safety

- Preview the full batch first.
- After each confirmed write, update the external ID map before issuing the next write.
- On partial failure, report completed, skipped, failed, and retryable items.
- Provide manual revert payloads without claiming true rollback.
