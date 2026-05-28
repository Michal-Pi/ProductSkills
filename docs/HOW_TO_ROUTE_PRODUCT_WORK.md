# How to Route Product Work

> Replaces the legacy `HOW_TO_USE_PRODUCT_OS_WORKFLOW.md` (which described the now-retired `workflow-product-operating-system`). Routing is now adapter-owned. The canonical routing reference is `references/routing/artifact-to-workflow.md`.

## TL;DR

ProductSkills is a pack of focused PM skills (13 total in 0.3.0). There is **no master workflow**. The adapter (Claude / Codex / Cursor / Gemini) classifies the input artifact and routes to one of the skills. If the input doesn't clearly match a row in the routing table, the adapter asks the user to clarify intent — it does not silently pick.

## The routing table

The full table is in `references/routing/artifact-to-workflow.md`. Summary:

| If your input is… | …route to |
|---|---|
| Raw interviews / support / sales notes | **pm-discovery** (cluster into themes) |
| Inbound feature-request backlog needing routing decisions | **pm-roadmap** (intake-triage) |
| Founder hypothesis, no customer evidence | **workflow-discovery-to-prd** (returns blocked + research plan) |
| Synthesized research ready to draft a PRD | **workflow-discovery-to-prd** |
| Opportunity or strategy question | **pm-strategy** (which bet) OR **pm-validation** (test assumption) |
| Rough PRD with gaps — "continue the workflow" framing | **workflow-discovery-to-prd** (spec-reviews internally) |
| Standalone "review this PRD" request | **pm-docs/spec-review** |
| Approved PRD ready for delivery | **workflow-prd-to-linear-delivery** |
| Delivery scope (already split) | **pm-delivery** (escalate to workflow-prd-to-linear-delivery for Linear preview) |
| Launch request | **pm-gtm/launch-readiness** |
| Post-launch metric / signal / experiment result | **pm-growth/experiment-readout** or **pm-gtm/post-launch-review** |
| Decision needing durable record | **pm-docs/decision-memo** (narrative form or bullet log entry) |
| Decision needing socialization to internal audiences | **pm-stakeholder-comms/decision-comms** |

## Safety contract

External tool writes (Notion, Linear) are dry-run first, with explicit confirmation tied to the previewed payload, `idempotency_key`, and `dry_run_payload_hash`. Display names (team keys, label names, page titles) are never write-ready — resolve to tool IDs first. Never claim rollback; provide a manual revert payload instead. The canonical safety contract is `references/mcp/dry-run-preview.md`.

## When the workflow halts

Workflows return a structured `blocked-workflow` envelope per `schemas/blocked-workflow.schema.json` with `handoff_target: pm-discovery` (the canonical resume target — see `references/workflows/workflow-lifecycle-statuses.md`).

## Boundary disambiguators (the disputed pairs)

| Pair | Disambiguator |
|---|---|
| pm-roadmap vs pm-strategy | Prioritization decision already made → pm-roadmap. Still choosing bets → pm-strategy. |
| pm-discovery vs pm-roadmap (both have "intake-triage") | Raw evidence to cluster into themes → pm-discovery. Request backlog needing routing → pm-roadmap. |
| pm-docs/decision-memo vs pm-stakeholder-comms/decision-comms | For the record → pm-docs. To inform the team → pm-stakeholder-comms. Same data, different framing. |
| pm-stakeholder-comms vs pm-gtm | Internal audience (exec, board, eng lead, GTM peer) → pm-stakeholder-comms. External (customers, press, in-product release notes) → pm-gtm. |
| pm-validation vs pm-growth | Pre-build experiment on an assumption → pm-validation. Post-ship experiment on a live product metric → pm-growth. |
| pm-metrics vs pm-growth | Designing the metric tree or north-star → pm-metrics. Using the tree to find leverage → pm-growth. |

## Lifecycle statuses

The shared lifecycle status list (`intake_received`, `evidence_insufficient`, `evidence_synthesized`, `prd_review_required`, `approved_for_delivery`, `ready_for_launch_review`, `learning_loop_open`, `blocked`, etc.) lives in `references/workflows/workflow-lifecycle-statuses.md` and is enforced by `schemas/workflow-stage.schema.json`. Re-entry tests (Phase 4 Task 4.2) validate transitions against `evals/allowed-transitions.yaml`.

## Migration from 0.2.x

If you previously invoked `workflow-product-operating-system` directly: in 0.3.0 the adapter handles classification. Submit the same artifact; the adapter routes it. For Notion or Linear writes you previously routed via `pm-tooling`: that skill is gone — `workflow-prd-to-linear-delivery` (Linear) and `workflow-discovery-to-prd` (optional Notion sync) own the dry-run safety contract now.

## Adapter rename note

The Claude/Codex/Cursor adapter is renamed from `product-operating-system` to `product-skills` in 0.3.0. Installer backward-compat is handled in Phase 5 Task 5.2b — for one minor release the installer accepts the old name and emits a deprecation warning.
