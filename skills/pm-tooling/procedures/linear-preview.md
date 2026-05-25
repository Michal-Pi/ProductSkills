# Linear Preview

Use when preparing Linear epics, stories, tasks, or bugs.

## Steps

1. Convert delivery work into issue payloads using `../../../templates/linear-delivery-handoff.md`.
2. Build payloads according to `../../../references/mcp/linear-mcp-contract.md` and `../../../references/methods/tooling-dry-run.md`.
3. Use `tool-id-resolution.md` to mark any unresolved team, label, state, project, or owner IDs before confirmed writes.
4. Validate required fields, labels, priorities, dependencies, and acceptance criteria. Epics may have empty acceptance criteria; stories, tasks, bugs, and chores need testable criteria.
5. Show a dry-run issue list.
6. Ask for explicit user confirmation tied to the issue list, idempotency key, and dry-run payload hash before any live write.
7. Preserve external IDs for idempotent updates when available.

## Output

Return dry-run payloads, validation notes, dry-run payload hash, confirmation question, and manual fallback.
