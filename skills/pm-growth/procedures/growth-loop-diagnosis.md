# Growth Loop Diagnosis

Use when a product has loop or funnel symptoms that need root-cause analysis.

## Steps

1. Draw the current loop or funnel in words.
2. Identify the constrained step and affected segment.
3. Separate symptoms from plausible causes.
4. Check activation, retention, monetization, and distribution dependencies.
5. Form hypotheses ranked by evidence and impact.
6. Convert hypotheses into experiments with guardrails.

## Output

Return bottleneck, evidence, hypotheses, experiments, metrics, and decision thresholds.

## Done when

- The current loop or funnel is described in words with at least three named metrics (with formulas or baselines) sourced from the supplied data; metrics whose baseline is unknown are explicitly labeled "baseline unknown."
- The constrained step and affected segment are identified, with symptoms held separate from plausible causes and activation, retention, monetization, and distribution dependencies each checked or marked "not applicable" with a reason.
- At least three experiments are proposed, each with a primary metric, a guardrail, and a decision rule (ship, iterate, stop); hypotheses are ranked by evidence and impact, not by intuition.
- When the supplied data cannot localize a constrained step or the funnel definition is missing, the procedure refuses to name a bottleneck and returns the instrumentation gap as the next action.
