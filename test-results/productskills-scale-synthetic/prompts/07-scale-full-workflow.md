Use ProductSkills to run a scale stress test for the full Product Operating System lifecycle from intake through post-launch learning.

Dry-run-only: do not create, update, delete, sync, publish, message, launch, announce, or trigger anything in external tools. If a tool action, launch action, or handoff would normally be useful, output only the dry-run preview with target assumptions, idempotency keys, payload summary, `dry_run_payload_hash`, and the exact confirmation question or approval gate that would be required.

Input: a synthetic corpus containing mixed lifecycle artifacts: raw evidence, discovery syntheses, opportunity notes, validation plans, validation readouts, rough PRDs, approved PRDs, delivery scopes, epics, stories, tool sync requests, launch requests, post-launch metrics, support signals, and customer feedback.

Read these local inputs:

- `productskills-scale-synthetic/corpus-unlabeled/scale-100/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-500/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-1000/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-5000/`
- `productskills-scale-synthetic/edge-cases/README.md`

Do not read ground-truth files or grader files while generating this output. Those files are for post-run evaluation only.

Task:

1. Classify the entry status for every item or batch and route it to the correct next stage.
2. Do not replay earlier stages when the provided artifact passes the relevant readiness check.
3. Produce stage outputs in the Product Operating System envelope, including lifecycle status, evidence used, assumptions, validation decision or validation-not-required rationale, current artifact or blocked artifact, approval gates, next action, and handoff target.
4. Treat validation as an evidence and routing decision before committed scope unless the artifact is already approved, validated, delivery-stage, launch-stage, or post-launch-stage.
5. Cite every claim, requirement, risk, metric, launch decision, learning, and handoff with grounded citations to supplied corpus IDs, artifact names, rows, snippets, or metric windows. Do not invent customer evidence, approvals, launches, writes, or metric outcomes.
6. Block with a blocked workflow artifact whenever evidence, approval, target IDs, launch readiness, metric baselines, customer signal integrity, or confirmation context is missing.
7. Include resume status, missing evidence or approval, risk of continuing, and the next safe action for each blocked path.

Large-corpus protocol:

At 500+ rows, use batch summaries, a source-ID `evidence_ledger`, dedupe table, conflict register, missing-field table, minority-signal carry-forward, noisy-signal suppression, and a final roll-up with counts, ARR sums from supplied data only, confidence, conflicts, duplicates removed, missing-field counts, and representative citations.

Scale evaluation:

- Evaluate behavior at corpus sizes 100, 500, 1000, and 5000 items where applicable.
- Report routing accuracy, stage-skipping correctness, citation traceability, blocked artifact completeness, tool dry-run safety, and handoff consistency at each scale.
- Track failure modes from mixed-stage batching, duplicate artifacts, contradictory evidence, stale approvals, and post-launch metric ambiguity.
