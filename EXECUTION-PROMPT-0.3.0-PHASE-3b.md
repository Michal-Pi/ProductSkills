# Execution Prompt — ProductSkills 0.3.0, Phase 3b

> **Use this prompt to start a NEW Claude Code session for Phase 3b execution.**
> Copy the entire content below the `---` and paste it as your first message.

---

You are continuing execution of ProductSkills 0.3.0. **Phase 3a is complete and pushed.** Your job is **Phase 3b — Content-threshold grader hardening + LLM-judge advisory + orchestrator integration** (SDD §Phase 3b, Tasks 3.2, 3.7, 3.8, 3.9, 3.10, 3.b1). The design is locked; do not redesign. Execute task by task, with a codex review at the end of 3b before the user decides on Phase 4.

# Critical context (read in this exact order)

1. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/SDD-0.3.0.md`** — the implementation plan. **§0 locked decisions; §6b external-review adjustments (A2 split 3a/3b — 3b is now; A4 minimal LLM-judge advisory layer; A13 conditional skill declaration; A14 drop global 600-word floor; A15 TDD for grader modules); §Phase 3b (Tasks 3.2, 3.7, 3.8, 3.9, 3.10, 3.b1) is your scope; §8 release-acceptance criteria.** Do not relitigate §0 or §6b.
2. **`/Users/pilawski/My_projects/skillsos/.review-tmp/R3-test-corpus.md`** — the grader research file. Specifically: §Minimum-content thresholds (~25 rows, calibrated against Claude 0.2.1), §G2 density gates, §G10 section-anchored must-include, §G1 judge prompt design. R3 is canonical for thresholds — do not invent.
3. **`/Users/pilawski/My_projects/skillsos/.review-tmp/phase3a-calibration.md`** — the Phase 3a calibration smoke result. **You are calibrating against the same Claude/Gemini 0.2.1 baselines.** Phase 3a delivered Claude 12/12 + 6/6 PASS; Gemini 12/12 fp + 4/12 pl + 6/6 neg CAUGHT. Phase 3b must NOT regress those numbers and SHOULD increase Gemini's payload-catch rate above 4/12 (target: 8-12/12 once min-content + section-anchored prose check the prose-heavy positives).
4. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/scripts/grade_artifact.py`** — the existing grader. Phase 3a added `load_forbidden_phrases`, `scan_forbidden_phrases`, `extract_declared_skills`, `check_provenance`. The parser at lines 86-264 is the recursive 3-level YAML parser from Task 3.0. Lines 393-411 are `_split_quality_bar` (reuse for section-anchored prose).
5. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/scripts/grade_artifact_payloads.py`** — the Phase 3a payload module. Has `extract_payloads`, `grade_payloads`, kind aliases (`_KIND_ALIASES`), per-kind realism + hash-format checks. Extend; don't replace.
6. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/scripts/grade_refusal.py`** — the Phase 3a refusal module. Reuse for orchestrator integration in Task 3.9.
7. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/scripts/check_tool_safety.py:66`** — `validate_schema`. **Continue to reuse.** Don't write a parallel validator.
8. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/scripts/grade_productskills_synthetic_e2e.py`** — the orchestrator that Task 3.9 wires the Phase 3a + 3b modules into.
9. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/tests/test_*.py`** — 42 Phase 3a tests across `test_parse_expected.py`, `test_grade_refusal.py`, `test_grade_artifact_payloads.py`, `test_forbidden_phrases.py`, `test_skill_declarations.py`. Use these as the pattern for Phase 3b tests (TDD per A15, `unittest` framework, NOT pytest — pytest is not installed).
10. **`/Users/pilawski/.claude/CLAUDE.md`** — user's global rules.

# Where Phase 3a left things

**Branch:** `feature/0.3.0-execution` (pushed; HEAD is `52fe1ef`). **Do NOT branch.** Keep stacking Phase 3b commits on top.

**Working directory:** `/Users/pilawski/My_projects/skillsos/Design Docs Product/`.

**Last 6 commits (Phase 3a):**

```
52fe1ef fix(grader): per-occurrence forbidden-marker check + blocked-workflow spelling alias   ← Codex P2 + P3 fixes
1e9cdb2 fix(grader): accept externalIdMap as items-equivalent in linear batch envelope         ← calibration tweak
154a89c feat(grader): conditional skill declaration extraction (provenance_required flag)      ← Task 3.5
73e401f feat(grader): add forbidden-phrase scanner for rubric-echo detection                   ← Task 3.3
c4c0c9d feat(grader): add JSON payload extraction, schema validation, and hash format check    ← Tasks 3.1 + 3.4
751d8ef feat(grader): add deterministic refusal contracts for 6 negative tests                 ← Task 3.6
```

**Current health checks (must be true at the start of your session):**
- `node bin/product-skills.mjs dist-check` → **PASS**
- `python3 -m unittest discover -s tests -p 'test_*.py' -v` → **42/42 PASS**
- `python3 scripts/check_package.py` → **FAIL with 42 errors** (Phase 4 turf — do NOT touch)

**Environment quirks (unchanged from Phase 3a):**
- Python 3.14.5
- **PyYAML is NOT installed.** Use `parse_simple_fixture` from `grade_artifact.py`.
- **pytest is NOT installed.** Use standard-library `unittest`.
- The codex CLI is at `/Users/pilawski/.nvm/versions/node/v22.21.0/bin/codex`. Reachable as `codex`. Use it for the end-of-phase review.

# Mission

Execute SDD §Phase 3b (Tasks 3.2, 3.7, 3.8, 3.9, 3.10, 3.b1). Net change after Phase 3b: the deterministic grader catches per-section content failures (evidence-ID counts, scored opportunities, etc.), discriminates prose-form rubric usage from bullet-echo, has eval-map v2 with first-class negatives, and is fully integrated into the orchestrator. Plus an advisory LLM-judge layer that reports concrete-reasoning score without flipping pass/fail.

**Phase 3b estimated at ~5-7 engineering days.**

# Hard gates (DO NOT VIOLATE)

1. **TDD for every new module + every change to a Phase 3a module** (per A15). Tests first, RED-GREEN-REFACTOR. The 42 Phase 3a tests must still pass after every commit.
2. **No new runtime dependencies.** No `pip install`. If you need an LLM client for Task 3.b1, see Task 3.b1's design constraints below.
3. **Reuse `check_tool_safety.validate_schema`** for all schema validation.
4. **Don't touch the 42 pre-known check_package errors.** They are Phase 4 Task 4.5 and Task 4.6 turf.
5. **Don't regress Phase 3a calibration.** After every commit, re-run the calibration smoke (see `.review-tmp/phase3a-calibration.md` for the methodology) and confirm Claude 12/12 positives + 6/6 negatives still PASS. If a 3b change breaks Claude, the change is wrong — adjust the threshold, don't override Claude.
6. **The LLM-judge layer is ADVISORY in 0.3.0** (per A4). Score is reported, NEVER flips pass/fail.
7. **All commits use Conventional Commits** (`feat:`, `refactor:`, `chore:`, `docs:`, `test:`, `feat(grader):`, etc.).
8. **Never commit directly to main; never force-push without explicit user approval.** Per CLAUDE.md.

# What is locked (do not redesign)

From SDD §0 + §6b + Phase 3a learnings:
- 13-skill package; canonical resume target for evidence-blocked = `pm-discovery`.
- The 6 negative refusal contracts are stable in `evals/refusals/`. Phase 3b does NOT change them.
- The 20 forbidden-phrase patterns are stable in `evals/forbidden-phrases.yaml`. Phase 3b MAY add patterns; should not remove.
- Drop the global 600-word floor (A14). Per-section structural counts ARE the right granularity — that is what Task 3.2 ships.
- `required_json_payloads` and `provenance_required` fields are stable in `evals/expected/*.yaml`.
- Phase 3a's bullet-anchored G3.06/G3.12/G3.13/G3.19 patterns can be relaxed BACK to non-bullet form once Task 3.7 (section-anchored prose with `anchored: prose` + `min_words_in_context: 30`) ships, IF the section-anchored check provides the same Claude-discrimination guarantee. Verify with calibration before relaxing.

# Recommended execution order (within Phase 3b)

Tasks 3.2 and 3.7 are mostly independent (different fields in `evals/expected/*.yaml`). Task 3.b1 is independent. Task 3.8 depends on 3.6's negatives + 3.9's integration. Task 3.9 depends on 3.2, 3.7, 3.b1. Task 3.10 is last.

Suggested order:

1. **Task 3.2 — Per-skill min-content thresholds (G2).** Add `min_content:` block to every relevant `evals/expected/*.yaml` using R3 §Minimum-content thresholds (~25 rows). Add helpers to `grade_artifact.py`: `count_evidence_ids(text)`, `count_table_rows(section_name, text)`, `count_section_bullets(section_name, text)`. Calibrate against Claude 0.2.1 (must pass) and Gemini 0.2.1 (target: ≥6 of 12 positives catch). DO NOT enforce the global 600-word floor (A14 dropped it).
2. **Task 3.7 — Section-anchored must-include (G10).** Extend `evals/expected/*.yaml` with `must_include_in_section:` block per R3 §G10. Add `extract_section_text(markdown, section_name)` and `phrase_in_prose_context(phrase, section_text, min_words)` to `grade_artifact.py`. After Task 3.7 lands, re-evaluate the 4 bullet-anchored patterns from Phase 3a (G3.06, G3.12, G3.13, G3.19) — if section-anchored covers them, relax the bullet-anchor and let the prose check do the discrimination.
3. **Task 3.b1 — Minimal LLM-judge advisory layer (A4 / G-1).** Add `scripts/judge_artifact_llm.py` — single dimension `concrete_reasoning` 1-4 scale. Prompt at `evals/judge-prompts/concrete-reasoning.md` calibrated with 3 example outputs at each score 1-4. Output goes to `graded/<runtime>/<prompt>.judge.json`. **Does NOT flip pass/fail in 0.3.0.** This task may need an LLM client — discuss the dependency decision with the user before adding any.
4. **Task 3.8 — eval-map v2 with negatives.** Bump `test-results/productskills-e2e-synthetic/eval-map.json` version to 2; add the `negatives:` array per R3 §eval-map.json restructuring. Each negative references its refusal contract + grounding fixture. Update the orchestrator (Task 3.9) to process both positives and negatives.
5. **Task 3.9 — Orchestrator integration.** Wire the new modules + Phase 3a modules into `scripts/grade_productskills_synthetic_e2e.py`. Pipeline per SDD §Phase 3 / Task 3.9. Each artifact gets a single merged graded JSON. **This addresses Codex P1 finding from Phase 3a — orchestrator wiring was intentionally deferred to 3b.**
6. **Task 3.10 — Calibration & threshold verification.** Re-run the orchestrator end-to-end on Claude/Gemini 0.2.1 baselines. Target per SDD §3.10: Claude 18/18 PASS (12 positives + 6 negatives), Codex 17+/18 PASS, Gemini 0-3/12 positives PASS + 0-2/6 negatives PASS. Write `.review-tmp/phase3b-calibration.md` documenting every threshold's calibrated value + observed Claude/Gemini value. Any Claude regression → adjust threshold downward + document. Any Gemini overpass → tighten pattern + document.

# Per-task TDD specifications

**Task 3.2 — Per-skill min-content thresholds:**
- `tests/test_min_content.py` — 8+ tests: (a) `count_evidence_ids` finds `INT-001..060` across a long discovery synthesis artifact (≥40 IDs); (b) Claude's 01 passes `evidence_id_count: 12` threshold; (c) Gemini's 01 fails (11 IDs < 12); (d) `count_table_rows("scores", text)` counts markdown table rows under the `## scores` heading; (e) Claude's 02 has ≥4 scored opportunities; Gemini's 02 has 1 (fail); (f) `count_section_bullets("opportunities", text)` for prose+bullet hybrid; (g) absent `min_content:` block in an expected fixture is silently allowed (advisory until 3b spec — but 3b spec IS now, so this should fail explicitly: "fixture must declare min_content block"); (h) every existing positive fixture parses with min_content block intact.
- Add the R3 §Minimum-content thresholds table (~25 rows) to the 12 positive fixtures (skip product-os-* per the Task 4.6 deferral).

**Task 3.7 — Section-anchored must-include:**
- `tests/test_section_anchored.py` — 6+ tests: (a) `extract_section_text(text, "scores")` returns the slice from `## scores` to next h2; (b) `phrase_in_prose_context("opportunity scored against criteria weights", section_text, min_words=30)` passes when the phrase sits in a ≥30-word paragraph; (c) same phrase as a 5-word bullet fails; (d) bold-prefixed bullet `- **Opportunity**: scored against criteria weights` (Gemini form) does NOT pass `anchored: prose`; (e) Claude's 02 passes for all expected anchored phrases; (f) Gemini's 02 fails on the section-anchored prose check for the same phrases.

**Task 3.b1 — Minimal LLM-judge advisory:**
- Discuss dependency strategy with the user BEFORE coding. Options: (a) stdlib HTTP client to Anthropic API (requires `ANTHROPIC_API_KEY` env var; advisory-only mode means the orchestrator skips silently when the key is absent); (b) a stub/mock implementation that scores based on heuristic features (evidence ID count, prose paragraph density, table presence) — no network, no API key — and is labeled "judge-stub" in graded JSON.
- `tests/test_judge_concrete_reasoning.py` — 4+ tests: (a) the judge prompt template loads; (b) a known-rich artifact scores ≥3; (c) a known-skeleton artifact scores ≤2; (d) graded JSON contains the score + the dimension name + advisory marker.
- Note: when using the API path, mark tests as "skip if no `ANTHROPIC_API_KEY`" — do NOT make CI fail on missing API key.

**Task 3.8 — eval-map v2:**
- `tests/test_eval_map.py` — 4+ tests: (a) eval-map.json is valid JSON; (b) version is 2; (c) `negatives:` array has 6 entries; (d) each negative entry references an existing refusal contract + grounding fixture.

**Task 3.9 — Orchestrator integration:**
- `tests/test_orchestrator_pipeline.py` — 6+ tests: (a) a positive artifact's graded JSON contains keys from grade_artifact + grade_artifact_payloads + scan_forbidden_phrases + check_provenance + grade_artifact.min_content + grade_artifact.section_anchored + judge_artifact_llm (advisory); (b) a negative artifact's graded JSON contains grade_refusal output; (c) merging preserves the structured `failures` list with module-of-origin; (d) the orchestrator runs end-to-end against Claude 12+6 baselines without errors; (e) the orchestrator emits a run-level summary tallying pass/fail per module; (f) Codex P1 is closed — `required_json_payloads` IS now read by the orchestrator path.

**Task 3.10 — Calibration:**
- This is a smoke run, not a unit test. Write `.review-tmp/phase3b-calibration.md` documenting every threshold's value + observed Claude/Gemini score. Required: Claude 18/18 PASS. If any Claude check fails, adjust the threshold downward by 1-2 and document. If Gemini passes a check we expect to catch, tighten and document.

# Execution mode

- **Autonomous within the phase.** Don't ask the user for small decisions. The one exception: Task 3.b1 dependency choice — discuss BEFORE coding because it has a CI/secret-management implication.
- **Subagent dispatch is OPTIONAL.** Phase 3b tasks are mostly single-file extensions of ~100-300 lines plus tests. Do them inline. Task 3.2's 25-row threshold table is a batch write — inline-tier still.
- **Use TaskCreate to track per-task progress.**
- **Brief updates as you work.** One sentence at start of task, one sentence on result.

# When you hit a blocker

1. Re-read the SDD section for the current task — the answer is usually in "Done when" or §6b.
2. Check R3 §<section> for the deterministic threshold.
3. Check `.review-tmp/phase3a-calibration.md` for what 3a calibrated against — same Claude/Gemini baselines.
4. If still blocked, use AskUserQuestion with one precise question.

# End-of-phase ritual (mandatory)

When Tasks 3.2, 3.7, 3.b1, 3.8, 3.9, 3.10 are all complete:

1. **Run health checks:**
   - `node bin/product-skills.mjs dist-check` — must PASS
   - `python3 -m unittest discover -s tests -p 'test_*.py' -v` — every Phase 3a + 3b test passing
   - `python3 scripts/check_package.py` — expect 42 errors (unchanged; Phase 4 turf)
2. **Run the Phase 3b calibration smoke** against 0.2.1 baselines and commit `.review-tmp/phase3b-calibration.md`. Calibration target per SDD §3.10:
   - Claude 18/18 PASS (12 positives + 6 negatives)
   - Codex 17+/18 PASS (if Codex artifacts are available; otherwise document the gap)
   - Gemini 0-3/12 positives PASS + 0-2/6 negatives PASS
3. **Request a codex review** of the full Phase 3b diff:
   ```
   cd "/Users/pilawski/My_projects/skillsos/Design Docs Product"
   codex review --base 52fe1ef --title "Phase 3b of SDD-0.3.0 (Tasks 3.2, 3.7, 3.8, 3.9, 3.10, 3.b1)"
   ```
   (`52fe1ef` is the last Phase 3a commit. Adjust if you stack more commits before kicking off 3b.)
4. **Triage findings** — accept/reject each with explicit reason. Apply accepted fixes as additional commits. Document the triage in the calibration doc (mirror the Phase 3a triage section format).
5. **Summarize for the user** in 2-3 sentences: what shipped, what's next (Phase 4 = corpus expansion, NEW-01..23 cases), and any callouts.
6. **Push the branch** (`git push`, upstream already set).
7. **Ask the user** before starting Phase 4.

# What you do NOT do

- Do not redesign anything in §0 or §6b. Locked.
- Do not regress Phase 3a calibration (Claude 12/12 + 6/6 must remain PASS).
- Do not modify the `test-results/**` historical baselines. They are Phase 3 calibration anchors.
- Do not touch `docs/PACKAGE_INSTALLER_SDD.md` — separate workstream.
- Do not "fix" the 42 pre-known check_package errors. Phase 4 Tasks 4.5 and 4.6 own them.
- Do not ship the full 5-dimension LLM judge — that's 0.4.0. 3b only ships single-dimension `concrete_reasoning` as advisory.
- Do not flip Phase 3a's `provenance_required: false` defaults to true unless 0.3.1 corpus expansion adds positive cases that justify it.

# Memory

Auto-memory at `/Users/pilawski/.claude/projects/-Users-pilawski-My-projects-skillsos/memory/MEMORY.md`. Read at session start. Update only for durable cross-session facts — task progress lives in TaskCreate/TaskUpdate.

# Confirmation step before starting

When you load this prompt:
1. Confirm you've read SDD §Phase 3 + §6b + R3 §Minimum-content thresholds + R3 §G10 + `.review-tmp/phase3a-calibration.md`.
2. Confirm you understand the calibration anchor: Phase 3a left Claude 12/12 + 6/6 PASS; Phase 3b must preserve that AND increase Gemini catch rate.
3. Confirm you're on branch `feature/0.3.0-execution`. Run `git status` (working tree clean) and `git log --oneline -3` (top should be `52fe1ef`).
4. State your first task (recommended: Task 3.2 — per-skill min-content thresholds).
5. **Then begin.** User has pre-authorized Phase 3b execution.

---

**You are ready to begin Phase 3b. Start with the recommended order above unless the user has redirected.**
