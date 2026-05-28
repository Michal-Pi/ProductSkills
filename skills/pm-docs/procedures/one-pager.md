# One-Pager

## Goal

Produce a leadership-facing narrative one-pager (also called a vision brief or bet brief) that frames a product opportunity, the proposed bet, expected outcome, and the explicit ask of the reader — fitting on a single page so executives and cross-functional peers can react in one read.

## Input expected

- The bet or opportunity in one sentence (what we would do)
- Why now (the trigger, the window of opportunity, why this beats the next-best alternative)
- Target segment or customer (who benefits, ideally cited from `pm-discovery` or `pm-strategy/opportunity-sizing`)
- Expected outcome (a target metric movement — cite `pm-metrics` if available)
- Rough size (engineer-weeks or quarters; placeholder allowed but flagged)
- Known dependencies (other teams, infra, contracts)
- Reader and the ask: approval, feedback, or no-action FYI
- Optional: graded evidence (per `../../../references/methods/evidence-grading.md`)

## Output produced

A filled `../../../templates/one-pager.md` — narrative-first (prose paragraphs, not bullet lists), ≤500 words total, with one explicit ask of the reader, success-metric callout, and graded evidence behind every material claim.

## Steps

1. Confirm the ask. If the reader's desired action is not provided, stop and ask: approval, feedback, or FYI? A one-pager without a clear ask becomes a status memo and should be routed to `pm-stakeholder-comms`.
2. Open with the bet in one sentence — what we would do and for whom — before any context. Leaders skim the first sentence first.
3. Write the "why now" paragraph. If no time-bound trigger exists (regulatory window, competitor move, contract renewal, organizational moment), say so explicitly — many one-pagers fail because "why now" is missing.
4. Frame the customer and problem in 2-3 sentences. Cite a discovery artifact, interview corpus, or quantified opportunity from `pm-strategy/opportunity-sizing` if available. Inline placeholder evidence is allowed only when explicitly flagged "uncited — to confirm."
5. Sketch the proposed solution outline at the *concept* level — what the customer would experience, not how engineering would build it. If solution detail belongs in the doc, the artifact is a PRD, not a one-pager (route to `prd`).
6. State the expected outcome as a target metric movement with baseline + target + window. If the metric is unknown, flag the gap and route to `pm-metrics` rather than fabricate a number.
7. Name the top 2-3 risks. Steelman them; do not strawman.
8. Close with the ask. State it as a single imperative sentence: "We are asking for approval to staff this in Q3," "We are asking for written feedback by <date>," or "This is an FYI; no action needed."
9. Grade every material evidence claim H / M / L per `../../../references/methods/evidence-grading.md`. Anything ungraded reads as conjecture.

## Links

- Template: `../../../templates/one-pager.md`
- Reference: `../../../references/methods/evidence-grading.md`
- Reference: `../../../references/checklists/docs-quality.md`
- Optional upstream: the pm-strategy opportunity-sizing procedure when sizing is missing — see `../../pm-strategy/SKILL.md`
- Adjacent: the spec-review procedure in this skill (run after drafting to catch ungraded claims and missing ask)

## Done when

- The document fits ≤500 words (one printed page).
- The opening sentence states the bet — no preamble.
- "Why now" is named explicitly, even if the answer is "no time-bound trigger; opportunistic."
- The customer and problem are cited from a real source OR explicitly flagged "uncited — to confirm."
- The expected outcome is a measurable target with baseline + target + window, OR a flagged metric gap routed to `pm-metrics`.
- Exactly one explicit ask of the reader is stated (approval / feedback / FYI).
- Every material evidence claim is graded H / M / L.
- Narrative-first: prose paragraphs dominate; no section is reduced to a checklist or table when a sentence would do.
