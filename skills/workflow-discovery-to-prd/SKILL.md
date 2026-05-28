---
name: workflow-discovery-to-prd
description: End-to-end workflow that turns customer research, interviews, VoC notes, support feedback, sales asks, market evidence, and product goals into an evidence-backed PRD with assumption map, open questions, success metrics, and next actions. Use when the user asks to turn discovery or research into requirements.
---

# Workflow: Discovery to PRD

Turn messy product discovery evidence into an evidence-backed PRD.

## Procedure

- Use `procedures/discovery-to-prd.md` for the complete workflow, stop points, fallbacks, and approval gates.
- Use `../../references/workflows/discovery-to-prd-contract.md` for the handoff contract.
- Use `../../schemas/discovery-to-prd-handoff.schema.json` for structured handoff fields.

## Guardrails

- Do not invent evidence or collapse assumptions into facts.
- Stop for user approval before promoting weak evidence into PRD scope.
- If Notion sync is requested, produce a dry-run preview first and require explicit confirmation before any write.
- When this workflow halts with `status: blocked` for missing evidence, set `resume_target: pm-discovery` on the blocked-workflow envelope. Use `pm-validation` only when the gap is specifically a validation gap (testable hypothesis lacks a test method). See `../../references/workflows/workflow-lifecycle-statuses.md` §"Canonical resume targets" for the full rule.
