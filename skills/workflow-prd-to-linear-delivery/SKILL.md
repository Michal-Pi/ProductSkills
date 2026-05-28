---
name: workflow-prd-to-linear-delivery
description: End-to-end workflow that converts a PRD, product spec, feature brief, or validated scope into epics, user stories, acceptance criteria, sprint plan, and Linear-ready issue payloads. Use when the user asks to break a PRD into delivery work or create Linear issues from product requirements.
---

# Workflow: PRD to Linear Delivery

Convert a PRD or validated scope into delivery artifacts and safe Linear previews.

## Procedure

- Use `procedures/prd-to-linear-delivery.md` for the complete workflow, stop points, fallbacks, and approval gates.
- Use `../../references/workflows/prd-to-linear-delivery-contract.md` for the handoff contract.
- Use `../../schemas/prd-to-delivery-handoff.schema.json` for structured handoff fields.

## Guardrails

- Do not create implementation tasks before product scope, non-goals, and acceptance criteria are clear.
- Preserve assumptions, risks, and open product questions in the delivery handoff.
- Linear behavior is dry-run first; require explicit confirmation tied to the preview payload before any write.
- When this workflow halts with `status: blocked` for missing evidence, set `resume_target: pm-discovery` on the blocked-workflow envelope. Use `pm-validation` only when the gap is specifically a validation gap (testable hypothesis lacks a test method). See `../../references/workflows/workflow-lifecycle-statuses.md` §"Canonical resume targets" for the full rule.
