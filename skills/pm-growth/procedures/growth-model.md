# Growth Model

Use when mapping how the product grows.

## Steps

1. Define business goal, target segment, and time horizon.
2. Map acquisition, activation, retention, monetization, expansion, and referral or loop mechanics.
3. Identify inputs, outputs, conversion points, and compounding effects.
4. Add baseline metrics when available.
5. Name bottleneck candidates and evidence confidence.
6. Recommend the next diagnostic or experiment.

## Output

Use `../../../templates/growth-model.md`.

## Done when

- Business goal, target segment, and time horizon are populated; each lifecycle stage (acquisition, activation, retention, monetization, expansion, referral or loop) is either mapped or explicitly marked "not part of this model" with a reason.
- At least three named metrics carry formulas or baseline values from the supplied data; metrics without baselines are labeled "baseline unknown" rather than fabricated.
- Bottleneck candidates are ranked by evidence confidence (not intuition), and at least one next diagnostic or experiment is recommended with its expected learning.
- When business goal, target segment, or time horizon is missing, the model refuses to draw mechanics and returns those gaps as the first deliverable.
