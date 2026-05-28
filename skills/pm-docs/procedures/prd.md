# PRD

## Goal

Author or revise a Product Requirements Document — the durable, structured commitment artifact that scopes a feature or initiative for engineering, design, GTM, and leadership. This procedure is invoked both as a standalone request (the user has evidence and a decision and wants the doc) and as the writing step inside `workflow-discovery-to-prd` (which orchestrates evidence gates and stop points, then delegates writing here).

## Input expected

- Objective (the outcome the PRD commits to)
- Target user / segment and the decision status (decided / in-flight / blocked)
- Available evidence (interviews, support, analytics, market, prior validation) — with citations
- Scope intent (what the user wants in vs. out)
- Constraints (capacity, deadlines, dependencies, contracts)
- Optional: upstream artifacts — `pm-strategy/prioritization-decision` if the bet came from a prioritization run, `pm-discovery` corpus, `pm-validation` decision, `pm-metrics` tree

## Output produced

A filled `../../../templates/prd.md` with all 14 sections non-empty OR explicitly marked "open question." When the PRD feeds delivery, the structured handoff schema applies — see the prd-to-delivery handoff schema at `../../../schemas/prd-to-delivery-handoff.schema.json`.

## Steps

1. Clarify objective, target user, and decision status. The objective is a single-sentence outcome (what changes for the user / business by when). The target user is segment + job-to-be-done, cited from a discovery source. The decision status flags whether scope is committed or still under review — PRDs authored before the decision is made are RFCs (route to the rfc procedure).
2. Pull evidence from discovery, analytics, market, and stakeholder sources. Grade every material claim H / M / L per `../../../references/methods/evidence-grading.md`. Citations are mandatory; uncited claims must be marked as assumptions, not evidence.
3. Separate assumptions and open questions from confirmed facts. Assumptions are working beliefs the PRD accepts; open questions are gaps that need resolving. Each assumption names which decision it underpins; each open question names an owner and a target answer date.
4. Define scope, non-goals, solution outline, success metrics, risks, and rollout notes. Scope is customer-visible outcomes, not implementation tasks. Non-goals are mandatory and must each name a reason (out of strategy, deferred to later PRD, unbounded risk). Solution outline stays at concept level — implementation detail belongs in the downstream engineering SDD, not the PRD.
5. Add acceptance-level product requirements without over-specifying implementation. Requirements describe behavior and outcomes from the user's perspective. If a "requirement" reads like an implementation directive ("use Postgres," "build a React modal"), strip it back to the behavior it enforces.
6. Flag gaps that block delivery. Missing evidence, missing metric, unresolved dependency, undecided UX — each blocking gap is named as an open question with a path to closure. A PRD with hidden gaps fails downstream; surface them in the artifact, do not paper over them.

## Spec-review pass

Before declaring the PRD done, run the spec-review procedure (in this same skill) over the draft. Spec-review applies the universal quality gate — severity rubric, missing sections, ungraded claims, scope-vs-non-goals conflicts. Blocking findings either get resolved or get documented as open questions.

## Links

- Template: `../../../templates/prd.md`
- Reference: `../../../references/methods/evidence-grading.md`
- Reference: `../../../references/checklists/docs-quality.md`
- Schema (when feeding delivery): `../../../schemas/prd-to-delivery-handoff.schema.json`
- Adjacent (quality gate, run before declaring done): the spec-review procedure in this skill

## Done when

- Every PRD section is non-empty OR explicitly marked "open question" with owner and target date.
- Evidence is separated from inference — every material claim is either cited (with grade H / M / L) or marked as an assumption.
- Success metrics are measurable: each metric carries baseline + target + window, OR explicitly flags a metric gap routed to `pm-metrics`.
- Non-goals are explicit, and each non-goal names a reason (out of strategy, deferred, unbounded risk).
- Spec-review checklist passes with zero blocking issues, OR every remaining blocking issue is documented as an open question with owner and target close date.
