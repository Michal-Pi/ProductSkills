# Decision Memo

## Goal

Write either a narrative **decision memo** or a single-row **decision-log entry** that records a durable product decision with provenance — what was decided, by whom, on what date, with what evidence, against what alternatives, and with what revisit trigger. This is the *for-the-record* artifact; socializing the decision to stakeholders is a separate concern handled by `pm-stakeholder-comms/decision-comms`.

## Form selection

The procedure produces two forms; the user request determines which:

- **Narrative form** (default) — produces a multi-section memo filled from `../../../templates/decision-memo.md`. Use when the user request includes any of: `memo`, `ADR`, `architecture decision record`, `record this decision`, `decision document`, `write up the decision`, or when no form keyword is provided.
- **Bullet-log form** — produces a 3-5 line entry filled from `../../../templates/decision-log-entry.md`, designed to append to a single running decision log. Use when the user request includes any of: `log entry`, `running log`, `decision log`, `quick decision`, `add to the log`, `append to log`.
- **Ambiguity rule:** if both signals appear, or neither appears, default to narrative. State the selected form explicitly in the output so the reader knows which shape was produced.
- **Mixed-batch rule:** if the user asks to record multiple decisions in one request, choose one form for all of them; do not interleave. Bullet-log form is usually correct for batches of ≥3.

## Input expected

- The decision in one sentence
- Date of decision and decision owner (name + role)
- ≥2 options considered, with evidence per option
- Why the selected option won (rationale)
- Assumptions and risks
- Expected outcome (the metric this decision is supposed to move, cited from `pm-metrics` if available)
- Revisit trigger or expiry condition (a date, a metric threshold, or an event)
- Optional: upstream prioritization-decision artifact when the decision came from a `pm-strategy` prioritization run

## Output produced

- Narrative form: filled `../../../templates/decision-memo.md` — ≥30 lines, sections per the template (decision, date, owner, context, options, evidence per option, selected option + rationale, assumptions, risks, expected outcome, revisit trigger).
- Bullet-log form: filled `../../../templates/decision-log-entry.md` — a 3-5 line entry appendable to a single running log file, with the same load-bearing fields (decision, owner, date, rationale gist, revisit) compressed into a stable row shape.

The output explicitly names which form was selected and why (form-selection rationale).

## Steps

1. **Select the form** using the rules above. State the selected form and the keyword that triggered the selection at the top of the output.
2. State the decision in a single sentence. Two sentences means the decision has not been fully resolved — surface that and route back to `pm-strategy/prioritization` or `pm-stakeholder-comms/ask-framing` for the unresolved half.
3. Record the date and the decision owner explicitly. Decisions without a named decider are not decisions yet (they are asks — route to `pm-stakeholder-comms/ask-framing`).
4. List ≥2 options considered, even when one feels obviously correct. The bar for "considered" is: the option was evaluated against the same evidence, not just acknowledged. Strawman options fail the Done When check.
5. For each option, summarize the evidence and grade it H / M / L per `../../../references/methods/evidence-grading.md`. Evidence missing per option is a tell that the comparison was post-hoc rationalization.
6. State why the selected option won. Two sentences max — link to the prioritization artifact if the decision came from a `pm-strategy` run (see the upstream prioritization procedure in `../../pm-strategy/SKILL.md`).
7. Name assumptions and risks explicitly. Assumptions are claims taken as true without proof; risks are things that could invalidate the decision. Keep them separate.
8. State the expected outcome as a metric movement (baseline + target + window). Cite `pm-metrics` if a metric tree exists; if not, flag the gap rather than fabricate.
9. Name a revisit trigger: a date, a metric threshold, or an event ("if activation drops below 25%," "by Q3 review," "if competitor X launches Y"). Decisions without a revisit trigger become tribal lore.
10. If narrative form: fill all sections of the template; do not collapse to bullets. If bullet-log form: keep the entry 3-5 lines, append-shape, and ensure every load-bearing field appears even compressed.

## Links

- Template (narrative): `../../../templates/decision-memo.md`
- Template (bullet log entry): `../../../templates/decision-log-entry.md`
- Reference: `../../../references/methods/evidence-grading.md`
- Upstream (when the decision came from a prioritization run): the prioritization procedure in pm-strategy — see `../../pm-strategy/SKILL.md`
- Adjacent (socializing the decision, distinct from recording it): the decision-comms procedure in pm-stakeholder-comms — see `../../pm-stakeholder-comms/SKILL.md`

## Done when

- The output declares which form was selected (narrative or bullet-log) and which keyword triggered the selection.
- The decision is stated in a single sentence.
- Date and decision owner (name + role) are present.
- ≥2 options are listed with rationale per option, and no option is strawmanned.
- Evidence is graded H / M / L per claim per `../../../references/methods/evidence-grading.md`.
- Assumptions and risks are listed separately, not merged.
- Expected outcome is a measurable metric movement (baseline + target + window) OR an explicit metric-gap flag routed to `pm-metrics`.
- A revisit trigger is named (date, metric threshold, or event); "revisit when convenient" is not acceptable.
- In narrative form: every template section is filled and the output is ≥30 lines. In bullet-log form: the entry is 3-5 lines with every load-bearing field present.
