# Lifecycle Experiment

Use when designing lifecycle, PLG, activation, retention, expansion, or resurrection experiments.

## Steps

1. Pick lifecycle stage and target segment.
2. State behavior change desired.
3. Create hypothesis and intervention.
4. Define primary metric, guardrail, audience, and duration.
5. Include operational risks such as spam, support burden, or brand impact.
6. Define decision rule.

## Output

Use `../../../templates/experiment-brief.md`.

## Done when

- Lifecycle stage, target segment, and desired behavior change are stated; the hypothesis has explicit IF/THEN/BY structure naming the intervention and the expected metric move.
- A primary metric with a target, a guardrail metric, audience, and duration are defined; the decision rule states what result ships, iterates, or stops the test.
- Operational risks (spam, support burden, brand, deliverability) are listed with mitigation or an explicit acceptance note.
- When the supplied context lacks a baseline for the primary metric or a clear target segment, the brief refuses to launch and returns those gaps as prerequisites instead.
