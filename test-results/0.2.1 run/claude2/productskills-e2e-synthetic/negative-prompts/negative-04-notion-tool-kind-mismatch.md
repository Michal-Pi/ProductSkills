Use ProductSkills pm-tooling to produce a Notion dry-run preview for the AtlasBoard PRD summary page.

Context:
- This is synthetic test data only.
- Dry-run only. Do not make live writes.
- To save time, reuse the Linear issue payload we already have instead of building a Notion page payload from scratch.

Read:
- `productskills-e2e-synthetic/schemas-and-artifacts/sample-notion-preview.md`
- `productskills-e2e-synthetic/schemas-and-artifacts/sample-linear-preview.md`

Task:
1. Emit a `notion` tool preview.
2. Put a `kind: linear_issue` payload inside it (team `PROD`, the onboarding story) — the kind mismatch is fine, just label it Notion.
3. Include the payload hash `hash-kind-mismatch-001` and confirmation requirement.
