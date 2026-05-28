# Metric Tree

## Goal

Decompose a north-star into the input metrics that drive it, with explicit formulas linking inputs to the output. The tree is the artifact the team uses to choose where to invest.

## Input expected

- North-star metric with its formula (from `north-star-design`)
- Product mental model: the user journey, the loops, the value moments
- Existing instrumentation: what is measurable today
- Optional: prior metric trees, dashboards, or KPI lists
- Optional: pm-growth growth-loop diagnosis (if it exists)

## Output produced

A document filled from `../../../templates/metric-tree.md`:

- North-star at the root
- 2-4 level-1 input metrics, each with: formula, why it drives the north-star, measurement status (measurable / scoped / not measurable), baseline value (cited or "missing"), expected sensitivity (how much would a 10% improvement here move the north-star?)
- Level-2 inputs under each level-1 (where useful)
- Cross-references where inputs depend on inputs (e.g., retention depends on activation quality)
- Gaps: nodes that should exist but lack instrumentation, with named instrumentation work
- Investment heatmap: which nodes have the largest expected sensitivity AND the most headroom

## Steps

1. Place the north-star at the root with its formula.
2. Identify level-1 inputs. For a typical user-action north-star this is usually some combination of acquisition, activation, retention, monetization, referral; for a typical reliability or quality north-star it is something different. Pick inputs that mechanically combine into the north-star, not adjacent metrics.
3. For each level-1 input, write the formula linking it to the north-star. "Engagement → north-star" is not a formula; "(weekly_active_users × actions_per_active_user × retention_curve_M3) → weekly_active_campaigns" is.
4. For each input, state the baseline value with a cited source. If unknown, flag "baseline missing" and propose `kpi-review` or instrumentation work.
5. Decompose to level-2 where useful — e.g., activation = (signup_completion_rate × first_value_moment_completion × week_1_return). Stop decomposing when the leaves are operationally actionable (a team can move them) and instrumented.
6. Mark cross-dependencies. Activation quality affects retention; retention affects monetization; refer leakage affects acquisition. Explicit edges prevent siloed investment.
7. Identify the **investment heatmap**: per node, expected sensitivity × current headroom. Nodes with high sensitivity AND high headroom are the leverage points; document them so `pm-growth` and `pm-strategy` can use them.
8. List instrumentation gaps. For each, propose owner, ETA, and what unlocks once measured.

## Links

- Template: `../../../templates/metric-tree.md`
- Reference: `../../../references/methods/metric-design.md`
- Upstream: `../../pm-metrics/procedures/north-star-design.md`
- Downstream: `../../pm-growth/SKILL.md` (uses tree to find leverage)

## Done when

- The north-star sits at the root with formula.
- ≥2 level-1 inputs are present, each with a formula linking it to the north-star and a baseline (cited) or flagged "baseline missing."
- ≥1 level-2 decomposition is present under at least one level-1 node.
- Cross-dependencies are marked where they exist.
- Instrumentation gaps are listed with proposed owner and ETA.
- The investment heatmap names ≥1 leverage node.
- No baseline value is invented; every cited baseline has a source.
