# Large-Corpus Synthesis Protocol

Use this protocol when product evidence is too large, repetitive, contradictory, or noisy to review safely in one pass. It extends the existing `evidence_ledger` concept; do not create a separate evidence vocabulary.

## When Required

Run this protocol when any input set has at least 500 evidence rows, multiple source files with repeated customer signals, known or likely duplicates, contradictory segment evidence, or material missing fields.

For smaller inputs, use the same fields in lighter form when citation drift, duplication, or conflicting evidence would change the decision.

## Required Working Tables

Maintain these tables while synthesizing. They may be intermediate artifacts, but the final output must summarize them.

| Table | Required fields | Purpose |
|---|---|---|
| `batch_summary` | batch ID, source files, source-ID range, row count, included segments, candidate opportunities, material conflicts, missing-field count, duplicate count, confidence notes | Prevents context compression from erasing source boundaries. |
| `evidence_ledger` | source ID, source file, segment, evidence type, claim supported, direct quote or row summary, confidence, ARR if supplied, opportunity candidate, decision impact | Preserves traceability for every material claim. |
| `dedupe_table` | canonical source ID, duplicate source IDs, duplicate reason, same account or same opportunity, fields merged, count removed, ARR treatment | Prevents repeated records from becoming false validation. |
| `conflict_register` | conflict ID, source IDs, affected segment, conflicting claims, confidence per side, decision impact, routing outcome | Keeps contradictions visible through PRD, delivery, launch, and learning artifacts. |
| `missing_field_table` | source ID, missing field, affected decision, safe assumption if any, required follow-up | Blocks or narrows claims that depend on absent evidence. |

## Signal Carry-Forward Rules

Carry forward minority signals when they have high ARR exposure, safety/compliance implications, launch-readiness impact, workflow-blocking severity, or segment-strategy relevance. Low frequency is not a reason to drop them.

Suppress noisy signals when they are high frequency but low value, cosmetic, weakly tied to outcome impact, duplicated, segment-mismatched, or unsupported by customer behavior. Suppression means "monitor or defer with evidence," not "delete from the ledger."

## Citation Rules By Scale

| Scale | Citation requirement |
|---|---|
| Fewer than 100 rows | Cite every material claim with exact source IDs or artifact sections. |
| 100-499 rows | Cite each opportunity, conflict, and blocked decision with representative source IDs plus source counts. |
| 500-999 rows | Use batch summaries and representative citations. Cite every conflict, minority signal, blocker, and high-impact recommendation with exact source IDs. |
| 1000+ rows | Use batch summaries, `evidence_ledger`, dedupe table, conflict register, and missing-field table. Final claims may use representative citations, but audit tables must retain exhaustive source-ID coverage for material decisions. |

Never cite only a broad file name for a material claim at 500+ rows. If exhaustive citation would make the answer unusable, cite representative source IDs in the narrative and attach or summarize the exhaustive ledger counts.

## Final Roll-Up

The final synthesis must include one roll-up row per opportunity, blocked decision, or material signal:

| Field | Requirement |
|---|---|
| Opportunity or signal | Customer problem or product risk, not only a requested solution. |
| Source count | Count before and after dedupe. |
| ARR sum | Sum only supplied ARR; do not infer missing ARR. |
| Confidence | High, medium, or low with reason. |
| Representative citations | Exact source IDs that support the claim. |
| Conflicts | Count and conflict-register references. |
| Duplicates removed | Count and dedupe-table references. |
| Missing fields | Count and missing-field-table references. |
| Decision | Proceed, validate, monitor, suppress as noise, block, or carry forward as minority risk. |

If the output advances to PRD, delivery, tool preview, launch, or post-launch learning, carry unresolved conflicts, duplicates removed, missing-field counts, and minority signals into the downstream artifact rather than treating synthesis as final certainty.
