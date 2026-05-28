# Guardrail Design

## Goal

Define the guardrails that must hold while the team moves a primary metric — so the team does not move A by breaking B. Guardrails are the metrics that protect against unintended consequences.

## Input expected

- Primary metric being moved (from `north-star-design` or `metric-tree`)
- Product context: what could break when this metric improves
- Risk hypotheses from the team (e.g., "if we push activation harder, support load spikes")
- Optional: historical incidents where a metric was moved at the cost of another
- Optional: regulatory, contractual, or compliance constraints that are non-negotiable

## Output produced

A document filled from `../../../templates/guardrails.md`:

- Primary metric and its target window
- 3-6 guardrails, each with: name, formula, current baseline (cited), threshold (must stay above / below value), severity (blocking / yellow-flag / awareness), owner-when-breached, related risk hypothesis
- Watch cadence per guardrail (real-time / daily / weekly)
- Tripwire procedure: what happens when a guardrail trips (rollback / pause / escalate / accept-with-named-exception)
- "Not a guardrail" list — metrics the team considered but decided not to track, with reason

## Steps

1. State the primary metric and its target window from `metric-tree` or `north-star-design`.
2. Brainstorm risk hypotheses. For each plausible way to move the primary metric, name what could break:
   - User-experience guardrails (e.g., support ticket rate, task completion time, satisfaction)
   - Quality guardrails (e.g., error rate, perf p95, defect escape)
   - Business guardrails (e.g., margin, COGS per user, refund rate)
   - Compliance guardrails (e.g., privacy opt-out rate, content moderation events)
3. For each candidate guardrail, write the formula and find a baseline (cited). No invented numbers.
4. Set the threshold: above what value is the metric safe; below what value does the team commit to act? Threshold without a commitment is decoration.
5. Assign severity:
   - **Blocking** — if breached, the change ships back / rolls back; non-negotiable.
   - **Yellow flag** — if breached, the team huddles within 24h and decides whether to continue.
   - **Awareness** — tracked; no automatic action.
6. Set watch cadence per guardrail. Real-time guardrails need dashboards or alerts; weekly guardrails are reviewed in status memos.
7. Define the tripwire procedure per guardrail. Who acts; what action; on what authority. A guardrail without a tripwire is theater.
8. List "not a guardrail" — metrics the team explicitly chose not to track, with reason. This signals what the team is willing to risk.

## Links

- Template: `../../../templates/guardrails.md`
- Reference: `../../../references/methods/metric-design.md`
- Upstream: `../../pm-metrics/procedures/north-star-design.md`, `../../pm-metrics/procedures/metric-tree.md`

## Done when

- Primary metric and target window are stated.
- ≥3 guardrails are defined, each with formula, baseline (cited), threshold, severity, owner-when-breached, watch cadence.
- Every threshold has a commit-to-act (tripwire procedure).
- Severity classifications are explicit; no "blocking" guardrail without a rollback or pause procedure.
- "Not a guardrail" list exists — the team has explicitly named what it is willing to risk.
- No baseline is invented; every baseline cites a source or is flagged "baseline missing" and routed to instrumentation work.
