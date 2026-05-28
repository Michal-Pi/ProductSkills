# VoC Synthesis

Use for messy customer notes, interviews, sales calls, support tickets, surveys, or feedback exports.

## Steps

1. Inventory sources and target segments.
2. Extract direct evidence, preserving short important quotes.
3. Cluster evidence into themes.
4. For each theme, name affected user, job, pain, severity, frequency, and confidence.
5. Separate observations from interpretation.
6. For large corpora, process source batches and maintain the `evidence_ledger`, dedupe table, conflict register, missing-field table, minority-signal carry-forward, and noisy-signal suppression from `../../../references/methods/large-corpus-synthesis.md`.
7. Convert strong themes into opportunities and weak themes into research questions.

## Output

Include themes, evidence, quotes, confidence, assumptions, opportunity candidates, and recommended next learning. At scale, add a roll-up with source counts before and after dedupe, ARR sums from supplied data only, representative citations, conflict counts, duplicate removals, and missing-field counts.
