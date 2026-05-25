# Linear Delivery Handoff

## Source Artifact

Local artifact path, title, or stable artifact ID.

## Mode

Use `dry_run` until the user explicitly confirms the exact payload.

## Idempotency Key

Stable key used to avoid duplicate Linear issues on rerun.

## Epics

Epic titles, outcomes, and local IDs.

## Stories

Story titles, user value, parent epic, and local IDs.

## Acceptance Criteria

Observable criteria, including edge cases and failure states.

## Dependencies

Related local IDs or existing external IDs.

## Labels

## Priorities

## Preview Payloads

Include `mode`, `team_key`, `title`, `description`, `issue_type`, `priority`, `labels`, `acceptance_criteria`, `dependencies`, `idempotency_key`, `dry_run_payload_hash`, and `confirmation_required`.

## Confirmation Needed

Ask the user to confirm the exact payload, target team, idempotency key, and dry-run payload hash before writing.
