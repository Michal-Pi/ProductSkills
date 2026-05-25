---
name: pm-tooling
description: Product tooling workflows for Notion and Linear MCP integration, workspace discovery, safe artifact sync, Linear issue planning, Notion page creation, roadmap sync, external ID mapping, idempotent updates, and preview-before-write. Use when the user asks to create, update, preview, or sync Notion pages, Linear issues, roadmap databases, sprint plans, or external tool payloads.
---

# PM Tooling

Sync product artifacts into tools safely.

## Core Procedures

- Use `procedures/workspace-bootstrap.md` before writes or sync setup.
- Use `procedures/notion-preview.md` for Notion dry-run payloads.
- Use `procedures/linear-preview.md` for Linear dry-run payloads.
- Use `procedures/tool-id-resolution.md` before confirmed writes that require workspace, team, label, state, database, or page IDs.
- Use `procedures/external-id-map.md` for idempotent update planning.

## References

- Use `../../references/mcp/notion-mcp-contract.md` for Notion payload behavior.
- Use `../../references/mcp/linear-mcp-contract.md` for Linear payload behavior.
- Use `../../references/methods/tooling-dry-run.md` for dry-run, idempotency, and batch safety conventions.
- Use `../../references/checklists/tooling-safety.md` before any external write.
- Use `../../templates/linear-delivery-handoff.md` for delivery issue previews.

## Rules

- Always preview external writes before executing.
- Require explicit user confirmation for Notion or Linear writes.
- Use `.product-os/workspace.json` for workspace IDs and conventions.
- Use `.product-os/external-id-map.json` for idempotent updates.
- Never claim true rollback. Provide manual revert payloads instead.
