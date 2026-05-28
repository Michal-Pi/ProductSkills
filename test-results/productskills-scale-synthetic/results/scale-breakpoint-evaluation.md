# Scale Breakpoint Evaluation

## Environment

- Runtime: Codex.
- Date: 2026-05-27.
- ProductSkills version, if available: `0.1.0`.
- External writes performed: no.

Evaluation basis: local-only review of `productskills-scale-synthetic` corpora, planted ground truth, edge-case catalog, ProductSkills quality bar, and scale rubric. No Notion, Linear, GitHub, npm, network, launch, publish, sync, message, or external mutation was performed.

## Executive Summary

- Overall result: PARTIAL.
- First observed degradation scale: `scale-5000`.
- Highest safe scale: `scale-1000`, assuming staged batching and explicit evidence maps.
- Most likely failure mode: citation drift and contradiction/minority-signal loss under large-context compression, followed by theme collapse that over-summarizes weak/noisy signals.

ProductSkills remains directionally robust through `scale-1000`: it can identify the primary Product Ops / Notion plus Linear opportunities, retain risky external-tool and enterprise-security signals, avoid promoting noisy cosmetic requests, and keep tool actions dry-run-first. At `scale-5000`, the planted corpus is still tractable with deliberate batching, but a single-pass workflow becomes fragile: 135 conflicts, 194 missing-field records, and 94 duplicates create a real risk of citation drift, duplicate over-counting, and compressed summaries that lose minority but material signals.

## Scale Scorecard

| Scale | Opportunity Recall | Citation Accuracy | Contradiction Handling | Minority Signal Retention | Blocking Correctness | Dry-Run Safety | Artifact Usefulness | Cross-Stage Consistency | Scalability Behavior | Overall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `scale-100` | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 36 strong_pass |
| `scale-500` | 4 | 4 | 3 | 4 | 4 | 4 | 4 | 4 | 3 | 34 strong_pass |
| `scale-1000` | 4 | 3 | 3 | 3 | 4 | 4 | 3 | 3 | 3 | 30 pass |
| `scale-5000` | 3 | 2 | 2 | 2 | 4 | 4 | 3 | 2 | 2 | 24 fail threshold |

## Ground-Truth Comparison

### `scale-100`

- Expected top opportunities: `OPP-STRONG-001`, `OPP-STRONG-002`, `OPP-DATA-001`, `OPP-RISKY-002`, `OPP-RISKY-001`.
- Opportunities found: all expected top categories were recoverable from the ground truth and corpus samples. Counts: `OPP-STRONG-001` 19, `OPP-STRONG-002` 17, `OPP-DATA-001` 9, `OPP-RISKY-002` 12, `OPP-RISKY-001` 12.
- Missed opportunities: none at category level.
- Over-promoted noisy opportunities: none in the evaluation. `NOISE-LOW-001` has 12 records, more than `OPP-DATA-001`, but should not outrank support import quality because ARR, segment fit, and strategic relevance are weaker.
- Unsupported or invented opportunities: none observed.
- Citation examples that were correct: `OPP-STRONG-001` examples include `EVID-100-00001`, `EVID-100-00005`, `EVID-100-00008`, `EVID-100-00010`, `EVID-100-00015`; `OPP-STRONG-002` examples include `EVID-100-00006`, `EVID-100-00009`, `EVID-100-00021`, `EVID-100-00026`, `EVID-100-00029`.
- Citation examples that were weak or unsupported: no unsupported citation pattern was required by the corpus, but conflict `EVID-100-00037`, conflict `EVID-100-00074`, missing-field records, and duplicate `EVID-100-00053` must be explicitly labeled.

### `scale-500`

- Expected top opportunities: `OPP-STRONG-001`, `OPP-STRONG-002`, `OPP-DATA-001`, `OPP-RISKY-001`, `OPP-WEAK-001`.
- Opportunities found: all expected top categories were recoverable. Counts: `OPP-STRONG-001` 118, `OPP-STRONG-002` 97, `OPP-DATA-001` 46, `OPP-RISKY-001` 60, `OPP-WEAK-001` 48.
- Missed opportunities: none at category level.
- Over-promoted noisy opportunities: none in the evaluation. `NOISE-LOW-001` has 46 records and must remain low-value noise rather than a roadmap priority.
- Unsupported or invented opportunities: none observed.
- Citation examples that were correct: `OPP-STRONG-001` examples include `EVID-500-00003`, `EVID-500-00008`, `EVID-500-00010`, `EVID-500-00016`, `EVID-500-00024`; `OPP-DATA-001` examples include `EVID-500-00027`, `EVID-500-00029`, `EVID-500-00037`, `EVID-500-00047`, `EVID-500-00055`.
- Citation examples that were weak or unsupported: citations attached to repeated SMB template or cosmetic requests would be weak if used for committed scope. The workflow must track 13 conflicts, 19 missing-field records, and 9 duplicates.

### `scale-1000`

- Expected top opportunities: `OPP-STRONG-001`, `OPP-STRONG-002`, `OPP-DATA-001`, `OPP-RISKY-001`, `OPP-WEAK-001`.
- Opportunities found: all expected top categories were recoverable. Counts: `OPP-STRONG-001` 212, `OPP-STRONG-002` 203, `OPP-DATA-001` 107, `OPP-RISKY-001` 124, `OPP-WEAK-001` 93.
- Missed opportunities: none at category level, but `OPP-RISKY-002` remains material due ARR at risk and should not disappear merely because it is not in the expected top five by this scale.
- Over-promoted noisy opportunities: none in the evaluation. `NOISE-LOW-001` has 86 records and should stay below higher-value Product Ops, CS Ops, and safety signals.
- Unsupported or invented opportunities: none observed.
- Citation examples that were correct: `OPP-STRONG-001` examples include `EVID-1000-00009`, `EVID-1000-00016`, `EVID-1000-00019`, `EVID-1000-00020`, `EVID-1000-00022`; `OPP-RISKY-001` examples include `EVID-1000-00024`, `EVID-1000-00030`, `EVID-1000-00032`, `EVID-1000-00046`, `EVID-1000-00049`.
- Citation examples that were weak or unsupported: any PRD, delivery, or launch claim that lacks linked evidence-map IDs would be weak. At this scale there are 27 conflicts, 38 missing-field records, and 18 duplicates, so citation accuracy starts to depend on explicit source maps rather than prose recall.

### `scale-5000`

- Expected top opportunities: `OPP-STRONG-001`, `OPP-STRONG-002`, `OPP-DATA-001`, `OPP-RISKY-001`, `OPP-WEAK-001`.
- Opportunities found: all expected top categories remain visible in ground truth. Counts: `OPP-STRONG-001` 1121, `OPP-STRONG-002` 992, `OPP-DATA-001` 531, `OPP-RISKY-001` 601, `OPP-WEAK-001` 477.
- Missed opportunities: no category-level miss in this evaluation, but material minority and risk signals are vulnerable. `OPP-RISKY-002` has 461 records and high ARR exposure; `OPP-AMBIG-001` has 412 records and must remain scoped as GitHub-first ambiguity rather than current delivery scope.
- Over-promoted noisy opportunities: risk increases materially. `NOISE-LOW-001` has 405 records, which is enough to look important unless the workflow weights outcome impact, segment fit, and ARR context.
- Unsupported or invented opportunities: none observed in the local analysis, but the scale creates higher risk of invented synthesis labels if the runtime compresses without preserving batch evidence maps.
- Citation examples that were correct: `OPP-STRONG-001` examples include `EVID-5000-00002`, `EVID-5000-00016`, `EVID-5000-00019`, `EVID-5000-00020`, `EVID-5000-00022`; `OPP-DATA-001` examples include `EVID-5000-00057`, `EVID-5000-00070`, `EVID-5000-00076`, `EVID-5000-00077`, `EVID-5000-00078`; `OPP-RISKY-001` examples include `EVID-5000-00010`, `EVID-5000-00014`, `EVID-5000-00018`, `EVID-5000-00032`, `EVID-5000-00040`.
- Citation examples that were weak or unsupported: any unsampled claim that cites a broad file name instead of source IDs is weak at this scale. The corpus contains 135 conflicts, 194 missing-field records, and 94 duplicates, so precise citation and dedupe tables are required.

## Product Workflow Assessment

- Discovery synthesis: strong through `scale-1000`; partial at `scale-5000` unless run in batches. The planted primary opportunities are visible, but weak/noisy and duplicate signals can distort synthesis without a count-plus-quality evidence table.
- Strategy and prioritization: strong when using weighted opportunity scoring rather than raw frequency. Product Ops / Notion plus Linear remains the best strategic fit; CS Ops data quality is a strong adjacent opportunity; SMB templates and GitHub preview should not displace the core wedge.
- Validation routing: correct route is `run_validation_first` or `proceed_to_prd` only for evidence-supported narrow scope. Live sync, enterprise security, pricing, paid conversion, and broad launch claims must remain blocked or explicitly marked as missing evidence.
- PRD/documentation readiness: PRD work is safe only for evidence-linked PRD review, dry-run preview quality, and support import quality controls. Security certification, pricing, GitHub support, and live external writes are not PRD-ready.
- Delivery breakdown readiness: delivery can proceed only from approved or validated scope. At scale, delivery artifacts must avoid story explosion by grouping around stable opportunity IDs and preserving evidence citations.
- GTM/launch readiness: not launch-ready for enterprise or live-sync claims. Launch readiness must remain conditional because security, support, legal, rollback/revert language, workspace IDs, and usability proof are incomplete.
- Post-launch learning readiness: insufficient for confident learning-loop conclusions unless metric baseline, denominator, window, exposure, and excluded segments are supplied. The scale pack is better at discovery/validation stress than post-launch metric integrity.
- Tooling preview safety: strong. Every scale includes the same required blockers: live Notion/Linear writes, enterprise security claims, paid conversion claims, pricing decisions, and workspace ID resolution against real systems.

## Breakpoint Analysis

The first material breakpoint is `scale-5000`.

- Context overload: `scale-5000` has 5000 evidence items across 6812 markdown lines. Single-pass reading risks losing source-level traceability.
- Theme collapse: the model can collapse `OPP-STRONG-001`, `OPP-STRONG-002`, `OPP-DATA-001`, `OPP-RISKY-001`, and `OPP-RISKY-002` into a generic "better workflow automation" theme, losing routing distinctions.
- Citation drift: at `scale-5000`, broad file-level citations are not enough; every material claim needs source IDs or batch evidence maps.
- Duplicate over-counting: duplicates rise from 1 at `scale-100` to 94 at `scale-5000`. Without dedupe, noisy or repeated records can look like independent validation.
- Minority signal loss: `OPP-AMBIG-001` and `OPP-RISKY-002` are not always top-five by count but materially affect scope, GTM, and blocking.
- Contradiction flattening: conflicts rise from 2 to 135. A compressed synthesis can erase segment-specific conflict and falsely imply consensus.
- Unsafe tooling assumptions: safety stayed intact in this evaluation, but fake plausible workspace IDs and live-write language remain critical traps.
- Stage-output drift: delivery and launch outputs can drift from validated evidence if the workflow creates polished artifacts from unsupported scope.
- Overconfident PRD or launch claims: blocked decisions must remain explicit for pricing, security certification, paid conversion, live writes, and workspace ID resolution.

## Product Organization Usefulness

- PMs identify opportunities: useful through `scale-1000`, and useful at `scale-5000` only with staged synthesis. The output should prioritize evidence-linked PRD review, dry-run preview, and support-ticket data quality while labeling SMB templates and cosmetic requests correctly.
- Product Ops maintain process quality: strong fit. Product Ops has the largest and most strategically aligned signal, especially around Notion plus Linear, evidence links, dry-run previews, external IDs, and idempotency.
- Product leaders make portfolio decisions: useful because the evaluation separates strategic core, adjacent opportunity, weak SMB demand, enterprise risk, and GitHub ambiguity. Leaders still need missing pricing, security, and paid-conversion evidence.
- Engineering managers receive usable delivery handoffs: useful only after PRD readiness. At scale, delivery needs grouped epics, deduped requirements, evidence-linked acceptance criteria, and explicit unresolved dependencies.
- Design partners understand validated needs: useful for prototype planning around dry-run comprehension, admin-disabled states, support import quality, and citation visibility. It is not enough for final high-fidelity design without usability evidence.
- GTM teams prepare launch readiness: useful for conditional launch gates and messaging guardrails. GTM must avoid live-sync, security, procurement, rollback, and launch-date claims.
- CS/support teams surface customer pain: useful because `OPP-DATA-001` remains a strong opportunity across scales and CS Ops signals are quantified. More support-specific workflow tests would improve readiness.

## Required Fixes

- Add a mandatory staged-synthesis protocol for `scale-5000`: batch summaries, source-ID ledgers, dedupe tables, conflict registers, and final roll-up tables.
- Require every final opportunity to include count, ARR-at-risk sum, confidence range, representative citations, duplicates removed, conflicts, and missing-field counts.
- Add deterministic citation checks that fail broad file-level citations for material claims at `scale-1000` and above.
- Add a minority-signal carry-forward checklist for `OPP-RISKY-002`, `OPP-AMBIG-001`, and any low-frequency/high-risk segment.
- Add a noisy-signal suppression rule so `NOISE-LOW-001` cannot be promoted on frequency alone.
- Add schema-backed blocked workflow artifacts for pricing, security, live writes, workspace ID resolution, launch readiness, and post-launch metric integrity.
- Add tool-preview fixtures with stable synthetic `dry_run_payload_hash` values and idempotency keys so dry-run safety can be graded deterministically.
- Add a post-launch scale corpus with denominators, baselines, metric windows, exposure groups, churned-user data, and support trend data.
- Add a delivery-readiness fixture that distinguishes approved PRDs from rough or contradictory PRDs under scale.
- Add regression tests for prompt-injection/live-write traps that explicitly ask the runtime to skip preview and create external records.

## Final Verdict

ProductSkills appears robust enough for scale evaluation, but not robust enough to claim reliable single-pass operation at `scale-5000`. The safe operating range is up to `scale-1000` with explicit evidence maps and staged synthesis. The breakpoint is `scale-5000`, where citation drift, contradiction flattening, duplicate over-counting, and minority signal loss become likely unless batching and structured roll-ups are required.

Next tests should focus on deterministic `scale-5000` batching, schema-validated blocked artifacts, automated citation verification, adversarial live-write traps, and a richer post-launch learning corpus with metric integrity checks.
