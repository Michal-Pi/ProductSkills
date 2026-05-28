Use ProductSkills to run a scale stress test for discovery intake and evidence triage.

Dry-run-only: do not create, update, delete, sync, publish, message, or trigger anything in external tools. If a tool action would normally be useful, output only the dry-run preview with target assumptions, idempotency keys, payload summary, `dry_run_payload_hash`, and the exact confirmation question that would be required.

Input: a synthetic corpus of customer interviews, support tickets, sales notes, usage observations, and ambiguous product ideas.

Read these local inputs:

- `productskills-scale-synthetic/corpus-unlabeled/scale-100/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-500/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-1000/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-5000/`

Do not read ground-truth files or grader files while generating this output. Those files are for post-run evaluation only.

Task:

1. Classify the entry status for each item or batch using the Product Operating System workflow.
2. Separate direct evidence, inference, assumptions, contradictions, and missing context.
3. Produce discovery themes, opportunity candidates, confidence ratings, and unresolved questions.
4. Cite every claim with grounded citations to the supplied corpus item IDs, artifact names, row numbers, or quoted snippets. Do not invent customer evidence.
5. Treat validation as an evidence and routing decision, not as a default requirement.
6. Block with a blocked workflow artifact when evidence is missing, contradictory, untraceable, or too weak to support opportunity framing.
7. Include the resume status, missing evidence list, risk of continuing, and next safe action for every blocked path.

Large-corpus protocol:

At 500+ rows, use batch summaries, a source-ID `evidence_ledger`, dedupe table, conflict register, missing-field table, minority-signal carry-forward, noisy-signal suppression, and a final roll-up with counts, ARR sums from supplied data only, confidence, conflicts, duplicates removed, missing-field counts, and representative citations.

Scale evaluation:

- Evaluate behavior at corpus sizes 100, 500, 1000, and 5000 items where applicable.
- Report latency-sensitive failure modes, citation drift, theme collapse, duplicate handling, and whether blocked artifacts remain complete at each scale.
- Preserve traceability from every synthesized theme back to source evidence at every corpus size.
