# Guardrails

> Output template for `pm-metrics/guardrail-design`. Guardrails protect against unintended consequences when moving a primary metric.

## Header

- **Primary metric:** _name + formula (link to north-star or metric-tree node)_
- **Target window:** _e.g., +5pp by 2026-Q4_
- **Author:** _PM_
- **Date:** _YYYY-MM-DD_

## Guardrails

| # | Name | Formula | Baseline (cited) | Threshold | Severity | Owner-when-breached | Watch cadence | Tripwire procedure | Risk hypothesis |
|---|---|---|---|---|---|---|---|---|---|
| 1 | _Support ticket rate per active user_ | _tickets_W / WAU_W_ | _0.04 (cite source)_ | _stay below 0.06_ | _yellow_ | _PM + Support lead_ | _daily_ | _Within 24h, decide pause / proceed_ | _Aggressive activation pushes load to support_ |
| 2 | _Error rate p95_ | _err_5xx / requests_ | _0.2% (cite)_ | _stay below 0.5%_ | _blocking_ | _Eng lead_ | _real-time_ | _Rollback on breach; postmortem_ | _Activation funnel changes may regress checkout_ |
| 3 | _Margin per active user_ | _revenue/user − COGS/user_ | _<cite>_ | _stay above $X_ | _yellow_ | _Finance + PM_ | _weekly_ | _Surface in status memo; revisit pricing_ | _Free-trial bias may erode margin_ |

> Add 3-6 rows. Every blocking guardrail must have a rollback or pause procedure.

## Severity definitions

- **Blocking** — if breached, the change ships back / rolls back; non-negotiable. Authority: _<role>_.
- **Yellow flag** — if breached, team huddles within 24h and decides whether to continue.
- **Awareness** — tracked; no automatic action.

## Not a guardrail (explicit non-watches)

| Metric | Why not tracked |
|---|---|
| _Brand sentiment_ | _too slow to react; tracked separately by marketing_ |
| _Specific cohort retention_ | _the primary metric already captures the relevant signal_ |

## Sources

- Primary metric definition: _link to north-star or metric-tree_
- Historical incidents informing risk hypotheses (optional): _link_
- Instrumentation references: _link_
