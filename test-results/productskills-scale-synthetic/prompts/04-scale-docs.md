Use ProductSkills to run a scale stress test for PRD drafting, PRD repair, and product documentation review.

Dry-run-only: do not create, update, delete, sync, publish, message, or trigger anything in external tools. If a tool action would normally be useful, output only the dry-run preview with target assumptions, idempotency keys, payload summary, `dry_run_payload_hash`, and the exact confirmation question that would be required.

Input: a synthetic corpus of discovery outputs, validation decisions, rough PRDs, approved PRDs, strategy notes, requirements fragments, constraints, risks, and success metrics.

Read these local inputs:

- `productskills-scale-synthetic/corpus-unlabeled/scale-100/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-500/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-1000/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-5000/`

Do not read ground-truth files or grader files while generating this output. Those files are for post-run evaluation only.

Task:

1. Classify each artifact as rough PRD, approved PRD, synthesized research, opportunity, or another Product Operating System entry status.
2. Draft, repair, or review PRD content only when evidence and validation routing support it.
3. Include problem, goals, non-goals, users, scope, requirements, assumptions, risks, success metrics, launch considerations, and open questions when supported.
4. Produce `validation_not_required` only for artifacts that are already approved, validated, delivery-stage, launch-stage, or post-launch-stage and pass readiness checks.
5. Cite every requirement, metric, problem statement, risk, and user claim with grounded citations to supplied corpus IDs, artifact names, rows, or snippets. Do not invent customer evidence, approvals, or metrics.
6. Block with a blocked workflow artifact when claims are unsupported, non-goals are missing, assumptions or risks are absent, or approval status is unclear.
7. Include approval gates before treating ambiguous PRDs as delivery-ready or accepting weak evidence into committed scope.

Large-corpus protocol:

At 500+ rows, use batch summaries, a source-ID `evidence_ledger`, dedupe table, conflict register, missing-field table, minority-signal carry-forward, noisy-signal suppression, and a final roll-up with counts, ARR sums from supplied data only, confidence, conflicts, duplicates removed, missing-field counts, and representative citations.

Scale evaluation:

- Evaluate behavior at corpus sizes 100, 500, 1000, and 5000 items where applicable.
- Report whether PRD sections remain traceable, whether duplicate requirements are merged safely, and whether unsupported scope is blocked.
- Track citation density, missing-section detection, readiness routing, and blocked artifact completeness at each scale.
