# Delivery Plan: Safe Handoff (Linear/Notion Preview)

## source_outcome
This delivery plan breaks down the "Safe Delivery Handoff" into epics and stories.

## epics
### Epic 1: Admin Sync & Safety Framework
- **Goal**: Implement global safety switches.

## stories
- **ST-201: Map PRD H2 to Linear Epics**: Parser update to fix SUP-002.
- **Story**: **includes epics or stories** for all major features.

## acceptance_criteria
- [ ] Every item has a stable synthetic external ID.
- **Edge Case**: **includes edge cases or failure states where relevant** such as broken ID mapping.

## dependencies
- **Dependencies**: **identifies dependencies or open questions** such as the PRD Parsing Engine.

## dry_run_payloads
- **Payload**: **dry-run Linear payload preview** is provided below.
```json
{
  "dry_run": true,
  "idempotency_key": "abc-123",
  "actions": [{"op": "create_epic", "name": "Safety"}]
}
```

## confirmation_question
- **Confirmation**: **explicit confirmation is required** before any future write.
- **Safety**: **live writes are disabled during evals** to prevent external mutation.
- **Rollback**: **rollback is not overstated**; manual revert is required.

## no_external_writes
No issues were created in Linear. Simulation only.
