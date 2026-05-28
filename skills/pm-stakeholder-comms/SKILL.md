---
name: pm-stakeholder-comms
description: Author internal stakeholder communications — exec/leadership updates, recurring product status memos, ask framings for cross-functional decisions, and post-decision socialization. Use when the user asks to write a status update, exec memo, ask doc, or to communicate a decision to a team or leadership audience. Do not use for durable record-keeping (route to pm-docs/decision-memo), customer-facing release notes or launch comms (route to pm-gtm), or product specs/RFCs (route to pm-docs).
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# PM Stakeholder Comms

Internal-audience product communications. Every output starts from a structured audience + intent contract; otherwise the procedure refuses.

## Core Procedures

- For executive or leadership status memos, use `procedures/exec-update.md`.
- For recurring product status (weekly / biweekly / monthly), use `procedures/status-memo.md`.
- For framing a single ask of a stakeholder (decision needed, escalation, resource request), use `procedures/ask-framing.md`.
- For socializing a decision *after* it has been made, use `procedures/decision-comms.md`.

## References

- Use `../../references/methods/stakeholder-comms.md` for audience-first framing, BLUF, ask/risk/decision balance, and tone calibration by audience tier.
- Use `../../templates/exec-update.md`, `../../templates/status-memo.md`, `../../templates/ask-framing.md`, `../../templates/decision-comms.md` for the artifacts.

## Required input contract (load-bearing)

Every procedure in this skill REFUSES to produce output unless the caller supplies, at minimum, **`audience.tier` and `intent`**. The full structured input expected per procedure is:

- `audience: { tier: exec | lead | peer | board, function: eng | gtm | design | finance | legal | cs, decision_authority: yes | no }`
- `intent: ask | status | escalation | fyi | decision-comms`
- `key_message: <single sentence — the BLUF>`
- `risks_to_surface: [<list>]` (may be empty for `fyi`)
- `decisions_or_asks: [<list>]` (required for `ask` / `escalation` / `decision-comms`; may be empty for `status` / `fyi`)
- `evidence_anchors: [<INT- / SUP- / SALES- / GTM- / ...>]` (required when claims are made)
- `next_action: <owner + date, if any>`

This is what distinguishes a PM stakeholder communication from a generic memo. Without audience tier, you cannot calibrate tone, depth, or framing; without intent, you cannot choose the right structure (a `status` reads differently from an `ask`).

## Method Selection

- Audience is executive or board + intent is status → `exec-update`.
- Audience is mixed internal + intent is status, on a recurring cadence → `status-memo`.
- Intent is `ask` or `escalation`, single decision → `ask-framing`.
- A decision has already been made and the team needs to know → `decision-comms`.

## Boundary rules

- **For-the-record vs for-the-audience.** `pm-docs/decision-memo` produces the durable artifact (audit trail, future-reader). `pm-stakeholder-comms/decision-comms` produces the message that informs people the decision happened. If the user wants both, they are separate outputs from separate skills.
- **Internal vs customer.** `pm-gtm` owns customer-facing launch comms, release notes, and external press. `pm-stakeholder-comms` owns internal stakeholder comms (exec, eng, GTM peers, board).
- Do **not** use this skill for: PRDs (route to `pm-docs`), customer-facing release notes (route to `pm-gtm`), experiment writeups (route to `pm-growth/experiment-readout`), or postmortems (route to `pm-docs/postmortem`).

## Stop rules

- If `audience.tier` is missing → refuse with: "Stakeholder communication requires `audience.tier` (exec / lead / peer / board). Please supply, then resume."
- If `intent` is missing → refuse with: "Stakeholder communication requires `intent` (ask / status / escalation / fyi / decision-comms). Please supply, then resume."
- If `intent` is `ask`, `escalation`, or `decision-comms` AND `decisions_or_asks` is empty → refuse: name the ask or decision.
- If the request mentions a customer-facing audience (press, customers, end users, public release notes) → refuse and route to `pm-gtm`.
- If the request asks for a durable decision record → refuse and route to `pm-docs/decision-memo`.
