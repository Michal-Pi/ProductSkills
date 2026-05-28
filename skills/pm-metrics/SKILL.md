---
name: pm-metrics
description: Design product metrics that anchor decisions — north-star selection, metric trees, input/output decomposition, guardrails, KPI review. Use when the user asks to choose a north-star metric, decompose a goal into measurable inputs, define guardrails, or review existing KPI definitions for measurability. Do not use for running an experiment against a metric (route to pm-growth or pm-validation) or for diagnosing growth bottlenecks (route to pm-growth/growth-loop-diagnosis).
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# PM Metrics

Design the metrics that anchor every other PM artifact. Outputs from this skill are cited by PRDs (success metrics), roadmaps (target windows), strategy (opportunity sizing), and growth (leverage points).

## Core Procedures

- For choosing a north-star and confirming it is measurable, use `procedures/north-star-design.md`.
- For decomposing a goal into a metric tree with explicit formulas, use `procedures/metric-tree.md`.
- For defining guardrails per metric (don't move A without watching B), use `procedures/guardrail-design.md`.
- For reviewing existing KPI definitions for measurability and tractability, use `procedures/kpi-review.md`.

## References

- Use `../../references/methods/metric-design.md` for north-star principles, leading-vs-lagging, input/output decomposition, and common pitfalls.
- Use `../../templates/north-star.md`, `../../templates/metric-tree.md`, `../../templates/guardrails.md` for outputs.

## Method Selection

- The team does not yet have a north-star → start with `north-star-design`.
- A north-star exists but is poorly decomposed → `metric-tree`.
- A north-star moves but secondary outcomes (quality, satisfaction, risk) are not watched → `guardrail-design`.
- A KPI exists but the team doubts its measurability or tractability → `kpi-review`.

## Boundary rules

- pm-metrics **designs the tree**; pm-growth **uses the tree to find leverage**. Diagnostics ("why isn't activation moving?") route to `pm-growth/growth-loop-diagnosis`.
- PRD "success metrics" sections cite the tree. When a PRD has weak metrics, pm-metrics may be invoked as a sub-procedure of `pm-docs/prd`.
- Do **not** use pm-metrics for running an experiment against a metric — route to `pm-growth` or `pm-validation`.
- Do **not** invent baseline numbers, target values, or industry benchmarks. Every claim of "current value" or "industry typical" requires a cited source. If the source is missing, the metric is flagged as "baseline missing" and the team is asked to instrument before targeting.

## Stop rules

- If the north-star candidate cannot be measured today and no instrumentation plan is proposed → refuse and route to engineering to scope instrumentation before designing the tree.
- If the user asks for "the right metric" without naming the product goal → refuse and route to `pm-strategy` to clarify the goal.
- If the user requests a specific numerical target without a baseline → refuse and ask for the baseline or propose `kpi-review` to assess current state first.
