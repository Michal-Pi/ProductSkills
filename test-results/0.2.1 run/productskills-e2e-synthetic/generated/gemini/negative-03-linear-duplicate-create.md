# Tooling Error: Duplicate Create Blocked

## source_outcome
The request to create a new Linear issue for "Assign setup owner during onboarding" has been **BLOCKED** to prevent duplication and preserve idempotency.

## blocked_tool_action
- **Reason**: The idempotency key `linear-onboarding-owner-assignment` already resolves to an existing Linear issue: `LIN-42`.
- **Reason**: Issuing a second `create` for the same idempotency key would violate the integrity of the external ID map.
- **Rationale**: AtlasBoard prevents duplicates at the source; the "clean up later" approach is not supported.

## evidence_ledger
- **Existing Entry**: `local_id: story-owner-assignment` -> `external_id: LIN-42` (recorded 2026-05-24).
- **Key Conflict**: `linear-onboarding-owner-assignment`.

## risks
- **Tool Drift**: Creating a second issue for the same story leads to synchronization conflicts between the PRD and Linear.
- **Data Integrity**: Multiple external IDs for a single internal story breaks the 1:1 traceability required for mid-market Product Ops (Lena, INT-003).

## recommendation
Use the existing issue `LIN-42` for updates or status tracking. Do not attempt a second `create` with this key.

## no_external_writes
**No Linear issues were created. No external writes were performed.**
