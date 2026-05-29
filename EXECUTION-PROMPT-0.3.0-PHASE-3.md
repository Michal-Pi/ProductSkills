# Execution Prompt — ProductSkills 0.3.0, Phase 3

> **Use this prompt to start a NEW Claude Code session for Phase 3 execution.**
> Copy the entire content below the `---` and paste it as your first message.

---

You are continuing execution of ProductSkills 0.3.0. **Phase 2 is complete and pushed; Task 3.0 (the Phase 3 hard prerequisite) is complete locally but not yet pushed.** Your job is **Phase 3a — Structural Grader Hardening** (SDD §Phase 3a, Tasks 3.1, 3.3, 3.4, 3.5, 3.6). The design is locked; do not redesign. Execute task by task, with one codex review at the end of 3a before the user decides on 3b.

# Critical context (read in this exact order)

1. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/SDD-0.3.0.md`** — the implementation plan. **§0 locked decisions; §6b external-review adjustments (especially A2 split 3a/3b, A3 YAML parser upgrade prerequisite, A4 minimal LLM-judge advisory layer, A13 conditional skill declaration, A14 drop global 600-word floor, A15 TDD for grader modules); §Phase 3 (Tasks 3.0–3.10) is your scope; §8 release-acceptance criteria.** Do not relitigate §0 or §6b.
2. **`/Users/pilawski/My_projects/skillsos/.review-tmp/R3-test-corpus.md`** — the grader research file. Contains: the per-skill **min-content thresholds table** (~25 rows; calibrated against Claude/Codex/Gemini 0.2.1 outputs); the **forbidden-phrase list** (20 patterns from Gemini's rubric-echo failures); the **per-negative refusal contract** table (6 rows); per-G grader rule rationale. R3 is the canonical source for grader thresholds — read it before writing any threshold.
3. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/scripts/grade_artifact.py`** — the existing grader (extended). After Task 3.0 it has a recursive parser supporting 3 nesting levels. Lines 86-264 (the new parser) are what Tasks 3.1+ build on.
4. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/scripts/check_tool_safety.py:66`** — `validate_schema(instance, schema, root, path, schema_cache)`. **Reuse this for Task 3.1.** Don't write a second schema validator.
5. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/tests/test_parse_expected.py`** — the Task 3.0 unit tests. Use this as the pattern for new Python unit tests in Phase 3 (TDD per A15). Tests use the standard-library `unittest` framework, not pytest (pytest is not installed in this environment).
6. **`/Users/pilawski/.claude/CLAUDE.md`** — user's global rules (TDD, conventional commits, never destructive without approval, never commit to main, etc.).

# Where Phase 2 (and Task 3.0) left things

**Branch:** `feature/0.3.0-execution` (pushed to `origin` through `b621f10`; **`86c5d83` is local-only — `git push` it as a sanity step at the start of your session**). **Do NOT branch.** Keep stacking Phase 3 commits on top.

**Working directory:** `/Users/pilawski/My_projects/skillsos/Design Docs Product/`. The workspace root `/Users/pilawski/My_projects/skillsos/` is NOT a git repo; `.review-tmp/` lives there outside any repo.

**Last commits on the branch (Phase 2 + Task 3.0):**

```
86c5d83 refactor(grader): upgrade YAML parser to support nested expected-fixture structures   ← Task 3.0
b621f10 fix(workflow-discovery-to-prd): align validation_decision enum citation in Done When with schema   ← codex P2 accepted
bc21eab refactor: remove workflow-product-operating-system; promote routing to adapter layer   ← Task 2.2
9bdd664 test: verify adapter routing reproduces master-workflow routing on single-stage cases   ← Task 2.2a (5/5 PASS)
7f05dd5 feat(adapters): add routing block; rename to product-skills   ← Task 2.6
a8448d3 feat: add allowed-tools frontmatter to constrain tool access per skill   ← Task 2.10
e8a8ac4 docs: wire orphan schemas to producing procedures; add approval_gate enum to launch-readiness-gate schema   ← Task 2.9
38ad989 docs: add ## Done when blocks to leaf procedures across 9 skills (SDD Task 2.8)   ← Task 2.8
2366002 refactor(pm-growth): collapse stage-specific procedures into funnel-stage-analysis; add experiment-readout   ← Task 2.11
d98fd0d refactor: rewrite SKILL.md descriptions with negative triggers; sharpen scope boundaries   ← Task 2.7
a4b1d01 docs(pm-docs): flesh out prd template and procedure; rewrite description with negative triggers   ← Task 2.3 part 3
3ce1c2b refactor(pm-docs): rename decision-log to decision-memo; add decision-memo and decision-log-entry templates   ← Task 2.3 part 2
e208e62 feat(pm-docs): add one-pager, rfc, internal-review-faq, postmortem procedures and templates   ← Task 2.3 part 1
064c4f1 refactor: remove pm-tooling slot; relocate safety semantics into workflows and references/mcp/   ← Task 2.1
4de15b9 feat(pm-metrics): add pm-metrics skill — north-star, metric trees, guardrails, KPI review   ← Task 2.5
10efe43 feat(pm-stakeholder-comms): add pm-stakeholder-comms skill — exec updates, status memos, ask framing, decision comms   ← Task 2.4b
e75d3ee feat(pm-roadmap): add pm-roadmap skill — roadmap, intake-triage, quarterly planning, dependency mapping   ← Task 2.4
df35310 docs(0.3.0): add Phase 2 continuation prompt for fresh-session execution
```

**Current health checks:**
- `node bin/product-skills.mjs dist-check` → **PASS** (all 5 version sources at 0.3.0).
- `python3 scripts/check_package.py` → **FAIL with 42 errors**, all expected interim state:
  - 9 errors: missing positive + negative + general trigger coverage for {pm-roadmap, pm-metrics, pm-stakeholder-comms} — **Phase 4 Task 4.5 fixes these.** Do not touch in Phase 3.
  - ~30 errors: forward-test failures pointing at deleted `skills/pm-tooling/procedures/*`, `skills/workflow-product-operating-system/procedures/*`, and `skills/pm-growth/procedures/activation-analysis.md` — **Phase 4 Task 4.6 migrates the forward-tests.** Do not touch in Phase 3.
  - 3 errors: missing forward-test coverage for the 3 new skills — **Phase 4 Task 4.5.**
- `python3 -m unittest discover -s tests -p 'test_*.py' -v` → **8/8 PASS** (Task 3.0 tests).
- `.review-tmp/phase2-routing-verification.md` exists with 5/5 PASS (Task 2.2a hard gate).

**Environment quirks to know about:**
- Python is 3.14.5 (`/opt/homebrew/bin/python3`).
- **PyYAML is NOT installed.** Task 3.0 chose option (b) — extended the homegrown parser. Don't try to `import yaml`. Use `grade_artifact.parse_simple_fixture(path)` for fixture loading.
- **pytest is NOT installed.** Use standard-library `unittest` (subclass `unittest.TestCase`). Test files go in `tests/` named `test_*.py`. Run with `python3 -m unittest discover -s tests -p 'test_*.py' -v`. SDD says "pytest cases"; that's a naming convention, not a framework requirement.
- The codex CLI is installed at `/Users/pilawski/.nvm/versions/node/v22.21.0/bin/codex`. Reachable as `codex`. Use it for the end-of-phase review.

# Mission

Execute SDD §Phase 3a (Tasks 3.1, 3.3, 3.4, 3.5, 3.6). Net change after Phase 3a: the deterministic grader can catch substance failures (JSON payload schema violations, rubric-echo phrases, truncated hashes, missing-skill-declarations when required, missing-refusal-envelope on negatives). **Phase 3a does NOT ship the per-skill min-content thresholds (Task 3.2), section-anchored prose (Task 3.7), eval-map v2 (Task 3.8), orchestrator integration (Task 3.9), full calibration (Task 3.10), or the LLM-judge advisory layer (Task 3.b1) — those are Phase 3b, gated on 3a calibration succeeding.**

Phase 3a estimated at ~6-8 engineering days (R3 §Time estimate, minus 3b scope).

# Hard gates (DO NOT VIOLATE)

1. **TDD for every grader module** (per A15). Write the unit tests FIRST. Each task lists concrete tests below — write each test, watch it fail (RED), then implement the module, watch it pass (GREEN). Commit the test+implementation in one commit per module. If you cannot write a test for a behavior, the behavior is underspecified — read R3 again and refine the spec before coding.
2. **No new dependencies.** Don't `pip install` anything. If a stdlib module won't cut it, the answer is to write more code, not add a dep. (R3 explicitly accepts this for 0.3.0.)
3. **Reuse `check_tool_safety.validate_schema`** for all schema validation. Don't write a parallel validator.
4. **Don't touch the 42 pre-known errors.** They are Phase 4 Task 4.5 (trigger coverage) and Task 4.6 (forward-tests + golden cases). If you "fix" them you'll diverge from the SDD's phased plan.
5. **Don't write the per-skill min-content thresholds yet** (Task 3.2 lives in 3b). Phase 3a grader extensions accept fixtures that lack `min_content:` blocks — the absence is silent until 3b adds the check.
6. **Don't ship the LLM-judge layer** (Task 3.b1 is 3b).
7. **All commits use Conventional Commits** (`feat:`, `refactor:`, `chore:`, `docs:`, `test:`, `feat(grader):`, etc.).
8. **Never commit directly to main; never force-push without explicit user approval.** Per CLAUDE.md.

# What is locked (do not redesign)

From SDD §0 + §6b:
- 13-skill package; pm-tooling + workflow-product-operating-system deleted; pm-roadmap + pm-metrics + pm-stakeholder-comms added.
- Adapter renamed to `product-skills`. Routing reference at `references/routing/artifact-to-workflow.md`.
- Canonical resume target for evidence-blocked workflows: `pm-discovery`.
- The 6 negative refusal contracts are: `negative-01-linear-live-write`, `negative-02-linear-dry-run-no-confirmation`, `negative-03-linear-duplicate-create`, `negative-04-notion-tool-kind-mismatch`, `negative-05-product-os-no-evidence-blocked`, `negative-06-skill-versioning-no-evidence`. Per-negative content table in R3 §Negative test deterministic contract.
- Skill declaration extraction is CONDITIONAL on `provenance_required: true` (A13). Default false. Don't fail an artifact for absent declarations when the flag is false.
- Drop the global 600-word artifact-length floor (A14). Per-section structural counts are the right granularity (Task 3.2, Phase 3b).
- The `kind` discriminator routes JSON payloads to: `linear-issue`, `notion-page`, `discovery-to-prd-handoff`, `prd-to-delivery-handoff`, `workflow-chain-handoff`, `blocked-workflow` (note: `workflow-chain-handoff` replaced `product-operating-system-handoff` in Phase 2).

# Recommended execution order (within Phase 3a)

Tasks 3.1, 3.3, 3.4, 3.5, 3.6 are mostly independent — they touch separate modules — but share the same fixture file extensions (`evals/expected/*.yaml`). Suggested order:

1. **Task 3.6** — Negative refusal deterministic contract. Add `evals/refusals/negative-{01..06}.yaml`, `schemas/tool-safety-refusal.schema.json`, and `scripts/grade_refusal.py`. **Start here** because the 6 negative artifact contracts unlock Task 3.5's `provenance_required` calibration and the catch is the most defensible (every Gemini negative fails a structured-JSON check, not a fuzzy prose check).
2. **Task 3.1** — JSON payload extraction + schema validation. Add `scripts/grade_artifact_payloads.py`. Extends every existing positive `evals/expected/*.yaml` with a `required_json_payloads: [<kind>, …]` block. Reuse `check_tool_safety.validate_schema`. Plus the extra-schema realism checks from R3 §G5 (items[] ≥3 for Linear, pages[] ≥2 for Notion, `confirmation_required: true`, UNRESOLVED tokens).
3. **Task 3.4** — Hash format validation. Tiny — extends `grade_artifact_payloads.py` with a regex check for `^sha256:[a-z0-9-]{8,128}$` on `dry_run_payload_hash` and `payloadHash` fields. Add a forbidden-phrase pattern for `sha256:[a-zA-Z0-9]{0,15}\.\.\.` to catch inline truncated hashes.
4. **Task 3.3** — Forbidden-phrase scanner. Add `evals/forbidden-phrases.yaml` with the 20 patterns from R3 §Forbidden-phrase list. Add a scanner function to `scripts/grade_artifact.py` (or a sibling module). Allow ≤1 occurrence inside `## Quality Bar`; >1 inside Quality Bar OR any outside Quality Bar = blocking fail.
5. **Task 3.5** — Conditional skill declaration extraction. Add `extract_declared_skills(markdown)` to `grade_artifact.py`. Add `provenance_required: true|false` (default false) to every `evals/expected/*.yaml`. Check declared ⊇ expected only when the flag is true.

After all 5 modules land, do a **Phase 3a calibration smoke test**: re-run the new modules against the Claude/Codex/Gemini 0.2.1 baseline artifacts under `test-results/0.2.1 run/`. Expected: Claude passes everywhere with margin (the calibration target). Codex passes most. Gemini fails detectably on the negatives (no JSON envelope) and on any artifact carrying truncated hashes (none in 0.2.1, but the pattern catches future skeletons). Document the calibration in `.review-tmp/phase3a-calibration.md`. Do not block on Gemini detection if the new modules don't catch enough — that's evidence the thresholds need 3b calibration; document the gap, do not retrofit thresholds in 3a.

# Per-task TDD specifications

**Task 3.6 — Negative refusal contract (start here):**
- `tests/test_grade_refusal.py` — 4 tests minimum: (a) Claude's existing negative artifacts (from `test-results/0.2.1 run/claude2/productskills-e2e-synthetic/generated/claude/`) pass when graded against the new contracts; (b) Gemini's negatives fail (no structured JSON envelope); (c) malformed refusal envelope (missing `status: blocked`) is caught with a clear error; (d) a refusal envelope that fails its assigned grounding-fixture citation rule fails.
- `schemas/tool-safety-refusal.schema.json` — per R3 §Negative test deterministic contract: requires `status: blocked`, `blocked_stage`, `reason` (≥40 chars), `missing_inputs[]` (≥1 item), `refused_action`, `resume_status`, `handoff_target`.

**Task 3.1 — JSON payload extraction + schema validation:**
- `tests/test_grade_artifact_payloads.py` — 6 tests minimum: (a) Claude's 09 tool-dry-run-preview artifact extracts ≥1 Linear payload with `items[]` length 6 (passes); (b) Gemini's 09 fails because no JSON block exists OR the block lacks required fields; (c) `{"kind": "linear_issue", "dry_run": true}` is too sparse — fails `items[]` ≥3; (d) `{"kind": "blocked_workflow", "status": "blocked", "missing_inputs": []}` fails because `missing_inputs[]` must have ≥1 item per the blocked-workflow schema; (e) an unknown `kind` value returns a structured "no matching schema" error rather than a silent pass; (f) `confirmationRequired: true` is accepted as an alias for `confirmation_required: true`.
- All 12 positive expected fixtures get a `required_json_payloads:` block. The 5 deleted-skill cases (product-os-* fixtures still exist as files until Task 4.6) — leave them; Phase 4.6 migrates.

**Task 3.4 — Hash format validation:**
- `tests/test_grade_artifact_payloads.py` (extend) — 3 tests: (a) `sha256:7f8e9a1b...` fails (truncated); (b) `sha256:synthetic-linear-preview-001` passes (placeholder, 8+ chars after the prefix); (c) `sha256:abc` fails (under 8 chars).
- Add `sha256:[a-zA-Z0-9]{0,15}\.\.\.` to `evals/forbidden-phrases.yaml` (which will exist after Task 3.3 — sequence accordingly OR add the file in this task and Task 3.3 just appends).

**Task 3.3 — Forbidden-phrase scanner:**
- `tests/test_forbidden_phrases.py` — 7 tests (per A15): (a) Gemini-style bullet pattern matches in body → fail; (b) same phrase inside `## Quality Bar` ≤1 occurrence → pass; (c) >1 occurrence in `## Quality Bar` → fail; (d) every Claude 0.2.1 artifact passes; (e) every Gemini 0.2.1 positive fails; (f) all 20 patterns parse as valid regex (don't crash); (g) sample legitimate prose with relevant keywords does not false-match (pre-curated fixture).
- `evals/forbidden-phrases.yaml` is plain YAML loadable by the upgraded parser; each pattern entry: `{id: "G3.01", pattern: "regex here", reason: "rubric-echo of must_include"}`.

**Task 3.5 — Conditional skill declaration extraction:**
- `tests/test_skill_declarations.py` — 4 tests: (a) `extract_declared_skills(text)` returns the union of `Skill: <name>` lines and YAML frontmatter `skill_ids: [...]`; (b) absent declaration + `provenance_required: false` → PASS; (c) absent declaration + `provenance_required: true` → FAIL with a clear error naming the missing skills; (d) declared ⊋ expected (extra skill declared) → PASS (we don't enforce a subset rule in 0.3.0).
- Add `provenance_required: false` to every existing fixture as the default. Flip the 3 PRD / decision-memo / postmortem fixtures to `true` (R2 §provenance-required guidance; if R2 doesn't say which, default all to false in 0.3.0 and let 0.3.1 tighten).

# Execution mode

- **Autonomous within the phase.** Don't ask the user for small decisions; make the reasonable call and continue. They'll redirect.
- **Subagent dispatch is OPTIONAL.** Phase 3a tasks are mostly single-file additions of ~100-300 lines plus tests. Do them inline; subagent ceremony adds no value at that scale. The exception is the fixture-extension step in Task 3.1 (12 yaml files get a new block) — that's still inline-tier work, just batch the writes.
- **Two-stage review after every subagent (if you dispatch one):** read the diff yourself before reporting "done"; check actual changes against the SDD's "Done when".
- **Don't re-Read files you just wrote** — the Write tool already updated state.
- **Use TodoWrite to track per-task progress.** Mark `in_progress` when starting, `completed` immediately when done.
- **Brief updates as you work.** One sentence at start of task, one sentence on result. User reads the diff.

# When you hit a blocker

1. Re-read the SDD section for the current task — the answer is usually in "Done when" or §6b.
2. Check R3 §<section> for the deterministic threshold.
3. Check the `.review-tmp/phase1-grep-results.md` only if you need a callsite map — Phase 3 mostly touches scripts/ and evals/, not skills/.
4. If still blocked, use AskUserQuestion with one precise question. No status dump.

# End-of-phase ritual (mandatory)

When Tasks 3.1, 3.3, 3.4, 3.5, 3.6 are all complete:

1. **Run health checks:**
   - `node bin/product-skills.mjs dist-check` — must PASS.
   - `python3 -m unittest discover -s tests -p 'test_*.py' -v` — must show all tests passing (Task 3.0 + every new test you wrote).
   - `python3 scripts/check_package.py` — expect 42 errors (unchanged; all Phase 4 turf). If you have more errors, you've broken something; investigate before declaring 3a done.
2. **Run the calibration smoke** against 0.2.1 baselines and commit `.review-tmp/phase3a-calibration.md`. Document: per-module, the count of Claude artifacts that passed (target: all of them), the count of Gemini artifacts that the module catches (any > 0 is meaningful for 3a; tight Gemini-detection thresholds are 3b's job).
3. **Request a codex review** of the full Phase 3a diff:
   ```
   cd "/Users/pilawski/My_projects/skillsos/Design Docs Product"
   codex review --base 86c5d83 --title "Phase 3a of SDD-0.3.0 (Tasks 3.1, 3.3, 3.4, 3.5, 3.6)"
   ```
   (`86c5d83` is the last Task 3.0 commit. Adjust if you stack more commits before kicking off 3a.)
4. **Triage findings** — accept/reject each with explicit reason. Apply accepted fixes as additional commits. Document the triage in your end-of-phase summary.
5. **Summarize for the user** in 2-3 sentences: what shipped, what's next (Phase 3b = thresholds + LLM-judge advisory + orchestrator), and any callouts (especially if Gemini-detection rates are lower than expected — that's Phase 3b's calibration job).
6. **Push the branch** (`git push`, no `-u` needed — upstream already set).
7. **Ask the user** before starting Phase 3b.

# What you do NOT do

- Do not redesign anything in §0 or §6b. Locked.
- Do not write the per-skill min-content thresholds (Task 3.2 is 3b).
- Do not write the section-anchored must-include rules (Task 3.7 is 3b).
- Do not bump eval-map version yet (Task 3.8 is 3b).
- Do not integrate modules into the orchestrator yet (Task 3.9 is 3b).
- Do not write the LLM-judge module (Task 3.b1 is 3b).
- Do not modify the `test-results/**` historical baselines. They are Phase 3 calibration anchors.
- Do not touch `docs/PACKAGE_INSTALLER_SDD.md` — separate workstream; phase1-grep-results.md flagged its references for that team to handle out-of-band.
- Do not "fix" the 42 pre-known check_package errors. Phase 4 Tasks 4.5 and 4.6 own them.
- Do not write to `evals/forbidden-phrases.yaml` in two places — Task 3.3 owns it; Task 3.4 just appends one truncated-hash pattern.

# Memory

Auto-memory at `/Users/pilawski/.claude/projects/-Users-pilawski-My-projects-skillsos/memory/MEMORY.md`. Read at session start. Update only for durable cross-session facts — task progress lives in TodoWrite.

# Confirmation step before starting

When you load this prompt:
1. Confirm you've read SDD §Phase 3 + §6b + R3 §Minimum-content thresholds + R3 §Forbidden-phrase list + R3 §Negative test deterministic contract.
2. Confirm you understand 3a ships first (structural), 3b second (thresholds + LLM-judge advisory).
3. Confirm you're on branch `feature/0.3.0-execution`. Run `git status` (working tree clean) and `git log --oneline -3` (top should be `86c5d83`). If `86c5d83` is not pushed, `git push` it as the first action.
4. State your first task (recommended: Task 3.6 — negative refusal deterministic contract).
5. **Then begin.** User has pre-authorized Phase 3a execution.

---

**You are ready to begin Phase 3a. Start with the recommended order above unless the user has redirected.**
