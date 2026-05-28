Use ProductSkills pm-tooling to preview fake Linear and Notion artifacts for AtlasBoard, dry-run only.

Context:
- This is synthetic test data only.
- Dry-run only. Do not make live Notion, Linear, GitHub, npm, or network writes.
- Do not discover real workspace IDs.
- Use fake IDs only where needed and clearly label unresolved IDs.

Read:
- `productskills-e2e-synthetic/product/existing-prd-approved.md`
- `productskills-e2e-synthetic/product/constraints.md`
- `productskills-e2e-synthetic/schemas-and-artifacts/sample-delivery-handoff.md`
- `productskills-e2e-synthetic/schemas-and-artifacts/sample-linear-preview.md`
- `productskills-e2e-synthetic/schemas-and-artifacts/sample-notion-preview.md`

Task:
1. Produce Linear dry-run preview payloads for epics and stories.
2. Produce Notion dry-run preview payloads for PRD summary, decision log, and launch checklist pages.
3. Include idempotency keys, external ID map entries, payload hashes, unresolved workspace/team/database/page IDs, and confirmation requirements.
4. Explicitly state that no external writes were performed.
5. Block any live write request and explain the missing confirmations and workspace resolution steps.
