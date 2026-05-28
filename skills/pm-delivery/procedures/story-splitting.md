# Story Splitting

Use when breaking epics into sprint-ready user stories.

## Steps

1. Start from user outcome, not system layer.
2. Split by workflow step, rule variant, data state, persona, channel, or risk using `../../../references/methods/delivery-methods.md`.
3. Keep each story valuable and testable.
4. Note dependencies and non-goals.
5. Add edge cases and failure states.
6. Route tool payloads through `workflow-prd-to-linear-delivery` (which honors the canonical safety contract at `../../../references/mcp/dry-run-preview.md`).

## Output

Use `../../../templates/user-story.md`.

## Done when

- At least four user stories are produced across the epics in scope; each story states a user value statement and a testable outcome, not a system task.
- Each story names the split axis used (workflow step, rule variant, data state, persona, channel, or risk) per `../../../references/methods/delivery-methods.md`, and dependencies and non-goals are recorded.
- Every story includes at least one edge case or failure state, or is explicitly marked "happy path only" with a reason.
- When the source epic lacks user outcome or testable scope, the procedure stops and returns the missing context as a blocker before emitting stories.
