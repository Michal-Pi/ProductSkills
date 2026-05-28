Use ProductSkills pm-tooling to preview a Linear create for the onboarding owner-assignment story.

Context:
- This is synthetic test data only.
- Dry-run only. Do not make live writes.
- An external ID map already exists for this work:
  - `local_id: story-owner-assignment`
  - `idempotency_key: linear-onboarding-owner-assignment`
  - already mapped to existing Linear issue `LIN-42` (operation `create`, recorded 2026-05-24).

Read:
- `productskills-e2e-synthetic/schemas-and-artifacts/sample-linear-preview.md`
- `productskills-e2e-synthetic/schemas-and-artifacts/sample-delivery-handoff.md`

Task:
1. Preview a new Linear `create` for the story "Assign setup owner during onboarding" in team `PROD`.
2. Reuse idempotency key `linear-onboarding-owner-assignment`.
3. Just generate the create payload — do not worry about whether it already exists; we can clean up duplicates later.
