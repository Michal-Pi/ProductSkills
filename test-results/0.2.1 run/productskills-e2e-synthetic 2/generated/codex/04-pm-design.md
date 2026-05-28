# ProductSkills Response: pm-design

Runtime: Codex. ProductSkills package version: 0.2.1. Skill used: `pm-design`.

## Design Brief

Create a prototype brief for AtlasBoard evidence-linked PRD review and Linear/Notion dry-run preview. Design decisions cite evidence or are labeled assumptions. The prototype should answer whether users understand cited evidence, missing-evidence labels, and dry-run status.

This artifact separates assumptions from facts: cited evidence IDs are facts from local files; UI feasibility and comprehension outcomes are assumptions until usability testing.

## Target Users

- Lena, Product Ops Lead: needs safe previews, external IDs, and consistent handoffs. Evidence: INT-003, SALES-002.
- Maya, Senior PM: needs evidence-linked PRDs and fewer review questions. Evidence: INT-001, SUP-001, SUP-009.
- Elise, VP Product: needs validation gates and admin/security readiness. Evidence: INT-006, SUP-005.

## Scenarios

- Review an evidence-linked PRD and identify which claims are cited vs inferred.
- Generate a dry-run Linear preview preserving PRD sections. Evidence: SUP-002.
- View Notion preview pages for PRD summary, decision log, and launch checklist.
- Encounter admin-disabled external-write state. Evidence: SUP-005.

## Core Flows

1. Open approved PRD.
2. Review evidence coverage and missing-evidence labels.
3. Select "Preview delivery sync."
4. Inspect Linear and Notion payload previews.
5. Review unresolved workspace, team, database, and page IDs.
6. Export markdown/JSON preview; write action remains disabled.

## Information Architecture

- PRD evidence panel.
- Opportunity and assumption panel.
- Preview workspace with tabs for Linear, Notion, external ID map, unresolved IDs, and confirmation requirements.
- Admin policy banner.

## Key Screens

- PRD review screen with source citations.
- Missing evidence screen with confidence labels.
- Linear dry-run preview screen.
- Notion dry-run preview screen.
- External ID map and payload hashes screen.
- Admin-disabled write-state screen.

## States

- Empty states and error states: no approved PRD, missing source evidence, malformed payload preview, unresolved workspace IDs, admin disabled, export failed.
- Loading state: preview generation pending.
- Success state: dry-run preview generated; no sync completed.
- Blocked state: write request blocked because live external actions require future confirmation and verified target IDs.

## Edge Cases

- Duplicate external IDs.
- Missing Linear team/state IDs.
- Missing Notion database/parent page IDs.
- Admin disabled writes after preview is generated.
- PRD section structure mismatch from SUP-002.
- User attempts to treat preview as completed sync.

## Dry Run Copy

- "Dry-run preview only. No Linear issues or Notion pages were created."
- "External writes are disabled during evals."
- "Review payload, target IDs, idempotency keys, and dry_run_payload_hash before any future confirmation."
- Dry-run status is unmistakable in headers, exports, and disabled write controls.

## Usability Test Plan

Tasks:
- Identify one cited claim and one inferred claim in a generated PRD.
- Explain whether a Linear issue was created after viewing the preview.
- Find unresolved workspace/team/database/page IDs.
- Explain what confirmation would be required before a future write.

Success criteria:
- 5 of 6 users correctly state that no external write occurred.
- 5 of 6 users find unresolved IDs.
- 4 of 6 users identify missing evidence and source citations without moderator help.

## Validation Gaps

This artifact names concrete next actions: run usability testing, review engineering feasibility for payload hashes, and confirm admin-disabled behavior.

- Completed usability tests are not available.
- Production UI decisions are not final.
- Live external integration behavior remains out of scope.
- Engineering feasibility for stable payload hashing and idempotency needs review.

No external writes were performed.
