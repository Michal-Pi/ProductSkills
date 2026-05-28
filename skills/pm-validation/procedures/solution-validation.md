# Solution Validation

Use when testing whether a proposed solution solves a validated problem.

## Steps

1. Restate the validated problem and target segment.
2. Name the solution assumptions.
3. Choose method: concept test, prototype usability test, concierge test, fake door, beta, or A/B test.
4. Define task, expected behavior, success metric, and guardrail.
5. Identify false-positive risks such as politeness, novelty, or sample bias.
6. Recommend decision based on results.

## Output

Return test plan, metrics, risks, decision thresholds, and next action.

## Done when

- The validated problem and target segment are restated with the evidence ID(s) that validated them; if no prior problem validation exists, the procedure stops and routes to problem validation.
- At least three solution assumptions are listed as IF/THEN/BY hypotheses; the chosen test method is justified against the riskiest one.
- Task, expected behavior, primary metric, guardrail, and decision threshold are stated before testing; false-positive risks (politeness, novelty, sample bias, observer effect) are listed with the controls applied.
- Results-to-decision mapping (ship, iterate, scope down, reject) is bound to the decision threshold; weak results are not promoted to "validated" without explicitly relaxing the threshold and naming the trade-off.
