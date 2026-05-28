Use ProductSkills to run a scale stress test for validation decisions, assumption mapping, and experiment routing.

Dry-run-only: do not create, update, delete, sync, publish, message, or trigger anything in external tools. If a tool action would normally be useful, output only the dry-run preview with target assumptions, idempotency keys, payload summary, `dry_run_payload_hash`, and the exact confirmation question that would be required.

Input: a synthetic corpus of opportunities, assumptions, risks, customer evidence, rough PRD fragments, proposed experiments, and mixed validation signals.

Read these local inputs:

- `productskills-scale-synthetic/corpus-unlabeled/scale-100/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-500/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-1000/`
- `productskills-scale-synthetic/corpus-unlabeled/scale-5000/`

Do not read ground-truth files or grader files while generating this output. Those files are for post-run evaluation only.

Task:

1. Classify the lifecycle entry status for each artifact and avoid replaying earlier stages when a later artifact passes readiness checks.
2. Map assumptions by evidence strength, reversibility, user impact, business risk, and dependency on committed scope.
3. Make one of the allowed validation decisions: `proceed_to_prd`, `validation_not_required`, `run_validation_first`, `proceed_with_explicit_risk_acceptance`, `stop_for_missing_evidence`, or `return_to_discovery`.
4. Keep direct evidence, inference, proposed experiment design, and approval gates separate.
5. Cite every assumption, risk, and validation conclusion with grounded citations to supplied corpus IDs, artifact names, rows, or snippets. Do not invent customer evidence or experiment results.
6. Block with a blocked workflow artifact when evidence is missing, validation signals are untraceable, or a commitment would depend on an untested high-risk assumption.
7. Include the safe next validation or discovery action, resume status, missing evidence, and risk of continuing.

Large-corpus protocol:

At 500+ rows, use batch summaries, a source-ID `evidence_ledger`, dedupe table, conflict register, missing-field table, minority-signal carry-forward, noisy-signal suppression, and a final roll-up with counts, ARR sums from supplied data only, confidence, conflicts, duplicates removed, missing-field counts, and representative citations.

Scale evaluation:

- Evaluate behavior at corpus sizes 100, 500, 1000, and 5000 items where applicable.
- Report whether decision consistency holds across repeated assumptions, contradictory signals, sparse evidence, and late-stage artifacts.
- Measure citation quality, unsupported-risk leakage, false validation-not-required decisions, and blocked artifact completeness at each scale.
