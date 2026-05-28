# Dry-Run Preview — Canonical Safety Contract

> This is the **canonical** safety contract for any external write (Notion, Linear, or other tool MCP). If a SKILL.md `## Safety summary` block and this document disagree, this document wins. Consolidates the procedures previously held under `skills/pm-tooling/`.

## The five rules

1. **Preview before write.** No external write proceeds without a dry-run payload shown to the user first.
2. **Explicit confirmation tied to the exact payload.** Confirmation must reference the `idempotency_key` and `dry_run_payload_hash` of the previewed payload. Generic "yes go ahead" is not confirmation.
3. **`idempotency_key` is required for every confirmed write.** Re-running the same operation with the same key must be safe (update an existing target, not create a duplicate).
4. **Resolve display names to IDs before confirmed writes.** Team keys, label names, project names, workspace names, page titles, and state names are not write-ready identifiers. Resolve to the tool's UUID/ID and preview both forms.
5. **Never claim rollback.** Provide a manual revert payload instead. External tools may not support transactional rollback; do not imply they do.

## Default flow (every write)

1. **Workspace bootstrap.** Establish workspace, database, team, project identifiers. If `.product-os/workspace.json` is missing, return a safe bootstrap preview with `version: 1` and an empty `workspaces` list; record conventions only after user confirms exact content. Never store API tokens, secrets, or credentials in `.product-os/workspace.json`.
2. **External-ID check.** Before any create, check `.product-os/external-id-map.json` for a matching local-ID → external-ID mapping. If a mapping exists, preview an **update**, not a create.
3. **Tool-ID resolution.** Resolve every display name to its tool ID. List unresolved names explicitly. Stop and ask the user if any required ID is missing or ambiguous.
4. **Build dry-run payload.** Required fields (from `references/methods/tooling-dry-run.md`):
   - `mode: dry_run`
   - `source_artifact`
   - `target`
   - `operation: create | update | archive | link | no-op`
   - `payload`
   - `validation`
   - `idempotency_key`
   - `dry_run_payload_hash`
   - `confirmation_required: true`
5. **Validate payload shape** against the per-tool schema:
   - Notion: `schemas/notion-page.schema.json` — see `references/mcp/notion-mcp-contract.md` for fields.
   - Linear: `schemas/linear-issue.schema.json` — see `references/mcp/linear-mcp-contract.md` for fields.
6. **Show the user the preview.** Include: target object, fields that will change, missing required identifiers, validation warnings, manual fallback, confirmation question.
7. **Get explicit confirmation tied to the preview.** Confirmation must reference the `idempotency_key` AND the `dry_run_payload_hash`.
8. **Write only after confirmation.** Confirmed-write payload must have:
   - `mode: confirmed_write`
   - `confirmation_required: false`
   - `confirmation_evidence: <concise record of the user's exact approval>`
   - `dry_run_payload_hash: <matches the previewed payload hash>`
9. **Record external IDs** after each confirmed write to `.product-os/external-id-map.json`. Update the map before issuing the next write in a batch.

## Batch safety

- **Preview the full batch first** before any write.
- **After each confirmed write in a batch, update the external-ID map before the next write.** A mid-batch failure that did not update the map causes the next run to create duplicates.
- **On partial failure, report** completed, skipped, failed, and retryable items.
- **Provide manual revert payloads.** Do not claim true rollback.

## Tool-ID resolution detail

Display names are not write-ready. Before any confirmed write that depends on tool-specific IDs:

- **Linear:** resolve `team_key` → `team_id`, `label_name` → `label_id`, `workflow_state_name` → `state_id`, `project_name` → `project_id`, `owner_email_or_handle` → `owner_id`.
- **Notion:** resolve `workspace_name` → `workspace_id`, `database_name` → `database_id`, `parent_page_title` → `parent_page_id`, target page title → page ID (if updating an existing page).
- Include both the display name and the resolved ID in the dry-run preview.
- If an ID is missing or ambiguous, **stop and ask** for the exact target or provide setup instructions. Never guess.

## External-ID map (idempotency)

- Every local artifact gets a stable local ID derived from artifact title, source path, or explicit artifact ID.
- Validate the map shape against `schemas/external-id-map.schema.json`.
- Before any create, check the map. If a mapping exists, preview an **update** instead of a create.
- After each confirmed write, **record** the external ID and source-artifact reference in the map **before** issuing the next write.
- Never store API tokens, secrets, or credentials in `.product-os/external-id-map.json`.
- For batch operations, checkpoint progress and surface partial failures.

## Workspace bootstrap detail

Before preparing any Notion or Linear writes for a workspace:

1. Ask for or discover workspace, database, team, and project identifiers.
2. Validate workspace shape against `schemas/product-os-workspace.schema.json`.
3. If no workspace file exists, return a safe bootstrap preview for `.product-os/workspace.json` with `version: 1` and an empty or user-confirmed `workspaces` list.
4. Record conventions in `.product-os/workspace.json` only after the user confirms the exact content.
5. Never store API tokens, secrets, or credentials in the workspace file.
6. Never guess IDs when multiple targets are plausible — stop and ask.
7. If MCP tools are unavailable, produce setup instructions and dry-run payloads for manual use.

## Per-tool contracts

For payload field expectations and per-tool guardrails (the field list, the schema reference, the per-tool `Never...` clauses), read:

- **Notion:** `references/mcp/notion-mcp-contract.md`
- **Linear:** `references/mcp/linear-mcp-contract.md`
- **Conventions shared across tools:** `references/methods/tooling-dry-run.md` (preview standard, idempotency, batch safety)

## When this contract is invoked

Two workflows are responsible for honoring this contract:

- **`workflow-prd-to-linear-delivery`** — Linear writes for delivery artifacts (epics, stories, tasks).
- **`workflow-discovery-to-prd`** — optional Notion page previews for evidence-backed PRDs.

Both workflows' SKILL.md MUST carry a `## Safety summary` block reproducing the five rules at the top of this document; this reference is the canonical version they cite. If either workflow's safety summary and this reference diverge, **this reference wins** and the workflow's summary is the bug.

## Quality bar

A confirmed-write payload is acceptable only when ALL of the following hold:

- `mode == "confirmed_write"`
- `confirmation_required == false`
- `confirmation_evidence` is a non-empty record of the user's approval
- `dry_run_payload_hash` matches the hash of the previewed payload
- Every required ID is resolved (no display names in write fields)
- `idempotency_key` is present and stable
- The previewed payload was shown to the user before this confirmed payload was constructed
- The external-ID map has been checked (and, after the write, will be updated before any subsequent write)

If any condition fails, **refuse** and surface a `blocked-workflow` envelope (`schemas/blocked-workflow.schema.json`) describing the missing precondition.
