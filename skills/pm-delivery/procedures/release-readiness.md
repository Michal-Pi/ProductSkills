# Release Readiness

Use when deciding whether scoped work can ship.

## Steps

1. Check scope completion and non-goals.
2. Review acceptance criteria, test coverage expectations, and unresolved defects.
3. Confirm analytics, support, docs, rollout, and stakeholder readiness.
4. Identify risk, mitigation, and owner.
5. Decide ship, staged rollout, hold, or cut scope.

## Output

Return readiness checklist, blockers, risks, decision, and next action.

## Done when

- The readiness checklist covers scope, acceptance criteria, test coverage, defects, analytics, support, docs, rollout, and stakeholder alignment; any dimension not applicable is marked "N/A" with a reason rather than omitted.
- Every blocker and risk has an owner and a mitigation, or is explicitly marked "no mitigation - acceptance required."
- A single decision (ship, staged rollout, hold, or cut scope) is recorded with the evidence and decision rule that produced it; staged rollouts include the gating metric and audience.
- When acceptance criteria, test coverage data, or defect lists are missing, the procedure refuses to issue a ship decision and instead returns the gap list as blockers.
