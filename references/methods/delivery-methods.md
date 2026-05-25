# Delivery Methods

Use this reference when converting product intent into buildable, testable work.

## Story Splitting Patterns

- Workflow step
- User role or permission
- Data state
- Rule or policy variation
- Channel or platform
- Happy path before edge cases
- Risk spike before full build
- Manual or concierge first version

## Acceptance Criteria Patterns

- Given/when/then behavior
- State transition
- Permission or access rule
- Error handling
- Empty state
- Instrumentation event
- Non-functional product requirement

## Release Readiness Checks

- Scope and non-goals are clear
- Stories are testable
- Edge cases and failure states are named
- Analytics and support are ready
- Rollout and mitigation plan exist
- Open product decisions have owners

## Guardrails

- Avoid splitting only by backend, frontend, or database layer unless the work is explicitly technical.
- Do not turn unresolved product questions into engineering tasks.
- Keep delivery artifacts connected to evidence and assumptions.
