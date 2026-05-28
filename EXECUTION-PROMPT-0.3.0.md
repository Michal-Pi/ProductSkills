# Execution Prompt — ProductSkills 0.3.0

> **Use this prompt to start a new Claude Code session for execution.**
> Copy the entire content below the `---` and paste it as your first message.

---

You are picking up execution of ProductSkills 0.3.0 — a major release of a product-management skills package. The design is **complete and approved**. Your job is to **execute the plan**, not redesign it.

# Critical context (read in this exact order)

1. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/SDD-0.3.0.md`** — the implementation plan. ~1300 lines. **Locked decisions are in §0; do not relitigate them.** The phases and tasks (§7 onward) are what you execute. **External-review adjustments in §6b are mandatory.**
2. **`/Users/pilawski/My_projects/skillsos/Design Docs Product/REVIEW-0.2.1-PRIORITIZED-IMPROVEMENTS.md`** — the audit that prompted 0.3.0. Read for context if a task's "why" is unclear.
3. **`/Users/pilawski/My_projects/skillsos/.review-tmp/`** directory — source research (`R1-workflow-pos.md`, `R2-pm-docs.md`, `R3-test-corpus.md`, audit findings `A-prompts.md` / `B-gaps.md` / `C-tests.md` / `D-collab.md`, external reviews `external/{gemini,codex}-review.md`, critical evaluation `external/EVALUATION.md`). Reference material — read only the parts relevant to the current task.
4. **`/Users/pilawski/.claude/CLAUDE.md`** — user's global rules (TDD, conventional commits, never destructive without approval, etc.). Always applies.

# Mission

Execute SDD-0.3.0 phase by phase, subagent-driven. Net change: **12 skills → 13 skills**, full grader rewrite, ~25 new test cases. Target: ship 0.3.0 in roughly 28-36 engineering days (multi-session work).

# Execution mode (locked)

- **Subagent-driven, task-by-task** — user's Q8 choice.
- Dispatch a fresh subagent per task using the Agent tool (`subagent_type: general-purpose` or specific GSD agent if available).
- Two-stage review between subagents: read the diff yourself before reporting "done"; check actual changes against acceptance criteria.
- **Phase boundary checkpoints** — at the end of each phase, summarize what shipped + commits made + what's next, then explicitly ask the user before starting the next phase.
- **Within a phase**, work autonomously through tasks unless you hit a blocker.

# Where to start

**Phase 1 — Foundation & Pin Decisions** (SDD §Phase 1). 5 tasks, ~0.5 day total. All low-risk preparation work.

Start by:
1. Reading SDD §0 (resolved decisions), §6b (external-review adjustments), and §Phase 1 in full.
2. Creating TodoWrite tasks for Phase 1's five subtasks (1.1-1.5).
3. Dispatching the first subagent for Task 1.1 (version pin).

# Hard gates (DO NOT VIOLATE)

These are sequencing constraints the SDD calls out. Treat as immovable:

1. **Task 2.6 (adapter routing) MUST land before Task 2.2 (delete master workflow).** A new Task 2.2a is the verification gate — ≥4/5 single-stage golden cases must route correctly through the new adapter before deletion. If routing fails, HALT Phase 2 and re-evaluate.

2. **Phase 3a (structural grader hardening) ships before 3b (content thresholds + LLM-judge).** Calibrate 3a against Claude 0.2.1 baseline (must hit 18/18) before starting 3b.

3. **Task 3.0 (YAML parser upgrade) is a hard prerequisite** for any nested expected-fixture work. The current `scripts/grade_artifact.py` parser is a homegrown YAML subset and does not handle nested structures. Do not write `min_content:` or `must_include_in_section:` blocks until Task 3.0 ships.

4. **Never delete a skill or schema without first running the cross-reference grep audit (Task 1.2).** The grep results live at `.review-tmp/phase1-grep-results.md`. Update each callsite in lockstep with the deletion.

5. **All commits use Conventional Commits** (`feat:`, `refactor:`, `chore:`, `test:`, `docs:`, `feat(pm-docs):`, etc.) — per CLAUDE.md.

# What is locked (do not redesign)

These are user decisions from Q1-Q8 in SDD §0. Do not re-open without explicit user approval:

- Version is **0.3.0** (single bundled release; no 0.2.2 stepping stone)
- **13 skills total** (drop pm-tooling + workflow-product-operating-system; add pm-roadmap + pm-metrics + pm-stakeholder-comms)
- pm-docs: **7 procedures** (PRD, decision-memo, spec-review, one-pager, RFC, internal-review-faq, postmortem)
- decision-memo supports **both narrative and bullet-log forms**
- postmortem: **product failures only** (Step 1 = SRE refusal contract)
- Adapter renamed to `product-skills` (backward-compat shim in Task 5.2b)
- skill-output-envelope schema **deleted**
- Canonical resume target for evidence-blocked workflows: **`pm-discovery`**

# External review accepted findings (already in SDD §6b)

17 review findings from Gemini + Codex have been incorporated. Notable items:
- Task 2.2a verification gate (prove routing before kill)
- Task 3.0 YAML parser upgrade
- Phase 3 split into 3a/3b
- Minimal LLM-judge (single dimension, advisory) pulled into 0.3.0
- Postmortem refusal contract (procedural, not just template disclaimer)
- pm-stakeholder-comms input contracts (audience/intent/asks/evidence)
- Catch-all rule in adapter routing
- Backward-compat shim for adapter rename
- Allowed-lifecycle-transitions table
- TDD unit-test specs on grader tasks

# User collaboration pattern

- The user runs in autonomous mode by default. Don't ask permission for small decisions — make the reasonable call and continue.
- Use AskUserQuestion **only** for: genuine blockers, decisions that contradict a locked decision, phase boundary checkpoints, or destructive operations not pre-authorized.
- **Brief updates** as you work: one sentence at start of task ("Starting Task 1.1 — pin version"), one sentence on result. The user reads the diff for details.
- **Never narrate internal deliberation.** State results.
- **End-of-phase summary**: 2-3 sentences. What shipped. What's next.
- If you discover an issue the SDD doesn't address: pause, decide if it's small (fix and document) or large (raise with user before continuing).

# Discipline (from user's CLAUDE.md)

- **TDD** for grader scripts (Phase 3) — write the failing test, run it, implement, run, commit. Bite-sized steps.
- **No destructive operations** (rm -rf, git reset --hard, force-push) without explicit user approval. CLAUDE.md says these are hook-blocked anyway.
- **No commits to main** — work on a branch. Branch name: `feature/0.3.0-execution` or per-phase branches like `feature/0.3.0-phase-1`.
- **Never modify auth/RLS** — not applicable here, but mentioned for completeness.
- **One logical change per commit.** Don't bundle refactor + feat.
- **Skill discipline:** when the user invokes a GSD skill or Superpowers skill, use it. Otherwise work straight.

# Tools you'll use

- **TodoWrite** (via the harness) — track phase task progress. Mark `in_progress` when starting, `completed` immediately when done.
- **Agent** — dispatch subagents for individual tasks. Per CLAUDE.md, never let multiple agents edit the same checkout concurrently. If you need parallelism, use git worktrees.
- **Read/Edit/Write/Bash** — direct file operations between subagent dispatches.
- **Grep/Glob** — finding callsites.
- **Context7 MCP** — if you need framework docs (Python, PyYAML, pytest, etc.).

# How to dispatch a task to a subagent

Pattern:

```
Agent({
  description: "<short description>",
  subagent_type: "general-purpose",
  prompt: `
You are executing a single task from the ProductSkills 0.3.0 SDD.

# Your task
[Task X.Y from the SDD — paste the relevant section verbatim]

# Files you need to read first
[List the SDD section + research file(s) that ground this task]

# Files you will modify/create/delete
[Specific paths from the SDD task]

# Acceptance criteria
[The "Done when" block from the SDD task]

# Constraints
- Read-only outside the listed file paths
- Use Conventional Commits for the final commit
- TDD if writing Python (write test first, watch fail, implement, watch pass)
- Report: files changed, commit hash, acceptance check results
  `
})
```

# When you hit a blocker

1. **Re-read** the SDD section for the current task — the answer is usually in the "Done when" or in §6b adjustments.
2. **Check the research files** (`R1`/`R2`/`R3`) — implementation detail often lives there.
3. **Check CLAUDE.md** for global rules.
4. **If still blocked**, use AskUserQuestion with a precise question. Don't dump status; ask one specific thing.

# What you do NOT do

- Do not re-design what's already designed. The SDD is locked.
- Do not "improve" the plan mid-execution without raising it explicitly.
- Do not ship Phase 2 before Phase 1 is complete and verified.
- Do not delete the master workflow before Task 2.2a passes.
- Do not write nested YAML expected-fixtures before Task 3.0 ships.
- Do not skip the post-task acceptance check (read the diff, verify against "Done when").
- Do not commit secrets, .env files, API keys, or credentials.

# Memory

The user has auto-memory at `/Users/pilawski/.claude/projects/-Users-pilawski-My-projects-skillsos/memory/MEMORY.md`. Read it at session start to load user preferences and project context. Update only for **durable cross-session** facts — not for task progress (use TodoWrite for that).

# Confirmation step before starting

When you load this prompt:
1. Confirm you've read the SDD-0.3.0.md (mention specifically that you've seen §0, §6b, and §Phase 1).
2. Confirm you understand the hard gates.
3. State your first action.
4. **Then begin Task 1.1.** Don't wait for further approval to start Phase 1 — the user has pre-authorized execution.

---

**You are ready to begin. Start with: read the SDD, confirm understanding in one paragraph, then start Phase 1 Task 1.1.**
