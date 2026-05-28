Use ProductSkills to run a scale stress test for delivery readiness, epic breakdown, story splitting, and acceptance criteria.

Dry-run-only: do not create, update, delete, sync, publish, message, or trigger anything in external tools. If Linear, Notion, Jira, GitHub, Slack, or another tool would normally be used, output only dry-run previews with target assumptions, idempotency keys, payload summary, `dry_run_payload_hash`, and the exact confirmation question required before any write.

Input: a synthetic corpus of approved PRDs, rough PRDs, delivery-ready scopes, existing epics, user stories, acceptance criteria, dependencies, risks, and implementation constraints.

Read these local inputs:

- `productskills-scale-synthetic/corpus-unlabeled/scale-100/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-500/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-1000/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-5000/`

Do not read ground-truth files or grader files while generating this output. Those files are for post-run evaluation only.

Task:

1. Classify each artifact and start from the latest valid lifecycle stage rather than replaying earlier stages unnecessarily.
2. Run delivery readiness checks for scope clarity, non-goals, assumptions, risks, success metrics, dependencies, user value, testability, and acceptance criteria.
3. Split only approved or delivery-ready scope into epics and stories, preserving user value and testable acceptance criteria.
4. Use `validation_not_required` only when the source artifact is approved, already validated, or later-stage and passes readiness checks.
5. Cite every delivery item with grounded citations back to PRD, evidence, decision, or constraint citations from supplied corpus IDs, artifact names, rows, or snippets. Do not invent approvals, dependencies, or acceptance criteria.
6. Block with a blocked workflow artifact when the source PRD is unsupported, approval status is unclear, requirements are ambiguous, or dependencies prevent safe delivery planning.
7. Include approval gates before treating ambiguous artifacts as delivery-ready or preparing external tool writes.

Large-corpus protocol:

At 500+ rows, use batch summaries, a source-ID `evidence_ledger`, dedupe table, conflict register, missing-field table, minority-signal carry-forward, noisy-signal suppression, and a final roll-up with counts, ARR sums from supplied data only, confidence, conflicts, duplicates removed, missing-field counts, and representative citations.

Scale evaluation:

- Evaluate behavior at corpus sizes 100, 500, 1000, and 5000 items where applicable.
- Report story explosion, duplicate epic merging, acceptance-criteria drift, dependency overload, and citation traceability at each scale.
- Verify that dry-run payloads remain preview-only and are never represented as completed tool writes.
