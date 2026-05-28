# Product Operating System Procedure

Use when the user asks to move product work across multiple lifecycle stages or when an input artifact could reasonably start from more than one product workflow.

## Entry Classification

Classify the input before running any stage. Assign `entry_status`, `detected_artifact_type`, `missing_context`, and `next_stage`.

| Input type | Entry status | Required check | Next stage |
|---|---|---|---|
| Raw interviews, support tickets, sales notes | `intake_received` | source inventory | evidence triage |
| Founder hypothesis with no evidence | `evidence_insufficient` | missing evidence list | blocked research plan |
| Synthesized research | `evidence_synthesized` | confidence and gaps | opportunity framing |
| Opportunity or strategy note | `opportunity_framed` | assumptions and risks | evidence decision |
| Rough PRD | `prd_review_required` | PRD quality review | PRD repair or delivery gate |
| Approved PRD | `approved_for_delivery` | scope, non-goals, assumptions, risks | delivery readiness gate |
| Delivery-ready scope | `delivery_review_required` | story value, acceptance criteria, dependencies | delivery repair or tool preview |
| Existing epics or stories | `delivery_review_required` | user value and testability | delivery repair |
| Notion or Linear sync request | `ready_for_tool_preview` | source artifact and target IDs | dry-run preview |
| Launch request | `ready_for_launch_review` | audience, impact, risk, support | launch readiness |
| Post-launch metrics or signal | `learning_loop_open` | metric and signal integrity | learning synthesis |

Re-entry rules:

- Do not replay earlier stages when the provided artifact passes its readiness check.
- Record missing earlier evidence as risk or open questions.
- Move backward only when the readiness check fails.
- Use `validation_not_required` when input is already approved, already validated, or starts from a later lifecycle artifact.

## Lifecycle Statuses

Use the canonical statuses in `../../../references/workflows/workflow-lifecycle-statuses.md` and `../../../schemas/workflow-stage.schema.json`.

Every stage output must use `../../../templates/workflow-stage-output.md` and conform to `../../../schemas/workflow-stage-output.schema.json` when structured output is requested.

## Stage Order

1. Intake classification.
2. Evidence triage using `../../../skills/pm-discovery/procedures/intake-triage.md` and `../../../skills/pm-discovery/procedures/voc-synthesis.md`.
3. Opportunity framing using `../../../skills/pm-discovery/procedures/opportunity-framing.md`.
4. Evidence and validation decision using `../../../templates/validation-decision.md`, `../../../skills/pm-validation/procedures/assumption-map.md`, `../../../skills/pm-discovery/procedures/research-plan.md`, and `../../../skills/pm-validation/procedures/experiment-design.md`.
5. PRD review or drafting using `../../../skills/pm-docs/procedures/prd.md`, `../../../skills/pm-docs/procedures/spec-review.md`, and `../../../skills/workflow-discovery-to-prd/procedures/discovery-to-prd.md`.
6. Delivery readiness gate using `../../../skills/workflow-prd-to-linear-delivery/procedures/prd-to-linear-delivery.md`.
7. Delivery split using `../../../skills/pm-delivery/procedures/epic-breakdown.md`, `../../../skills/pm-delivery/procedures/story-splitting.md`, and `../../../skills/pm-delivery/procedures/acceptance-criteria.md`.
8. Tool dry-run preview using `../../../skills/pm-tooling/procedures/notion-preview.md`, `../../../skills/pm-tooling/procedures/linear-preview.md`, `../../../skills/pm-tooling/procedures/tool-id-resolution.md`, and `../../../skills/pm-tooling/procedures/external-id-map.md`.
9. Launch readiness using `../../../templates/launch-readiness-gate.md`, `../../../skills/pm-gtm/procedures/launch-readiness.md`, `../../../skills/pm-gtm/procedures/positioning-messaging.md`, and `../../../references/methods/launch-planning.md`.
10. Post-launch learning loop using `../../../templates/post-launch-learning-loop.md`, `../../../skills/pm-gtm/procedures/post-launch-review.md`, `../../../skills/pm-growth/procedures/activation-analysis.md` when relevant, and `../../../skills/pm-discovery/procedures/intake-triage.md` for new signals.

## Large-Corpus Evidence Protocol

When the workflow receives 500+ evidence rows, multiple repeated source files, or likely duplicate/conflicting/noisy evidence, run `../../../references/methods/large-corpus-synthesis.md` before committing scope or routing downstream.

Required scale artifacts:

- batch summaries;
- an `evidence_ledger` with source IDs for material claims;
- a dedupe table;
- a conflict register;
- a missing-field table;
- minority-signal carry-forward notes;
- noisy-signal suppression notes;
- a final roll-up with counts before and after dedupe, ARR sums from supplied data only, confidence, conflicts, duplicates removed, missing-field counts, and representative citations.

At 1000+ rows, broad file-level citations are insufficient for material decisions. Narrative output may use representative citations, but the working ledger must preserve exhaustive source-ID coverage for opportunities, conflicts, blockers, minority signals, and suppressed noise.

## Evidence And Validation Decision

Produce a validation decision before creating or changing committed scope unless the input starts from an approved, already validated, delivery, launch, or post-launch artifact.

Allowed decisions:

- `proceed_to_prd`: evidence is sufficient for requirements work.
- `validation_not_required`: the artifact is approved, validated, or future-state and only needs readiness review.
- `run_validation_first`: the next commitment depends on an untested assumption.
- `proceed_with_explicit_risk_acceptance`: evidence is weak, but the user explicitly accepts the risk.
- `stop_for_missing_evidence`: committed scope would be irresponsible.
- `return_to_discovery`: the artifact is too ambiguous or contradictory to repair directly.

Use `../../../schemas/validation-decision.schema.json` and keep direct evidence, inference, and provided artifacts separate.

## Blocked State

Return `../../../templates/blocked-workflow.md` when the workflow cannot safely advance. A blocked state is complete enough to resume later.

Block when:

- No customer evidence exists for a PRD commitment.
- A rough PRD has unsupported claims that drive scope.
- An approved PRD lacks non-goals, assumptions, risks, or success metrics needed for delivery.
- A Notion or Linear sync request lacks source artifact, target IDs, or confirmation context.
- A launch request lacks audience, support readiness, rollout risk, or success metrics.
- A post-launch readout lacks baseline, metric window, or customer signal integrity.

## Approval Gates

Ask for explicit approval before:

- Promoting weak evidence into committed scope.
- Accepting risk instead of running validation.
- Treating an ambiguous PRD as approved for delivery.
- Creating or updating external tool records.
- Launching, announcing, or handing off a release with unresolved customer, support, legal, or operational risk.

Tool confirmations must name the exact dry-run payload, target, idempotency keys, and `dry_run_payload_hash`.

## Completion Standard

The workflow is complete when it emits a `product-operating-system-handoff` with:

- current lifecycle status;
- stage outputs in the shared envelope;
- current artifact or blocked artifact;
- approval gates;
- blocked reasons if any;
- next actions;
- handoff target.

The loop is complete only when launch learning produces either a next discovery input, a decision to iterate, a decision to monitor, or a decision to stop.
