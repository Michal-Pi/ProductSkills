# Assumption Map

Use when a product idea, PRD, or strategy depends on untested beliefs.

## Steps

1. State the decision being de-risked.
2. List desirability, viability, feasibility, usability, GTM, and compliance assumptions.
3. Score each assumption by importance and evidence strength.
4. Identify the riskiest assumption.
5. Choose the smallest useful test.
6. Define success metric, guardrail, and decision rule.

## Output

Use `../../../templates/validation-plan.md` for the highest-risk assumption and include the full assumption table.

## Done when

- The assumption table lists at least four assumptions, each tagged with one of desirability, viability, feasibility, usability, GTM, or compliance; categories absent from the input are explicitly marked "not applicable" with a reason.
- Each assumption is scored on importance and evidence strength using a stated scale; the riskiest assumption is named and one validation plan is drafted against it.
- The validation plan defines a primary metric, guardrail, and decision rule that would invalidate the assumption; vague tests ("ask customers") are rewritten or rejected.
- When the decision being de-risked is not stated, the procedure refuses to score assumptions and returns the decision-clarification question instead.
