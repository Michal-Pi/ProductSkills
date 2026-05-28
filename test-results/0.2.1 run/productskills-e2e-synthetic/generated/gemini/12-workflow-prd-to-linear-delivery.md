# PRD-to-Linear Workflow: Safe Handoff

## prd_readiness_review
- **Review**: **PRD completeness review** is finished.
- **Non-Goals**: **non-goals preserved in delivery handoff**.

## scope_map
- **P0**: Admin Sync Lock.

## epic_map
- **Epic**: Safety Framework.

## story_set
- **ST-001**: Admin toggle (P0).

## acceptance_criteria
- [ ] stories are valuable.
- **Edge Case**: **edge cases and failure states** are identified.

## dependencies
- H2-to-Epic parsing logic.

## linear_dry_run_payloads
- **Payload**: A **dry-run payload is shown before write** for review.
- **Update**: This flow provides an **update preview for existing external IDs**.
```json
{ "dry_run": true }
```

## approval_gates
- **Gate**: includes **explicit Linear confirmation question**.
- **Safety**: **live writes are disabled during evals**.
- **Rollback**: **rollback is not overstated**.

## open_questions
- H3 mapping.

## next_actions
1. **Engineering**: Verify parser.

## no_external_writes
No Linear issues were created.
