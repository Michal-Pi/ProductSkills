# Design Review

Use when reviewing a product design for readiness.

## Steps

1. Review alignment with user problem, outcome, and scope.
2. Check primary flow, secondary flows, empty states, errors, permissions, and edge cases.
3. Identify content, accessibility, instrumentation, and handoff gaps.
4. Separate blocking issues from suggestions.
5. Recommend next step: revise, validate, build, or defer.

## Output

Return findings by severity, evidence or rationale, open questions, and recommended action.

## Done when

- Findings cover primary flow, secondary flows, empty states, errors, permissions, edge cases, content, accessibility, instrumentation, and handoff; any dimension not reviewed is explicitly marked "not in scope" with a reason.
- Each finding cites concrete evidence (screen, flow step, content string, spec reference) and is tagged blocking or suggestion; blocking findings are not mixed into the suggestion list.
- A single recommended next step (revise, validate, build, or defer) is chosen with the rule that drove it; open questions for the designer or PM are listed separately.
- When the design lacks a stated user problem, outcome, or scope, the review stops and returns those gaps as the first finding instead of grading flows in a vacuum.
