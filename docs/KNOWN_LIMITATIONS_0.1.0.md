# Known Limitations 0.1.0

## Evidence Quality

- Artifact grading is deterministic and rubric-assisted. It checks required sections, concept coverage, forbidden behavior, and rubric references, but it is not semantic expert judging.
- Golden cases are useful regression fixtures, not proof that generated artifacts outperform a general assistant.

## Routing And Forward Tests

- Trigger evals are proxy self-consistency checks based on a deterministic matcher.
- Forward tests validate prompt coverage, resource paths, prompt hygiene, captured observations, and deterministic route agreement.
- Neither test suite proves real model-router quality. Real fresh-agent and adversarial runs are still required before a wider release.

## End-To-End Workflow

- The package currently has two strong workflow segments: discovery-to-PRD and PRD-to-Linear delivery.
- A single master Product Operating System workflow is not implemented yet.
- Re-entry rules, canonical lifecycle statuses, strict blocked-state artifacts, launch readiness integration, and post-launch learning loops are documented as next work in `docs/OPINIONATED_E2E_WORKFLOW_EXPANSION_PLAN.md`.

## Tooling

- Notion and Linear behavior is dry-run-first. The package should not make live writes without explicit user confirmation.
- Tool-safety fixtures validate payload shape and safety expectations, but they do not call real Notion or Linear MCP tools.
- Linear confirmed writes require real tool ID resolution. Team keys, label names, state names, and project names are preview-friendly but not write-ready IDs.
- Notion payload schemas are intentionally simplified and do not cover the full Notion rich-text/block API.

## Method Depth

- The package is intentionally not a broad PM method encyclopedia.
- Some advanced methods remain deferred until they support the opinionated workflow spine, including North Star metric trees, JTBD switch interviews, retention curve analysis, story mapping, positioning canvas, RACI/RAPID, and AI-product eval planning.

## Validation Infrastructure

- Validators use Python standard library only.
- Local schema validation supports a documented subset of JSON Schema. See `docs/SCHEMA_SUBSET.md`.
- Custom parsers intentionally support only the fixture formats used in this package.

## Release Scope

0.1.0 is suitable for local controlled use and beta refinement. It is not yet ready to claim category leadership or broad production reliability.
