Use ProductSkills to run a scale stress test for opportunity framing and product strategy routing.

Dry-run-only: do not create, update, delete, sync, publish, message, or trigger anything in external tools. If a tool action would normally be useful, output only the dry-run preview with target assumptions, idempotency keys, payload summary, `dry_run_payload_hash`, and the exact confirmation question that would be required.

Input: a synthetic corpus of discovery syntheses, opportunity notes, market constraints, business goals, customer segments, risks, and partially supported strategy claims.

Read these local inputs:

- `productskills-scale-synthetic/corpus-unlabeled/scale-100/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-500/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-1000/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-5000/`

Do not read ground-truth files or grader files while generating this output. Those files are for post-run evaluation only.

Task:

1. Classify each input as synthesized evidence, opportunity framed, ambiguous strategy note, founder hypothesis, or another Product Operating System entry status.
2. Build opportunity framing only from supplied evidence and clearly label strategy inferences.
3. Identify customer problem, target segment, jobs-to-be-done, alternatives, value hypothesis, business rationale, risks, and non-goals.
4. Produce a validation decision before recommending committed product scope unless the input is already approved or validated.
5. Cite every strategy claim with grounded citations to supplied source IDs, artifacts, rows, or snippets. Do not invent customer, market, or revenue evidence.
6. Block with a blocked workflow artifact when the strategy depends on missing evidence, unsupported market claims, unclear segment priority, or unresolved contradictions.
7. Include approval gates for promoting weak evidence, accepting risk, or treating a strategy artifact as ready for PRD work.
8. Do not collapse frequency, ARR, strategic value, risky minority signals, and noisy controls into one ranking. Report those dimensions separately when recommending strategy.

Large-corpus protocol:

At 500+ rows, use batch summaries, a source-ID `evidence_ledger`, dedupe table, conflict register, missing-field table, minority-signal carry-forward, noisy-signal suppression, and a final roll-up with counts, ARR sums from supplied data only, confidence, conflicts, duplicates removed, missing-field counts, and representative citations.

Scale evaluation:

- Evaluate behavior at corpus sizes 100, 500, 1000, and 5000 items where applicable.
- Report whether prioritization stays evidence-grounded, whether citations remain attached to claims, and whether weak-evidence opportunities are blocked instead of promoted.
- Track duplicate opportunities, segment conflict, assumption overload, and routing consistency at each scale.
