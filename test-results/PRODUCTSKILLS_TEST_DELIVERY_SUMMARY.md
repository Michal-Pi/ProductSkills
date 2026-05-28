# ProductSkills Synthetic Test Delivery Summary

Date: 2026-05-27

This delivery package contains synthetic ProductSkills test inputs, prompts, expected observations, generated scale corpora, ground truth, runbooks, and result files for the AtlasBoard fictional product.

No real customer data, secrets, API keys, private business information, or real external workspace IDs are included. No live Notion, Linear, GitHub, npm, network, launch, publish, sync, or external write operations were performed.

## Package Contents

### Curated E2E Pack

Directory: `productskills-e2e-synthetic/`

Purpose: tests every shipped ProductSkills skill and workflow on a compact, realistic product lifecycle scenario.

Includes:

- Synthetic evidence files.
- Product context files.
- 12 copy-pasteable skill/workflow prompts.
- 12 expected-observation files.
- Sample PRD, validation, delivery, launch, learning, Linear preview, and Notion preview artifacts.
- Runtime meta-prompts for Codex, Claude, and Gemini.
- Result files from Codex, Claude, and Gemini.

Skills and workflows covered:

| Prompt | Skill Or Workflow |
| --- | --- |
| `01-pm-discovery.md` | `pm-discovery` |
| `02-pm-strategy.md` | `pm-strategy` |
| `03-pm-validation.md` | `pm-validation` |
| `04-pm-design.md` | `pm-design` |
| `05-pm-docs.md` | `pm-docs` |
| `06-pm-delivery.md` | `pm-delivery` |
| `07-pm-growth.md` | `pm-growth` |
| `08-pm-gtm.md` | `pm-gtm` |
| `09-pm-tooling.md` | `pm-tooling` |
| `10-workflow-product-operating-system-full.md` | `workflow-product-operating-system` |
| `11-workflow-discovery-to-prd.md` | `workflow-discovery-to-prd` |
| `12-workflow-prd-to-linear-delivery.md` | `workflow-prd-to-linear-delivery` |

### Scale Stress Pack

Directory: `productskills-scale-synthetic/`

Purpose: tests where ProductSkills degrades or breaks at larger corpus sizes and under adversarial edge cases.

Includes:

- Deterministic corpus generator.
- Generated corpora at 100, 500, 1000, and 5000 evidence items.
- Planted ground-truth JSON files for each scale.
- 9 scale prompts, including a master breakpoint evaluation prompt.
- Scale scoring rubric.
- Edge-case catalog.
- Runbook.
- Scale breakpoint result files.

Scale levels:

| Scale | Purpose |
| --- | --- |
| `scale-100` | Sanity check. |
| `scale-500` | Medium-context citation and contradiction stress. |
| `scale-1000` | Large-corpus staged synthesis test. |
| `scale-5000` | Breakpoint test for batching, citation drift, duplicate over-counting, and minority-signal loss. |

## Tests Run

### 1. ProductSkills Install And Validation

Verified locally:

```text
ProductSkills status
- installed: yes
- version: 0.1.0
- validation: pass
- adapter: codex present via AGENTS.md
- adapter: claude present via .claude/skills/product-operating-system/SKILL.md
- adapter: cursor present via .cursor/rules/product-operating-system.mdc
- adapter: gemini present via GEMINI.md
```

### 2. Curated E2E Manual Run

Result file:

- `productskills-e2e-synthetic/results/manual-run-2026-05-27.md`

Summary:

- All 12 prompts passed against expected observations.
- No external systems were used.
- Dry-run behavior passed for tooling, GTM, delivery, and workflow cases.

### 3. Cross-Runtime E2E Evaluations

Result files:

- `productskills-e2e-synthetic/results/codex-e2e-evaluation-2026-05-27.md`
- `productskills-e2e-synthetic/results/claude-e2e-evaluation-2026-05-27.md`
- `productskills-e2e-synthetic/results/gemini-e2e-evaluation-2026-05-27.md`

Summary:

| Runtime | Overall Result | Notes |
| --- | --- | --- |
| Codex | PASS | Strong lifecycle coverage, evidence discipline, and dry-run tooling safety. |
| Claude | PARTIAL | Strong coverage, but flagged gaps in pure blocked-state testing, adversarial live-write testing, and automated grading. |
| Gemini | PASS | Strong evidence discipline, operational safety, and workflow routing. |

Key cross-runtime finding:

- All runtimes found the test pack useful for product-organization evaluation.
- Claude was stricter and identified additional test-design gaps.
- No runtime reported external writes.

### 4. Scale Breakpoint Evaluations

Result files:

- `productskills-scale-synthetic/results/scale-breakpoint-evaluation.md`
- `productskills-scale-synthetic/results/claude-scale-breakpoint-evaluation-2026-05-27.md`

Summary:

| Runtime/File | Overall Result | First Degradation | Highest Safe Scale | Main Failure Mode |
| --- | --- | --- | --- | --- |
| Codex scale breakpoint | PARTIAL | `scale-5000` | `scale-1000` with staged batching | citation drift, contradiction/minority-signal loss, theme collapse risk |
| Claude scale breakpoint | PARTIAL | `scale-1000` | `scale-500` for fully verifiable end-to-end synthesis | citation drift, false precision, duplicate over-counting |

Shared scale conclusion:

- ProductSkills remains safe under scale: dry-run tooling behavior and blocking rules did not degrade.
- Analytical fidelity degrades with larger corpora.
- The main breakpoint is not safety, but traceability: citation completeness, deduplication, contradiction enumeration, and minority-signal retention become fragile.
- A single-pass approach is not reliable at `scale-5000`; staged batching and structured evidence ledgers are required.

## Key Strengths Found

- Complete coverage of all 9 ProductSkills family skills and 3 workflows.
- Strong evidence discipline through concrete synthetic IDs.
- Explicit uncertainty and blocked-state expectations.
- Realistic dry-run-first Notion and Linear safety model.
- Useful lifecycle coverage from messy evidence through PRD, delivery, tooling preview, GTM, and learning.
- Scale pack exposes meaningful breakpoints instead of only confirming happy paths.

## Key Gaps Found

- Add pure "no evidence -> blocked workflow" prompts to the curated E2E pack.
- Add adversarial live-write prompts that ask the runtime to skip preview and create external records.
- Wire expected observations to automated graders where possible.
- Add deterministic citation validation for scale runs.
- Add opportunity-level aggregate ground truth to reduce false precision at large scale.
- Add richer post-launch learning data with baselines, denominators, exposure windows, churned-user data, and support trend data.
- Add unlabeled planted opportunities to test true discovery rather than only recovering explicit opportunity labels.

## Recommended Next Improvements

1. Add automated scoring scripts for citation accuracy, opportunity recall, duplicate handling, and blocked-state correctness.
2. Extend `scale-5000` prompts to require staged batch summaries, evidence ledgers, dedupe tables, and conflict registers.
3. Add negative tooling tests based on fake but plausible workspace IDs and direct live-write trap instructions.
4. Add schema validation for blocked workflow, validation decision, PRD handoff, delivery handoff, launch readiness, and tool previews.
5. Compare the same result files across Codex, Claude, and Gemini with a runtime-comparison artifact.

## Files To Start With

- Curated E2E README: `productskills-e2e-synthetic/README.md`
- Curated E2E index: `productskills-e2e-synthetic/00-test-index.md`
- Cross-runtime meta-prompt: `productskills-e2e-synthetic/meta-prompts/evaluate-productskills-end-to-end.md`
- Scale README: `productskills-scale-synthetic/README.md`
- Scale runbook: `productskills-scale-synthetic/runbook.md`
- Scale breakpoint prompt: `productskills-scale-synthetic/prompts/09-scale-breakpoint-evaluation.md`
- Scale rubric: `productskills-scale-synthetic/graders/scale-rubric.md`
