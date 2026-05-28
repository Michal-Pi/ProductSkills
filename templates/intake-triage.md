# Intake Triage

> Output template for `pm-roadmap/intake-triage`. Fill every column. One row per input item.

## Header

- **Backlog name / window:** _e.g., Atlas inbound — 2026-W18 to W21_
- **Source mix:** _e.g., 12 support / 7 sales / 3 exec / 5 interview_
- **Strategy anchors used as filter:** _name the pillars or north-star inputs (cite pm-strategy / pm-metrics)_
- **Triage performed by:** _name_
- **Date:** _YYYY-MM-DD_

## Triage table

| id | source | problem (de-jargoned) | requested solution | evidence grade | strategic fit | duplicate-of | routing decision | next action | owner | follow-up date |
|---|---|---|---|---|---|---|---|---|---|---|
| INT-001 | support | _Onboarding step 3 confuses non-admins_ | _Add tooltip_ | B | yes — activation pillar | — | research | route to pm-discovery to confirm theme | @pm | 2026-06-04 |
| SAL-014 | sales | _Enterprise needs SSO claims mapping_ | _SAML attribute editor_ | A | yes — enterprise pillar | — | validate | smallest experiment to confirm willingness-to-pay | @pm | 2026-06-11 |
| EXE-002 | exec | _Concern about churn in mid-market_ | _"Build retention dashboard"_ | C | partial — needs metric tree | — | research | route to pm-metrics + pm-growth | @pm | 2026-06-18 |
| INT-007 | support | _Same as INT-001_ | _Help text_ | B | yes | INT-001 | (duplicate; folded into cluster) | — | — | — |

### Allowed routing decisions

- **ignore** — below evidence bar AND no strategic fit
- **monitor** — track recurring weak signals
- **research** — route to `pm-discovery` (problem unclear)
- **validate** — route to `pm-validation` (solution uncertain, problem clear)
- **sequence** — eligible for `pm-strategy/prioritization` then roadmap (evidence ≥B AND strategic fit clear)
- **escalate** — out of PM scope (incident → on-call; legal / pricing → respective owners)

## Justification block

For each item: one-line justification citing the rule that triggered the routing decision (e.g., "Evidence C + strategic fit unclear → research per intake-triage step 4").

## Duplicate clusters (top 3)

| cluster name | item count | total ARR or affected-users (cited; do not invent) | representative ids |
|---|---|---|---|
| _Onboarding step 3 confusion_ | 8 | _from supplied source; if no source, leave blank_ | INT-001, INT-007, … |

## Roll-up

- **Ignore:** _n_
- **Monitor:** _n_
- **Research:** _n_
- **Validate:** _n_
- **Sequence:** _n_
- **Escalate:** _n_
- **Duplicates folded:** _n_
- **Items with missing context:** _n_ (listed below)

## Items with missing context / open questions

- INT-XYZ — _what data is missing to grade or route_

## Do not roadmap (with reasons)

| id | reason |
|---|---|
| INT-XXX | _evidence grade D, no source_ |
| SAL-YYY | _strategic fit no — out of pillar scope_ |

## Sources

- Strategy: _link to pm-strategy artifact_
- Metric tree (if used): _link to pm-metrics output_
- Evidence grading rubric: `../references/methods/evidence-grading.md`
