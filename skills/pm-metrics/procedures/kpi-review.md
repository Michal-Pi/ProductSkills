# KPI Review

## Goal

Audit a set of existing KPI definitions for measurability, tractability, and decision-relevance. Output is a per-KPI verdict and recommendations: keep / revise / retire / instrument.

## Input expected

- The KPI list (names, descriptions, current targets if any)
- How each KPI is currently measured (event source, dashboard link, formula)
- Who owns each KPI and how it is used in decisions
- Optional: dashboards, prior reviews, or incident reports referencing the KPI

## Output produced

A document with one row per KPI plus a roll-up:

- **Per KPI:** name, current definition, current source/formula, measurability check (Y/N + reason), tractability check (Y/N + reason — can the team move it?), decision-relevance check (Y/N + reason — what decision does this KPI inform?), verdict (keep / revise / retire / instrument), recommendation (specific action), owner-of-action
- **Roll-up:** counts per verdict, total instrumentation gaps, top KPIs to revise first
- A "missing KPI" list: gaps in the existing set that the team should add (with reason)

## Steps

1. For each KPI, restate the definition in plain language and check if the formula is precise. Ambiguous formulas ("user engagement," "activation rate" without a definition) get **revise**.
2. Measurability check: can the KPI be computed from the current data sources? If not, mark **instrument** and name the missing event / property / source.
3. Tractability check: can the team move this KPI through product action? KPIs that depend mostly on external factors (market conditions, sales pipeline timing) are mark **awareness only** — they are not actionable PM KPIs.
4. Decision-relevance check: what decision does this KPI inform? If the answer is "we just report it," mark **retire** unless it is a regulatory or contractual obligation.
5. Goodhart's-law check: could the team game this KPI without delivering user value? If yes, recommend pairing with a guardrail (via `guardrail-design`).
6. Verdict per KPI:
   - **keep** — definition precise, measurable, tractable, decision-relevant
   - **revise** — fix the definition or formula
   - **retire** — KPI does not inform a decision and is not regulated
   - **instrument** — definition is right but data is missing
7. Identify missing KPIs. Compare against the product's north-star and metric tree (if either exists). Gaps go on the "missing KPI" list with reason.
8. Recommend a sequence for the team to act on revisions: instrument the highest-value gaps first; retire low-value KPIs to free attention.

## Links

- Reference: `../../../references/methods/metric-design.md`
- Adjacent: `../../pm-metrics/procedures/metric-tree.md` (when revising, the tree provides the structural anchor)
- Adjacent: `../../pm-metrics/procedures/guardrail-design.md` (when KPI is gameable)

## Done when

- Every KPI in the input has a verdict (keep / revise / retire / instrument) with one-line rationale.
- Measurability, tractability, and decision-relevance are each checked explicitly per KPI.
- Goodhart's-law check is performed per KPI and gameable ones are paired with a guardrail recommendation.
- A "missing KPI" list exists naming gaps against the north-star or metric tree.
- A roll-up table shows counts per verdict and identifies the top 3 highest-impact actions.
- No invented baseline or industry benchmark appears anywhere in the output.
