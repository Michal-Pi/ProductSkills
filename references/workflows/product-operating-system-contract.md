# Product Operating System Handoff Contract

This contract connects discovery, validation, docs, delivery, tooling, GTM, and learning-loop work.

## Producer

`workflow-product-operating-system`

## Consumers

- `workflow-discovery-to-prd` for discovery, opportunity, validation-decision, and PRD drafting work.
- `workflow-prd-to-linear-delivery` for delivery readiness, story split, and Linear dry-run preview.
- `pm-gtm` for launch readiness, positioning, release comms, and post-launch review.
- `pm-growth` for metric diagnosis or experiment follow-up.
- Future agents that resume from a stage output envelope.

## Accepted Entry Artifacts

- Raw customer evidence or product signal.
- Founder hypothesis or feature idea.
- Synthesized research, opportunity notes, or strategy notes.
- Rough PRD, approved PRD, validated scope, delivery plan, epics, or stories.
- Notion or Linear sync request with product artifact context.
- Launch request, release plan, post-launch metrics, or customer signal.

## Required Fields

- `workflow_id`: `workflow-product-operating-system`
- `current_status`: canonical lifecycle status
- `entry_status`: canonical lifecycle status assigned at intake
- `source_artifacts`: artifact paths, summaries, or references provided by the user
- `stage_outputs`: ordered outputs using the shared workflow stage envelope
- `current_artifact`: current PRD, delivery handoff, tool preview, launch gate, learning loop artifact, or blocked artifact
- `approval_gates`: decisions that require human approval before scope, risk acceptance, launch, or writes
- `blocked_by`: missing inputs, unresolved decisions, or unsafe assumptions
- `next_actions`: ordered next steps with recommended owner when known
- `handoff_target`: next workflow, family skill, procedure, or human role

## Lifecycle Statuses

Use `references/workflows/workflow-lifecycle-statuses.md`. Do not invent local status names when a canonical status fits.

## Stage Output Contract

Each stage output must include:

- workflow ID;
- stage ID;
- status;
- artifact type and artifact body or reference;
- evidence used, with direct evidence, inference, and provided artifacts distinguished;
- assumptions;
- approval gate;
- blocked reasons;
- next action;
- handoff target.

## Re-Entry Rules

- Re-entry does not require replaying earlier stages when provided artifacts pass readiness checks.
- Future-state artifacts enter through readiness checks.
- Missing earlier evidence is recorded as risk, not fabricated.
- Failed readiness checks may move the workflow backward to repair, validation, or discovery.

## Evidence And Validation Decision Rules

- `validation_not_required` is valid for approved PRDs, already validated scope, delivery artifacts, launch requests, and post-launch learning inputs.
- Weak evidence cannot become committed scope without explicit risk acceptance.
- Missing evidence must produce research, validation, or blocked output rather than invented PRD claims.

## Blocked-State Rules

Blocked output must explain:

- the blocked stage;
- what is missing;
- risk if continued;
- safe partial output;
- recommended next action;
- questions for the user;
- resume status;
- handoff target.

## Launch Readiness Rules

Launch readiness must cover audience, customer impact, positioning, support readiness, enablement readiness, rollout risk, success metrics, and post-launch learning plan. It must not invent market claims or roadmap promises.

## Learning Loop Rules

Post-launch learning must connect metric readout, guardrails, customer signal, assumption updates, and next decision. Learnings should become next discovery inputs when they affect roadmap or scope.

## Tool-Safety Rules

Notion and Linear outputs are dry-run previews until explicit user confirmation. Confirmations must be tied to target workspace or team, payload, idempotency keys, and `dry_run_payload_hash`.
