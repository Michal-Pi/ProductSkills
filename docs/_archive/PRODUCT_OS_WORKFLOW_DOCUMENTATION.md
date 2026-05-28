# Product Operating System Workflow Documentation

## Purpose

`workflow-product-operating-system` is the master workflow for moving product work through the full operating loop:

```text
intake
-> evidence triage
-> opportunity framing
-> evidence and validation decision
-> PRD review or drafting
-> delivery readiness gate
-> delivery split
-> tool dry-run preview
-> launch readiness
-> post-launch learning loop
-> next discovery input
```

The workflow is opinionated but not rigid. It chooses the right entry point for the artifact the user provides, preserves lifecycle state, and stops with a useful blocked artifact when advancing would require invented evidence or unsafe assumptions.

## Primary Assets

- Skill router: `skills/workflow-product-operating-system/SKILL.md`
- Procedure: `skills/workflow-product-operating-system/procedures/product-operating-system.md`
- Contract: `references/workflows/product-operating-system-contract.md`
- Lifecycle statuses: `references/workflows/workflow-lifecycle-statuses.md`
- Handoff schema: `schemas/product-operating-system-handoff.schema.json`

## Core Rules

- Evidence quality determines commitment level.
- Validation is an evidence and routing decision, not a mandatory replay step.
- Approved PRDs, delivery artifacts, launch requests, and post-launch metrics enter through readiness checks.
- Missing earlier evidence is recorded as risk or open questions, not fabricated.
- Every stage should emit a resumable stage output envelope.
- A blocked state is a valid product artifact when the workflow cannot safely advance.
- Notion and Linear behavior is dry-run first until the user confirms the exact target, payload, idempotency keys, and payload hash.

## Re-Entry Points

| Input | Entry status | Required check | Next stage |
|---|---|---|---|
| Raw interviews, tickets, sales notes | `intake_received` | source inventory | evidence triage |
| Founder hypothesis with no evidence | `evidence_insufficient` | missing evidence list | blocked research plan |
| Synthesized research | `evidence_synthesized` | confidence and gaps | opportunity framing |
| Opportunity or strategy note | `opportunity_framed` | assumptions and risks | evidence decision |
| Rough PRD | `prd_review_required` | PRD quality review | PRD repair or delivery gate |
| Approved PRD | `approved_for_delivery` | scope, non-goals, assumptions, risks | delivery readiness gate |
| Delivery artifacts | `delivery_review_required` | value, acceptance criteria, dependencies | delivery repair or tool preview |
| Notion or Linear sync request | `ready_for_tool_preview` | source artifact and target IDs | dry-run preview |
| Launch request | `ready_for_launch_review` | audience, impact, risk, support | launch readiness |
| Post-launch metrics or signal | `learning_loop_open` | metric and signal integrity | learning synthesis |

## Stage Output Envelope

Each stage should emit:

- `workflow_id`
- `stage_id`
- `status`
- `artifact_type`
- `artifact`
- `evidence_used`
- `assumptions`
- `approval_gate`
- `blocked_by`
- `next_action`
- `handoff_target`

Use `templates/workflow-stage-output.md` and `schemas/workflow-stage-output.schema.json`.

## Blocked Workflow Output

Use `templates/blocked-workflow.md` and `schemas/blocked-workflow.schema.json` when the workflow cannot safely advance.

Blocked outputs must include:

- blocked stage;
- status;
- reason;
- missing inputs;
- risk if continued;
- safe partial output;
- recommended next action;
- questions for the user;
- resume status;
- handoff target.

## Validation Decision

Use `templates/validation-decision.md` and `schemas/validation-decision.schema.json`.

Allowed decisions:

- `proceed_to_prd`
- `validation_not_required`
- `run_validation_first`
- `proceed_with_explicit_risk_acceptance`
- `stop_for_missing_evidence`
- `return_to_discovery`

Use `validation_not_required` when the user starts from an approved, already validated, delivery, launch, or post-launch artifact that passes readiness checks.

## Launch And Learning

Launch readiness uses `templates/launch-readiness-gate.md` and `schemas/launch-readiness-gate.schema.json`.

Post-launch learning uses `templates/post-launch-learning-loop.md` and `schemas/post-launch-learning.schema.json`.

The workflow should not end at tickets created or launch handed off. It should convert launch outcomes into metric readout, customer signal, assumption updates, decision, next discovery inputs, and follow-up actions.
