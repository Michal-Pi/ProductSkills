---
name: pm-discovery
description: Product discovery workflows for customer interviews, VoC synthesis, research planning, raw-evidence intake clustering, support/sales feedback triage, customer pains, jobs-to-be-done, opportunity framing, and discovery-to-PRD preparation. Use when the user asks to analyze customer evidence, synthesize interviews, cluster raw evidence into themes, or plan product research. Do not use for routing inbound feature requests into roadmap-sequencing decisions (route to pm-roadmap/intake-triage); for the end-to-end discovery-to-PRD orchestration (route to workflow-discovery-to-prd, which calls this skill for the synthesis step); or for prioritization between opportunities (route to pm-strategy).
---

# PM Discovery

Turn messy customer and market inputs into structured product evidence.

## Core Procedures

- For intake triage, use `procedures/intake-triage.md`.
- For VoC synthesis, use `procedures/voc-synthesis.md`.
- For interview analysis, use `procedures/interview-analysis.md`.
- For research planning, use `procedures/research-plan.md`.
- For opportunity framing, use `procedures/opportunity-framing.md`.

## References

- Use `../../references/frameworks/continuous-discovery.md` for opportunity solution trees and assumption-first discovery.
- Use `../../references/methods/evidence-grading.md` when rating confidence.
- Use `../../references/methods/large-corpus-synthesis.md` when evidence volume requires batching, dedupe, conflict tracking, or noisy-signal suppression.
- Use `../../references/methods/research-methods.md` when choosing discovery methods.
- Use `../../references/checklists/discovery-method-coverage.md` before considering discovery work complete.
- Use `../../templates/research-plan.md` when evidence is too thin for a PRD or delivery commitment.

## Output Standard

Always separate direct evidence from inference. Preserve important quotes. Mark evidence confidence as high, medium, or low. For large corpora, preserve the `evidence_ledger`, batch summaries, duplicate handling, conflict register, missing fields, minority signals, and noisy-signal suppression decisions.

## Guardrails

- Do not convert discovery into delivery commitments without an explicit validation or PRD step.
- Do not invent customer evidence.
- If evidence is thin, return questions and a research plan instead of pretending certainty.
