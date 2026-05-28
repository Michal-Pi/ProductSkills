# Interview Analysis

Use when analyzing one or more customer interviews.

## Steps

1. Identify interviewee segment, context, and goal.
2. Extract facts, behaviors, quotes, emotions, workarounds, and purchase or usage signals.
3. Tag each signal by job, pain, desired outcome, trigger, and alternative.
4. Identify contradictions and interviewer bias.
5. Synthesize patterns only when supported by multiple signals or mark them as hypotheses.
6. Recommend follow-up questions or validation steps.

## Output

Return evidence table, themes, confidence, assumptions, and follow-up research plan.

## Done when

- The evidence table contains at least twelve distinct evidence IDs across the supplied interviews, each tagged by job, pain, desired outcome, trigger, and alternative; signals without one of those tags are flagged "tag missing" rather than dropped.
- Themes labeled with a confidence level cover at least four distinct customer signals, and any theme supported by a single signal is explicitly marked "hypothesis only."
- Contradictions and interviewer bias are recorded as their own list, not folded into themes; quotes are short and attributable.
- When fewer than three interviews or insufficient signal density are present, the procedure declines to synthesize patterns and instead returns a follow-up research plan with the gaps to fill.
