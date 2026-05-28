# Exec Update

## Goal

Produce a short, BLUF-led executive or leadership status memo calibrated to executive-tier attention budget. The reader has 60-120 seconds; everything else fights for that time.

## Input expected (REQUIRED — procedure refuses without these)

- `audience: { tier: exec | board, function: <function>, decision_authority: yes | no }` — **REQUIRED**
- `intent: status | escalation | fyi | decision-comms` — **REQUIRED**
- `key_message: <one sentence — the BLUF>` — **REQUIRED**
- `risks_to_surface: [<list>]` — required when intent ≠ `fyi`
- `decisions_or_asks: [<list>]` — required when intent is `escalation` or `decision-comms`
- `evidence_anchors: [<id>]` — required for any claim of progress, risk, or change
- `next_action: <owner + date>` — required when intent is `escalation` or `decision-comms`
- Optional: prior exec-update (used for delta framing)

## Output produced

A document filled from `../../../templates/exec-update.md`:

- BLUF (1 sentence)
- TL;DR (3 bullets max)
- Status of committed bets (Green / Yellow / Red with one-line reason, cited)
- Risks to surface (named, with evidence anchor and proposed mitigation)
- Decisions made or needed (each with owner and date)
- Asks of the exec audience (if any)
- Optional appendix link (deep-dive doc URL)

## Refusal contract (Step 1)

1. If `audience.tier` is missing OR not in `{exec, board}` → refuse: "exec-update is for `exec` or `board` audiences only. Use `status-memo` for peer / lead audiences."
2. If `intent` is missing → refuse: "Specify intent (status / escalation / fyi / decision-comms)."
3. If `intent` is `escalation` or `decision-comms` AND `decisions_or_asks` is empty → refuse: name the decision or ask.
4. If any progress / risk claim is made AND `evidence_anchors` is empty → refuse: cite the source.

Refusal is structured (machine-readable) so the caller can resume after supplying inputs:

```json
{
  "status": "blocked",
  "reason": "<which contract field was missing>",
  "missing_inputs": ["<field>", "..."],
  "resume_status": "ready_to_resume_once_inputs_supplied"
}
```

## Steps

1. Run the refusal contract above. Halt on any failure.
2. Calibrate tone for `audience.tier`: exec/board = decision-oriented, 60-120 second read, no jargon, no acronyms without expansion, no internal team names without one-line context.
3. Write the BLUF — the single sentence the reader leaves with if they read nothing else.
4. Write TL;DR ≤3 bullets. Each bullet = a delta from prior period or a decision-relevant fact.
5. Status of committed bets: list 3-7 bets max. Each line: bet name, color (G / Y / R), one-line reason, evidence anchor. Yellow and Red require a stated mitigation or a stated ask.
6. Risks: surface only material risks (would change a quarter outcome, a launch, or a metric trajectory). Cite evidence. Propose mitigation or ask for help.
7. Decisions made: each line: decision, who decided, when, link to decision-memo (`pm-docs/decision-memo`) if one exists.
8. Decisions needed: each line: decision, why it's escalating, recommended option + alternatives, deadline, owner-of-the-decision.
9. Asks: explicit, one per line, with owner and date.

## Links

- Template: `../../../templates/exec-update.md`
- Reference: `../../../references/methods/stakeholder-comms.md`
- Adjacent (for the durable record of a decision): the pm-docs decision-memo procedure (see `../../pm-docs/SKILL.md`)

## Done when

- The refusal contract was run and either halted with structured refusal OR every required field is supplied.
- BLUF is one sentence and reads as a decision-relevant statement, not a hedged status.
- TL;DR is ≤3 bullets and every bullet is a delta or decision-relevant fact.
- Every progress / risk claim has a cited `evidence_anchor`.
- Every Yellow / Red bet has either a stated mitigation or a stated ask.
- Decisions-needed list names the decision-owner, recommended option, and deadline; recommended option without alternatives is not allowed.
- Document length is calibrated to a 60-120 second read; sections that exceed budget are linked to an appendix, not inlined.
