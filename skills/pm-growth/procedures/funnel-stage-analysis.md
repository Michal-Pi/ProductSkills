# Funnel-Stage Analysis (Parameterized)

## Goal

Diagnose a single funnel stage — **activation**, **retention**, or **monetization** — by mapping the value moment for the stage, naming the bottleneck, and proposing experiments with metric, guardrail, and decision rule. The stage is a parameter; the analysis structure is shared.

## Input expected

- `stage: activation | retention | monetization` — **REQUIRED**
- Target segment (or "all" if not stratified)
- Current bottleneck symptoms (e.g., "signup completion is 60% but only 12% reach first-value moment")
- Data: instrumentation for the stage's value moment; baselines from `pm-metrics` if available
- Optional: prior experiment history on the stage
- Optional: known dependencies (acquisition quality affecting activation; activation quality affecting retention)

## Output produced

A structured stage analysis filled to the shape below:

- Stage and target segment
- Stage definition (precise: what counts as "activated" / "retained" / "monetized" for this product)
- Value-moment map (steps from stage entry to stage outcome)
- Bottleneck identification (where users drop, with cited evidence)
- Cross-stage cause check (what upstream/downstream stages might be the real cause)
- Hypothesis list (ranked by evidence strength and expected impact)
- Experiment proposals (each with primary metric, guardrail metric, audience, duration, decision rule)
- Open questions and follow-ups

## Steps

1. **Validate stage parameter.** If `stage` is missing or not one of `activation | retention | monetization`, refuse and ask which stage.
2. **Apply the stage-specific definition rule:**
   - **activation**: define the activation event (the first-value moment) and the time window for it. Map every step from signup to the activation event.
   - **retention**: define the retained behavior and the time window (e.g., week-2 return, M3 monthly active). Segment by use case, acquisition source, plan, persona, or activation path.
   - **monetization**: define the monetization objective (conversion to paid, expansion, ARPU lift, etc.), the segment, and the pricing metric or willingness-to-pay anchor.
3. **Map the value moment.** Walk through the user's journey for this stage. Identify the steps explicitly. Use a numbered list, not prose.
4. **Identify the bottleneck.** Cite evidence (a funnel number, a cohort retention curve, a conversion rate). Bottleneck claims without an evidence anchor are refused.
5. **Cross-stage check (stage-specific):**
   - activation → check whether acquisition quality is the real cause (low-intent traffic looks like an activation problem).
   - retention → check whether activation depth (did the user really reach first value?) is the real cause.
   - monetization → check whether the issue is value, packaging, timing, trust, procurement, or price (not all monetization issues are pricing issues).
6. **Propose hypotheses** ranked by evidence strength and expected impact. Each hypothesis names the proposed change and the mechanism by which it would move the stage metric.
7. **Propose experiments** for the top hypotheses. Use `../../../templates/experiment-brief.md` for each. Required per experiment: primary metric, guardrail metric, audience, duration, decision rule.
8. **List open questions** — anything the data can't yet answer (e.g., "we need a segment cut by acquisition channel to distinguish hypothesis A from B").

## Stage-specific guardrails

- **activation**: do not propose tooltip-style fixes without an evidence base; UX friction that looks like a tooltip problem is often a value-clarity problem.
- **retention**: distinguish product-value retention failures from reminder/lifecycle/segmentation failures. A re-engagement campaign that pulls users back without restored value masks the problem.
- **monetization**: do not assume price is the lever. Walk through value / packaging / timing / trust / procurement before pricing changes.

## Links

- Template: `../../../templates/experiment-brief.md`
- Reference: `../../../references/frameworks/growth-models.md` (per-stage frameworks)
- Adjacent: `growth-loop-diagnosis.md` when the stage analysis surfaces a cross-loop dependency (do not duplicate; route to loop diagnosis)
- Metric anchor: outputs cite `pm-metrics` north-star and metric-tree where they exist

## Done when

- The `stage` parameter is set and validated (one of activation / retention / monetization).
- Stage-specific definition is precise (event + window for activation; behavior + window for retention; objective + metric for monetization).
- Value-moment steps are listed and at least one bottleneck is named with a cited evidence anchor.
- The cross-stage cause check ran explicitly and concluded either "stage is the real cause" or "upstream cause X — route to that stage's analysis."
- ≥2 hypotheses are ranked with stated mechanism.
- ≥1 experiment proposal exists with primary metric, guardrail metric, audience, duration, and decision rule, using `experiment-brief.md`.
- Stage-specific guardrails were applied (the appropriate one — tooltip-trap for activation, masking-recheck for retention, levers-walk for monetization).
- Open questions list non-answerable items rather than silently dropping them.
