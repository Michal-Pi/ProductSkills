# PRD — Product Requirements Document

> Output template for `pm-docs/prd`. Fill every section. If a section cannot be answered yet, mark it explicitly as "open question" with an owner and a date — do not silently leave it blank. Replace placeholder text in italics.

## Objective

_The single-sentence outcome this PRD commits to. What changes for the user / business by when. State the outcome, not the feature._

## Customer

_Target segment, the job-to-be-done, and the trigger context. Cite the discovery source — interview corpus, segment definition from pm-strategy, support cluster from intake-triage. If the customer is conjecture, mark it open and route to pm-discovery._

## Evidence

_Graded evidence behind the problem and the proposed solution. Use H / M / L per `../references/methods/evidence-grading.md`. Separate evidence from inference — a claim derived from an interview theme is inference, not evidence, until grounded in citations._

## Problem

_The user problem in 2-4 sentences. What hurts today, when, for whom. The problem must be solvable without naming the chosen solution; if the problem reads like a backwards-derived justification for a pre-decided solution, surface that and re-frame._

## Assumptions

_Claims taken as true without proof. List separately from open questions: assumptions are working beliefs the PRD accepts; open questions are gaps that need resolving. Each assumption identifies which decision it underpins so future readers can re-test it._

## Scope

_What ships in this PRD. State scope as customer-visible outcomes, not implementation tasks. Where scope is uncertain, mark the uncertain edges explicitly so reviewers can challenge them._

## Non-Goals

_What this PRD explicitly does NOT cover, even when reviewers might expect it to. Non-goals must be explicit — a missing non-goals section is a scope ambiguity, not a clean PRD. Each non-goal names the reason (out of strategy, deferred to later PRD, unbounded scope risk, etc.)._

## Solution Outline

_Concept-level description of what the customer will experience. Not implementation detail — that belongs in the engineering SDD downstream. Cite related design explorations from pm-design if any._

## User Experience

_The key flows in 2-5 bullets or one short diagram. Cite mockups, prototypes, or usability test plans from pm-design where they exist. Where UX is undecided, mark it as an open question with a design owner._

## Success Metrics

_Measurable outcomes with baseline + target + window. Cite the metric tree from pm-metrics if it exists; if the metric does not exist yet, flag the gap explicitly and route to pm-metrics rather than fabricate a number. A success metric without baseline + window is unfalsifiable and fails the Done When check._

## Risks

_What could invalidate the bet, broken down by category: customer (we're wrong about the problem), evidence (the data is thinner than it looks), execution (build / launch / rollout risk), and external (market, dependency, regulatory). Steelman, do not strawman._

## Open Questions

_Gaps that need resolving before scope is committed. Each open question names an owner and a target answer date. Open questions are not a dumping ground — every entry has a path to closure._

## Next Actions

_The immediate work to make this PRD shippable: research to run, validation to design, dependencies to confirm, reviews to schedule. Each next action has an owner and a date._
