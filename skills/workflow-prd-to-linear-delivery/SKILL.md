---
name: workflow-prd-to-linear-delivery
description: End-to-end workflow that converts a PRD, product spec, feature brief, or validated scope into epics, user stories, acceptance criteria, sprint plan, and Linear-ready issue payloads — under the canonical dry-run safety contract (preview before write, explicit confirmation, idempotency, never claim rollback). Use when the user asks to break a PRD into delivery work, create Linear issues from product requirements, or produce a safe Linear dry-run preview. Do not use for standalone epic/story decomposition without Linear (route to pm-delivery); for PRD writing or review (route to pm-docs); or for sequencing initiatives into quarters (route to pm-roadmap).
---

# Workflow: PRD to Linear Delivery

Convert a PRD or validated scope into delivery artifacts and safe Linear previews.

## Procedure

- Use `procedures/prd-to-linear-delivery.md` for the complete workflow, stop points, fallbacks, and approval gates.
- Use `../../references/workflows/prd-to-linear-delivery-contract.md` for the handoff contract.
- Use `../../schemas/prd-to-delivery-handoff.schema.json` for structured handoff fields.

## Safety summary

This workflow may write to Linear (and optionally Notion). Every write follows preview-before-write semantics:

1. **Preview before write.** No external write proceeds without a dry-run payload shown to the user.
2. **Explicit confirmation tied to the exact payload** (idempotency key + dry-run payload hash). Generic approval is not confirmation.
3. **`idempotency_key` is required on every confirmed write.** Re-running with the same key must update, not duplicate.
4. **Resolve display names to tool IDs before confirmed writes** (Linear team/label/state, Notion workspace/database/page). Never treat display names as write-ready.
5. **Never claim rollback.** Provide a manual revert payload instead.

**Canonical safety contract:** see `../../references/mcp/dry-run-preview.md`. If this summary and the reference disagree, the reference wins.

## Guardrails

- Do not create implementation tasks before product scope, non-goals, and acceptance criteria are clear.
- Preserve assumptions, risks, and open product questions in the delivery handoff.
- Linear behavior is dry-run first; require explicit confirmation tied to the preview payload before any write. See `../../references/mcp/dry-run-preview.md`.
- When this workflow halts with `status: blocked` for missing evidence, set `resume_target: pm-discovery` on the blocked-workflow envelope. Use `pm-validation` only when the gap is specifically a validation gap (testable hypothesis lacks a test method). See `../../references/workflows/workflow-lifecycle-statuses.md` §"Canonical resume targets" for the full rule.
