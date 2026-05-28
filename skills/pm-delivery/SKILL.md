---
name: pm-delivery
description: Convert validated product scope into agile delivery artifacts — epics, user stories with split rationale, acceptance criteria including edge cases and failure states, sprint plans, task breakdowns, and the delivery handoff envelope. Use when the user asks to break product work into epics, stories, acceptance criteria, tasks, milestones, or sprint plans. Do not use for sequencing themes across quarters or capacity planning (route to pm-roadmap); for tool payload safety or Linear dry-run previews (route to workflow-prd-to-linear-delivery, which carries the canonical dry-run safety contract); or for choosing what to build in the first place (route to pm-strategy).
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# PM Delivery

Convert validated product scope into delivery artifacts without losing product intent.

## Core Procedures

- Use `procedures/epic-breakdown.md` for epic maps.
- Use `procedures/story-splitting.md` for sprint-ready user stories.
- Use `procedures/acceptance-criteria.md` for criteria and edge cases.
- Use `procedures/release-readiness.md` for ship or hold decisions.

## References

- Use `../../references/methods/delivery-handoff.md` for product-to-engineering handoffs.
- Use `../../references/methods/delivery-methods.md` for story splitting, acceptance criteria, and release checks.
- Use `../../references/checklists/delivery-method-coverage.md` before finalizing delivery handoffs.
- Use `../../templates/epic.md` and `../../templates/user-story.md` for structured outputs.

## Guardrails

- Do not create implementation tasks before product scope is clear.
- Stories must be valuable, testable, and small enough to plan.
- Acceptance criteria must include edge cases and failure states when relevant.
