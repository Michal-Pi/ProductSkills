# Decision Comms

## Goal

Socialize a decision that has *already been made* — inform the team and stakeholders the decision happened, why, what changes for whom, and what's next. This is distinct from `pm-docs/decision-memo`, which produces the durable for-the-record artifact. `decision-comms` is the message that travels.

## Input expected (REQUIRED — procedure refuses without these)

- `audience: { tier: exec | lead | peer | board, function: <function or mixed>, decision_authority: no }` — **REQUIRED**
- `intent: decision-comms` — **REQUIRED**
- `key_message: <one sentence — what was decided>` — **REQUIRED**
- `decisions_or_asks: [<the decision(s) being communicated>]` — **REQUIRED, non-empty**
- `decision_made_by: <name + role + date>` — **REQUIRED**
- `decision_memo_link: <url to pm-docs/decision-memo artifact>` — **REQUIRED IF the decision is durable**; if no memo exists, the procedure recommends creating one before sending
- `rationale: <why this option was chosen>` — **REQUIRED**
- `affected_audiences: [{ audience: <name>, impact: <one line> }]` — **REQUIRED**
- `next_action: { owner, date, action }` — required when the decision triggers immediate follow-up
- `risks_to_surface: [<list>]` — may be empty
- `evidence_anchors: [<id>]` — required when claims are made

## Output produced

A document filled from `../../../templates/decision-comms.md`:

- BLUF (the decision itself)
- Why this decision (rationale, ≤3 sentences, cite evidence)
- Decision-maker + date + link to durable memo
- Who is affected and how (per-audience impact line)
- What changes operationally (concrete shifts in plans, roadmap, ownership)
- Open risks acknowledged
- Next actions with owner + date
- How to ask questions (a designated channel / owner)

## Refusal contract (Step 1)

1. If `audience.tier` is missing → refuse.
2. If `intent` ≠ `decision-comms` → refuse: route to the appropriate procedure.
3. If `decisions_or_asks` is empty → refuse: name the decision.
4. If `decision_made_by` is missing → refuse: a decision without a named decider is not a decision yet — route to `ask-framing` or `pm-docs/decision-memo`.
5. If `decision_memo_link` is missing AND the decision is durable (changes roadmap, scope, ownership, or strategy) → refuse with: "Decision-comms socializes a recorded decision. Create the durable memo via `pm-docs/decision-memo` first, then resume." (For genuinely lightweight comms — e.g., a meeting time change — the procedure may proceed with `decision_memo_link: not_required` explicitly set.)
6. If `rationale` is missing → refuse: communicating a decision without a reason erodes trust.
7. If `affected_audiences` is empty → refuse: every decision affects someone; name them.

## Steps

1. Run the refusal contract.
2. BLUF is the decision itself in a single sentence.
3. Rationale: ≤3 sentences. Avoid restating the entire ask-framing or memo. Link to the memo for the long version.
4. Identify affected audiences explicitly. Per audience: what changes for them. "Everyone" is not an audience — break it down.
5. Operational changes: what shifts in plans, roadmap, ownership, scope. Be concrete; "we'll adjust accordingly" is not concrete.
6. Open risks acknowledged: list residual risks the decision did not eliminate.
7. Next actions: who does what by when.
8. Designate a question channel (Slack thread, doc comments, office hours) so the comms doesn't generate dispersed back-channel confusion.

## Links

- Template: `../../../templates/decision-comms.md`
- Reference: `../../../references/methods/stakeholder-comms.md`
- Upstream (the durable record of the decision): the pm-docs decision-memo procedure (see `../../pm-docs/SKILL.md`)
- Adjacent (if there's a related ask that produced the decision): `../../pm-stakeholder-comms/procedures/ask-framing.md`

## Done when

- Refusal contract ran.
- BLUF is the decision in one sentence.
- Decision-maker is named with role and date.
- A `decision_memo_link` is provided OR the procedure has explicitly classified the decision as lightweight.
- Rationale is ≤3 sentences with cited evidence.
- `affected_audiences` is non-empty and each row names a concrete impact.
- Operational changes are concrete (named plans, roadmap rows, ownership shifts), not vague.
- Open risks are listed even if mitigated; residuals are acknowledged.
- A question channel is designated.
