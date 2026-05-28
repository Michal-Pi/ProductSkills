# Roadmap

> Output template for `pm-roadmap/roadmap-build` and `pm-roadmap/quarterly-planning`. Fill every section. Replace placeholder text in italics.

## Header

- **Roadmap name:** _e.g., Atlas H2 2026 — Reliability + Activation_
- **Owner:** _PM owner_
- **Time horizon:** _Now-Next-Later / Quarterly / Date range_
- **Time shape:** _now-next-later | quarterly | half | annual_
- **Last updated:** _YYYY-MM-DD_
- **North-star metric (cited):** _from pm-metrics; if absent, write `MISSING — flag to pm-metrics`_
- **Prioritization method upstream:** _e.g., RICE — see <link to prioritization-decision>_

## Strategic anchors

- **Active strategic pillars / themes the roadmap serves:** _2-5 pillars, one line each_
- **Locked commitments (regulatory / contract / executive):** _list with source citation; these are not discretionary_

## Capacity envelope

| Slice | Team | Headcount | Weeks | Velocity factor | Leave / KTLO subtracted | Slack reserved | Net capacity |
|---|---|---|---|---|---|---|---|
| _Now / Q1_ | _team_ | _N_ | _W_ | _0.0–1.0_ | _N hours / pts_ | _≥15%_ | _result_ |

_Cite every number. Estimates without a source are not capacity claims._

## Themes × time grid

| Theme | Now / Q1 | Next / Q2 | Later / Q3+ |
|---|---|---|---|
| _Theme 1_ | _Bet A (conf: H, cap: 4w, metric: M1)_ | _Bet C (conf: M)_ | _Bet D (conf: L)_ |
| _Theme 2_ | _Bet B (conf: H)_ | … | … |

## Bet detail

For each bet listed in the grid:

### Bet: _<title>_

- **Theme:** _which theme_
- **Time-slice:** _Now / Q1 / etc._
- **Confidence band:** _High (scoped, sized, deps known) | Medium (scoped, sized, ≥1 unresolved dep) | Low (unscoped or unsized)_
- **Capacity estimate:** _engineer-weeks; cite source — sizing doc / analog comparison / placeholder_
- **Primary success metric:** _cite metric ID from pm-metrics; if absent, `MISSING — route to pm-metrics`_
- **Target window:** _when the metric is expected to move and by how much_
- **Owner / driver:** _name_
- **Dependencies:** _list cross-initiative or upstream-team dependencies; cite dependency-mapping entry_
- **Open questions / risks:** _explicit list_

## Slack buffer

- **Reserved %:** _≥15%_
- **Use cases:** _unplanned escalations, carry-over from prior slice, dependency slippage_

## Not in this roadmap

| Bet from prioritized backlog | Reason excluded | Revisit when |
|---|---|---|
| _Bet X_ | _capacity exhausted_ | _next planning cycle_ |
| _Bet Y_ | _dependency unresolved_ | _post infra-quarter_ |
| _Bet Z_ | _confidence Low — needs research / validation_ | _after `pm-discovery` runs_ |

## Next-period candidates (for the next planning cycle)

- _Named bets so next quarter starts with a prepared shortlist, not a blank page_

## Assumptions and open questions

- _e.g., "Assume infra ships rate-limiter by week 6 — UNCONFIRMED, owner: @infra-lead"_
- _e.g., "Bet C lacks a success metric — route to pm-metrics before commit"_

## Sources

- Prioritization decision: _link_
- Capacity inputs: _link or doc reference_
- Dependency mapping: _link or `dependency-mapping` output_
- Strategy / pillars: _link to pm-strategy artifact_
