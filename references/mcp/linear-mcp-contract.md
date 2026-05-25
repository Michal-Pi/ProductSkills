# Linear MCP Contract

Linear integration is optional and must use preview-before-write behavior.

## Default Flow

1. Convert product scope into epics, stories, tasks, and acceptance criteria.
2. Resolve human-readable team, project, state, and label names to tool IDs before confirmed writes.
3. Build a dry-run issue payload.
4. Validate the payload shape against `schemas/linear-issue.schema.json`.
5. Show the issue list, labels, priorities, owners, and dependencies.
6. Ask for explicit confirmation tied to the idempotency key, dry-run payload hash, and target issue list.
7. Write only after confirmation.
8. Store external IDs for idempotent updates when available.

## Issue Payload Expectations

- `mode`: `dry_run` or `confirmed_write`
- `team_key`: human-readable Linear team key for preview and user confirmation
- `team_id`: resolved Linear team UUID for confirmed writes
- `title`: issue title
- `description`: issue body
- `issue_type`: epic, story, task, bug, or chore
- `priority`: no_priority, low, medium, high, urgent
- `labels`: list of human-readable label names for preview
- `label_ids`: resolved Linear label UUIDs for confirmed writes when labels are used
- `state_id`: resolved Linear workflow state UUID when needed
- `acceptance_criteria`: list of testable criteria; may be empty for epics, but stories, tasks, bugs, and chores need at least one criterion
- `dependencies`: list of related issue references or local IDs
- `idempotency_key`: stable key for reruns
- `dry_run_payload_hash`: required for confirmed writes and must match the previewed payload
- `confirmation_required`: true for dry-run previews
- `confirmation_evidence`: required for confirmed writes; summarize the user's exact approval

## Guardrails

- Never make live Linear writes during evals.
- Never create implementation issues before scope and acceptance criteria are clear.
- Never silently update existing issues; use external ID mapping and preview changes first.
- Never set `mode: confirmed_write` without explicit user approval for the exact payload.
- Never treat team keys, label names, project names, or state names as write-ready IDs. Resolve and preview tool IDs first.
