# PRD to Linear Delivery Handoff Contract

This contract connects docs, delivery, and Linear tooling.

## Producer

`workflow-prd-to-linear-delivery`

## Consumers

- `pm-delivery` for iteration on epics, stories, and acceptance criteria.
- Linear dry-run payloads are produced by this workflow under the canonical safety contract at `references/mcp/dry-run-preview.md`.
- Engineering planning or sprint planning after product approval.

## Required Fields

- `workflow_id`: `workflow-prd-to-linear-delivery`
- `decision_status`: one of `blocked`, `needs_product_decision`, `ready_for_delivery_review`, `ready_for_linear_preview`, `approved_for_linear_write`
- `source_prd`: title, source path or summary, artifact ID when known, and version or date when known
- `readiness_review`: blocking issues, non-blocking improvements, unsupported claims, and delivery recommendation
- `scope_map`: in-scope capabilities, non-goals, dependencies, assumptions, excluded requests, and sequencing constraints
- `epics`: local ID, title, outcome, completion criteria, dependencies, risks, and priority
- `stories`: local ID, parent epic ID, story, user value, split rationale, dependencies, and priority
- `acceptance_criteria`: story ID, success path, edge cases, errors, permissions, empty states, and observability needs
- `linear_preview`: dry-run payloads, target team, labels, idempotency keys, payload hash, validation notes, and confirmation question
- `approval_gates`: decisions that need human approval before issue creation or updates
- `open_questions`: unresolved product, design, engineering, data, compliance, or GTM questions
- `next_actions`: ordered actions with owner or recommended owner when known

## Quality Rules

- Delivery work must preserve product intent, assumptions, and non-goals.
- When this workflow is entered from the master Product Operating System workflow, map readiness to canonical lifecycle statuses from `references/workflows/workflow-lifecycle-statuses.md`.
- Approved PRD re-entry does not require validation replay; record evidence gaps as risks and continue through delivery readiness.
- Stories must be valuable, testable, and small enough to plan.
- Acceptance criteria must include edge cases and failure states when relevant.
- Linear previews must never imply a live write has happened.
- Existing external IDs must produce update previews instead of duplicate create previews.

## Linear Safety

`linear_preview` must follow `references/mcp/dry-run-preview.md` (canonical safety contract) and `references/mcp/linear-mcp-contract.md` (payload field expectations). A confirmed write requires explicit user approval for the exact preview, including target team, issue list, idempotency keys, and `dry_run_payload_hash`.
