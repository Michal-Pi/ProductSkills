# claude.zip — ProductSkills Synthetic E2E Claude Run Artifacts

Bundles the Claude-specific outputs from the **2026-05-27** and **2026-05-28** runs, plus the
restored negative-prompt inputs that enabled them. Directory structure under
`productskills-e2e-synthetic/...` is preserved so the relative links inside the result files
keep resolving when the zip is extracted into a tree.

## Environment captured

- Runtime: Claude (Claude Code), model `claude-opus-4-7` (Opus 4.7, 1M context).
- ProductSkills package: `0.2.1` (verified across `VERSION`, `registry.json`, `package.json`,
  and the Claude adapter header).
- Adapter: `.claude/skills/product-operating-system/SKILL.md`.
- Pack version: 12 mapped core prompts (`eval-map.json`) + 6 negative prompts (restored).
- **External writes performed: none** — all dry-run; the 6 negatives requested unsafe writes
  and were refused.

## Contents

### Claude artifacts (18, both runs share the same generated paths)

`productskills-e2e-synthetic/generated/claude/`

12 core artifacts:

- `01-pm-discovery.md` … `12-workflow-prd-to-linear-delivery.md`

6 negative refusal/blocking artifacts:

- `negative-01-linear-live-write.md`
- `negative-02-linear-dry-run-no-confirmation.md`
- `negative-03-linear-duplicate-create.md`
- `negative-04-notion-tool-kind-mismatch.md`
- `negative-05-product-os-no-evidence-blocked.md`
- `negative-06-skill-versioning-no-evidence.md`

> Note: `generated/claude/` is a single directory shared across runs (the path doesn't carry a
> date). The artifacts inside reflect today's (2026-05-28) regenerated content. Yesterday's
> per-prompt artifacts had the same paths and were superseded by today's regeneration.

### Claude grader outputs (19)

`productskills-e2e-synthetic/graded/claude/`

- 12 deterministic grader JSONs for the core prompts (one per `01-pm-discovery.json` …
  `12-workflow-prd-to-linear-delivery.json`).
- `summary.json` (12/12 passed, 0 failed, 0 missing).
- 6 manual graded JSONs for the negatives (`grader: manual`, `graded_on: 2026-05-28`).

### Claude result files (2 — both runs)

`productskills-e2e-synthetic/results/`

- `claude-run-2026-05-27.md` — yesterday's run (artifact-backed; first revision to cover the
  restored 6 negatives).
- `claude-run-2026-05-28.md` — today's full end-to-end run on ProductSkills 0.2.1; 18/18 PASS.

### Restored negative-prompt inputs (authored 2026-05-27)

`productskills-e2e-synthetic/negative-prompts/`

- `README.md` — provenance: each of the 6 negative cases is grounded 1:1 in a shipped
  ProductSkills fixture under `.product-skills/evals/`. Not recovered original content.
- 6 adversarial prompt files (negative-01 … negative-06).

`productskills-e2e-synthetic/expected-observations/negative-prompts/`

- 6 expected-observation files matching the 6 prompts above; each cites its grounding
  fixture (4 `tool-safety-fixtures/*-negative` + 2 `golden-cases/*-no-evidence*`).

## What is *not* in this zip (intentional)

- Codex / Gemini / manual run artifacts — the user asked specifically for Claude runs.
- The original 12-prompt inputs (`prompts/`, `evidence/`, `product/`, `schemas-and-artifacts/`)
  and the shipped ProductSkills package (`.product-skills/`) — those are the pack itself,
  not Claude-specific artifacts. Both result files reference them by repo-relative path.
- `eval-map.json` — pack metadata, not Claude output.
- The grader script (`scripts/grade_productskills_synthetic_e2e.py`) — environment, not output.

If you want a fully self-contained zip including pack inputs, ask and I'll rebuild it.

## Reading order

1. `productskills-e2e-synthetic/results/claude-run-2026-05-28.md` — today's result file. Links to every generated artifact + graded JSON.
2. `productskills-e2e-synthetic/results/claude-run-2026-05-27.md` — yesterday's run, kept for history.
3. `productskills-e2e-synthetic/negative-prompts/README.md` — provenance for the 6 restored negatives.
4. Spot-check any `generated/claude/*.md` against the matching `graded/claude/*.json`.

## Pack total

**18/18 PASS** (12 grader-verified core, all overall_score 4/4 + 6 manually graded negative).
