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

## Done when

- The evidence ledger contains at least twelve distinct evidence IDs spanning at least three source types (interview, ticket, survey, sales call, analytics note); every quote is short, attributable, and tied to an evidence ID.
- At least four themes carry an explicit confidence label, with affected user, job, pain, severity, and frequency populated; observations and interpretation are held in separate columns.
- Strong themes are converted to opportunity candidates and weak themes to research questions; minority signals are carried forward in the ledger rather than discarded.
- For large corpora the roll-up reports source counts before and after dedupe, ARR sums derived only from supplied data, and conflict/missing-field counts; when the corpus is too thin or too noisy to support four themes, the procedure refuses to synthesize and returns a research plan instead.
