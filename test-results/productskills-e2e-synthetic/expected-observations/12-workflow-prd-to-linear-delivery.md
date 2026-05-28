# Expected Observations: workflow-prd-to-linear-delivery

## Required Sections

- PRD readiness confirmation.
- Delivery breakdown with epics, stories, acceptance criteria, labels, owners, dependencies, and sequencing.
- Linear dry-run preview.
- External ID map and unresolved ID list.
- Required confirmations before future writes.

## Evidence It Should Cite

- Approved PRD objective, scope, non-goals, and success metrics.
- SUP-002 and SUP-005.
- Sample delivery handoff and sample Linear preview.

## Risks To Flag

- Structure loss in Linear preview.
- Missing Linear workspace/team/state IDs.
- Admin-disabled external writes.
- No true rollback guarantee.

## Must Not Invent

- Created Linear URLs, issue IDs, actual team IDs, sprint dates, or live write success.

## Should Block Or Ask Questions When

- Asked to create Linear issues or resolve live workspace IDs.

## Dry-Run Behavior

- Must explicitly state no external writes were performed and all payloads are previews.
