# Status Memo

## Goal

Produce a recurring product status memo (typically weekly or biweekly) for an internal mixed audience (eng leads, GTM peers, design peers, adjacent PMs). Differs from `exec-update` in audience tier (peer / lead vs exec / board), depth (more detail allowed), and rhythm (recurring cadence with delta framing).

## Input expected (REQUIRED — procedure refuses without these)

- `audience: { tier: peer | lead, function: <function or mixed>, decision_authority: no }` — **REQUIRED**
- `intent: status | fyi` — **REQUIRED** (escalation / ask use other procedures)
- `key_message: <BLUF sentence>` — **REQUIRED**
- `cadence: weekly | biweekly | monthly` — **REQUIRED**
- `prior_period_link: <url or "first issue">` — required if cadence ≠ "first issue"
- `risks_to_surface: [<list>]` — may be empty for `fyi`
- `evidence_anchors: [<id>]` — required for any claim of progress or risk
- Optional: `top_priorities_next_period: [<list>]`

## Output produced

A document filled from `../../../templates/status-memo.md`:

- Header (period, cadence, audience, owner)
- BLUF
- Highlights since last period (shipped, validated, decided, learned)
- Status table (bet / theme: status color, delta from last period, evidence)
- Risks and blockers (with named owner and proposed mitigation)
- Decisions made (with link to decision-memos)
- Top priorities next period
- Optional appendix or deep-dive links

## Refusal contract (Step 1)

1. If `audience.tier` is missing OR is `exec` / `board` → refuse: "status-memo is for `peer` / `lead` audiences. For `exec` / `board`, use `exec-update`."
2. If `intent` is missing OR is `ask` / `escalation` / `decision-comms` → refuse: route to the appropriate procedure.
3. If `cadence` is missing → refuse: a recurring memo without a cadence cannot frame deltas.
4. If `cadence` ≠ "first issue" AND `prior_period_link` is missing → refuse: delta framing requires the prior period.
5. If progress / risk claims are made AND `evidence_anchors` is empty → refuse: cite sources.

Structured refusal envelope same shape as `exec-update`.

## Steps

1. Run the refusal contract.
2. Frame as a delta: every status-table row reports what changed since the prior period, not a snapshot.
3. Highlights: 3-7 bullets, each a concrete event (shipped X, decided Y, learned Z). Cite evidence.
4. Status table: bet/theme, color (G / Y / R), delta from prior period (improved / unchanged / regressed), one-line evidence.
5. Risks and blockers: each row names the owner and proposes a mitigation or ask. No risk listed without owner.
6. Decisions made this period: link to `pm-docs/decision-memo` artifacts. Decision-comms (this skill's separate procedure) handles socialization in detail; the status-memo notes the decision in passing.
7. Top priorities next period: 3-5 named items, each tied to a strategic anchor (cite pillar, north-star input, or committed bet).

## Links

- Template: `../../../templates/status-memo.md`
- Reference: `../../../references/methods/stakeholder-comms.md`

## Done when

- Refusal contract ran.
- Every row in the status table reports a delta, not a snapshot.
- Every risk has a named owner and a mitigation or ask.
- Every progress / risk claim cites an evidence anchor.
- Highlights are concrete events (verbs: shipped, decided, learned, observed), not abstractions.
- Top-priorities list ties each item to a strategic anchor.
- Cadence and prior-period-link are stated in the header (or "first issue" noted).
