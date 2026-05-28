---
name: pm-roadmap
description: Sequence chosen product bets into a roadmap artifact — themes, time slices, capacity envelopes, dependencies, and confidence bands. Use when the user asks to build a roadmap, plan a quarter, triage a feature-request backlog into routing decisions, or map cross-initiative dependencies. Do not use for choosing which bets to make (route to pm-strategy/prioritization) or for individual feature scoping (route to pm-discovery or pm-docs).
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# PM Roadmap

Sequence chosen bets into a presentable, capacity-aware roadmap. This skill assumes the prioritization decision has already been made — it does not re-rank.

## Core Procedures

- For building a themed, time-sliced roadmap from a prioritized backlog, use `procedures/roadmap-build.md`.
- For triaging an inbound feature-request backlog into routing decisions (ignore / monitor / research / validate / sequence), use `procedures/intake-triage.md`.
- For selecting the bets a quarter actually commits to from a prioritized list, use `procedures/quarterly-planning.md`.
- For surfacing dependencies across initiatives before commitment, use `procedures/dependency-mapping.md`.

## References

- Use `../../references/methods/roadmap-methods.md` to choose between Now-Next-Later, theme-based, time-sliced, and capacity-aware shapes.
- Use `../../references/methods/evidence-grading.md` when triaging requests with thin evidence.
- Use `../../references/methods/large-corpus-synthesis.md` when the intake backlog is large or noisy.
- Use `../../templates/roadmap.md` for the roadmap artifact.
- Use `../../templates/intake-triage.md` for triage outputs.

## Method Selection

- Use `roadmap-build` when the user has a prioritized list and asks for a roadmap artifact.
- Use `quarterly-planning` when the question is "what should we commit to next quarter" given capacity.
- Use `intake-triage` when the input is a request backlog (support tickets, sales asks, exec requests) — route each item before sequencing.
- Use `dependency-mapping` before committing to a quarter when ≥2 initiatives touch shared surfaces (auth, data model, infra).

## Boundary rules

- **pm-strategy chooses bets** (RICE/WSJF/ICE/etc); **pm-roadmap sequences chosen bets**. If the user is still deciding what to build, route to `pm-strategy/prioritization`.
- pm-roadmap produces a presentable artifact; pm-strategy produces a decision.
- Do **not** use pm-roadmap for individual feature scoping — route to `pm-discovery` (for problem framing) or `pm-docs/prd` (for the spec).
- Do **not** use pm-roadmap to author stakeholder updates about the roadmap — route to `pm-stakeholder-comms`.
- Capacity claims must cite a source (team headcount, average velocity, leave/holiday adjustments). Do not assert capacity by feel.

## Stop rules

- If no prioritized backlog is supplied AND the user asks for a "roadmap," ask the user to either supply one or route to `pm-strategy/prioritization` first.
- If the requested time horizon exceeds 4 quarters AND no strategy/north-star is referenced, refuse and ask for `pm-strategy` and `pm-metrics` inputs first.
- If a "request" is actually a customer outage or incident, refuse and route to engineering on-call (not a roadmap input).
