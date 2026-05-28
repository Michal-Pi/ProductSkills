# Execution Prompt — ProductSkills 0.3.0, Phase 2

> **Use this prompt to start a NEW Claude Code session for Phase 2 execution.**
> Copy the entire content below the `---` and paste it as your first message.

---

You are continuing execution of ProductSkills 0.3.0. **Phase 1 is complete and pushed.** Your job is **Phase 2 — Restructure Skills** (SDD §Phase 2). The design is locked; do not redesign. Execute task by task, with one codex review at the end of the phase before the user merges.

# Critical context (read in this exact order)

1. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/SDD-0.3.0.md`** — the implementation plan. **§0 locked decisions; §6b external-review adjustments; §Phase 2 (Tasks 2.1–2.11) is your scope; §8 release-acceptance criteria.** Do not relitigate §0.
2. **`/Users/pilawski/My_projects/skillsos/.review-tmp/phase1-grep-results.md`** — Phase 1 produced this. It classifies every callsite of `pm-tooling`, `workflow-product-operating-system`, `decision-log`, `skill-output-envelope`, `product-operating-system-handoff`, `product-operating-system-contract` into **live-code (must update)**, **doc-about-deletion (no action)**, and **historical-baseline (do not touch — Phase 3 calibration anchor)**. Use this as your callsite checklist for Tasks 2.1, 2.2, 2.3, 2.6.
3. **`/Users/pilawski/My_projects/skillsos/.review-tmp/R2-pm-docs.md`** — pm-docs rebuild research; has procedure templates, the updated SKILL.md description, and per-procedure `## Done when` blocks for Task 2.3.
4. **`/Users/pilawski/My_projects/skillsos/.review-tmp/R3-test-corpus.md`** — per-skill min-content thresholds (used by Phase 3, but Task 2.8 cross-references these when adding `## Done when` to procedures).
5. **`/Users/pilawski/My_projects/skillsos/.review-tmp/R1-workflow-pos.md`** — the kill-the-master-workflow research; relocation map for the 6 master-workflow capabilities.
6. **`/Users/pilawski/My_projects/skillsos/.review-tmp/external/EVALUATION.md`** — external review tensions, esp. A1 (verify routing BEFORE killing master workflow) and A16 (safety summary vs canonical reference for moved pm-tooling rules).
7. **`/Users/pilawski/.claude/CLAUDE.md`** — user's global rules (TDD, conventional commits, never destructive without approval, never commit to main, etc.).

# Where Phase 1 left things

**Branch:** `feature/0.3.0-execution` (pushed to `origin`, upstream tracking set). **Do NOT branch again.** Keep stacking Phase 2 commits on top.

**Working directory:** `/Users/pilawski/My_projects/skillsos/Design Docs Product/` — this is the package git repo. The workspace root `/Users/pilawski/My_projects/skillsos/` is NOT a git repo; `.review-tmp/` lives there outside any repo.

**6 commits already on the branch (Phase 1):**
```
6ae8c4e chore: drop workflow-product-operating-system from package.yaml entry_workflows (codex review P1-C)
c771d6d chore: bump .codex-plugin/plugin.json to 0.3.0 (codex review P1-A)
346f7f1 docs(workflows): pin canonical resume-target convention (SDD Task 1.5)
04ee21c feat(registry): update for 0.3.0 skill set — 13 skills (SDD Task 1.4)
d87a5eb chore: remove unused skill-output-envelope schema (SDD Task 1.3)
1a3e54b chore: pin version to 0.3.0 (SDD Task 1.1)
```

**Current health checks:**
- `node bin/product-skills.mjs dist-check` → **PASS** (all 5 version sources at 0.3.0).
- `python3 scripts/check_package.py` → **FAIL with 13 errors**, all expected interim state:
  - 3 errors: "Registry path does not exist for {pm-roadmap, pm-metrics, pm-stakeholder-comms}" — **Phase 2 Tasks 2.4, 2.4b, 2.5 fix these.**
  - 9 errors: missing positive + negative + general trigger coverage for the 3 new skills — **Phase 4 Task 4.5 fixes these.** Phase 2 alone will not bring check_package green; that happens at end of Phase 4.
  - 1 error: cascading forward-test missing SKILL.md error — clears with Phase 2.4.

**Registry quirk to know about:** Collection ID `pm-delivery` (after rename from `pm-delivery-tooling`) overlaps with skill ID `pm-delivery`. Different namespaces in `registry.json`; `check_package.py` validates them independently — no conflict. Don't "fix" this unless the user asks.

# Mission

Execute SDD §Phase 2 (Tasks 2.1–2.11) task by task. Net change after Phase 2: 13-skill set fully present, master workflow removed (with verified routing replacement), pm-docs rebuilt with 7 procedures, 3 new skills (`pm-roadmap`, `pm-metrics`, `pm-stakeholder-comms`) created, every SKILL.md has a `description:` with ≥1 negative trigger, every leaf procedure has a `## Done When` block, adapters carry routing blocks.

Phase 2 estimated at ~7–9 engineering days (SDD §9).

# Hard gates (DO NOT VIOLATE)

1. **Task 2.6 (adapter routing block) MUST land BEFORE Task 2.2 (delete master workflow).** Then Task 2.2a (verification gate) MUST PASS with ≥4 of 5 single-stage golden cases routing correctly through the new adapter, before Task 2.2 begins. If routing fails on 2+ cases, **HALT Phase 2** and re-evaluate the kill decision (the SDD's 85% confidence assumption is on the table). Both external reviewers (Gemini + Codex) flagged this as the highest-risk sequencing dependency.
2. **Task 2.6 puts the routing rule in BOTH the `description:` field AND the body** (per A9). Some adapter hosts route on description first. Also include the catch-all rule for unclassified inputs.
3. **Task 2.3 (pm-docs rebuild) — postmortem procedure Step 1 is the SRE-incident refusal contract** (per A8). It's procedural, not a template disclaimer. Refuses requests mentioning outage, downtime, SLA, SLO, auth failure, latency regression, on-call, infrastructure incident, security breach.
4. **Task 2.4b (pm-stakeholder-comms) — every procedure declares structured input contracts** (audience tier+function+authority, intent enum, key_message, risks, decisions_or_asks, evidence_anchors, next_action). Procedure REFUSES output if `audience.tier` or `intent` is missing. This is what makes it a PM skill, not a generic memo-writer.
5. **Task 2.1 — relocate pm-tooling safety semantics.** `workflow-prd-to-linear-delivery/SKILL.md` gets a 4-line `## Safety summary` block + explicit citation to `references/mcp/dry-run-preview.md` (per A16: visible summary + canonical reference resolves the Gemini-vs-Codex tension on whether to inline-duplicate the rules).
6. **Never delete a skill, schema, or doc without first verifying against** `.review-tmp/phase1-grep-results.md`. Update each callsite in lockstep with the deletion.
7. **All commits use Conventional Commits** (`feat:`, `refactor:`, `chore:`, `docs:`, `test:`, `feat(pm-docs):`, etc.).
8. **Never commit directly to main; never force-push without explicit user approval.** Per CLAUDE.md.

# What is locked (do not redesign)

From SDD §0 Q1–Q8 (Phase 1 already verified):
- 13 skills total (drop pm-tooling + workflow-pos; add pm-roadmap + pm-metrics + pm-stakeholder-comms)
- pm-docs: 7 procedures (PRD, decision-memo, spec-review, one-pager, RFC, internal-review-faq, postmortem)
- decision-memo supports both narrative + bullet-log forms (two templates, one procedure that selects on keywords)
- postmortem: product failures only (Step 1 = SRE refusal contract)
- Adapter renamed to `product-skills` (backward-compat shim is Phase 5 Task 5.2b; not Phase 2)
- Canonical resume target for evidence-blocked workflows: `pm-discovery` (Phase 1 Task 1.5 already pinned this)

# Recommended execution order (within Phase 2)

The SDD says Tasks 2.1–2.6 are interdependent and 2.7–2.11 are mostly independent. Recommended order to minimize churn and bring check_package back toward green ASAP:

1. **Task 2.4** — Add `pm-roadmap` skill. _(Creates skills/pm-roadmap/{SKILL.md, procedures/*.md} + templates + reference. Removes 1 of the 3 "Registry path does not exist" errors.)_
2. **Task 2.4b** — Add `pm-stakeholder-comms` skill. _(Removes 1 error; introduces the hard input-contract pattern per A10.)_
3. **Task 2.5** — Add `pm-metrics` skill. _(Removes the last "Registry path" error. Now check_package is down to 9 trigger-coverage errors + 1 forward-test cascade, all Phase 4.)_
4. **Task 2.1** — Remove pm-tooling slot; relocate safety semantics to `references/mcp/dry-run-preview.md` + `workflow-prd-to-linear-delivery/SKILL.md` `## Safety summary` block. Use `phase1-grep-results.md` §2 as your callsite checklist.
5. **Task 2.3** — Rebuild pm-docs (3 commits per SDD: add new procedures+templates; rename decision-log→decision-memo; flesh out PRD + rewrite description). Big task.
6. **Task 2.7** — Rewrite all 13 SKILL.md descriptions with negative triggers. Touches every skill but each edit is local.
7. **Task 2.8** — Add `## Done When` blocks to every leaf procedure (~40–50 files). Reference R3's per-skill min-content thresholds when picking acceptance conditions.
8. **Task 2.9** — Wire orphan schemas (4 schema-to-procedure citations + add `approval_gate` to launch-readiness schema OR remove from template).
9. **Task 2.10** — Add `allowed-tools:` frontmatter to every SKILL.md. File-ops-only for family skills; family-skills + Notion/Linear MCP for workflows; never `Bash`.
10. **Task 2.11** — Collapse pm-growth's 3 stage-specific procedures into one parameterized `funnel-stage-analysis.md`; add `experiment-readout.md`; add `## Method Selection` block.
11. **Task 2.6** — Update all 5 adapters with `## Routing` block (in description AND body); rename `product-operating-system` → `product-skills` for the `name:` field; add `references/routing/artifact-to-workflow.md` with the 12-row entry-classification table. **Backward-compat shim is Phase 5 Task 5.2b — not in Phase 2.**
12. **Task 2.2a** — Verify adapter routing. Take the 5 single-stage golden cases (`evals/golden-cases/product-os-*.md` except `product-os-full-happy-path.md`). Run each through an adapter-using runtime (Claude is the calibration target). Document observed routing in `.review-tmp/phase2-routing-verification.md`. **HARD GATE:** ≥4/5 PASS. If ≥2 FAIL, HALT phase and ask the user.
13. **Task 2.2** — Remove `workflow-product-operating-system`. Use `phase1-grep-results.md` §3 as your callsite checklist. Rename `schemas/product-operating-system-handoff.schema.json` → `schemas/workflow-chain-handoff.schema.json` and generalize `workflow_id` const. Archive 3 docs to `docs/_archive/`. Update `scripts/check_package.py` and `scripts/run_trigger_evals.py` to drop hard-coded references. The 6 master-workflow trigger tests and golden cases are NOT deleted here — they're migrated/retargeted in Phase 4 Task 4.6.

# Execution mode (locked from Phase 1)

- **Autonomous within the phase.** Don't ask the user for small decisions; make the reasonable call and continue. They'll redirect.
- **Subagent dispatch is OPTIONAL per task.** For small, deterministic edits (single-file frontmatter add, single string replacement), do them inline — subagent ceremony adds no value. For large edits with many files (Task 2.3 pm-docs rebuild, Task 2.8 add `## Done when` to 40+ procedures, Task 2.6 multi-adapter routing), dispatch a fresh `general-purpose` Agent per task with a self-contained brief: SDD section quoted, files to read first, files to modify/create/delete, acceptance criteria from "Done when".
- **Two-stage review after every subagent:** read the diff yourself before reporting "done"; check actual changes against the SDD's "Done when".
- **TodoWrite to track per-task progress.** Mark `in_progress` when starting, `completed` immediately when done.
- **Brief updates as you work.** One sentence at start of task, one sentence on result. User reads the diff.

# When you hit a blocker

1. Re-read the SDD section for the current task — the answer is usually in "Done when" or §6b.
2. Check the `.review-tmp/` research files.
3. Check `phase1-grep-results.md` for callsite coverage.
4. If still blocked, use AskUserQuestion with one precise question. No status dump.

# End-of-phase ritual (mandatory)

When Tasks 2.1–2.11 are all complete:

1. **Run health checks:**
   - `node bin/product-skills.mjs dist-check` — must PASS.
   - `python3 scripts/check_package.py` — expect ~9 errors remaining (all trigger-coverage for new skills, which Phase 4.5 fixes). If you have MORE errors than 9, investigate before declaring Phase 2 done.
   - Confirm the 5 adapter routing verification result is committed at `.review-tmp/phase2-routing-verification.md`.
2. **Request a codex review** of the full Phase 2 diff:
   ```
   cd "/Users/pilawski/My_projects/skillsos/Design Docs Product"
   codex review --base 6ae8c4e --title "Phase 2 of SDD-0.3.0 (Tasks 2.1-2.11)"
   ```
   (`6ae8c4e` is the last Phase 1 commit. Adjust if you stack more commits before kicking off Phase 2.)
3. **Triage findings** — accept/reject each with explicit reason. Apply accepted fixes as additional commits. Document the triage in your end-of-phase summary.
4. **Summarize for the user** in 2–3 sentences: what shipped, what's next (Phase 3 = grader hardening), and any callouts (especially if routing-verification went 4/5 with one legitimate divergence, or if any deferred SDD task was promoted to Phase 3).
5. **Push the branch** (`git push`, no `-u` needed — upstream already set).
6. **Ask the user** before starting Phase 3.

# What you do NOT do

- Do not redesign anything in §0. Locked.
- Do not delete the master workflow before Task 2.2a passes.
- Do not write nested-YAML expected fixtures (`min_content:`, `must_include_in_section:`) — that's Phase 3 (gated on Task 3.0 YAML parser upgrade).
- Do not write a customer-facing FAQ in pm-docs/internal-review-faq.md — it's the internal-review form (the rename per A11 disambiguates exactly this).
- Do not skip the routing-verification gate. Two external reviewers ranked it the highest-risk dependency.
- Do not modify the `test-results/**` historical baselines. They are Phase 3 calibration anchors.
- Do not touch `docs/PACKAGE_INSTALLER_SDD.md` — separate workstream; phase1-grep-results.md flagged its 5 stale references for that team to handle out-of-band.

# Memory

Auto-memory at `/Users/pilawski/.claude/projects/-Users-pilawski-My-projects-skillsos/memory/MEMORY.md`. Read at session start. Update only for durable cross-session facts — task progress lives in TodoWrite.

# Confirmation step before starting

When you load this prompt:
1. Confirm you've read SDD §Phase 2 + §6b + `phase1-grep-results.md`.
2. Confirm you understand the Task 2.6 → 2.2a → 2.2 hard gate.
3. Confirm you're on branch `feature/0.3.0-execution` and the working tree is clean.
4. State your first task (recommended: Task 2.4 — add pm-roadmap).
5. **Then begin.** User has pre-authorized Phase 2 execution.

---

**You are ready to begin Phase 2. Start with the recommended order above unless the user has redirected.**
