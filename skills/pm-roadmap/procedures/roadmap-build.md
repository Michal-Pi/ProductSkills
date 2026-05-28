# Roadmap Build

## Goal

Turn a prioritized backlog of bets into a themed, time-sliced roadmap artifact with explicit confidence bands and capacity envelopes.

## Input expected

- Prioritized backlog (from `pm-strategy/prioritization` — RICE/WSJF/ICE/scorecard output, or equivalent ranked list with method noted)
- Time horizon (e.g., 2 quarters, 1 year, Now/Next/Later)
- Team capacity inputs: headcount, average completed-bet rate, known leave/holiday windows
- Optional: existing north-star + input metrics from `pm-metrics` (used for theme labelling and target-window framing)
- Optional: known dependencies surfaced by the dependency-mapping procedure

## Output produced

- A roadmap document filled from `../../../templates/roadmap.md`:
  - Themes × time-slice grid (rows = themes; columns = Now/Next/Later or Q1..Qn)
  - Per-bet entry with: title, theme, time-slice, owner-or-driver, confidence band (high / medium / low), capacity estimate, dependency callouts, primary success metric (cited from `pm-metrics` if available)
  - Capacity envelope per slice with utilization % and overflow flag
  - Explicit "Not in this roadmap" list (bets the prioritization ranked but capacity excluded)
  - Open questions and assumptions block

## Steps

1. Confirm the prioritized backlog exists with a method noted. If absent, stop and route to `pm-strategy/prioritization`.
2. Pick a roadmap shape using `../../../references/methods/roadmap-methods.md` (Now-Next-Later default for fast-moving teams; quarterly time-sliced for committed teams; capacity-aware for teams shared across initiatives).
3. Cluster bets into 3-7 themes. Themes should be customer-job or strategic-pillar shaped, not team-shaped.
4. Place each bet on the time grid using capacity arithmetic: per-slice capacity = (engineers × weeks × velocity factor) − leave − fixed overhead. Bets without sized estimates use confidence band = low and flag for sizing.
5. Assign each bet a confidence band: **high** (scoped, sized, dependencies known); **medium** (scoped, sized but ≥1 unresolved dependency); **low** (unscoped or unsized).
6. Cite any cross-initiative dependency from the dependency-mapping procedure or flag as "dependency unverified" if no mapping ran.
7. Compute per-slice utilization. If >100%, surface the overflow and propose 2 cut/defer options.
8. List the explicit "Not in this roadmap" set drawn from the prioritized backlog tail — names + the reason (capacity / dependency / confidence).
9. Note any bet whose success metric is missing from `pm-metrics` and flag as a follow-up.

## Links

- Template: `../../../templates/roadmap.md`
- Reference: `../../../references/methods/roadmap-methods.md`
- Method selection upstream: `../../pm-strategy/procedures/prioritization.md`
- Dependencies upstream: `../../pm-roadmap/procedures/dependency-mapping.md`

## Done when

- Every roadmap slot has: title, theme, time-slice, confidence band, capacity estimate, and either a cited success metric or an explicit "metric gap — route to pm-metrics" flag.
- Per-slice utilization is computed and ≤100% OR overflow is surfaced with ≥2 cut/defer options.
- The "Not in this roadmap" list names every bet in the prioritized backlog that did not make the cut, with the reason.
- At least one cross-initiative dependency is either resolved (via the dependency-mapping procedure) or explicitly marked unverified.
- The output cites the prioritization method used upstream (the roadmap does not re-rank).
