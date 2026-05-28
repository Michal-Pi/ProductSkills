# Evidence Grading

Use this scale whenever a product artifact depends on uncertain evidence.

## Source Types

- Customer behavior: observed usage, churn, conversion, paid commitment, repeated support actions.
- Customer statement: interviews, surveys, sales calls, support tickets.
- Quantitative product data: analytics, cohort data, funnel data, retention, revenue.
- Market evidence: competitor behavior, category shifts, analyst reports, public pricing.
- Internal opinion: stakeholder belief, sales intuition, leadership preference.
- Inference: model judgment based on incomplete evidence.

## Confidence Levels

- High: repeated direct evidence from the target segment or strong quantitative signal.
- Medium: consistent but limited evidence, proxy data, or validated expert judgment.
- Low: anecdote, one-off signal, stale data, or untested internal opinion.

## Output Rule

When confidence is low or medium, include the next learning step needed to raise confidence.

## Resume target when evidence is missing

If a workflow blocks because evidence is insufficient (Low confidence with no clear next learning step, or no evidence at all for a load-bearing claim), set the blocked-workflow envelope's `resume_target` to `pm-discovery`. See `../workflows/workflow-lifecycle-statuses.md` §"Canonical resume targets" for the full disambiguation rule between `pm-discovery`, `pm-validation`, `pm-metrics`, and `pm-stakeholder-comms`.
