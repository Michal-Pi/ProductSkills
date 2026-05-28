# Discovery to PRD Handoff Contract

This contract connects discovery, validation, docs, and optional Notion tooling.

## Producer

`workflow-discovery-to-prd`

## Consumers

- `pm-docs` for PRD review or revision.
- `workflow-prd-to-linear-delivery` after scope approval.
- Optional Notion dry-run payloads follow `references/mcp/dry-run-preview.md` (canonical safety contract). The producing workflow keeps the safety summary in its SKILL.md.

## Required Fields

- `workflow_id`: `workflow-discovery-to-prd`
- `decision_status`: one of `blocked`, `needs_validation`, `validation_not_required`, `ready_for_prd_review`, `approved_for_delivery`
- `source_inventory`: input sources, source type, date or recency, segment, and owner when known
- `evidence_summary`: themes, direct evidence, confidence, contradictions, and evidence gaps
- `opportunity_frame`: outcome, customer opportunity, target segment, job, pain, current workaround, and solution ideas separated from problems
- `assumption_map`: assumptions by desirability, viability, feasibility, usability, GTM, and compliance risk
- `validation_recommendation`: test plan or rationale for proceeding without another test
- `prd`: PRD content or path using `templates/prd.md`
- `approval_gates`: decisions that need human approval before scope, validation, delivery, or tool sync
- `open_questions`: unresolved product, customer, metric, legal, GTM, or delivery questions
- `next_actions`: ordered actions with owner or recommended owner when known

## Quality Rules

- Direct evidence, inference, and assumptions must be separate.
- Weak evidence cannot become committed scope without an approval gate.
- Approved or future-state artifacts may use `validation_not_required` and proceed through readiness checks without replaying discovery.
- The PRD must name scope and non-goals.
- Success metrics must distinguish current baseline, target, and measurement gap when known.
- The handoff must be useful even when the workflow stops early.

## Optional Notion Handoff

Only include `notion_preview` when the user requests Notion sync. It must follow `references/mcp/dry-run-preview.md` (canonical safety contract) and keep `mode: dry_run` until explicit confirmation.
