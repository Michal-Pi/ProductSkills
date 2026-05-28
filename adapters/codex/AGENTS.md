<!-- PRODUCT_SKILLS_START -->
# ProductSkills

ProductSkills is a PM skill pack at `{{PACKAGE_STORE}}`. There is no master workflow — route product work to the right skill based on the input artifact type.

## Routing (artifact → skill)

| Input artifact | Routed skill / workflow |
|---|---|
| Raw interviews / support / sales notes | **pm-discovery** |
| Feature-request backlog needing routing | **pm-roadmap** (intake-triage) |
| Founder hypothesis, no evidence | **workflow-discovery-to-prd** (returns `decision_status: blocked` + research plan) |
| Synthesized research ready for PRD | **workflow-discovery-to-prd** |
| Opportunity or strategy question | **pm-strategy** (which bet) OR **pm-validation** (test assumption) |
| Rough PRD ("continue the workflow" framing) | **workflow-discovery-to-prd** (spec-reviews internally) |
| Standalone "review this PRD" request | **pm-docs** spec-review |
| Approved PRD | **workflow-prd-to-linear-delivery** |
| Delivery scope (already split) | **pm-delivery**; escalate to workflow-prd-to-linear-delivery for Linear preview |
| Launch request | **pm-gtm** launch-readiness |
| Post-launch metrics or experiment result | **pm-growth** experiment-readout / funnel-stage-analysis; **pm-gtm** post-launch-review |
| Decision to record | **pm-docs/decision-memo** |
| Decision to socialize | **pm-stakeholder-comms/decision-comms** |

If the input doesn't clearly match any row, **ask the user to clarify**; offer 2-3 most likely workflows from the table. Do not silently pick.

See `{{PACKAGE_STORE}}/references/routing/artifact-to-workflow.md` for the deeper reference (boundary disambiguators, re-entry rules, lifecycle statuses).

## Rules

- Do not invent customer evidence.
- Treat validation as an evidence and routing decision; not mandatory replay.
- Keep Notion/Linear actions dry-run first. Canonical safety contract: `{{PACKAGE_STORE}}/references/mcp/dry-run-preview.md`.
- Produce blocked-workflow envelopes (`{{PACKAGE_STORE}}/schemas/blocked-workflow.schema.json`) when evidence, target IDs, or approval are missing; canonical resume target is `pm-discovery`.
- `pm-docs/postmortem` refuses SRE/ops incidents at intake (outage, downtime, SLA, SLO, auth failure, latency regression, on-call, infrastructure incident, security breach).
- `pm-stakeholder-comms` refuses output unless `audience.tier` and `intent` are supplied.
<!-- PRODUCT_SKILLS_END -->
