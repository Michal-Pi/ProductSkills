# Stakeholder Communications

Methods reference for `pm-stakeholder-comms` procedures. Calibrate every output by **audience-first framing**, **BLUF (bottom line up front)**, balance of **ask / risk / decision**, and **tone calibration by audience tier**.

## Audience tiers

The skill's procedures take `audience.tier` as a required input. Each tier has different attention budget, depth tolerance, and language calibration.

| Tier | Attention budget | Depth tolerance | Language calibration |
|---|---|---|---|
| **board** | 90 seconds | Lowest — decisions and risks only | No internal jargon, no acronyms without expansion, no team names without one-line role context |
| **exec** | 60-120 seconds | Low-medium — decisions, risks, top deltas | Expand acronyms once, name owners by role, link deep-dives instead of inlining |
| **lead** | 3-5 minutes | Medium — context, status, tradeoffs | Some shared internal vocabulary acceptable; spell out cross-team dependencies |
| **peer** | 5-10 minutes | Higher — context, status, technical detail | Internal vocabulary expected; assumes shared context |

If `audience.tier` is missing, the procedure refuses. Tone calibration is not optional — a board update written in peer tone (e.g., 8 minutes of technical detail) buries the decision; a peer update written in board tone (60 seconds, no context) leaves the audience underinformed.

## BLUF — Bottom Line Up Front

The first sentence states the conclusion, decision, or ask. Not the topic, not the context, not the build-up. If the reader reads only the first sentence, they have the answer.

**Anti-patterns (refuse to ship):**

- "I wanted to share an update on…" → states the topic, not the conclusion.
- "Following our discussion last week…" → states the context, not the conclusion.
- "There are several things to consider…" → states the difficulty, not the conclusion.

**Patterns that pass:**

- "Project A is on track for end-of-quarter; Project B will slip 2 weeks pending infra ship."
- "Decision: we are deprecating the legacy import flow on 2026-08-01. Three teams affected — details below."
- "I need a yes/no on the additional headcount ask by Friday 2026-06-04 to lock the offer."

## The ask / risk / decision balance

Every internal communication carries some mix of three loads:

- **Ask:** a thing the audience must do (decide, approve, prioritize, deconflict)
- **Risk:** something the audience must know that could change outcomes
- **Decision (already made):** something the audience must know happened

A status memo is mostly decisions-already-made + risks + a small ask budget. An exec update is mostly status + risks + a focused ask. A decision-comms is entirely decisions-already-made. An ask-framing is entirely ask.

Mixing all three with no signal of which is which is the failure mode. The output template separates them visually and the procedures require which one is the dominant intent.

## Evidence anchors

Internal communications cite evidence the same way external artifacts do: short stable identifiers (`EVID-001`, `INT-042`, `SUP-117`, `METRIC-tree:activation/D7`). Claims without anchors are framed as opinion, not status.

Procedures REFUSE to ship claims of progress, risk, or change without an evidence anchor. This is what makes the skill trustworthy across rapid cadences — if every claim is cited, the audience does not need to chase down sources.

## When NOT to use this skill

- A customer is the audience → route to `pm-gtm` (launch comms, release notes, in-product messaging).
- A durable record of a decision is needed → route to `pm-docs/decision-memo`. Use `decision-comms` only to socialize the decision after the memo exists.
- A PRD or technical spec is being authored → route to `pm-docs/prd` or `pm-docs/rfc`.
- An experiment is being summarized for the team → route to `pm-growth/experiment-readout`.
- A postmortem is being written → route to `pm-docs/postmortem` (product failures only).

## Recurring-cadence rule

For `status-memo`, the prior-period link is required (or explicitly marked "first issue"). The procedure refuses without one because delta framing — "what changed since last period" — is the entire point of a recurring memo. A status memo that reads as a snapshot, not a delta, has no recurring value.

## Tone red flags

- Excessive hedging ("we believe", "it seems", "it could potentially") softens decisions into opinions.
- Passive voice on accountability ("a decision was made") removes ownership; name the decider.
- Overclaiming on evidence ("the data clearly shows") without an anchor is grader-style rubric-echo; cite or soften.
