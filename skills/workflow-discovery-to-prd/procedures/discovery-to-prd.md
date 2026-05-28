# Discovery to PRD Procedure

Use when the user wants to turn customer research, VoC, interviews, support tickets, sales feedback, analytics notes, or market evidence into a PRD.

## Entry Conditions

Start when at least one input exists:

- Raw customer evidence or research notes.
- A product outcome, business goal, or suspected opportunity.
- Existing discovery artifacts that need to become requirements.

If no target user, product area, or decision is stated, ask for the missing context before drafting a PRD. If evidence is absent, stop with `decision_status: blocked` or `needs_validation` and produce a research plan instead of a PRD.

## Workflow Steps

1. Intake and evidence inventory using `../../../skills/pm-discovery/procedures/intake-triage.md`.
2. VoC synthesis using `../../../skills/pm-discovery/procedures/voc-synthesis.md`.
3. Opportunity framing using `../../../skills/pm-discovery/procedures/opportunity-framing.md`.
4. Assumption mapping using `../../../skills/pm-validation/procedures/assumption-map.md`.
5. Evidence and validation decision using `../../../templates/validation-decision.md`. Validation is not mandatory when evidence is already sufficient or the user starts from an approved or future-state artifact.
6. Research or validation plan if the riskiest assumption is not already supported, using `../../../skills/pm-discovery/procedures/research-plan.md` or `../../../templates/validation-plan.md`.
7. PRD drafting using `../../../skills/pm-docs/procedures/prd.md` and `../../../templates/prd.md`.
8. Spec review using `../../../skills/pm-docs/procedures/spec-review.md`.
9. Optional Notion preview using `../../../references/mcp/dry-run-preview.md` (canonical safety contract). See `../../../references/mcp/notion-mcp-contract.md` for payload field expectations.

## Intermediate Artifacts

Produce these artifacts in order:

- `intake_inventory`: source list, dates, segments, evidence type, and owner when known.
- `evidence_ledger`: direct evidence, inference, confidence, and source trace.
- `voc_synthesis`: themes, quotes, severity, frequency, confidence, and contradictions.
- `opportunity_frame`: outcome, opportunities, target segments, jobs, pains, current workarounds, and solution ideas kept separate.
- `assumption_map`: desirability, viability, feasibility, usability, GTM, compliance assumptions, evidence strength, and riskiest assumption.
- `validation_decision`: decision, evidence strength, riskiest assumption, rationale, approval requirement, validation plan, risk acceptance note, and source artifacts.
- `research_or_validation_plan`: smallest useful research or test, audience, metric, guardrail, and decision rule when evidence is absent, weak, or mixed.
- `prd`: objective, customer, evidence, problem, assumptions, scope, non-goals, solution outline, UX notes, metrics, risks, open questions, and next actions.
- `handoff_contract`: structured fields from `../../../references/workflows/discovery-to-prd-contract.md`.
- `notion_dry_run_payload`: only when the user asks for Notion sync.

## Stop Points and Approval Gates

Stop before drafting the PRD when:

- The target customer or product outcome is unclear.
- Evidence is too thin to justify requirements.
- Customer problem and stakeholder-requested solution conflict.
- The highest-risk assumption needs validation before scope is committed.

Ask for approval before:

- Promoting an opportunity into PRD scope.
- Treating a validation plan as sufficient evidence.
- Publishing or syncing the PRD to Notion.

## Fallbacks for Missing Evidence

When this workflow halts with `status: blocked`, the structured halt artifact conforms to `../../../schemas/blocked-workflow.schema.json`, with `handoff_target: pm-discovery` (canonical resume target per `../../../references/workflows/workflow-lifecycle-statuses.md`).

- Missing customer evidence: return a research plan and questions with `decision_status: blocked` or `needs_validation`; do not draft final requirements or committed PRD scope.
- Approved, already validated, or future-state artifacts: use `validation_not_required`, run the relevant readiness check, and record missing earlier evidence as risk instead of replaying discovery.
- Missing metrics: propose candidate metrics and mark them as assumptions.
- Conflicting evidence: keep both interpretations and name the decision needed.
- Missing stakeholder constraints: mark constraints as open questions and exclude them from committed scope.
- Missing Notion workspace: return a dry-run payload plus setup instructions; do not infer a target.

## Handoff Contract

Before completion, populate the contract in `../../../references/workflows/discovery-to-prd-contract.md` and conform to `../../../schemas/discovery-to-prd-handoff.schema.json` where structured output is requested.

Minimum handoff fields:

- `workflow_id`
- `decision_status`
- `source_inventory`
- `evidence_summary`
- `opportunity_frame`
- `assumption_map`
- `validation_recommendation`
- `prd`
- `approval_gates`
- `open_questions`
- `next_actions`

## Completion Standard

The workflow is complete when the user has either:

- A reviewed PRD with explicit evidence, assumptions, scope, non-goals, metrics, risks, and open questions.
- A deliberate stop artifact explaining why the PRD is blocked and what evidence or approval is needed next.

If Notion sync is requested, completion means a dry-run payload exists and the user has been asked for explicit confirmation tied to the preview and idempotency key.

## Done when

- The VoC synthesis row set contains at least three rows, each with segment, problem, and evidence IDs; the assumption map lists at least four assumptions tagged across desirability, viability, feasibility, usability, GTM, and compliance (categories absent from the input are marked "not applicable" with a reason).
- The `validation_decision` artifact records decision status (`validation_required`, `validation_not_required`, `needs_validation`, or `blocked`), the riskiest assumption, the rationale, and any risk-acceptance note; downstream PRD writing is gated on this artifact being populated.
- The PRD covers objective, customer, evidence, problem, assumptions, scope, non-goals, solution outline, UX notes, metrics, risks, open questions, and next actions, each cited to discovery evidence IDs or explicitly marked as assumption; the handoff contract conforms to `../../../schemas/discovery-to-prd-handoff.schema.json`.
- When customer evidence, target user, or product outcome is missing, the workflow stops with `decision_status: blocked` or `needs_validation` and returns a research plan instead of a committed PRD; Notion sync, if requested, produces only a dry-run payload until the user confirms against the preview and idempotency key.
