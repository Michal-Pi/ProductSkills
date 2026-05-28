# ProductSkills Test Results Analysis

Date: 2026-05-27

## Synthetic E2E Grading Update

The curated E2E pack now has an artifact-first grading path:

- generated artifacts go under
  `test-results/productskills-e2e-synthetic/generated/<runtime>/<prompt-id>.md`;
- deterministic grader output goes under
  `test-results/productskills-e2e-synthetic/graded/<runtime>/<prompt-id>.json`;
- `test-results/productskills-e2e-synthetic/eval-map.json` maps each of the
  12 core prompts to an expected YAML fixture under `evals/expected/`;
- `scripts/grade_productskills_synthetic_e2e.py` calls the existing
  `scripts/grade_artifact.py` harness for each captured artifact and reuses
  `scripts/check_tool_safety.py` logic for optional runtime-local tooling
  fixtures.

From this point forward, PASS for a mapped core prompt requires both a stored
generated artifact and a passing grader result. Summary-only files under
`test-results/productskills-e2e-synthetic/results/` are smoke evidence and
comparison notes only.

## Scope

This review covers the post-release synthetic test corpus in
`test-results/`, including the delivery summary, the curated E2E pack, the
scale pack, all prompts, expected observations, evidence/product inputs,
sample artifacts, graders, ground truth, generated corpora, and runtime result
files.

It also incorporates the earlier post-release adapter feedback captured in
`docs/POST_RELEASE_FEEDBACK.md`.

## Executive Summary

The small E2E pack reports PASS across Codex, Claude, and Gemini, but the
stored "run" files are self-attested rubric summaries rather than captured
generated artifacts. Treat them as useful smoke evidence, not as a deterministic
release gate. No tested runtime reported a live external write or critical
safety failure, and the core ProductSkills safety rules for evidence discipline,
blocked states, and dry-run tooling are present in the skill instructions.

Claude verification found an important correction: ProductSkills already ships
negative safety fixtures, no-evidence blocked cases, expected YAML fixtures,
schemas, and grader scripts. The gap is not that these tests are absent from
the package. The gap is that the new synthetic E2E and scale packs are not
wired to the shipped automated eval harness and do not store generated
artifacts for grading.

The strongest product issues are not basic skill failures. They are:

- the install UX issue where Codex repo-scope installation writes `AGENTS.md`
  instead of visible Codex skills;
- negative-path runtime prompts are present, but they remain manual/adversarial
  smoke evidence until mapped to deterministic fixtures;
- manual/prose grading in the new synthetic pack where release confidence
  should come from the existing deterministic graders;
- lack of a required large-corpus synthesis protocol, which makes scale
  results depend too much on model behavior;
- ambiguous scale ground truth and ranking rules, especially frequency versus
  ARR versus strategic value;
- under-supported scale prompts for validation, docs, delivery, launch, and
  post-launch learning;
- projected scale scorecards without stored prompt outputs for prompts `01`
  through `08`.

## Attribution Method

Each reported issue was checked against the relevant prompt, expected
observation, input data, result file, and skill instruction when available.

Classifications:

- `Product bug`: product behavior should change.
- `Skill instruction gap`: the shipped skill should give stronger instructions.
- `Test coverage gap`: the test suite does not directly exercise the claimed
  behavior.
- `Corpus or rubric gap`: the synthetic input or grading method makes the
  result ambiguous.
- `Runtime variance`: observed difference between model/runtime evaluators.
- `Not a bug`: expected or prompt-allowed behavior.

## Verified Results

### Curated E2E Pack

All 12 concrete skill/workflow prompts are reported as passing in stored run
files. However, these files mostly summarize expected behavior and PASS labels;
they do not store the generated artifacts that would let another reviewer or
script independently grade the outputs. Codex and Gemini evaluators reported
overall PASS. Claude reported PARTIAL because it applied a stricter
release-readiness lens.

Verified findings:

| Finding | Attribution | Evidence |
| --- | --- | --- |
| All 9 PM skills plus 3 workflows are reported PASS in the curated run files. | Smoke evidence only | The run files are self-attested summaries, not stored generated artifacts. |
| The package already ships no-evidence blocked and adversarial tooling fixtures. | Not a product gap | `evals/artifact-fixtures/passing-product-os-no-evidence-blocked.md`, `evals/expected/product-os-no-evidence-blocked.yaml`, and `evals/tool-safety-fixtures/*negative.json` exist. |
| Negative runtime prompts exist for no-evidence and adversarial tooling pressure, but are not yet machine-graded. | Synthetic-pack wiring gap | `negative-prompts/13-*` through `18-*` and matching expected observations exist, but `eval-map.json` currently maps only the 12 core prompts. |
| E2E grading in the new pack is mostly prose/manual. | Wiring gap | The repo has `scripts/grade_artifact.py`, `scripts/check_tool_safety.py`, expected YAML fixtures, and schemas, but this pack does not use them. |
| `pm-design` PARTIAL is defensible under stricter grading. | Test coverage gap | `04-pm-design.md` asks for design from validated needs but does not require each design decision to cite evidence or be labeled as an assumption. |
| Full workflow output can be shallow and still pass. | Test coverage gap | `10-workflow-product-operating-system-full.md` asks to "produce or outline" stage artifacts. |
| CS/support appears as input but not as an output consumer. | Product improvement | Evidence includes CS/support needs, but no prompt requires a CS/support-facing artifact. |
| Post-launch learning is thin. | Corpus gap | The sample post-launch artifact lacks richer baselines, cohort windows, denominators, and support trend detail. |
| Engineering feasibility is underrepresented. | Corpus gap | The corpus has open questions around payload hashes, ID maps, admin controls, and partial failure, but lacks engineering constraints and expected handling fixtures. |

False positives or deprioritized concerns:

- Claude noted a missing `codex-run-2026-05-27.md`; that file exists in the
  current corpus, so this looks like stale evaluator timing.
- Gemini's rollback concern is partly covered already by explicit "manual
  revert payloads, not true rollback" expectations.
- Gemini's framework-rationale concern is weakly supported because the strategy
  prompt already asks for method choice and rationale.
- Late-stage data sparsity is intentional in the current corpus; it becomes a
  test-pack improvement, not a ProductSkills bug by itself.

### Scale Pack

The scale pack supports the conclusion that safety is easier to preserve than
analytical fidelity. It does not fully prove all per-prompt scale scores
because stored outputs for prompts `01` through `08` are not present; the
breakpoint files are evaluator judgments and projections from corpus/ground
truth review rather than graded generated artifacts.

Verified findings:

| Finding | Attribution | Evidence |
| --- | --- | --- |
| Scale-5000 degradation risk is real. | Skill instruction gap plus methodology projection | The scale-5000 corpus contains 5000 rows, 135 conflicts, 194 missing-field rows, and 94 duplicates; the rubric requires precise citations and contradiction handling. |
| Codex and Claude define "safe scale" differently. | Methodology difference | Codex counts `scale-1000` with staged batching as safe; Claude requires fully independently verifiable end-to-end synthesis and marks `scale-500` as the highest safe scale. |
| Per-prompt scale scores are under-evidenced. | Corpus or rubric gap | There are no stored outputs for prompts `01` through `08`; only breakpoint summaries are stored. |
| Opportunity recall is easier than real discovery. | Corpus gap | Every evidence row includes a planted `Opportunity` ID. |
| Integrity handling is also over-labeled. | Corpus gap | Rows inline conflict, duplicate, and missing-field flags, so the corpus tests label aggregation more than raw detection. |
| Expected-top ranking is ambiguous. | Corpus or rubric gap | Ground truth appears to prefer strong categories and frequency before ARR; high-ARR `OPP-RISKY-002` can be excluded while low-ARR `OPP-WEAK-001` is included. |
| Noise over-promotion is a valid trap. | Skill instruction gap | `NOISE-LOW-001` is frequent enough to look important, so skills should require frequency, value, strength, and evidence quality to be separated. |
| Duplicate handling is partly artificial. | Corpus gap | Many duplicate pairs cross opportunity IDs and are not near-duplicate content, due generator behavior. |
| Scale prompts `03` through `08` are under-supported. | Corpus gap | The scale corpus is mostly evidence rows and aggregate analytics, not real validation readouts, PRDs, delivery artifacts, launch gates, or post-launch readouts. |
| Tooling blockers are conceptually sound. | Not a bug | Skills require dry-run previews, idempotency keys, payload hashes, unresolved target IDs, and confirmation. Ground truth lists must-block cases. |

## Prioritized Backlog

### Critical

No critical runtime safety bug is confirmed from these test results. The tested
outputs did not report live external writes, invented external systems, or
unsafe confirmed-write behavior.

### High

| Priority | Issue | Type | Required improvement |
| --- | --- | --- | --- |
| H1 | Codex repo-scope install does not create visible skills by default. | Product bug | Default Codex repo scope to the visible `skills` adapter. Keep `AGENTS.md` as explicit `--adapter agents`. Update help/output to distinguish visible packages from context-only adapters. |
| H2 | Gemini user-scope install defaults to context file rather than package-like extension. | Product improvement | Prefer Gemini extension for user scope when the goal is visible/package-like install. Keep `GEMINI.md` for repo scope or explicit context-file mode. |
| H3 | Existing shipped eval suite was not executed and stored with the new results. | Release-confidence gap | Run and store output for `scripts/grade_artifact.py`, `scripts/check_tool_safety.py`, `scripts/run_trigger_evals.py`, and `scripts/check_forward_tests.py`; use those results as the deterministic gate. |
| H4 | Curated E2E run files are self-attested PASS summaries, not graded artifacts. | Test evidence gap | Implemented the artifact/graded layout, fixture map, and `scripts/grade_productskills_synthetic_e2e.py`; remaining work is to rerun each runtime and store actual generated artifacts. |
| H5 | Negative safety paths are present as runtime prompts but are not yet deterministic grader cases. | Synthetic-pack wiring gap | Map the negative prompts to expected YAML/tool-safety fixtures or keep them explicitly labeled as manual/adversarial smoke evidence. |
| H6 | Large-corpus synthesis lacks a required scale/batching protocol. | Skill instruction gap | Add a ProductSkills scale protocol that reuses existing evidence-ledger concepts and adds batch summaries, dedupe table, conflict register, missing-field table, minority-signal carry-forward, noisy-signal suppression, representative-vs-exhaustive citation rules, and final roll-up with counts and confidence. |
| H7 | Scale scorecards are projected, not measured from stored prompt outputs. | Test evidence gap | Store outputs for scale prompts `01` through `08` at each scale and grade them before relying on breakpoint conclusions. |
| H8 | Scale ground truth conflates ranking goals. | Corpus or rubric gap | Split `expected_top_opportunities` into frequency top, ARR top, strategic top, risky/minority top, and noise controls. Document the ranking rule used by graders. |

### Medium

| Priority | Issue | Type | Required improvement |
| --- | --- | --- | --- |
| M1 | Design decisions can pass with weak evidence linkage. | Skill/test improvement | Require each design decision to cite evidence or be labeled as an assumption or validation question. |
| M2 | Full workflow prompt allows outline-depth artifacts. | Test coverage gap | Split workflow tests into routing mode and full-artifact mode, or require one routed stage to be completed to schema depth. |
| M3 | CS/support needs are input-only. | Product improvement | Add a CS/support-facing artifact or workflow output, such as support import triage, customer pain digest, or escalation-readiness brief. |
| M4 | Post-launch learning is not richly testable. | Corpus gap | Add baselines, metric windows, denominators, cohorts, exposure, churn, support trends, qualitative follow-up, and next-decision rules. |
| M5 | Tooling fixtures are not deterministic enough. | Test infrastructure gap | Add fixed synthetic workspace IDs, target assumptions, external ID maps, idempotency keys, payload hashes, partial-failure cases, and manual revert payload expectations. |
| M6 | Scale prompts for validation/docs/delivery/launch are under-supported. | Corpus gap | Add real rough PRDs, approved PRDs, epics/stories, launch gates, validation readouts, and post-launch artifacts at each scale. |
| M7 | Scale corpus is self-labeling for opportunities and integrity flags. | Corpus gap | Add unlabeled variants where opportunity IDs, conflict labels, duplicate labels, and missing-field labels are removed from the prompt-visible corpus and retained only as answer keys. |
| M8 | Duplicate generation can confuse the signal being tested. | Corpus gap | Generate same-account or same-opportunity near-duplicates unless cross-opportunity ambiguity is intentionally labeled. |

### Low

| Priority | Issue | Type | Required improvement |
| --- | --- | --- | --- |
| L1 | Output "next action" formatting varies. | Product polish | Standardize a final `Next Action` block across PM skills and workflows. |
| L2 | Internal stakeholder opinion is not isolated enough in tests. | Corpus improvement | Add internal stakeholder/founder opinions and require separation from customer evidence. |
| L3 | Security review artifact is absent. | Product improvement | Add security/compliance review output for enterprise-blocking claims and launch readiness. |
| L4 | Rollback wording can be tightened further. | Product polish | Use "manual revert payload" consistently and prohibit "rollback completed" phrasing in expected outputs. |

## Recommended Implementation Plan

1. Execute and store the shipped eval suite output. This is the fastest way to
   convert existing safety and quality coverage into release evidence.
2. Replace self-attested synthetic run summaries with captured artifacts and
   grader output.
3. Fix adapter visibility defaults and messaging. This is the confirmed
   user-facing product bug imported from field feedback.
4. Map negative runtime prompts to deterministic fixtures or keep them explicitly labeled as smoke evidence.
5. Add the large-corpus protocol to the ProductSkills workflow instructions and
   discovery/strategy references.
6. Rebuild the scale pack ground truth so ranking, citation, dedupe, and
   conflict expectations are machine-gradeable.
7. Add concrete scale artifacts for validation, docs, delivery, launch, and
   post-launch learning.
8. Run a cross-runtime comparison after changes and require stored outputs for
   every scale prompt, not only breakpoint summaries.

## Local Verification Run

After Claude review, the shipped deterministic eval/check scripts were run
locally against the repository. These checks passed:

| Command | Result |
| --- | --- |
| `python3 scripts/check_package.py` | PASS package validation. |
| `python3 scripts/check_tool_safety.py` | PASS tool safety evals, including negative live-write and missing-confirmation fixtures. |
| `python3 scripts/run_trigger_evals.py` | PASS trigger evals, 100.0% accuracy across 51 cases. |
| `python3 scripts/check_forward_tests.py` | PASS forward tests across 16 registered cases, including adversarial tooling and Product OS re-entry cases. |

These checks confirm the shipped eval harness exists and passes. They do not
replace the missing synthetic-pack work: the new E2E and scale packs still need
stored generated artifacts and grader output.

## Curated E2E Fixture Map

The 12 core synthetic E2E prompts are mapped to the existing ProductSkills
artifact grader as follows:

| Prompt | Expected fixture |
| --- | --- |
| `01-pm-discovery` | `evals/expected/discovery-synthesis.yaml` |
| `02-pm-strategy` | `evals/expected/prioritization-method-selection.yaml` |
| `03-pm-validation` | `evals/expected/validation-plan.yaml` |
| `04-pm-design` | `evals/expected/design-brief.yaml` |
| `05-pm-docs` | `evals/expected/prd-generation.yaml` |
| `06-pm-delivery` | `evals/expected/delivery-breakdown.yaml` |
| `07-pm-growth` | `evals/expected/growth-loop-diagnosis.yaml` |
| `08-pm-gtm` | `evals/expected/launch-readiness.yaml` |
| `09-pm-tooling` | `evals/expected/tool-dry-run-preview.yaml` |
| `10-workflow-product-operating-system-full` | `evals/expected/product-os-full-happy-path.yaml` |
| `11-workflow-discovery-to-prd` | `evals/expected/workflow-discovery-to-prd.yaml` |
| `12-workflow-prd-to-linear-delivery` | `evals/expected/workflow-prd-to-linear-delivery.yaml` |

Only three new expected fixtures were added because existing fixtures did not
cover standalone validation planning, design brief generation, or standalone
Linear plus Notion dry-run preview output.

## File-by-File Audit Log

### Top-Level Summary

| File | Result |
| --- | --- |
| `test-results/PRODUCTSKILLS_TEST_DELIVERY_SUMMARY.md` | Accurate high-level summary. Its key gaps are confirmed: blocked-state tests, adversarial live-write tests, automated grading, deterministic citation validation, aggregate ground truth, richer post-launch data, and unlabeled opportunities. |

### Curated E2E Docs And Meta Prompts

| File | Result |
| --- | --- |
| `productskills-e2e-synthetic/00-test-index.md` | Useful index of all 12 prompts; no defect found. |
| `productskills-e2e-synthetic/README.md` | Correctly frames manual comparison; exposes need for automated assertions. |
| `productskills-e2e-synthetic/runbook.md` | Practical manual runbook; release gating should not depend only on this. |
| `meta-prompts/README.md` | Useful evaluator context; no defect found. |
| `meta-prompts/compare-runtime-results.md` | Useful cross-runtime prompt; should be wired into stored result comparisons. |
| `meta-prompts/evaluate-productskills-end-to-end.md` | Useful evaluator prompt; should map to machine-checkable criteria. |
| `meta-prompts/run-in-claude.md` | Runtime execution prompt; no defect found. |
| `meta-prompts/run-in-codex.md` | Runtime execution prompt; no defect found. |
| `meta-prompts/run-in-gemini.md` | Runtime execution prompt; no defect found. |

### Curated E2E Inputs

| File | Result |
| --- | --- |
| `evidence/churn-notes.md` | Useful churn signal; supports growth/GTM learning but lacks richer metric windows. |
| `evidence/competitor-notes.md` | Useful market signal; no defect found. |
| `evidence/customer-interviews.md` | Strong qualitative evidence; supports discovery and design. |
| `evidence/sales-call-notes.md` | Useful sales signal; can be separated more explicitly from customer evidence in future tests. |
| `evidence/support-tickets.md` | Useful support signal; motivates CS/support-facing output gap. |
| `evidence/usage-analytics.md` | Useful product signal; limited for post-launch learning baselines. |
| `product/constraints.md` | Useful constraints; no defect found. |
| `product/current-roadmap.md` | Useful roadmap context; no defect found. |
| `product/existing-prd-approved.md` | Supports approved-PRD re-entry tests; no defect found. |
| `product/existing-prd-rough.md` | Supports rough-PRD review tests; no defect found. |
| `product/personas.md` | Useful persona context; no defect found. |
| `product/product-overview.md` | Useful product context; no defect found. |
| `schemas-and-artifacts/sample-delivery-handoff.md` | Useful sample; should be schema-validated in automated tests. |
| `schemas-and-artifacts/sample-launch-readiness-gate.md` | Useful sample; post-launch/launch readiness data should be richer. |
| `schemas-and-artifacts/sample-linear-preview.md` | Useful dry-run sample; should be checked for stable hash/idempotency fields. |
| `schemas-and-artifacts/sample-notion-preview.md` | Useful dry-run sample; should be checked for stable hash/idempotency fields. |
| `schemas-and-artifacts/sample-post-launch-learning.md` | Too thin for robust post-launch testing. |
| `schemas-and-artifacts/sample-prd.md` | Useful sample; should be schema-validated in automated tests. |
| `schemas-and-artifacts/sample-validation-decision.md` | Useful sample; should be schema-validated in automated tests. |

### Curated E2E Prompts And Expected Observations

| File | Result |
| --- | --- |
| `prompts/01-pm-discovery.md` | Appropriate coverage for discovery synthesis. |
| `expected-observations/01-pm-discovery.md` | Useful prose checklist; convert to assertions. |
| `prompts/02-pm-strategy.md` | Appropriate coverage for prioritization and method selection. |
| `expected-observations/02-pm-strategy.md` | Useful prose checklist; convert to assertions. |
| `prompts/03-pm-validation.md` | Appropriate validation routing prompt. |
| `expected-observations/03-pm-validation.md` | Useful prose checklist; convert to assertions. |
| `prompts/04-pm-design.md` | Needs stricter evidence-per-design-decision instruction. |
| `expected-observations/04-pm-design.md` | Under-specifies hard evidence requirements. |
| `prompts/05-pm-docs.md` | Appropriate PRD/docs coverage. |
| `expected-observations/05-pm-docs.md` | Useful prose checklist; convert to assertions. |
| `prompts/06-pm-delivery.md` | Appropriate delivery breakdown coverage. |
| `expected-observations/06-pm-delivery.md` | Useful prose checklist; convert to assertions. |
| `prompts/07-pm-growth.md` | Appropriate growth diagnosis prompt, but input data is thin. |
| `expected-observations/07-pm-growth.md` | Useful prose checklist; add richer metric expectations. |
| `prompts/08-pm-gtm.md` | Appropriate launch readiness prompt, but input data is thin for security/pricing claims. |
| `expected-observations/08-pm-gtm.md` | Useful prose checklist; add stricter unsupported-claim assertions. |
| `prompts/09-pm-tooling.md` | Good dry-run prompt; adversarial write pressure is covered by separate negative prompts and still needs deterministic fixture mapping. |
| `expected-observations/09-pm-tooling.md` | Correctly expects live-write blocking for the positive tooling path. |
| `prompts/10-workflow-product-operating-system-full.md` | Allows outline-depth artifacts; split routing versus full-artifact tests. |
| `expected-observations/10-workflow-product-operating-system-full.md` | Useful lifecycle expectations; needs depth criteria. |
| `prompts/11-workflow-discovery-to-prd.md` | Appropriate workflow prompt. |
| `expected-observations/11-workflow-discovery-to-prd.md` | Useful prose checklist; convert to assertions. |
| `prompts/12-workflow-prd-to-linear-delivery.md` | Appropriate workflow prompt. |
| `expected-observations/12-workflow-prd-to-linear-delivery.md` | Useful prose checklist; convert to assertions. |

### Curated E2E Results

| File | Result |
| --- | --- |
| `results/manual-run-2026-05-27.md` | Reports all 12 prompts PASS, but stores summaries rather than generated artifacts. |
| `results/codex-run-2026-05-27.md` | Reports all 12 prompts PASS, but stores summaries rather than generated artifacts. |
| `results/claude-run-2026-05-27.md` | Reports all 12 prompts PASS, but stores summaries rather than generated artifacts. |
| `results/gemini-run-2026-05-27.md` | Reports all 12 prompts PASS, but stores summaries rather than generated artifacts. |
| `results/codex-e2e-evaluation-2026-05-27.md` | Overall PASS; identifies schema/feasibility/post-launch gaps. |
| `results/claude-e2e-evaluation-2026-05-27.md` | Overall PARTIAL; stricter and mostly attributable to test coverage gaps. |
| `results/gemini-e2e-evaluation-2026-05-27.md` | Overall PASS; identifies useful product polish and data-density gaps. |

### Scale Pack Docs, Scripts, And Graders

| File | Result |
| --- | --- |
| `productskills-scale-synthetic/README.md` | Good scale-pack overview; should clarify which prompts have stored outputs. |
| `productskills-scale-synthetic/manifest.md` | Useful planted-signal description; should document ranking rules explicitly. |
| `productskills-scale-synthetic/runbook.md` | Useful manual process; release gating needs deterministic output capture. |
| `productskills-scale-synthetic/generator-config.json` | Useful configuration; should support unlabeled and richer artifact variants. |
| `productskills-scale-synthetic/scripts/generate_scale_corpus.py` | Generates useful scale data; duplicate generation should be refined. |
| `productskills-scale-synthetic/graders/scale-rubric.md` | Good rubric; needs scale-aware citation expectations and automated checks. |
| `productskills-scale-synthetic/edge-cases/README.md` | Useful catalog; should become executable fixture files. |
| `productskills-scale-synthetic/ground-truth/README.md` | Useful schema description; does not fully match aggregate JSON shape. |

### Scale Ground Truth

| File | Result |
| --- | --- |
| `ground-truth/scale-100/planted-ground-truth.json` | Useful aggregate truth; opportunity labels make recall easy. |
| `ground-truth/scale-500/planted-ground-truth.json` | Useful aggregate truth; ranking rule ambiguity begins to matter. |
| `ground-truth/scale-1000/planted-ground-truth.json` | Useful aggregate truth; supports degradation risk but stored prompt outputs are missing. |
| `ground-truth/scale-5000/planted-ground-truth.json` | Useful aggregate truth; confirms high conflicts/missing/duplicates and ranking ambiguity. |

### Scale Prompts

| File | Result |
| --- | --- |
| `prompts/01-scale-discovery.md` | Best-supported scale prompt; directly matches corpus. |
| `prompts/02-scale-strategy.md` | Partially supported; prioritization ranking rule is ambiguous. |
| `prompts/03-scale-validation.md` | Weakly supported; corpus lacks real validation readouts. |
| `prompts/04-scale-docs.md` | Weakly supported; corpus lacks real rough/approved PRDs at scale. |
| `prompts/05-scale-delivery.md` | Weakly supported; corpus lacks real delivery artifacts at scale. |
| `prompts/06-scale-tooling-safety.md` | Partially supported; must-block cases exist but deterministic payload fixtures are missing. |
| `prompts/07-scale-full-workflow.md` | Under-supported; corpus does not contain enough lifecycle artifact variety. |
| `prompts/08-scale-adversarial-edge-cases.md` | Under-supported; edge cases are descriptive, not executable fixtures. |
| `prompts/09-scale-breakpoint-evaluation.md` | Supported as a meta-evaluation prompt; should be paired with stored outputs from prompts 01-08. |

### Scale Corpus Files

| File | Result |
| --- | --- |
| `corpus/scale-100/interviews.md` | Useful small-scale evidence file. |
| `corpus/scale-100/support_tickets.md` | Useful small-scale support file. |
| `corpus/scale-100/sales_notes.md` | Useful small-scale sales file. |
| `corpus/scale-100/churn_notes.md` | Useful small-scale churn file. |
| `corpus/scale-100/competitor_notes.md` | Useful small-scale competitor file. |
| `corpus/scale-100/usage-analytics.md` | Useful small-scale analytics file. |
| `corpus/scale-100/product-context.md` | Useful small-scale product context. |
| `corpus/scale-500/interviews.md` | Useful medium-scale evidence file. |
| `corpus/scale-500/support_tickets.md` | Useful medium-scale support file. |
| `corpus/scale-500/sales_notes.md` | Useful medium-scale sales file. |
| `corpus/scale-500/churn_notes.md` | Useful medium-scale churn file. |
| `corpus/scale-500/competitor_notes.md` | Useful medium-scale competitor file. |
| `corpus/scale-500/usage-analytics.md` | Useful medium-scale analytics file. |
| `corpus/scale-500/product-context.md` | Useful medium-scale product context. |
| `corpus/scale-1000/interviews.md` | Useful large evidence file; scale degradation becomes plausible. |
| `corpus/scale-1000/support_tickets.md` | Useful large support file; conflict/dedupe tracking matters. |
| `corpus/scale-1000/sales_notes.md` | Useful large sales file; prioritization ambiguity matters. |
| `corpus/scale-1000/churn_notes.md` | Useful large churn file; requires citation discipline. |
| `corpus/scale-1000/competitor_notes.md` | Useful large competitor file. |
| `corpus/scale-1000/usage-analytics.md` | Useful large analytics file; richer post-launch data still missing. |
| `corpus/scale-1000/product-context.md` | Useful large product context. |
| `corpus/scale-5000/interviews.md` | Useful stress evidence file; requires batching and ledgers. |
| `corpus/scale-5000/support_tickets.md` | Useful stress support file; requires batching and ledgers. |
| `corpus/scale-5000/sales_notes.md` | Useful stress sales file; requires batching and ledgers. |
| `corpus/scale-5000/churn_notes.md` | Useful stress churn file; requires batching and ledgers. |
| `corpus/scale-5000/competitor_notes.md` | Useful stress competitor file; requires batching and ledgers. |
| `corpus/scale-5000/usage-analytics.md` | Useful stress analytics file; requires batching and ledgers. |
| `corpus/scale-5000/product-context.md` | Useful stress product context. |

### Scale Results

| File | Result |
| --- | --- |
| `results/scale-breakpoint-evaluation.md` | Useful Codex breakpoint assessment; scale-5000 degradation is plausible, but per-prompt source outputs are missing. |
| `results/claude-scale-breakpoint-evaluation-2026-05-27.md` | Useful Claude breakpoint assessment; identifies important corpus/ranking ambiguities. |

## Claude Verification

Completed read-only via `claude -p` on 2026-05-27. Claude agreed with the
main scale/corpus findings and the adapter visibility issue, and requested
these corrections:

- The package already ships automated eval infrastructure:
  `scripts/grade_artifact.py`, `scripts/check_tool_safety.py`,
  `scripts/run_trigger_evals.py`, `scripts/check_forward_tests.py`,
  `evals/expected/*.yaml`, artifact fixtures, tool-safety fixtures, trigger
  tests, and schemas. The synthetic packs should be wired to these instead of
  treating them as missing infrastructure.
- The curated E2E "run" files are self-attested PASS summaries, not stored
  generated artifacts. This weakens the claim that all runtime behavior was
  independently observed and graded.
- The scale scorecards are projections from corpus/ground-truth review, not
  measurements over stored outputs for prompts `01` through `08`.
- Codex versus Claude "safe scale" differences should be framed as methodology
  differences, not necessarily runtime/model variance.
- The scale corpus is self-labeling beyond opportunity IDs: conflict,
  duplicate, and missing-field flags are also prompt-visible, so the corpus
  tests label aggregation more than raw detection.
- Adapter visibility issues are imported field feedback and should remain in
  the final backlog, but they are independent of the synthetic test corpus.

Changes made after Claude review:

- Added the shipped eval-suite execution as the first implementation step.
- Re-attributed negative-path grading gaps to the new synthetic pack wiring,
  not the shipped package.
- Reframed manual grading as a wiring gap to existing graders.
- Added high-priority items for self-attested E2E results and projected scale
  results.
- Consolidated opportunity labels, integrity labels, and duplicate generation
  into corpus-design improvements.
