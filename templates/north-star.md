# North-Star Metric

> Output template for `pm-metrics/north-star-design`. Fill every section.

## Header

- **Product / area:** _e.g., Atlas Campaigns_
- **Author:** _PM_
- **Date:** _YYYY-MM-DD_
- **Linked product goal:** _from pm-strategy artifact — link_
- **Target segment:** _named segment + their value moment_

## North-star

_<verb> <measurable noun> <window>_

Example: _weekly active campaigns sent per workspace_

## Formula

- **Numerator:** _precise definition_
- **Denominator:** _precise definition (or "absolute count")_
- **Exclusions:** _e.g., internal accounts, test workspaces_
- **Deduplication rule:** _e.g., one event per (workspace_id, campaign_id) per week_
- **Time window:** _e.g., trailing 7 days, ISO week_

## Why this metric

_One paragraph. How this metric mechanically links to the product goal._

## Leading vs lagging

- **Classification:** _leading / lagging_
- **Reason:** _what moves first; what this metric is downstream of_

## Measurability status

- [ ] **Measurable today** — events / properties cited: _<EVT-id>, <PROP-id>_
- [ ] **Measurable with named instrumentation work** — scope: _<work>_; owner: _<name>_; ETA: _<date>_
- [ ] **Not measurable** — procedure refused; routed to engineering to scope instrumentation

## Positive sanity checks (≥2)

- _Scenario that should move the metric in the expected direction_
- _Scenario that should move the metric in the expected direction_

## Negative sanity checks (Goodhart guard, ≥2)

- _Scenario where the metric could move without delivering user value_
- _Scenario where the metric could move without delivering user value_

> If any negative scenario is easy to execute, tighten the formula or pair with guardrails (`pm-metrics/guardrail-design`).

## Replacement watch

- _Observable condition that would prompt re-evaluating this north-star_

## Rejected candidates

| Candidate | Reason rejected |
|---|---|
| _Candidate B_ | _e.g., not measurable; gameable by support-driven inflation_ |

## Sources

- Goal artifact (pm-strategy): _link_
- Instrumentation schema reference: _link_
