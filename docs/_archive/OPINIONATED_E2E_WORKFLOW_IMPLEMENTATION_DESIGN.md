# Opinionated E2E Workflow Implementation Design

## Purpose

This document turns `docs/OPINIONATED_E2E_WORKFLOW_EXPANSION_PLAN.md` into an implementation-ready design.

The goal is to make the Product Operating System package feel like one strong workflow product, not a collection of PM methods. The workflow should support common starting points, carry state cleanly, stop safely when needed, and move product work from signal to launch learning without inventing evidence or forcing unnecessary validation.

## Design Position

The workflow is opinionated, but not rigid.

Core rules:

- Evidence quality determines commitment level.
- Validation is a decision, not always a mandatory stage.
- Re-entry from future or already-approved artifacts is first-class.
- Every stage emits resumable state.
- A blocked state is a useful product artifact.
- Tool writes are always dry-run first.
- Launch and learning are part of the operating loop, not optional afterthoughts.

## Existing Baseline

The current package has two strong workflow segments:

1. `workflow-discovery-to-prd`
   - evidence intake
   - VoC synthesis
   - opportunity framing
   - assumption mapping
   - research or validation recommendation
   - PRD drafting or blocked output
   - optional Notion dry-run

2. `workflow-prd-to-linear-delivery`
   - PRD readiness review
   - scope map
   - epics
   - stories
   - acceptance criteria
   - dependency and sequencing review
   - Linear dry-run payloads

Phase 11 also added no-evidence behavior for founder hypotheses:

- no customer evidence means no committed PRD scope;
- return research or validation plan instead;
- keep the workflow in `blocked` or `needs_validation`.

## Target Architecture

Add a master workflow that composes the existing workflows and extends the lifecycle:

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

The master workflow owns routing, lifecycle state, re-entry, stop behavior, and cross-stage handoffs. Existing family skills and subworkflows remain the execution units.

## Files To Add

### Skill

```text
skills/workflow-product-operating-system/
  SKILL.md
  procedures/
    product-operating-system.md
```

### References

```text
references/workflows/product-operating-system-contract.md
references/workflows/workflow-lifecycle-statuses.md
```

### Templates

```text
templates/workflow-stage-output.md
templates/blocked-workflow.md
templates/validation-decision.md
templates/launch-readiness-gate.md
templates/post-launch-learning-loop.md
```

### Schemas

```text
schemas/workflow-stage.schema.json
schemas/workflow-stage-output.schema.json
schemas/blocked-workflow.schema.json
schemas/validation-decision.schema.json
schemas/launch-readiness-gate.schema.json
schemas/post-launch-learning.schema.json
schemas/product-operating-system-handoff.schema.json
```

### Evals

```text
evals/golden-cases/product-os-full-happy-path.md
evals/golden-cases/product-os-no-evidence-blocked.md
evals/golden-cases/product-os-rough-prd-reentry.md
evals/golden-cases/product-os-approved-prd-reentry.md
evals/golden-cases/product-os-launch-readiness-reentry.md
evals/golden-cases/product-os-post-launch-learning.md

evals/expected/product-os-full-happy-path.yaml
evals/expected/product-os-no-evidence-blocked.yaml
evals/expected/product-os-rough-prd-reentry.yaml
evals/expected/product-os-approved-prd-reentry.yaml
evals/expected/product-os-launch-readiness-reentry.yaml
evals/expected/product-os-post-launch-learning.yaml
```

### Validator Updates

Update:

- `registry.json`
- `package.yaml`
- `scripts/check_package.py`
- `scripts/run_trigger_evals.py`
- `evals/trigger-tests.yaml`
- `evals/forward-tests/phase8-forward-tests.json`

## Master Workflow Skill

### `SKILL.md`

The `SKILL.md` must stay concise. It should trigger when the user asks to move product work across multiple stages, such as:

- from idea or evidence to PRD;
- from PRD to delivery;
- from delivery to tool preview;
- from delivery to launch readiness;
- from launch result to learning loop;
- from an ambiguous product artifact to the next correct workflow stage.

It should not duplicate the whole procedure. It should route to:

- `procedures/product-operating-system.md`
- `references/workflows/product-operating-system-contract.md`
- `schemas/product-operating-system-handoff.schema.json`

### Procedure Responsibilities

`product-operating-system.md` owns:

- input classification;
- re-entry point selection;
- lifecycle status assignment;
- stage execution order;
- evidence and validation decisioning;
- approval gates;
- blocked-state outputs;
- launch readiness;
- post-launch learning loop;
- handoff and resume behavior.

It delegates execution to existing family skills and workflows.

## Re-Entry Model

Re-entry is a core UX feature. The workflow should accept artifacts from any point in the product lifecycle and continue from the right stage.

| Input Type | Entry Status | Required Check | Next Stage |
|---|---|---|---|
| Raw interviews, support tickets, sales notes | `intake_received` | source inventory | evidence triage |
| Founder hypothesis with no evidence | `evidence_insufficient` | missing evidence list | blocked research plan |
| Synthesized research | `evidence_synthesized` | confidence and gaps | opportunity framing |
| Opportunity or strategy note | `opportunity_framed` | assumptions and risks | evidence decision |
| Rough PRD | `prd_review_required` | PRD quality review | PRD repair or delivery gate |
| Approved PRD | `approved_for_delivery` | scope, non-goals, assumptions, risks | delivery readiness gate |
| Delivery-ready scope | `delivery_review_required` | story value, ACs, dependencies | delivery repair or tool preview |
| Existing epics/stories | `delivery_review_required` | user value and testability | delivery repair |
| Notion/Linear sync request | `ready_for_tool_preview` | source artifact and target IDs | dry-run preview |
| Launch request | `ready_for_launch_review` | audience, impact, risk, support | launch readiness |
| Post-launch metrics or customer signal | `learning_loop_open` | metric and signal integrity | learning synthesis |

Rules:

- Re-entry does not require replaying earlier stages if their artifacts are provided and pass the required check.
- A future-state artifact is accepted as input, then reviewed for readiness.
- Missing earlier evidence is recorded as a risk, not silently fabricated.
- The workflow can move backward when a readiness check fails.

## Canonical Lifecycle Statuses

Add `schemas/workflow-stage.schema.json` and `references/workflows/workflow-lifecycle-statuses.md`.

Statuses:

- `intake_received`
- `evidence_insufficient`
- `evidence_synthesized`
- `opportunity_framed`
- `needs_validation`
- `validation_not_required`
- `ready_for_prd`
- `prd_review_required`
- `prd_ready`
- `ready_for_delivery_gate`
- `approved_for_delivery`
- `delivery_review_required`
- `delivery_ready`
- `ready_for_tool_preview`
- `ready_for_human_write_confirmation`
- `ready_for_launch_review`
- `launch_ready`
- `launched_or_handed_off`
- `learning_loop_open`
- `blocked`

Status design notes:

- `validation_not_required` is explicit. Some inputs are already validated, approved, or future-state artifacts.
- `blocked` means the workflow cannot safely advance without user input or missing evidence.
- `ready_for_human_write_confirmation` is only for tool previews, never live writes.

## Shared Stage Output Envelope

Every stage emits the same control fields so the workflow can resume.

Schema: `schemas/workflow-stage-output.schema.json`

Required fields:

```json
{
  "workflow_id": "workflow-product-operating-system",
  "stage_id": "string",
  "status": "string",
  "artifact_type": "string",
  "artifact": {},
  "evidence_used": [],
  "assumptions": [],
  "approval_gate": {
    "required": false,
    "reason": "",
    "question": ""
  },
  "blocked_by": [],
  "next_action": [],
  "handoff_target": ""
}
```

Rules:

- `artifact` can be a string, object, or path-like reference depending on context.
- `evidence_used` must distinguish direct evidence, inference, and provided artifacts.
- `approval_gate.required` is true when scope, risk acceptance, launch, or external write confirmation needs the user.
- `blocked_by` is non-empty when `status` is `blocked`.
- `handoff_target` names the next workflow, family skill, procedure, or human role.

## Blocked Workflow Artifact

Template: `templates/blocked-workflow.md`

Schema: `schemas/blocked-workflow.schema.json`

Required fields:

- `blocked_stage`
- `status`
- `reason`
- `missing_inputs`
- `risk_if_continued`
- `safe_partial_output`
- `recommended_next_action`
- `questions_for_user`
- `resume_status`
- `handoff_target`

Blocked-state rules:

- The blocked artifact must be useful on its own.
- It must explain what can safely be done now.
- It must state what cannot be safely committed.
- It must include the resume status so a future agent can continue.

Examples:

- no evidence for PRD request;
- rough PRD with unsupported claims;
- approved PRD missing non-goals;
- Linear sync request without team target;
- launch request without support readiness;
- post-launch readout without metric baseline.

## Evidence And Validation Decision

This replaces the phrase "hard validation gate" with a more precise implementation: an evidence and validation decision.

Validation is not always required. The decision can be:

- `proceed_to_prd`
- `validation_not_required`
- `run_validation_first`
- `proceed_with_explicit_risk_acceptance`
- `stop_for_missing_evidence`
- `return_to_discovery`

Schema: `schemas/validation-decision.schema.json`

Required fields:

- `decision`
- `evidence_strength`
- `riskiest_assumption`
- `rationale`
- `approval_required`
- `validation_plan`
- `risk_acceptance_note`
- `source_artifacts`

Decision rules:

- Use `validation_not_required` when input is already approved, already validated, or the user starts from a future lifecycle artifact that only needs readiness review.
- Use `proceed_to_prd` when evidence is sufficient for requirements work.
- Use `run_validation_first` when the next commitment depends on an untested assumption.
- Use `proceed_with_explicit_risk_acceptance` when evidence is weak but the user chooses to continue.
- Use `stop_for_missing_evidence` when the workflow cannot responsibly create committed scope.
- Use `return_to_discovery` when the current artifact is too ambiguous or contradictory to repair directly.

Important correction:

The workflow must not force validation on approved PRDs, already-validated scope, launch readiness inputs, or post-launch learning inputs. It should review readiness and record evidence gaps, but it should not replay discovery unless the input fails a readiness check.

## Master Workflow Stages

### Stage 1: Intake Classification

Purpose: determine entry point and status.

Inputs:

- raw evidence;
- idea;
- hypothesis;
- rough PRD;
- approved PRD;
- delivery work;
- tool sync request;
- launch request;
- post-launch metrics.

Outputs:

- `entry_status`
- `detected_artifact_type`
- `missing_context`
- `next_stage`

### Stage 2: Evidence Triage

Delegates to:

- `pm-discovery/procedures/intake-triage.md`
- `pm-discovery/procedures/voc-synthesis.md`

Outputs:

- source inventory;
- evidence ledger;
- confidence;
- gaps.

### Stage 3: Opportunity Framing

Delegates to:

- `pm-discovery/procedures/opportunity-framing.md`

Outputs:

- outcome;
- opportunity;
- target segment;
- job/pain/workaround;
- solution ideas separated from problems.

### Stage 4: Evidence And Validation Decision

Delegates to:

- `pm-validation/procedures/assumption-map.md`
- `pm-discovery/procedures/research-plan.md`
- `pm-validation/procedures/experiment-design.md`

Outputs:

- validation decision;
- risk acceptance gate if needed;
- research or validation plan if needed.

### Stage 5: PRD Review Or Drafting

Delegates to:

- `pm-docs/procedures/prd.md`
- `pm-docs/procedures/spec-review.md`
- `workflow-discovery-to-prd`

Outputs:

- PRD;
- PRD readiness review;
- unsupported claims;
- non-goals;
- metrics;
- approval gates.

### Stage 6: Delivery Readiness Gate

Delegates to:

- `workflow-prd-to-linear-delivery`
- `pm-docs/procedures/spec-review.md`

Outputs:

- delivery decision;
- blocking product questions;
- delivery-ready scope or blocked artifact.

### Stage 7: Delivery Split

Delegates to:

- `pm-delivery/procedures/epic-breakdown.md`
- `pm-delivery/procedures/story-splitting.md`
- `pm-delivery/procedures/acceptance-criteria.md`

Outputs:

- epics;
- stories;
- acceptance criteria;
- dependencies;
- sequencing;
- risks.

### Stage 8: Tool Dry-Run Preview

Delegates to:

- `pm-tooling/procedures/notion-preview.md`
- `pm-tooling/procedures/linear-preview.md`
- `pm-tooling/procedures/tool-id-resolution.md`
- `pm-tooling/procedures/external-id-map.md`

Outputs:

- Notion dry-run payloads;
- Linear dry-run payloads;
- idempotency keys;
- payload hashes;
- confirmation questions;
- missing target IDs;
- manual fallback.

### Stage 9: Launch Readiness

Delegates to:

- `pm-gtm/procedures/launch-readiness.md`
- `pm-gtm/procedures/positioning-messaging.md`
- `references/methods/launch-planning.md`

Outputs:

- launch readiness gate;
- audience;
- positioning;
- customer impact;
- enablement readiness;
- support readiness;
- rollout risks;
- success metrics;
- post-launch review plan.

### Stage 10: Post-Launch Learning Loop

Delegates to:

- `pm-gtm/procedures/post-launch-review.md`
- `pm-growth/procedures/activation-analysis.md` where relevant;
- `pm-discovery/procedures/intake-triage.md` for new signals.

Outputs:

- metric readout;
- guardrail readout;
- customer signal;
- assumption updates;
- decision;
- next discovery input;
- follow-up actions.

## Product Operating System Contract

File: `references/workflows/product-operating-system-contract.md`

Required sections:

- producer and consumers;
- accepted entry artifacts;
- lifecycle statuses;
- stage output contract;
- re-entry rules;
- evidence and validation decision rules;
- blocked-state rules;
- launch readiness rules;
- learning loop rules;
- tool-safety rules.

## Product Operating System Handoff Schema

File: `schemas/product-operating-system-handoff.schema.json`

Top-level required fields:

- `workflow_id`
- `current_status`
- `entry_status`
- `source_artifacts`
- `stage_outputs`
- `current_artifact`
- `approval_gates`
- `blocked_by`
- `next_actions`
- `handoff_target`

`stage_outputs` should be an array of `workflow-stage-output` objects.

## Registry And Manifest Changes

Update `registry.json`:

```json
{
  "id": "workflow-product-operating-system",
  "path": "skills/workflow-product-operating-system",
  "type": "workflow",
  "domain": "end-to-end"
}
```

Update `package.yaml`:

- add `workflow-product-operating-system` to `entry_workflows`;
- keep existing workflows as entry workflows for direct use;
- do not set `default_router` unless a real router skill is implemented.

## Trigger And Routing Design

The master workflow should trigger on:

- "take this from idea to launch";
- "what is the next product workflow step";
- "turn this artifact into the next product deliverable";
- "continue this product work";
- "run the product operating system workflow";
- "I have a PRD / delivery plan / launch request / post-launch metrics, what next?"

It should not trigger on:

- a single narrow request that clearly belongs to one family skill;
- general business writing;
- engineering-only implementation;
- live tool-write requests without product artifact context.

Add trigger tests:

- positive full workflow;
- positive rough PRD re-entry;
- positive launch readiness re-entry;
- positive post-launch learning loop;
- negative single PRD review that should route to `pm-docs`;
- negative Linear-only tooling request that should route to `pm-tooling`.

## Forward Tests

Add cases to `evals/forward-tests/phase8-forward-tests.json` or a new suite:

1. full path from raw evidence to launch learning;
2. founder hypothesis with no evidence;
3. rough PRD re-entry;
4. approved PRD re-entry;
5. delivery artifacts re-entry;
6. tool preview re-entry;
7. launch readiness re-entry;
8. post-launch metrics re-entry;
9. adversarial skip validation;
10. adversarial skip tool preview.

## Golden Cases

Add six golden cases:

1. `product-os-full-happy-path`
2. `product-os-no-evidence-blocked`
3. `product-os-rough-prd-reentry`
4. `product-os-approved-prd-reentry`
5. `product-os-launch-readiness-reentry`
6. `product-os-post-launch-learning`

Each expected fixture should test:

- correct lifecycle status;
- correct re-entry behavior;
- stage output envelope;
- blocked output where relevant;
- no invented evidence;
- approval gates;
- next action.

## Tool Safety Requirements

The master workflow inherits existing tool safety:

- Notion and Linear are dry-run first.
- Missing target IDs produce setup instructions, not guessed writes.
- Existing external ID mappings produce update previews.
- Confirmed writes require explicit user confirmation for the exact target, idempotency key, and payload hash.
- No live writes happen in evals.

The master workflow should not add new live tool behavior.

## Launch Readiness Requirements

The launch stage must not create unsupported claims.

Required checks:

- customer impact is clear;
- audience is known;
- support readiness is understood;
- enablement needs are captured;
- rollout risk is identified;
- success metrics and guardrails are defined;
- post-launch learning plan exists.

If these are missing, return a blocked launch-readiness artifact.

## Post-Launch Learning Requirements

The workflow closes the loop by converting launch evidence into new product inputs.

Required checks:

- success metrics;
- guardrail metrics;
- customer signal;
- assumption updates;
- decision;
- next discovery inputs;
- follow-up actions.

Decision values:

- `continue_rollout`
- `iterate`
- `pause`
- `rollback_or_manual_revert`
- `start_new_discovery`
- `close_loop`

Use `manual_revert` language for tools and launches when true rollback is not available.

## Implementation Order

Implement all eight capabilities in this order:

1. Master workflow skill, procedure, contract, registry, and package entry.
2. Canonical lifecycle statuses and stage output envelope.
3. Re-entry rules inside the master procedure.
4. Blocked workflow template and schema.
5. Evidence and validation decision schema and template.
6. Launch readiness gate schema/template integration.
7. Post-launch learning loop schema/template integration.
8. Tests, golden cases, forward cases, and structural validation requirements.

Rationale:

- The master workflow gives users the UX immediately.
- Status and envelope make every later stage resumable.
- Re-entry rules make future artifacts first-class.
- Blocked and validation decisions protect quality.
- Launch and learning complete the operating loop.
- Tests lock behavior after the design is represented in files.

## Validation Plan

After implementation, run:

```bash
python3 scripts/check_package.py .
python3 scripts/run_trigger_evals.py .
python3 scripts/grade_artifact.py --case product-os-no-evidence-blocked evals/artifact-fixtures/passing-product-os-no-evidence-blocked.md
python3 scripts/check_tool_safety.py .
python3 scripts/check_forward_tests.py .
python3 -m py_compile scripts/check_package.py scripts/run_trigger_evals.py scripts/grade_artifact.py scripts/check_tool_safety.py scripts/check_forward_tests.py
```

Also manually smoke:

1. idea with no evidence -> blocked research plan;
2. rough PRD -> PRD repair;
3. approved PRD -> delivery split;
4. launch request -> launch readiness;
5. post-launch metrics -> learning loop;
6. Linear write request -> dry-run preview and confirmation gate.

## Migration And Compatibility

Existing workflows remain valid:

- `workflow-discovery-to-prd`
- `workflow-prd-to-linear-delivery`

The master workflow composes them. It should not remove or rename existing workflows.

Existing schemas remain valid. New schemas should be additive.

Existing release-candidate docs should be updated to say:

- 0.1.0 shipped two workflow segments;
- the next implementation adds the master workflow spine;
- trigger and forward tests are still regression scaffolds until real-agent tests run.

## Non-Goals

- Do not add a broad method library.
- Do not build a separate router skill in this implementation unless routing breaks.
- Do not add live Notion or Linear writes.
- Do not remove existing workflows.
- Do not force validation when the user re-enters from an already-approved, validated, launch, delivery, or post-launch artifact.

## Definition Of Done

Implementation is done when:

- `workflow-product-operating-system` exists and is registered.
- The master workflow supports all major re-entry points.
- Canonical statuses and stage output envelope exist.
- Blocked workflow artifact exists and is tested.
- Evidence and validation decision exists and does not force validation for future-state re-entry.
- Launch readiness stage exists.
- Post-launch learning loop exists.
- Existing subworkflows are still usable.
- Golden cases and forward tests cover the full path and re-entry cases.
- Full validation passes.

