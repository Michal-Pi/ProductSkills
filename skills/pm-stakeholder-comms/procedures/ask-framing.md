# Ask Framing

## Goal

Frame a single ask of a stakeholder — a decision needed, an escalation, a resource request, or a deconflict — with enough structure that the recipient can act in one read, not a back-and-forth.

## Input expected (REQUIRED — procedure refuses without these)

- `audience: { tier: exec | lead | peer | board, function: <function>, decision_authority: yes | no }` — **REQUIRED**
- `intent: ask | escalation` — **REQUIRED**
- `key_message: <one sentence — the BLUF: the ask itself>` — **REQUIRED**
- `decisions_or_asks: [<the specific ask, one or more>]` — **REQUIRED, non-empty**
- `recommended_option: <recommended answer to the ask>` — **REQUIRED**
- `alternatives: [<≥1 alternative option with tradeoffs>]` — **REQUIRED**
- `deadline: <date and reason for the date>` — **REQUIRED**
- `risks_to_surface: [<list>]` — required for `escalation`
- `evidence_anchors: [<id>]` — required for claims of impact, urgency, or constraint
- `decision_owner: <name and role>` — **REQUIRED** (who can grant the ask)

## Output produced

A document filled from `../../../templates/ask-framing.md`:

- The ask, one sentence (BLUF)
- Why now (context, deadline driver, cited evidence)
- Recommended option with rationale
- Alternatives considered (≥1) with explicit tradeoffs
- Risks of not deciding by the deadline
- What we need from the decision-owner (a yes/no, a choice between options, a resource, a deconflict)
- Owner of the ask (you) + decision-owner (them) + date

## Refusal contract (Step 1)

1. If `audience.tier` is missing → refuse.
2. If `intent` is not `ask` or `escalation` → refuse: route to the appropriate procedure (status-memo for `status`, decision-comms for `decision-comms`).
3. If `decisions_or_asks` is empty → refuse: an ask procedure cannot run without an ask.
4. If `recommended_option` is missing → refuse: "Frame your recommended option before asking the stakeholder."
5. If `alternatives` is empty → refuse: a recommendation without alternatives is not an ask, it is a notification.
6. If `deadline` is missing → refuse: a deadline-less ask drifts.
7. If `decision_owner` is missing → refuse: name who can answer.
8. If impact / urgency claims exist AND `evidence_anchors` is empty → refuse: cite sources.

## Steps

1. Run the refusal contract.
2. Write the BLUF as the ask itself ("Approve $X for Y" / "Decide between A and B by Z" / "Resolve deconflict on shared surface S").
3. Why now: state the deadline driver. "By next quarter" is not a driver; "before pricing changes lock on 2026-07-01" is.
4. Recommended option + rationale (≤3 sentences). Cite evidence.
5. Alternatives: ≥1, each with: what it would mean, why we did not recommend it. Honest tradeoffs only — strawman alternatives undermine trust.
6. Risks of inaction: what gets worse if the deadline passes without a decision.
7. What we need: a single yes/no question, a choose-from-N question, or a named resource ask. Avoid ambiguous asks.
8. Calibrate tone for `audience.tier`. Exec/board: shorter, decision-anchored. Peer/lead: more context allowed.

## Links

- Template: `../../../templates/ask-framing.md`
- Reference: `../../../references/methods/stakeholder-comms.md`
- Downstream (after the decision is made): `../../pm-stakeholder-comms/procedures/decision-comms.md` to socialize.
- Adjacent (for the durable record of the decision): the pm-docs decision-memo procedure (see `../../pm-docs/SKILL.md`)

## Done when

- Refusal contract ran.
- BLUF reads as the ask itself, one sentence.
- Deadline is stated with a real driver, not a placeholder.
- Recommended option is named with rationale ≤3 sentences and cited evidence.
- ≥1 alternative is presented with honest tradeoffs (not a strawman).
- Risks of inaction are named.
- The "what we need" is a single concrete question or named ask, not ambiguous.
- Decision-owner is named with their role.
