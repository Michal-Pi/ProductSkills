# Artifact → Workflow Routing

Canonical entry-classification table used by every ProductSkills adapter. Given an input artifact, classify it once and route to the correct skill or workflow. The adapter is the router; the package does not have a master workflow.

## Routing table

| # | Input artifact type | Entry status (lifecycle) | Required check | Routed skill / workflow |
|---|---|---|---|---|
| 1 | Raw interviews, support tickets, sales notes, analytics rows | `intake_received` | source inventory exists | **pm-discovery** — `intake-triage` then `voc-synthesis` |
| 2 | Inbound feature-request backlog needing routing (sequence vs ignore vs research vs validate) | `intake_received` | source mix + strategic anchors named | **pm-roadmap** — `intake-triage` (the routing-decision flavor) |
| 3 | Founder hypothesis with no customer evidence | `evidence_insufficient` | missing-evidence list explicit | **workflow-discovery-to-prd** — runs intake, fails readiness, returns `decision_status: blocked` with a research plan (via pm-discovery/research-plan) and a blocked-workflow envelope |
| 4 | Synthesized research — themes and opportunities exist, ready to draft a PRD | `evidence_synthesized` | confidence per theme + gap list | **workflow-discovery-to-prd** |
| 5 | Opportunity or strategy note (prioritization needed OR assumptions to test) | `opportunity_framed` | assumptions and risks listed | **pm-strategy** (`prioritization`) if the question is which bet; **pm-validation** (`assumption-map`) if the question is what must be true |
| 6 | Rough PRD with gaps (the request is "continue the workflow from this PRD") | `prd_review_required` | spec-review checklist | **workflow-discovery-to-prd** — runs spec-review at Step 8 and routes back to discovery (research-plan) if readiness fails; converges to a completed PRD if readiness passes |
| 6a | Standalone request to review a PRD (no orchestration ask) | `prd_review_required` | spec-review checklist only | **pm-docs/spec-review** — one-shot review with severity-classified findings; no orchestration |
| 7 | Approved PRD ready to break into delivery work | `approved_for_delivery` | scope, non-goals, success metrics present | **workflow-prd-to-linear-delivery** |
| 8 | Delivery-ready scope already split (epics/stories exist) | `delivery_review_required` | story value + acceptance criteria + edge cases | **pm-delivery** (refine) — escalate to **workflow-prd-to-linear-delivery** if Linear preview is requested |
| 9 | Launch request (ship decision needed) | `ready_for_launch_review` | audience, impact, risk, support, enablement | **pm-gtm** — `launch-readiness` |
| 10 | Post-launch metric readout / signal / experiment result | `learning_loop_open` | metric + signal integrity | **pm-growth** — `experiment-readout` or `funnel-stage-analysis` (the diagnosis); **pm-gtm** — `post-launch-review` (adoption focus) |
| 11 | Decision needing a durable for-the-record artifact | `decision_pending_record` | options ≥2 + evidence + owner + date | **pm-docs** — `decision-memo` (narrative form) or **pm-docs/decision-memo** with bullet-log form (`templates/decision-log-entry.md`) |
| 12 | Decision needing socialization to a team or leadership audience | `decision_pending_comms` | audience.tier + intent + decision link | **pm-stakeholder-comms** — `decision-comms` |

## Boundary disambiguators (the disputed pairs)

These pairs use the same surface inputs but route to different skills. Adapters should walk both columns before picking:

- **Roadmap-sequence vs strategy-prioritize**: The prioritization decision has been made → `pm-roadmap`. The bet selection is still open → `pm-strategy`.
- **Discovery-cluster vs roadmap-route**: Inputs are raw evidence to cluster into themes → `pm-discovery`. Inputs are a backlog of requests needing routing decisions → `pm-roadmap`.
- **Decision-memo vs decision-comms** (per A12): User says "record this decision" or "ADR" → `pm-docs/decision-memo`. User says "tell the team we decided X" or "communicate the decision" → `pm-stakeholder-comms/decision-comms`. Same data, different framing.
- **Stakeholder-comms vs gtm**: Audience is internal (exec, board, eng lead, GTM peer) → `pm-stakeholder-comms`. Audience is external (customers, press, in-product release notes) → `pm-gtm`.
- **PM-validation vs PM-growth**: Pre-build experiment to test an assumption → `pm-validation`. Post-ship experiment against a metric on a live product → `pm-growth`.
- **PM-metrics vs PM-growth**: Designing the metric tree or selecting the north-star → `pm-metrics`. Using the tree to find leverage and run experiments → `pm-growth`.

## Catch-all rule (per A9)

**If the input doesn't clearly match any row in the table, do not silently pick a skill.** Ask the user to clarify intent and offer 2-3 most likely workflows from the table with their differentiators. Examples:

- "This looks like either a roadmap sequencing question (`pm-roadmap`) or a prioritization decision (`pm-strategy`). Do you have a prioritized list of bets already, or are you still choosing between them?"
- "I can take this as a decision memo for the record (`pm-docs/decision-memo`) OR as a message to socialize the decision (`pm-stakeholder-comms/decision-comms`). Which do you want?"

## Safety rules (apply universally)

These rules are owned by individual skills but the router enforces them at intake to fail fast:

1. **Never assume evidence the user did not supply.** Inputs without cited sources route to either a research plan or a refusal — never to a committed-scope artifact.
2. **External writes (Notion, Linear) are dry-run first.** Any input requesting a Notion or Linear write routes through `workflow-discovery-to-prd` or `workflow-prd-to-linear-delivery`, which honor the canonical safety contract at `references/mcp/dry-run-preview.md`.
3. **Blocked workflows return a structured envelope.** When the workflow halts, output validates against `schemas/blocked-workflow.schema.json`. Canonical resume target is `pm-discovery` (per `references/workflows/workflow-lifecycle-statuses.md` §"Canonical resume targets").
4. **Postmortems refuse SRE/ops incidents at intake.** `pm-docs/postmortem` Step 1 is a structured refusal contract for any input naming outage, downtime, SLA, SLO, auth failure, latency regression, on-call, infrastructure incident, or security breach.
5. **`pm-stakeholder-comms` refuses output without `audience.tier` and `intent`.** The structured input contract is load-bearing.

## Re-entry rules

When the input includes an existing lifecycle-state artifact (handoff envelope, stage output), do not replay earlier stages:

- If readiness check at the artifact's stated stage passes → continue from there.
- If the readiness check fails → move backward one stage and address the gap.
- `validation_not_required` is acceptable when the input is already approved, validated, or starts from a later lifecycle artifact.

See `references/workflows/workflow-lifecycle-statuses.md` for the canonical lifecycle status list and `evals/allowed-transitions.yaml` (when introduced in Phase 4) for legal state machine transitions.

## Cross-references

- Per-tool safety: `references/mcp/dry-run-preview.md`
- Canonical resume rules: `references/workflows/workflow-lifecycle-statuses.md`
- Lifecycle status schema: `schemas/workflow-stage.schema.json`
- Blocked-workflow envelope: `schemas/blocked-workflow.schema.json`
