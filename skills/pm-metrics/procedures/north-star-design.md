# North-Star Design

## Goal

Select a north-star metric for a product or product area, define its formula, confirm it is measurable today (or scope the instrumentation), and pin its expected leading vs lagging behavior.

## Input expected

- Product goal stated in user-outcome terms (from `pm-strategy`)
- Target customer segment and the value moment they experience
- Existing instrumentation: events, properties, identifiers available
- Optional: prior candidate metrics the team has used or considered
- Optional: constraints from regulatory, privacy, or contractual scope

## Output produced

A document filled from `../../../templates/north-star.md`:

- North-star candidate (verb + measurable noun + window)
- Formula (precise — operands, denominator, exclusions, deduplication rule, time window)
- Why this metric (links to product goal in one paragraph)
- Leading or lagging classification with reason
- Measurability status: **measurable today** (cite the event / property) | **measurable with named instrumentation work** (scope + owner) | **not measurable** (refuse and surface)
- Sanity checks: scenarios that should move the metric in the expected direction (positive checks) and scenarios where the metric should NOT move (negative checks — catches Goodhart's-law misuse)
- Replacement watch: signal patterns that would prompt re-evaluating this north-star (e.g., metric saturates, segment shifts, value moment changes)

## Steps

1. Restate the product goal in user-outcome terms. If the input goal is stated in feature or output terms ("ship X"), refuse and route to `pm-strategy/opportunity-framing`.
2. Propose 2-3 candidate north-stars. Each must be a verb + measurable noun + time window (e.g., "weekly active campaigns sent per workspace," not "engagement").
3. For each candidate, write the formula precisely: numerator, denominator, exclusions, dedup rule, time window.
4. Confirm measurability. For each formula component, cite the event or property in the current schema. If any component is missing, the candidate is "measurable with named instrumentation work" — name the work and the owner.
5. Classify leading vs lagging. A lagging metric (e.g., retention) is the right anchor but slow to move; pair with leading input metrics in `metric-tree`. A leading metric is the right anchor when the team needs short feedback loops; pair with a lagging guardrail.
6. Run positive sanity checks: name 2-3 scenarios that should move the metric in the expected direction.
7. Run negative sanity checks (Goodhart's-law guard): name ≥2 scenarios where the team could move the metric without delivering user value. If any are easy to game, either tighten the formula or pair with a guardrail in `guardrail-design`.
8. Recommend one candidate. Document the rejected ones with the reason.
9. Define a replacement watch: under what observable conditions would the team re-evaluate this north-star.

## Links

- Template: `../../../templates/north-star.md`
- Reference: `../../../references/methods/metric-design.md`
- Downstream: `../../pm-metrics/procedures/metric-tree.md`
- Adjacent: `../../pm-metrics/procedures/guardrail-design.md`

## Done when

- The chosen north-star is verb + measurable noun + window.
- The formula is precise: numerator, denominator, exclusions, dedup, window.
- Measurability is explicitly classified (measurable today / scoped instrumentation / not measurable). If "not measurable," procedure refused.
- Leading vs lagging is named with reason.
- ≥2 positive sanity scenarios and ≥2 negative (Goodhart-guard) scenarios are listed.
- Replacement watch conditions are named.
- Rejected candidates are listed with reasons.
