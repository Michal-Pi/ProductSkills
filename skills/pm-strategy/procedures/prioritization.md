# Prioritization

Use when choosing what to build, sequence, cut, or test.

## Steps

1. Clarify the decision: ranking, sequencing, scope negotiation, or experiment backlog.
2. List options and normalize them to comparable units.
3. Choose a method using `../../../references/frameworks/prioritization-models.md`.
4. Define criteria and confidence before scoring.
5. If the input is a large corpus, do not collapse frequency, ARR, strategic weight, risky minority signals, and noise controls into one ranking. Score each dimension separately before making a recommendation.
6. Score transparently, noting evidence, assumptions, conflicts, duplicates removed, and missing fields.
7. Run a sensitivity check for close decisions.
8. Recommend a decision and next action.

## Output

Use `../../../templates/prioritization-decision.md`.

## Done when

- At least three prioritization methods are compared in a table (or one is chosen with a one-line reason the others were rejected), and the selected method is sourced from `../../../references/frameworks/prioritization-models.md`.
- At least four options are scored against criteria whose weights sum to 1.0 ± 0.01; criteria and confidence are recorded before scores, not back-fitted after.
- For large-corpus inputs, frequency, ARR, strategic weight, minority signals, and noise controls are scored as separate dimensions and not collapsed into a single rank; conflicts, duplicates removed, and missing fields are noted on each row.
- A sensitivity check is run for close decisions (top-two within one weight-step of each other); when criteria or weights cannot be agreed by the decision-maker, the procedure refuses to publish a ranking and returns the criteria question instead.
