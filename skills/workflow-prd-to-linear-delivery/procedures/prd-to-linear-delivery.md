# PRD to Linear Delivery Procedure

Use when the user wants to convert a PRD, product spec, feature brief, or validated scope into epics, stories, acceptance criteria, sequencing, and Linear-ready issue previews.

## Entry Conditions

Start when the input includes a PRD or equivalent scope artifact with:

- Product outcome or objective.
- Target user or segment.
- Scope and non-goals.
- Requirements or user workflows.
- Known assumptions, risks, and open questions.

If scope is unclear, run a spec review first and stop with blocking questions instead of creating delivery issues.

## Workflow Steps

1. PRD completeness review using `../../../skills/pm-docs/procedures/spec-review.md`.
2. Scope split into epics using `../../../skills/pm-delivery/procedures/epic-breakdown.md`.
3. Story splitting using `../../../skills/pm-delivery/procedures/story-splitting.md`.
4. Acceptance criteria using `../../../skills/pm-delivery/procedures/acceptance-criteria.md`.
5. Dependency, sequencing, and release-risk review using `../../../references/methods/delivery-handoff.md`.
6. Linear dry-run preview using `../../../references/mcp/dry-run-preview.md` (canonical safety contract) and `../../../templates/linear-delivery-handoff.md`. See `../../../references/mcp/linear-mcp-contract.md` for payload field expectations.

## Intermediate Artifacts

Produce these artifacts in order:

- `prd_readiness_review`: blocking gaps, non-blocking improvements, unsupported claims, and delivery decision.
- `scope_map`: in-scope capabilities, non-goals, dependencies, assumptions, and excluded requests.
- `epic_map`: epics with local IDs, outcomes, completion criteria, risks, and sequencing notes.
- `story_set`: user stories grouped by epic with local IDs, user value, dependencies, and split rationale.
- `acceptance_criteria`: primary paths, edge cases, permissions, empty states, errors, and failure states.
- `delivery_handoff`: structured fields from `../../../references/workflows/prd-to-linear-delivery-contract.md`.
- `linear_dry_run_payloads`: issue previews only, never confirmed writes during the first pass.

## Stop Points and Approval Gates

Stop before story creation when:

- The PRD objective, target user, or scope is missing.
- Requirements conflict with stated non-goals.
- A product decision blocks delivery sequencing.
- Acceptance criteria would require inventing behavior.

Ask for approval before:

- Resolving ambiguous scope into an epic.
- Treating a product assumption as delivery-ready.
- Creating or updating Linear issues.

Linear writes require explicit confirmation tied to the exact dry-run payload list, `dry_run_payload_hash`, target team, and idempotency keys.

## Fallbacks for Missing Evidence

- Missing PRD sections: return `prd_readiness_review` with blocking questions and recommended PRD edits.
- Missing target Linear team: produce payloads with `team_key: TBD` and setup instructions; do not infer a team.
- Missing external ID map: use stable local IDs and preview creates; warn that reruns need `.product-os/external-id-map.json`.
- Existing external IDs present: preview updates instead of creates and show field-level changes.
- Linear MCP unavailable: return validated dry-run payloads for manual import.

## Handoff Contract

Before completion, populate the contract in `../../../references/workflows/prd-to-linear-delivery-contract.md` and conform to `../../../schemas/prd-to-delivery-handoff.schema.json` where structured output is requested.

Minimum handoff fields:

- `workflow_id`
- `decision_status`
- `source_prd`
- `readiness_review`
- `scope_map`
- `epics`
- `stories`
- `acceptance_criteria`
- `dependencies`
- `linear_preview`
- `approval_gates`
- `open_questions`
- `next_actions`

## Completion Standard

The workflow is complete when the user has either:

- A delivery-ready handoff with epics, stories, acceptance criteria, dependencies, sequencing, risks, and Linear dry-run payloads.
- A deliberate stop artifact explaining why delivery planning is blocked and what product decisions are needed next.

No live Linear write is complete until the user confirms the exact dry-run preview and idempotency keys.

## Done when

- The `epic_map` contains at least two epics with local IDs, outcomes, completion criteria, and sequencing notes; the `story_set` contains at least four user stories with stable local IDs grouped by epic and a noted split rationale.
- Each story has at least three distinct acceptance-criterion bullets covering the primary path; every epic carries at least one edge-case bullet (permission, empty state, error, or failure). Stories destined for Linear creation carry external IDs (or use stable local IDs with `team_key: TBD` flagged for setup).
- The `prd_readiness_review` separates blocking gaps from non-blocking improvements, the handoff conforms to `../../../schemas/prd-to-delivery-handoff.schema.json`, and dependencies plus sequencing notes are explicit (not implied).
- When the PRD lacks objective, target user, or scope, the workflow refuses to draft stories and returns blocking questions instead; `linear_dry_run_payloads` are issued as previews only, and live writes require explicit confirmation tied to the exact payload list, `dry_run_payload_hash`, target team, and idempotency keys.
