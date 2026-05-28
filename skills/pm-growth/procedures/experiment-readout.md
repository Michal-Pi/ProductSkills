# Experiment Readout

## Goal

Write up a completed growth experiment so the team has a durable record of what was tested, what the result was, what is decided (ship / iterate / kill / inconclusive), and what changes downstream (in the roadmap, in the metric tree, in the next experiment).

## Input expected

- The experiment brief (from `lifecycle-experiment.md` or `funnel-stage-analysis.md` proposal) — must include hypothesis, primary metric, guardrail metrics, audience, duration, decision rule
- Observed results — primary metric delta with confidence interval (or directional read with caveats if the test was underpowered), guardrail metric deltas
- Sample size and analysis cadence (peeked? interim? final?)
- Optional: qualitative feedback from users in the test arm
- Optional: known instrumentation issues that may affect read

## Output produced

A structured readout document with:

- Header: experiment id, hypothesis (1 sentence), test window, audience, sample size, primary metric, guardrails
- Result summary: primary metric delta + confidence; guardrail deltas; one-line conclusion (the BLUF)
- Decision: ship full / ship to subset / iterate / kill / inconclusive — with named decision-owner
- Why the decision (mechanism narrative, ≤3 sentences)
- What changes downstream:
  - Roadmap implication (which bet moves, is added, or is cut — cite `pm-roadmap`)
  - Metric-tree implication (sensitivity confirmed / updated — cite `pm-metrics`)
  - Next-experiment proposal (what to test next given what we learned)
- Open caveats: instrumentation issues, underpowered cuts, generalization concerns
- Sources: experiment brief link, dashboards, qualitative notes

## Steps

1. State the hypothesis and the decision rule that was set BEFORE the test. Do not retrofit the rule to the result.
2. Report the result against the pre-stated decision rule. Did it pass, miss, or fall in the ambiguous zone?
3. Report guardrail deltas honestly. A primary win paired with a guardrail trip is not a clean win — call it out.
4. Pick the decision (ship / iterate / kill / inconclusive). If inconclusive, say what additional data would resolve it and whether re-running is worth the cost.
5. Write the mechanism narrative: why do we believe the observed result happened? Avoid "the data clearly shows" — the data shows a delta; the mechanism is the team's hypothesis about what caused it.
6. Identify roadmap implications (cite `pm-roadmap` if a roadmap shift follows).
7. Identify metric-tree implications (was the predicted sensitivity correct? Update `pm-metrics`).
8. Propose the next experiment if there is one. Name the question it answers.
9. Surface caveats explicitly. Peeking, underpowered cuts, sample-ratio mismatch, instrumentation glitches.

## Refusal contract

- If the experiment had no pre-stated decision rule → refuse the readout (any decision rule retrofitted after seeing the result is unreliable). Route the team to write the decision rule into the brief, even retroactively, and label it as such.
- If the primary metric delta has no confidence interval AND the sample was small → refuse "ship" decisions and recommend either re-running or labeling as "directional, requires confirmation."

## Links

- Template: `../../../templates/experiment-brief.md` (the upstream brief that this reads out)
- Upstream: the lifecycle-experiment procedure (where briefs originate)
- Downstream: `../../pm-roadmap/SKILL.md` (roadmap shifts), `../../pm-metrics/SKILL.md` (tree updates)
- Schema: when the experiment is a post-launch learning loop, the readout structured fields conform to `../../../schemas/post-launch-learning.schema.json` — `decision` uses the enum `[iterate, monitor, scale, rollback_or_pause, return_to_discovery, stop]`.

## Done when

- Pre-stated hypothesis and decision rule are quoted at the top — not paraphrased.
- Primary metric delta has a confidence interval OR is explicitly labeled directional with sample-size caveat.
- Guardrail deltas are reported even when the team would prefer to bury them.
- Decision is one of: ship full, ship to subset, iterate, kill, inconclusive — named with decision-owner.
- Mechanism narrative is ≤3 sentences and does not overclaim ("the data clearly shows" is refused).
- Roadmap and metric-tree implications are explicit (or marked "no implication this cycle").
- Caveats are listed; silent caveats are not allowed.
- If the brief lacked a pre-stated decision rule, the readout was refused (per refusal contract).
