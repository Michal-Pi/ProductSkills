---
name: workflow-product-operating-system
description: Master workflow for taking product work across the operating system from idea, evidence, rough PRD, approved PRD, delivery plan, tool preview request, launch request, or post-launch metrics to the next correct product stage. Use when the user asks to continue product work, find the next workflow step, move from idea to launch, or route an ambiguous product artifact.
---

# Workflow: Product Operating System

Route product work through the full operating loop without forcing unnecessary replay.

## Procedure

- Use `procedures/product-operating-system.md` for entry classification, re-entry, lifecycle statuses, stop points, launch readiness, and learning-loop behavior.
- Use `../../references/workflows/product-operating-system-contract.md` for the cross-stage handoff contract.
- Use `../../references/methods/large-corpus-synthesis.md` when evidence is large, repetitive, contradictory, or noisy enough to require batching.
- Use `../../schemas/product-operating-system-handoff.schema.json` for structured handoff fields.

## Guardrails

- Treat validation as an evidence and routing decision, not a required stage for every input.
- Accept future-state artifacts through readiness checks; do not pretend earlier artifacts exist.
- Stop with a useful blocked artifact when evidence, approval, target workspace, launch readiness, or metric context is missing.
- Keep Notion and Linear behavior dry-run first until the user confirms the exact preview, target, idempotency keys, and payload hash.
