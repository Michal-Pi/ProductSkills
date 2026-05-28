# Intake Triage

Use when product feedback arrives from support, sales, interviews, reviews, analytics notes, or stakeholder requests.

## Steps

1. Normalize each input into source, user segment, problem statement, requested solution, evidence type, and date.
2. Separate customer problem from proposed solution.
3. Cluster inputs by customer job, pain, or workflow moment.
4. Mark confidence using `../../../references/methods/evidence-grading.md`.
5. Identify duplicates, contradictions, and missing context.
6. For large or noisy inputs, apply `../../../references/methods/large-corpus-synthesis.md` and preserve batch summaries, the `evidence_ledger`, dedupe table, conflict register, missing-field table, minority-signal carry-forward, and noisy-signal suppression.
7. Recommend whether to ignore, monitor, research, validate, or route to PRD.

## Output

Return clusters with evidence, confidence, assumptions, open questions, and next action. At scale, include final roll-up counts, ARR sums from supplied data only, confidence, conflicts, duplicates removed, missing-field counts, and representative citations.
