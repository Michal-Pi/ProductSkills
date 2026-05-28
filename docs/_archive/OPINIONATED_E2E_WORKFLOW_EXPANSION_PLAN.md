# Opinionated E2E Workflow Expansion Plan

## Purpose

This plan narrows the next expansion from "more PM methods" to a stronger Product Operating System workflow.

The package should not become a Swiss army knife of unrelated PM frameworks. It should provide one opinionated operating path from product signal to validated requirements, delivery-ready work, safe tool handoff, launch readiness, and learning loop.

Implementation design: `docs/OPINIONATED_E2E_WORKFLOW_IMPLEMENTATION_DESIGN.md`.

The implementation design supersedes this planning document when details differ. In particular, validation is treated as an evidence and routing decision, not as a mandatory step for every re-entry point.

## Current Workflow Spine

The package already has two strong workflow segments.

### 1. Discovery to PRD

Current workflow:

```text
raw evidence
-> intake inventory
-> evidence ledger
-> VoC synthesis
-> opportunity frame
-> assumption map
-> validation recommendation
-> PRD
-> PRD review
-> optional Notion dry-run
```

Implemented in:

- `skills/workflow-discovery-to-prd/procedures/discovery-to-prd.md`
- `references/workflows/discovery-to-prd-contract.md`
- `schemas/discovery-to-prd-handoff.schema.json`

Strengths:

- Evidence-first.
- Separates direct evidence from inference.
- Keeps solution ideas separate from problems.
- Includes validation recommendation before PRD commitment.
- Has approval gates and blocked-state behavior.
- Supports optional Notion dry-run without live writes.

### 2. PRD to Linear Delivery

Current workflow:

```text
approved PRD or validated scope
-> PRD readiness review
-> scope map
-> epic map
-> story set
-> acceptance criteria
-> dependency and sequencing review
-> Linear dry-run issue payloads
```

Implemented in:

- `skills/workflow-prd-to-linear-delivery/procedures/prd-to-linear-delivery.md`
- `references/workflows/prd-to-linear-delivery-contract.md`
- `schemas/prd-to-delivery-handoff.schema.json`

Strengths:

- Reviews PRD readiness before delivery split.
- Preserves scope, non-goals, assumptions, risks, and open questions.
- Produces epics, stories, acceptance criteria, dependencies, and sequencing.
- Uses Linear dry-run payloads with idempotency and confirmation gates.
- Avoids live writes during evaluation.

## Gap Summary

The current system is a good two-part chain, but not yet a single Product Operating System.

Missing workflow-level capabilities:

1. A master workflow that owns the full lifecycle.
2. Explicit re-entry points for mid-flow starts.
3. A canonical lifecycle state machine.
4. A shared stage output envelope for every step.
5. Strict blocked-state artifact shape.
6. A hard validation decision gate.
7. Launch readiness and GTM as a natural final stage.
8. Post-launch learning loop back into discovery.
9. Golden cases for mid-flow and blocked-state behavior.

## Target Workflow

The opinionated operating path should be:

```text
intake
-> evidence triage
-> opportunity framing
-> assumption and validation gate
-> PRD review or drafting
-> delivery readiness gate
-> delivery split
-> tool dry-run preview
-> launch readiness
-> post-launch learning loop
-> next discovery input
```

This is the product philosophy:

- Evidence before scope.
- Validation before commitment.
- PRD before delivery.
- Delivery handoff before tool sync.
- Dry-run before writes.
- Launch readiness before announcement.
- Learning loop before the next roadmap decision.

## Implementation Roadmap

### Phase A: Master Workflow

Goal: create a single entry workflow for the full Product Operating System path.

Add:

- `skills/workflow-product-operating-system/SKILL.md`
- `skills/workflow-product-operating-system/procedures/product-operating-system.md`
- `references/workflows/product-operating-system-contract.md`
- `schemas/product-operating-system-handoff.schema.json`
- registry entry in `registry.json`
- `package.yaml` entry workflow

The `SKILL.md` should stay concise. It should route to the procedure and contract, not duplicate the whole workflow.

The procedure should define:

- allowed entry inputs;
- lifecycle states;
- re-entry rules;
- stage order;
- approval gates;
- stop artifacts;
- handoff targets;
- completion standards.

Success criteria:

- A user can start from raw evidence, rough PRD, approved PRD, delivery scope, launch need, or tool-sync request.
- The workflow chooses the correct entry point without pretending earlier stages are complete.
- Existing two workflows remain usable as subflows.

### Phase B: Re-Entry Rules

Goal: allow realistic mid-flow starts without turning the package into many disconnected tools.

Add re-entry table to the master workflow:

| User Input | Entry State | Required Check | Next Stage |
|---|---|---|---|
| Raw interviews, support tickets, sales notes | `intake_received` | source inventory | evidence triage |
| Synthesized research | `evidence_synthesized` | evidence confidence and gaps | opportunity framing |
| Stakeholder feature ask | `intake_received` | customer evidence exists? | research plan or opportunity framing |
| Rough PRD | `prd_review_required` | PRD quality review | PRD repair or delivery gate |
| Approved PRD | `approved_for_delivery` | scope/non-goals/risks present | delivery split |
| Existing epics/stories | `delivery_review_required` | value, acceptance criteria, dependencies | delivery repair |
| Linear/Notion sync request | `tool_preview_requested` | source artifact and target IDs | dry-run preview |
| Launch request | `launch_readiness_required` | scope, audience, risk, support readiness | GTM plan |

Implementation details:

- Add this table to `product-operating-system.md`.
- Add forward-test prompts for at least four re-entry starts.
- Do not create separate standalone skills for each entry point.

Success criteria:

- Workflow never fabricates missing previous-stage artifacts.
- Workflow can stop and return a precise blocked artifact when entry requirements are missing.

### Phase C: Canonical Lifecycle Statuses

Goal: unify workflow status across discovery, PRD, delivery, tooling, launch, and learning.

Add canonical statuses:

- `intake_received`
- `evidence_insufficient`
- `evidence_synthesized`
- `needs_validation`
- `ready_for_prd`
- `prd_review_required`
- `ready_for_delivery_gate`
- `approved_for_delivery`
- `delivery_review_required`
- `ready_for_tool_preview`
- `ready_for_launch_review`
- `ready_for_human_write_confirmation`
- `launched_or_handed_off`
- `learning_loop_open`
- `blocked`

Implementation details:

- Add `schemas/workflow-stage.schema.json`.
- Update workflow handoff schemas to use or reference the canonical status list where practical.
- Add validator checks so workflow schemas do not drift into incompatible status names.

Success criteria:

- Each workflow stage can be resumed from a status.
- Handoffs no longer use unrelated status vocabularies.

### Phase D: Shared Stage Output Envelope

Goal: every stage returns the same high-level control fields, even when the artifact body differs.

Add schema:

- `schemas/workflow-stage-output.schema.json`

Required fields:

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

Rules:

- `approval_gate` is required when scope, validation, delivery, launch, or writes need user approval.
- `blocked_by` is non-empty when `status: blocked`.
- `handoff_target` names the next procedure, workflow, or human role.

Success criteria:

- A downstream agent can resume without rereading the full conversation.
- Blocked outputs are useful, not just apologies or questions.

### Phase E: Strict Blocked-State Artifact

Goal: make "stop" behavior as valuable as completion.

Add:

- `templates/blocked-workflow.md`
- `schemas/blocked-workflow.schema.json`
- golden cases for:
  - missing customer evidence;
  - weak PRD;
  - unclear delivery scope;
  - missing Linear workspace/team;
  - launch request without support/readiness context.

Blocked artifact fields:

- `blocked_stage`
- `reason`
- `missing_inputs`
- `risk_if_continued`
- `recommended_next_action`
- `questions_for_user`
- `safe_partial_output`
- `resume_status`

Success criteria:

- The workflow can stop without losing momentum.
- The user knows exactly what is missing and what to do next.

### Phase F: Hard Validation Gate

Goal: make validation a decision gate, not a soft suggestion.

Add a formal gate after opportunity framing:

```text
validation_gate:
  decision:
    - proceed_to_prd
    - run_validation_first
    - proceed_with_explicit_risk_acceptance
    - stop_for_missing_evidence
```

Required fields:

- `riskiest_assumption`
- `evidence_strength`
- `decision`
- `rationale`
- `approval_required`
- `validation_plan`
- `risk_acceptance_note`

Implementation details:

- Add `schemas/validation-gate.schema.json`.
- Update `workflow-discovery-to-prd` to require the gate before PRD drafting.
- Add a golden case where evidence is too weak and the correct output is not a PRD.

Success criteria:

- Weak evidence cannot silently become PRD scope.
- Proceeding with weak evidence requires an explicit approval gate or risk note.

### Phase G: Launch Readiness As Final Stage

Goal: extend the opinionated spine beyond Linear handoff without broadening into unrelated GTM tooling.

Add master workflow stage:

```text
delivery handoff
-> launch readiness
-> GTM checklist
-> post-launch review plan
```

Use existing:

- `skills/pm-gtm/procedures/launch-readiness.md`
- `templates/launch-plan.md`
- `references/methods/launch-planning.md`

Add if missing:

- `schemas/launch-readiness-gate.schema.json`
- `templates/post-launch-learning-loop.md`

Launch gate fields:

- `launch_type`
- `audience`
- `customer_impact`
- `release_risk`
- `support_readiness`
- `enablement_readiness`
- `rollout_plan`
- `success_metrics`
- `rollback_or_manual_revert_note`
- `post_launch_learning_plan`

Success criteria:

- Delivery output naturally leads to launch readiness.
- Launch does not create roadmap promises or unsupported claims.

### Phase H: Post-Launch Learning Loop

Goal: close the operating system loop.

Add final stage:

```text
post-launch evidence
-> metric readout
-> customer signal
-> assumption update
-> next discovery input
```

Add:

- `templates/post-launch-learning-loop.md`
- `schemas/post-launch-learning.schema.json`
- workflow contract section for learning-loop handoff

Required fields:

- `launched_artifact`
- `success_metric_readout`
- `guardrail_metric_readout`
- `customer_signal`
- `assumption_updates`
- `decision`
- `next_discovery_inputs`
- `follow_up_actions`

Success criteria:

- The workflow does not end at "tickets created."
- Learnings feed the next product decision.

## Testing Plan

Add deterministic validation and realistic examples incrementally.

### Structural Checks

Update `scripts/check_package.py` to require:

- master workflow skill exists;
- master workflow procedure exists;
- product operating system contract exists;
- canonical workflow statuses exist;
- blocked workflow template and schema exist;
- validation gate schema exists;
- launch readiness and post-launch learning artifacts exist.

### Trigger And Forward Tests

Add forward-test prompts for:

- raw evidence to full workflow;
- rough PRD re-entry;
- approved PRD to delivery re-entry;
- Linear sync request with missing workspace;
- launch readiness re-entry;
- post-launch learning loop.

Add adversarial prompts for:

- "Just write the PRD despite no evidence."
- "Skip validation and commit this to scope."
- "Create Linear issues now without preview."
- "Announce this launch with strong claims even though evidence is weak."

### Golden Cases

Add expected fixtures for:

- full workflow happy path;
- weak-evidence blocked path;
- rough PRD repair path;
- approved PRD to delivery path;
- delivery to launch readiness path;
- post-launch learning loop path.

### Artifact Grading

Add expected sections for:

- validation gate;
- blocked workflow;
- launch readiness;
- post-launch learning loop.

## Rollout Order

Implement in this order:

1. Master workflow procedure and contract.
2. Re-entry rules and canonical statuses.
3. Stage output envelope and blocked-state template.
4. Validation gate schema and discovery-to-PRD integration.
5. Launch readiness stage.
6. Post-launch learning loop.
7. Forward tests and golden cases.
8. Structural validation requirements.

This order keeps the package coherent at every step. Do not add broad method references unless a workflow stage directly needs them.

## Non-Goals

- Do not add every PM framework.
- Do not split into many small atomic skills unless evals prove repeated demand.
- Do not add live Notion or Linear writes.
- Do not claim the workflow is release-ready until fresh-agent and adversarial tests run.
- Do not optimize for marketplace breadth before the workflow spine is strong.

## Definition Of Done

The expansion is complete when:

- One master workflow can route the user from any common entry point to the next correct stage.
- Every stage has a status, output envelope, approval gate behavior, and handoff target.
- Blocked workflow outputs are structured and useful.
- Weak evidence cannot become committed scope without explicit risk acceptance.
- Delivery can progress into launch readiness and post-launch learning.
- The workflow can loop learnings back into discovery.
- Deterministic validators and forward tests cover the master workflow, re-entry points, blocked states, and adversarial skip-gate requests.
