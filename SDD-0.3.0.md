# ProductSkills 0.3.0 — Software Design Document

> **Author:** Audit + research synthesis, 2026-05-28
> **Status:** APPROVED — ready to execute (subagent-driven, task-by-task)
> **Predecessor audit:** `REVIEW-0.2.1-PRIORITIZED-IMPROVEMENTS.md` (this repo root)
> **Source research:** `.review-tmp/{A-prompts,B-gaps,C-tests,D-collab,R1-workflow-pos,R2-pm-docs,R3-test-corpus}.md`

## 0. Resolved decisions (2026-05-28)

| # | Decision | Choice |
|---|----------|--------|
| Q1 | Version number | **0.3.0** |
| Q2 | Release shape | **Single bundled release** (no 0.2.2 stepping stone) |
| Q3 | Stakeholder updates | **Create `pm-stakeholder-comms` skill in 0.3.0** (not deferred) |
| Q4 | Adapter rename | **Rename to `product-skills`** |
| Q5 | Final skill count | **13 skills total** (drop 2: pm-tooling, workflow-pos; add 3: pm-roadmap, pm-metrics, pm-stakeholder-comms) |
| Q6 | Decision-memo form | **Both narrative + bullet-log forms** |
| Q7 | Postmortem scope | **Product failures only** (excludes ops/SRE incidents) |
| Q8 | Execution mode | **Subagent-driven, task-by-task** with phase-boundary checkpoints |

---

## 1. Goal

Ship ProductSkills 0.3.0 — a release that **(a) removes routing competition** by retiring two slots (`workflow-product-operating-system`, `pm-tooling`), **(b) rebuilds `pm-docs` to deliver on its description**, **(c) adds three high-leverage missing skills** (`pm-roadmap`, `pm-metrics`, `pm-stakeholder-comms`), and **(d) hardens the test grader** so it can distinguish substantive analysis from rubric-echo skeletons.

Net change: 12 skills → **13 skills**. The slot count is intentionally expanded by one because the three additions cover distinct high-frequency PM jobs (quarterly roadmap, metric tree design, weekly stakeholder comms) that the current pack does not cover well.

---

## 2. Architecture

**Skill set (12 → 13):**

| Slot | 0.2.1 | 0.3.0 | Change |
|------|-------|-------|--------|
| 1 | pm-discovery | pm-discovery | Sharpen description + add negative triggers (Phase 2.7) |
| 2 | pm-strategy | pm-strategy | Sharpen + absorb `market-brief` (from pm-docs MRD reroute) |
| 3 | pm-validation | pm-validation | Sharpen description |
| 4 | pm-design | pm-design | Sharpen description |
| 5 | pm-docs | pm-docs (rebuilt) | **7 procedures (was 3); 6 new templates; aligned description.** See R2. |
| 6 | pm-delivery | pm-delivery | Sharpen description; cite `pm-docs/spec-review` as universal quality gate |
| 7 | pm-growth | pm-growth | Collapse 3 stage-specific procs into one `funnel-stage-analysis.md`; add `experiment-readout.md` |
| 8 | pm-gtm | pm-gtm | Sharpen description; reclaim "launch readiness" / "post-launch metrics" triggers buried under retired master workflow |
| 9 | **pm-tooling** | **pm-roadmap** (NEW) | **DROP pm-tooling**; ADD pm-roadmap (intake triage, roadmap build, quarterly planning, dependency mapping) |
| 10 | **workflow-product-operating-system** | **pm-metrics** (NEW) | **DROP master workflow (R1 KILL)**; ADD pm-metrics (north-star, metric trees, guardrails, KPI review) |
| 11 | workflow-discovery-to-prd | workflow-discovery-to-prd | Absorb large-corpus-synthesis trigger; cite blocked-workflow schema |
| 12 | workflow-prd-to-linear-delivery | workflow-prd-to-linear-delivery | Absorb tool-safety semantics from pm-tooling |
| **13** | — | **pm-stakeholder-comms** (NEW) | Exec updates, status memos, decision memos for stakeholders, ask framing |

**Grader architecture (Layer 1 ships in 0.3.0):**

```
scripts/
  grade_artifact.py                       # existing — extended
  grade_artifact_payloads.py              # NEW — JSON extraction + schema validation
  grade_refusal.py                        # NEW — 6 negative deterministic contracts
  check_run_consistency.py                # NEW — cross-artifact invariants
  check_evidence_id_grounding.py          # NEW — cited IDs must be in fixtures
  check_handoff_chain.py                  # NEW — Phase A→B→C invariants
  grade_productskills_synthetic_e2e.py    # orchestrator — extended

evals/
  forbidden-phrases.yaml                  # NEW — global rubric-echo patterns
  refusals/*.yaml                         # NEW — 6 negative contracts
  expected/*.yaml                         # EXTENDED — min_content, required_json_payloads, must_include_in_section
```

LLM-as-judge layer ships in 0.4.0 (advisory).

**Adapter routing:**

The entry-classification table from the (retired) master workflow moves into every adapter's SKILL.md as a routing block, plus a new shared reference `references/routing/artifact-to-workflow.md`. The adapter becomes the router.

---

## 3. Tech Stack

- SKILL.md frontmatter + body (existing format, no host changes)
- JSON Schema 2020-12 (existing — extend with refusal envelope schema)
- Python 3.x for grader scripts (existing)
- YAML for expected fixtures and forbidden-phrases (existing — extended)
- Markdown for procedures, templates, references (existing)

No new runtime dependencies.

---

## 4. Decision summary (locked-in inputs to this SDD)

| Decision | Source | Rationale |
|---|---|---|
| Drop `pm-tooling` as a slot | User approval | Infrastructure, not a PM job. Safety semantics relocate into the two workflow skills. |
| Drop `workflow-product-operating-system` | R1 KILL @ 85% confidence | Zero distinct positive triggers; 6 of 7 capabilities mechanically relocatable; run-10 ~30 lines of distinct content. |
| Add `pm-roadmap` | Audit gap, user approval | Quarterly mandatory deliverable. No current home. |
| Add `pm-metrics` | Audit gap, user approval | North-star tree anchors every other artifact. Cited in `findings.md:64` as deferred gap. |
| Add `pm-stakeholder-comms` | User Q3 (Resolved) | Most-frequent under-served PM job. Becomes a first-class skill, not deferred. |
| Rebuild `pm-docs` (NOT dissolve) | User approval | Make procedures match description: PRD, decision-memo, spec-review, one-pager, RFC, FAQ, postmortem. |
| Decision-memo: both narrative + bullet-log forms | User Q6 (Resolved) | Two templates: `decision-memo.md` (narrative), `decision-log-entry.md` (3-5 line bullet form). Procedure selects based on user request. |
| Postmortem: product failures only | User Q7 (Resolved) | Excludes ops/SRE incidents (eng-owned). Feature underperforms, sunset, missed-scope. |
| Adapter rename: `product-operating-system` → `product-skills` | User Q4 (Resolved) | Aligns with package name; old name was tied to retired master workflow. |
| MRD → `pm-strategy/market-brief.md` | R2 | Market analysis is strategy work; pm-docs reviews via spec-review. |
| Engineering SDD: out of scope | R2 | Eng-owned. PRD + handoff schema is sufficient. |
| Delete `skills/.../skill-output-envelope.schema.json` | R2 | "Universal" envelope cited by exactly one skill. Artifact-specific schemas remain. |
| Canonical resume target for evidence-blocked: `pm-discovery` | R3 (G8) | Pins divergence flagged in C-tests.md. `pm-validation` acceptable when gap is "validation needed," not "discovery needed." |
| Two-layer grader: deterministic now, LLM-judge in 0.4.0 | R3 | Keeps CI fast and reproducible; advisory layer deferred. |

---

## 5. Out of scope (deferred to 0.4.0+)

- LLM-as-judge advisory layer (`scripts/judge_artifact_llm.py`)
- Cross-runner invariant checks in CI (advisory only in 0.3.0)
- Engineering SDD authoring (eng-owned)
- Customer-facing FAQ / help docs (out of PM scope)
- Ops/SRE incident postmortems (eng/SRE-owned per Q7)

---

## 6. Risks

| # | Risk | Mitigation |
|---|------|------------|
| R1 | Adapter routing block doesn't reproduce master-workflow value | Phase 5 verification: re-run all 5 single-stage `product-os-*-reentry` golden cases against the new adapter routing. If any case routes wrong, halt 0.3.0 and re-evaluate KILL decision. |
| R2 | Grader hardening false-positives Claude artifacts | Calibration in Phase 3.10. Every threshold is derived from Claude 0.2.1 outputs minus margin. Calibration step must show Claude 18/18 PASS before grader ships. |
| R3 | pm-docs expansion (4 new procedures) introduces unfocused scope | Each new procedure has explicit "Done when" + at least one acceptance assertion in the grader. Cross-check description against procedures list before merge. |
| R4 | Routing-line in adapters competes with existing host-platform routing | Adapter changes are additive (routing block + entry table); they do not change the `name:` field or invocation pattern. Host platform routes to the adapter; adapter routes to the workflow. |
| R5 | Removing `pm-tooling` slot loses its "rules-only-skill" pattern | Replicate the `## Rules` block inside `workflow-prd-to-linear-delivery/SKILL.md` body so the safety semantics remain visible. |
| R6 | Three net-new skills (pm-roadmap, pm-metrics, pm-stakeholder-comms) have no test history | Each ships with ≥3 grader-checked test cases + ≥1 positive trigger test + ≥1 negative. Calibration thresholds for these skills are conservative (lower than mature skills) in 0.3.0 and tightened in 0.3.1 once Claude baselines accumulate. |
| R7 | Schema deletion (`skill-output-envelope`) breaks something external | Audit (`grep -rn 'skill-output-envelope' .`) before deletion. Phase 1.3. |
| R8 | Adapter rename (`product-operating-system` → `product-skills`) breaks existing installs | Phase 5.1 installer walkthrough; CHANGELOG callout; `install.sh` handles legacy adapter names with a fallback for ≥1 minor release. |
| R9 | 13 skills create more trigger competition | Each new skill has explicit negative triggers (Phase 2.7). Phase 4.4 router disambiguation tests cover boundary cases including new skills. |

---

## 6b. External-review adjustments (Gemini + Codex, 2026-05-28)

Two independent external reviewers (Gemini and Codex CLIs, read-only) reviewed the SDD against the package, research, and 0.2.1 test data. Their findings + the critical evaluation are in `.review-tmp/external/EVALUATION.md`. The accepted changes are baked into the phase tasks below. Top adjustments:

| # | Adjustment | Where it lands |
|---|------------|----------------|
| A1 | **Prove adapter routing BEFORE deleting master workflow** — both reviewers' strongest catch. The 5 single-stage golden cases must route correctly through the new adapter routing block before `workflow-product-operating-system` is deleted. | Task 2.6 (adapter routing) is re-sequenced BEFORE Task 2.2 (kill master workflow) with an explicit verification gate (Task 2.2a). |
| A2 | **Split Phase 3 grader hardening into 3a (structural) + 3b (thresholds)** — ship JSON validation, refusal contracts, and forbidden-phrase scan first (most defensible). Calibrate. Then ship min-content thresholds and section-anchored prose. | Phase 3 reorganized into 3a, 3b. |
| A3 | **Upgrade grader YAML parser BEFORE adding nested fields** — current `scripts/grade_artifact.py` parser doesn't handle nested YAML. SDD must not assume `min_content:` and `must_include_in_section:` are drop-in extensions. | New Task 3.0 (parser upgrade). |
| A4 | **Pull minimal LLM-judge layer into 0.3.0 as advisory** — single dimension ("concrete reasoning vs methodology echo"), 1-4 score, reported but doesn't flip pass/fail. Full 5-dimension judge still 0.4.0. | New Task 3b.X. |
| A5 | **Add explicit backward-compat task for the adapter rename** | New Task 5.2b. |
| A6 | **Migrate `evals/forward-tests/phase8-forward-tests.json` explicitly** — references pm-tooling and workflow-pos throughout. | Expanded Task 4.6. |
| A7 | **Add allowed-lifecycle-transitions table** for re-entry tests (state machine, not just schemas). | Expanded Task 4.2 + `evals/allowed-transitions.yaml`. |
| A8 | **Postmortem refuses SRE incidents at the procedure level**, not only in template disclaimer. | `procedures/postmortem.md` Step 1 = refusal contract. |
| A9 | **Adapter routing rule in `description:` field**, not only in body — some hosts route on description first. + add catch-all rule for unclassified inputs. | Task 2.6 updated. |
| A10 | **pm-stakeholder-comms gets hard PM-specific input contracts** (audience map, intent enum, decision/ask/risk) — prevents generic memo-writing. | Task 2.4b procedures expanded. |
| A11 | **Rename `procedures/faq.md` → `procedures/internal-review-faq.md`** — disambiguates from customer FAQ and pm-gtm launch FAQ. | Task 2.3 updated. |
| A12 | **Add router-disambiguation test** for pm-docs/decision-memo vs pm-stakeholder-comms/decision-comms (same data, different framing). | Task 4.4 expanded. |
| A13 | **Make `Skill: <name>` artifact declaration conditional** on `provenance_required: true` in expected fixtures (default false). | G6 grader rule softened. |
| A14 | **Drop the global 600-word floor** — keep only per-artifact structural counts. | G2 thresholds table updated. |
| A15 | **TDD for grader modules**: each Phase 3 task lists concrete pytest cases. | All Phase 3 tasks. |
| A16 | **Safety rules in workflow SKILL.md**: 4-line summary + canonical reference pointer (resolves Gemini-vs-Codex tension). | Task 2.1 updated. |

**Rejected reviewer suggestions** (documented for traceability):
- Drop FAQ + postmortem from pm-docs (Gemini G6): rejected — both are canonical PM artifacts; user resolved Q7.
- Defer pm-stakeholder-comms (Codex C-16): rejected — contradicts user Q3.
- Corpus-first sequencing (Gemini G-7): rejected — 0.2.1 corpus is sufficient calibration anchor; Codex's 3a/3b split addresses the underlying concern.

---

## 7. Phases

Phases are sequenced; later phases depend on earlier phases. Within a phase, tasks are mostly parallelizable except where noted. Each task lists: files, change description, acceptance criteria.

**Suggested commits per phase: 1 PR per phase, multiple conventional commits inside.**

---

## Phase 1 — Foundation & Pin Decisions

**Goal:** Lock in version, registry, and irreversible deletions. After Phase 1, every downstream task has unambiguous targets.

### Task 1.1 — Pin version 0.3.0 (or user-corrected number)

**Files:**
- Modify: `VERSION`
- Modify: `package.json`
- Modify: `registry.json:3` (the `version` field)
- Modify: `package.yaml`

**Change:** Write `0.3.0` to `VERSION`. Update `version` field in `package.json`, `package.yaml`, `registry.json`. No code change.

**Done when:** All four files agree on the version string. CI version check (if any) passes.

---

### Task 1.2 — Cross-reference audit (pre-deletion safety net)

**Files:** Read-only; no modifications.

**Change:** Run these greps and record results in `.review-tmp/phase1-grep-results.md`:

```
grep -rn "skill-output-envelope" .
grep -rn "pm-tooling" .
grep -rn "workflow-product-operating-system" .
grep -rn "decision-log" .
grep -rn "product-operating-system-handoff" .
grep -rn "product-operating-system-contract" .
```

**Done when:** A file at `.review-tmp/phase1-grep-results.md` lists every callsite. Phase 2 tasks use this list to update each callsite in lockstep with the deletions.

---

### Task 1.3 — Delete `skill-output-envelope` schema and references

**Files:**
- Delete: `schemas/skill-output-envelope.schema.json`
- Modify: `skills/pm-docs/SKILL.md` — remove the line referencing it
- Modify: any other file flagged in Task 1.2's grep results

**Change:** Per R2, the universal envelope is cited only by `pm-docs`. Delete it. Replace nothing.

**Done when:** `grep -rn "skill-output-envelope" .` returns zero matches. `pm-docs/SKILL.md` no longer references the schema.

**Commit:** `chore: remove unused skill-output-envelope schema`

---

### Task 1.4 — Update `registry.json`

**Files:**
- Modify: `registry.json`

**Change:**
- Remove the `pm-tooling` entry from `skills[]`
- Remove the `workflow-product-operating-system` entry from `skills[]`
- Add: `{"id": "pm-roadmap", "path": "skills/pm-roadmap", "type": "family", "domain": "roadmap"}`
- Add: `{"id": "pm-metrics", "path": "skills/pm-metrics", "type": "family", "domain": "metrics"}`
- Add: `{"id": "pm-stakeholder-comms", "path": "skills/pm-stakeholder-comms", "type": "family", "domain": "comms"}`
- Remove `pm-tooling` from the `pm-delivery-tooling` collection; rename collection to `pm-delivery`
- Remove `workflow-product-operating-system` from all three collections (`pm-core`, `pm-delivery-tooling`, `pm-growth-gtm`)
- Add `pm-roadmap` to `pm-core` collection
- Add `pm-metrics` to `pm-core` and `pm-growth-gtm` collections
- Add `pm-stakeholder-comms` to `pm-core` and `pm-growth-gtm` collections

**Done when:** Registry is valid JSON; the 3 new skills are present (13 total); deleted skills are absent; collections are coherent.

---

### Task 1.5 — Pin canonical resume-target convention

**Files:**
- Create or modify: `references/workflows/workflow-lifecycle-statuses.md` — add a "Canonical resume targets" section
- Modify: `references/methods/evidence-grading.md` if needed

**Change:** Document explicitly: "For a workflow that blocks due to missing evidence, the canonical resume target is `pm-discovery`. `pm-validation` is acceptable when the gap is specifically a validation gap (testable hypothesis exists but lacks test method/audience), not an evidence gap. `voc-synthesis` is a procedure name, not a resume target; do not use it."

**Done when:** The document contains the canonical rule and is cited from the two surviving workflow skills' guardrails.

---

## Phase 2 — Restructure Skills

**Goal:** Land the architectural changes. After Phase 2, the new skill set is in place and the deleted skills are removed.

### Task 2.1 — Remove `pm-tooling` slot; relocate procedures

**Files to MODIFY:**
- Delete: `skills/pm-tooling/` (entire directory)
- Create: `references/mcp/dry-run-preview.md` — consolidates `workspace-bootstrap.md`, `notion-preview.md`, `linear-preview.md`, `tool-id-resolution.md`, `external-id-map.md` into one procedure (per audit Tier-2 #14: collapse 5 procedures into 1-2)
- Optionally create: `references/mcp/id-resolution.md` as a separate doc if the consolidation is too dense in one file
- Modify: `skills/workflow-prd-to-linear-delivery/SKILL.md` — add a 4-line `## Safety summary` block listing the core rules (preview-before-write, explicit confirmation, idempotency-key required for writes, never claim rollback) + explicit citation: "**Canonical safety contract:** see `references/mcp/dry-run-preview.md`. If this summary and the reference doc disagree, the reference doc wins." (Per external-review A16: visible summary + canonical reference resolves the Gemini-vs-Codex tension on safety rule duplication.)
- Modify: `skills/workflow-prd-to-linear-delivery/procedures/prd-to-linear-delivery.md` — references to `pm-tooling/procedures/X.md` become `references/mcp/dry-run-preview.md` citations
- Modify: `skills/workflow-discovery-to-prd/procedures/discovery-to-prd.md` — same citation change for Notion preview path
- Update every callsite from Task 1.2 grep result

**Done when:**
- `skills/pm-tooling/` does not exist
- `grep -rn "pm-tooling" .` returns zero (except in CHANGELOG, archived docs)
- The 5 safety rules survive in `workflow-prd-to-linear-delivery/SKILL.md`
- `references/mcp/dry-run-preview.md` exists and is cited from both workflows

**Commit:** `refactor: remove pm-tooling slot; relocate safety semantics into workflows and references/mcp/`

---

### Task 2.2 — Remove `workflow-product-operating-system`; relocate capabilities

**Pre-condition (HARD GATE):** Task 2.6 (adapter routing block) must land FIRST. Task 2.2a (verification of adapter routing against 5 single-stage golden cases) must PASS before Task 2.2 begins. Do not delete the master workflow without verified routing behavior — both external reviewers flagged this as the highest-risk sequencing dependency.

**Files to MODIFY:**
- Delete: `skills/workflow-product-operating-system/` (entire directory)
- Delete: `references/workflows/product-operating-system-contract.md`
- Rename: `schemas/product-operating-system-handoff.schema.json` → `schemas/workflow-chain-handoff.schema.json`; generalize the `workflow_id` const (allow either narrower workflow OR a chained sequence)
- Modify: `references/workflows/workflow-lifecycle-statuses.md` — already shared; ensure it's cited from both narrower workflows' procedures
- Modify: `skills/workflow-discovery-to-prd/procedures/discovery-to-prd.md` — strengthen Step 2 (VoC synthesis) with the large-corpus-synthesis trigger that previously lived in the master workflow
- Modify: `skills/workflow-discovery-to-prd/SKILL.md` and `skills/workflow-prd-to-linear-delivery/SKILL.md` — guardrails surface re-entry rules at trigger time (the rules already exist in their contracts; promote one line into the SKILL.md)
- Modify: `skills/pm-gtm/SKILL.md` — claim "launch readiness" as a primary trigger (this was buried inside the master workflow); do NOT add stakeholder-update (pm-stakeholder-comms owns it per Task 2.5b)
- Modify: `skills/pm-growth/SKILL.md` — claim "post-launch metrics" / "learning loop" as primary triggers; add the post-launch-feeds-discovery rule to guardrails
- Update every callsite from Task 1.2 grep result

**Files to DELETE in docs/:**
- `docs/HOW_TO_USE_PRODUCT_OS_WORKFLOW.md` → rename to `docs/HOW_TO_ROUTE_PRODUCT_WORK.md` and convert content to a routing decision table
- `docs/PRODUCT_OS_WORKFLOW_DOCUMENTATION.md` → archive (move under `docs/_archive/`)
- `docs/PRODUCT_OS_WORKFLOW_TESTING_PLAN.md`, `OPINIONATED_E2E_WORKFLOW_*` → archive

**Done when:**
- `skills/workflow-product-operating-system/` does not exist
- `grep -rn "workflow-product-operating-system" .` returns zero except in CHANGELOG and `_archive/`
- The 6 master-workflow trigger tests in `evals/trigger-tests.yaml:42-73` are removed or re-targeted (see Phase 4)
- The 6 golden cases under `evals/golden-cases/product-os-*` are removed or re-targeted (see Phase 4)
- The new `schemas/workflow-chain-handoff.schema.json` validates against the same shape

**Commit:** `refactor: remove workflow-product-operating-system; promote routing to adapter layer`

---

### Task 2.3 — Rebuild `pm-docs`

**Files to ADD:**
1. `skills/pm-docs/procedures/one-pager.md`
2. `skills/pm-docs/procedures/rfc.md`
3. `skills/pm-docs/procedures/internal-review-faq.md` — **renamed from `faq.md`** (per A11) to disambiguate from customer FAQ (out of scope) and pm-gtm launch FAQ
4. `skills/pm-docs/procedures/postmortem.md` — **Step 1 = refusal contract** (per A8): "If the request mentions outage, downtime, SLA, SLO, auth failure, latency regression, on-call, infrastructure incident, security breach, or any SRE/ops domain, refuse and route to engineering-owned postmortem templates. Do not produce a product postmortem for an ops incident." This is procedural, not just a template disclaimer.
5. `templates/one-pager.md`
6. `templates/rfc.md`
7. `templates/internal-review-faq.md` — renamed from `templates/faq.md`
8. `templates/postmortem.md` — **product failures only** (per Q7); explicit "Out of scope: ops/SRE incidents — see eng-owned templates" line at top (template disclaimer; procedure refusal is the load-bearing check)
9. `templates/decision-memo.md` — **narrative form** (per Q6)
10. `templates/decision-log-entry.md` — **bullet form**, 3-5 lines per decision (per Q6)

**Files to RENAME:**
- `skills/pm-docs/procedures/decision-log.md` → `skills/pm-docs/procedures/decision-memo.md`

**Decision-memo procedure handles BOTH forms (per Q6):**
The single `decision-memo.md` procedure has a `## Form selection` block: narrative form (default — produces a memo per decision using `templates/decision-memo.md`) OR bullet log entry (produces a 3-5 line entry to append to a running log using `templates/decision-log-entry.md`). Procedure picks based on user request keywords ("memo," "ADR," "record this decision" → narrative; "log entry," "running log," "quick decision" → bullet).

**Files to MODIFY:**
- `skills/pm-docs/SKILL.md` — replace `description:` per R2 §Updated SKILL.md description; rewrite `## Core Procedures` to list all 7; add `## Method Selection` block (model on `pm-strategy`); remove the deleted envelope schema reference
- `skills/pm-docs/procedures/prd.md` — flesh out per Tier-1 #6; add `## Done When` (5 acceptance conditions)
- `skills/pm-docs/procedures/spec-review.md` — add `## Done When`; add severity rubric (blocking/improvement/nit); note "MAY be cited by other skills as the universal quality gate"
- `templates/prd.md` — flesh out with per-section prose guidance, modeled on `templates/research-plan.md`

**Procedure templates:** See R2 §Proposed procedures for the exact `## Done When` block per procedure. Each new procedure follows the same shape:

```markdown
# <Procedure Name>

## Goal
<one sentence>

## Input expected
<list>

## Output produced
<filled template, schema if applicable>

## Steps
1. ...
2. ...

## Links
- Template: `../../../templates/<name>.md`
- Reference: `../../../references/...`

## Done when
- <acceptance condition 1>
- <acceptance condition 2>
- ...
```

**Done when:**
- All 9 new files exist with non-stub content
- The renamed decision-memo procedure works (references updated everywhere)
- `pm-docs/SKILL.md` has 7 procedures listed and a description that names every one + negative triggers per R2

**Commits (3):**
1. `feat(pm-docs): add one-pager, rfc, faq, postmortem procedures and templates`
2. `refactor(pm-docs): rename decision-log to decision-memo; add decision-memo template`
3. `docs(pm-docs): flesh out prd template and procedure; rewrite description with negative triggers`

---

### Task 2.4 — Add `pm-roadmap` skill

**Files to ADD:**
- `skills/pm-roadmap/SKILL.md`
- `skills/pm-roadmap/procedures/roadmap-build.md` — sequence chosen bets into themes with confidence bands
- `skills/pm-roadmap/procedures/intake-triage.md` — feature-request intake → routing (this is the "feature-requests to roadmap" hero workflow named in the design doc but never built)
- `skills/pm-roadmap/procedures/quarterly-planning.md` — quarterly bet selection from prioritized backlog
- `skills/pm-roadmap/procedures/dependency-mapping.md` — explicit dependency identification across initiatives
- `templates/roadmap.md` — themes × time, with confidence band column
- `templates/intake-triage.md` — feature-request triage decision
- `references/methods/roadmap-methods.md` — Now-Next-Later, theme-based, time-sliced, capacity-aware

**Boundary rules (encoded in SKILL.md description with negative triggers):**

- pm-strategy chooses bets (RICE/WSJF/etc) → pm-roadmap sequences chosen bets
- pm-roadmap is the presentable artifact; pm-strategy is the decision method
- Do NOT use pm-roadmap for individual feature scoping (use pm-discovery or pm-docs)

**SKILL.md description (draft):**

> Sequence chosen product bets into a roadmap artifact — themes, time slices, capacity envelopes, dependencies, and confidence bands. Use when the user asks to build a roadmap, plan a quarter, triage a feature-request backlog, or map cross-initiative dependencies. Do not use for choosing which bets to make (route to pm-strategy/prioritization) or for individual feature scoping (route to pm-discovery or pm-docs).

**Done when:**
- All files exist with non-stub content (each procedure has Goal / Input / Output / Steps / Done When)
- SKILL.md description names every procedure and has ≥1 negative trigger
- Registry includes the new skill (Task 1.4)

**Commit:** `feat(pm-roadmap): add pm-roadmap skill — roadmap, intake-triage, quarterly planning, dependency mapping`

---

### Task 2.4b — Add `pm-stakeholder-comms` skill (NEW per Q3)

**Files to ADD:**
- `skills/pm-stakeholder-comms/SKILL.md`
- `skills/pm-stakeholder-comms/procedures/exec-update.md` — exec/leadership status memo
- `skills/pm-stakeholder-comms/procedures/status-memo.md` — recurring product status (weekly/biweekly)
- `skills/pm-stakeholder-comms/procedures/ask-framing.md` — structure a single "ask" of a stakeholder (decision needed, escalation, resource request)
- `skills/pm-stakeholder-comms/procedures/decision-comms.md` — communicate a decision *after it's made* (different from `pm-docs/decision-memo` which records it for posterity; this skill socializes it)

**Required structured inputs per procedure (per A10 — prevents generic memo-writing):**

Each procedure declares an `## Input expected` block with these MANDATORY fields:
- `audience: {tier: exec|lead|peer|board, function: eng|gtm|design|finance|legal|cs, decision_authority: yes|no}`
- `intent: ask | status | escalation | fyi | decision-comms`
- `key_message: <single sentence — the BLUF>`
- `risks_to_surface: [<list>]` (allowed to be empty for `fyi`)
- `decisions_or_asks: [<list>]` (required for `ask` / `escalation` / `decision-comms`; can be empty for `status` / `fyi`)
- `evidence_anchors: [<INT-/SUP-/SALES-/...>]` (required when claims are made)
- `next_action: <if any, with owner + date>`

Procedure refuses to produce output if `audience.tier` or `intent` is missing — this is what distinguishes PM stakeholder-comms from generic memo-writing.
- `templates/exec-update.md`
- `templates/status-memo.md`
- `templates/ask-framing.md`
- `templates/decision-comms.md`
- `references/methods/stakeholder-comms.md` — audience-first framing, BLUF, ask/risk/decision balance, tone calibration by audience tier

**Boundary rules (encoded in SKILL.md description with negative triggers):**

- pm-docs writes durable artifacts FOR THE RECORD; pm-stakeholder-comms writes socialization memos FOR AUDIENCES
- A decision-memo (pm-docs) is for the audit trail; a decision-comms message (pm-stakeholder-comms) is to inform the team and stakeholders the decision happened
- pm-gtm owns customer-facing launch comms; pm-stakeholder-comms owns internal stakeholder comms (exec, eng, GTM peers, board)
- Do NOT use pm-stakeholder-comms for PRDs (pm-docs), customer-facing release notes (pm-gtm), or experiment writeups (pm-growth/experiment-readout)

**SKILL.md description (draft):**

> Author internal stakeholder communications — exec/leadership updates, recurring product status memos, ask framings for cross-functional decisions, and post-decision socialization. Use when the user asks to write a status update, exec memo, ask doc, or to communicate a decision to a team or leadership audience. Do not use for durable record-keeping (route to pm-docs/decision-memo), customer-facing release notes or launch comms (route to pm-gtm), or product specs/RFCs (route to pm-docs).

**Done when:**
- All files exist with non-stub content (each procedure has Goal / Input / Output / Steps / Done When)
- SKILL.md description names every procedure and has ≥2 negative triggers
- Registry includes the new skill (Task 1.4)
- pm-docs SKILL.md description includes `pm-stakeholder-comms` as a negative trigger (route stakeholder updates here)

**Commit:** `feat(pm-stakeholder-comms): add pm-stakeholder-comms skill — exec updates, status memos, ask framing, decision comms`

---

### Task 2.5 — Add `pm-metrics` skill

**Files to ADD:**
- `skills/pm-metrics/SKILL.md`
- `skills/pm-metrics/procedures/north-star-design.md` — choose a north-star, define its inputs, ensure measurability
- `skills/pm-metrics/procedures/metric-tree.md` — decompose north-star into input metrics with explicit formulas
- `skills/pm-metrics/procedures/guardrail-design.md` — define guardrails per metric (don't move A without watching B)
- `skills/pm-metrics/procedures/kpi-review.md` — review existing KPI definitions for measurability + tractability
- `templates/north-star.md`
- `templates/metric-tree.md`
- `templates/guardrails.md`
- `references/methods/metric-design.md` — north-star principles, leading-vs-lagging, input-output, common pitfalls

**Boundary rules:**

- pm-metrics designs the tree → pm-growth uses the tree to find leverage
- PRD "success metrics" sections cite the tree (pm-metrics may be invoked as a sub-procedure of pm-docs/prd when metrics are weak)
- Do NOT use pm-metrics for running experiments (route to pm-growth or pm-validation)

**SKILL.md description (draft):**

> Design product metrics that anchor decisions — north-star selection, metric trees, input/output decomposition, guardrails, KPI review. Use when the user asks to choose a north-star metric, decompose a goal into measurable inputs, define guardrails, or review existing KPI definitions for measurability. Do not use for running an experiment against a metric (route to pm-growth or pm-validation) or for diagnosing growth bottlenecks (route to pm-growth/growth-loop-diagnosis).

**Done when:** Same shape as Task 2.4.

**Commit:** `feat(pm-metrics): add pm-metrics skill — north-star, metric trees, guardrails, KPI review`

---

### Task 2.6 — Update adapters with routing block (replaces the master workflow's role)

**Sequencing:** This task lands BEFORE Task 2.2 (kill master workflow). Verification gate is Task 2.2a.

**Files to MODIFY:**
- `adapters/claude/SKILL.md`
- `adapters/codex/SKILL.md`
- `adapters/codex/AGENTS.md`
- `adapters/cursor/product-operating-system.mdc` — also rename to `adapters/cursor/product-skills.mdc`
- `adapters/gemini/GEMINI.md`
- `adapters/gemini/extension/GEMINI.md`

**Files to ADD:**
- `references/routing/artifact-to-workflow.md` — the entry-classification table from the retired master workflow procedure, lifted as a shared reference

**Change per adapter:** Add a `## Routing` block to each adapter SKILL.md (or equivalent), containing:

1. **In the `description:` field (per A9):** a one-sentence routing rule — "Routes product work to the right skill/workflow based on input artifact type. See body for the routing table." This is critical because some hosts route primarily on description, not body.
2. **In the body:** The 12-row entry-classification table (artifact type → entry status → recommended workflow/skill)
3. **In the body:** Explicit "If the input is X, invoke skill Y" rules (≥4 rules covering the most common cases)
4. **Catch-all rule (per A9):** "If the input doesn't clearly match any row, ask the user to clarify intent and offer 2-3 most likely workflows. Do not silently pick."
5. A pointer to `references/routing/artifact-to-workflow.md` for the full table

**Adapter SKILL.md `name:` change:** the Claude/Codex adapter `name: product-operating-system` becomes `name: product-skills` (the package name in `registry.json`). Backward-compat handled in Task 5.2b — installer recognizes both old and new names for one minor release.

**Done when:**
- All 5 adapter files have a `## Routing` block citing the new shared reference
- The 12-row table exists in `references/routing/artifact-to-workflow.md`
- Adapter rename does not break installer (verify with `install.sh` walkthrough)
- The 5 single-stage golden cases from the (retired) master workflow route correctly through the adapter to the narrower workflow (verified in Phase 5)

**Commit:** `feat(adapters): add routing block; rename to product-skills`

---

### Task 2.2a — Verify adapter routing against single-stage golden cases (HARD GATE before Task 2.2)

**Pre-condition:** Task 2.6 complete (adapter routing block in place).

**Process:**
1. Take the 5 single-stage golden cases from the (still-present) master workflow: `evals/golden-cases/product-os-approved-prd-reentry.md`, `product-os-rough-prd-reentry.md`, `product-os-launch-readiness-reentry.md`, `product-os-no-evidence-blocked.md`, `product-os-post-launch-learning.md`.
2. Run each prompt against an adapter-using runtime (Claude is the calibration target). Do NOT invoke the master workflow directly; let the adapter route.
3. Observe which skill the adapter routes to.
4. Required outcome:
   - `product-os-approved-prd-reentry` → routes to `workflow-prd-to-linear-delivery`
   - `product-os-rough-prd-reentry` → routes to `workflow-discovery-to-prd`
   - `product-os-launch-readiness-reentry` → routes to `pm-gtm`
   - `product-os-no-evidence-blocked` → routes to `workflow-discovery-to-prd` (returns `decision_status: blocked`)
   - `product-os-post-launch-learning` → routes to `pm-growth` or `pm-gtm`

**Acceptance:** ≥4 of 5 cases route as expected. The 1 case that may legitimately diverge is `product-os-full-happy-path` (multi-stage chain — covered by Task 4.3 handoff chain).

**Done when:** Routing report committed at `.review-tmp/phase2-routing-verification.md`. Each of the 5 cases has: input prompt summary, observed routed skill, expected, PASS/FAIL.

**Failure mode:** If verification fails on ≥2 cases, **HALT Phase 2**, re-evaluate the kill decision (R1's 85% confidence assumed routing would work). Re-tune the adapter routing block or document the cases that need to remain in the master workflow.

**Commit:** `test: verify adapter routing reproduces master-workflow routing on single-stage cases`

---

### Task 2.7 — Rewrite all 13 SKILL.md `description:` fields

**Files to MODIFY:** every `skills/*/SKILL.md` in the 0.3.0 set (12 total after restructure).

**Change pattern (apply to every skill):**

Replace the existing `description:` with the structure:

```
description: <one scope sentence>. <Methods/artifact list — short, no longer than 1 line>. Use when the user asks to <positive triggers, exhaustive against the procedures>. Do not use for <negative trigger 1 — route to <skill>>; <negative trigger 2 — route to <skill>>.
```

Per-skill descriptions to write — exact text in R2 for `pm-docs`; for the other 11, follow the same pattern with at least one negative trigger per skill.

**Done when:**
- Each `description:` is ≤80 words
- Each has ≥1 negative trigger naming the nearest neighbor
- Framework/method keyword piles have been moved into a `## Methods Covered` body section
- `grep -L "Do not use" "Design Docs Product/skills/*/SKILL.md"` returns zero (every skill has a "Do not use" line)

**Commit:** `refactor: rewrite all SKILL.md descriptions with negative triggers; move keyword piles to body`

---

### Task 2.8 — Add `## Done When` blocks to every leaf procedure

**Files to MODIFY:** every `skills/*/procedures/*.md` (~40-50 files).

**Change:** Each leaf procedure gets a `## Done When` block with 3-5 concrete acceptance conditions. These replace the current one-line "Output" pointer.

**Template:**
```markdown
## Done when
- <condition 1: a structural check, e.g., "Every required section is non-empty OR explicitly marked open question">
- <condition 2: an evidence check, e.g., "≥4 evidence IDs cited across ≥2 source types">
- <condition 3: a quality check, e.g., "No claim asserts a fact without a cited source">
- <condition 4: a stop-rule check, e.g., "When evidence is missing, output is a research plan, not a PRD">
```

Acceptance conditions are calibrated against R3's per-skill threshold table (R3 §Minimum-content thresholds).

**Done when:** Every leaf procedure has a `## Done when` block. The grader (Phase 3) can cross-reference these conditions when applying min-content thresholds.

**Commit:** `docs: add Done When acceptance blocks to every leaf procedure`

---

### Task 2.9 — Wire orphan schemas next to their templates

**Files to MODIFY:**
- `skills/workflow-discovery-to-prd/procedures/discovery-to-prd.md` — cite `schemas/blocked-workflow.schema.json` in the Blocked State / Fallbacks section
- `skills/workflow-prd-to-linear-delivery/procedures/prd-to-linear-delivery.md` — same
- `skills/pm-gtm/procedures/launch-readiness.md` — cite `schemas/launch-readiness-gate.schema.json`
- `skills/pm-growth/procedures/<post-launch-related-proc>.md` — cite `schemas/post-launch-learning.schema.json`

**Schema correction (`schemas/launch-readiness-gate.schema.json`):**

Per D-collab.md, the template has an `approval_gate` field that the schema lacks. Add it to the schema OR remove from the template. Decision: add to schema as optional with enum `[pending, granted, rejected]`.

**Done when:** Every artifact-producing procedure references the corresponding schema (where one exists). No schema in `schemas/` is referenced by zero skills (except the eval-format ones: `forward-test-suite`, `tool-safety-fixture`).

**Commit:** `docs: wire orphan schemas to their producing procedures`

---

### Task 2.10 — Add `allowed-tools:` frontmatter

**Files to MODIFY:** every `skills/*/SKILL.md` in the 0.3.0 set.

**Change:** Add `allowed-tools:` frontmatter to each skill. Examples:

- `pm-discovery`: `[Read, Write, Edit, Grep, Glob]` (file ops only)
- `pm-strategy`, `pm-validation`, `pm-design`, `pm-docs`, `pm-delivery`, `pm-growth`, `pm-gtm`, `pm-roadmap`, `pm-metrics`: same — file ops only
- `workflow-discovery-to-prd`: `[Read, Write, Edit, Grep, Glob]` + MCP read tools (Notion fetch for evidence)
- `workflow-prd-to-linear-delivery`: `[Read, Write, Edit, Grep, Glob]` + Notion + Linear MCP tools (only mcp__notion__*, mcp__linear__* — NO Bash)

**Done when:** Every SKILL.md has an `allowed-tools:` line. No skill has `Bash` unless explicitly justified.

**Commit:** `feat: add allowed-tools frontmatter to constrain tool access per skill`

---

### Task 2.11 — Collapse `pm-growth` procedural redundancy

**Files to MODIFY:**
- Delete: `skills/pm-growth/procedures/activation-analysis.md`
- Delete: `skills/pm-growth/procedures/retention-analysis.md`
- Delete: `skills/pm-growth/procedures/monetization-analysis.md`
- Add: `skills/pm-growth/procedures/funnel-stage-analysis.md` — parameterized by stage (activation / retention / monetization). Three "How to Apply" subsections instead of three files.
- Add: `skills/pm-growth/procedures/experiment-readout.md` (per audit gap #7) — post-experiment readout: what we learned, what changes, what's next
- Modify: `skills/pm-growth/SKILL.md` — add `## Method Selection` block (modeled on `pm-strategy`) naming when to use `growth-loop-diagnosis` vs `funnel-stage-analysis(stage)` vs `lifecycle-experiment` vs `experiment-readout`

**Done when:**
- 3 old procedure files removed
- 2 new procedure files exist with non-stub content
- SKILL.md has explicit method selection block

**Commit:** `refactor(pm-growth): collapse stage-specific procedures into funnel-stage-analysis; add experiment-readout`

---

## Phase 3 — Grader Hardening

**Goal:** Make the test suite catch substance failures, not just structure failures. After Phase 3, the grader cannot be passed by rubric-echo skeletons.

Phase 3 depends on Phase 2 (skill structure must be locked before calibrating thresholds against it).

**Per A2 (external review): split into 3a (structural — JSON, refusal contracts, forbidden phrases — most defensible, ship first) and 3b (content thresholds, section-anchored prose, declaration extraction — ship after 3a calibration succeeds).**

### Task 3.0 — Upgrade grader YAML parser (HARD PREREQUISITE)

**Per A3 (external review): current `scripts/grade_artifact.py` parser is a homegrown YAML subset that does not handle nested structures. The R3 design assumes nested `min_content:` and `must_include_in_section:` blocks — those will silently fail to load with the current parser.**

**Files to MODIFY:**
- `scripts/grade_artifact.py` — replace `parse_expected_file()` either by (a) importing `PyYAML` (`yaml.safe_load`) if it's an acceptable dependency, OR (b) extending the homegrown parser to handle indented sub-dicts up to 3 levels deep.
- `scripts/check_tool_safety.py` — same parser replacement if it shares the helper.

**Unit tests required (TDD):**
- `test_parse_flat_yaml` — current shape must still pass
- `test_parse_nested_min_content` — new shape parses correctly
- `test_parse_nested_must_include_in_section` — new shape parses correctly
- `test_parse_deeply_nested_anchored` — 3-level nesting (section → phrase → anchored/min_words)
- `test_malformed_yaml_raises` — bad input yields clear error, not silent fail
- `test_backward_compat_against_existing_fixtures` — every existing expected/*.yaml still loads

**Done when:** All 6 unit tests pass; every existing `evals/expected/*.yaml` still loads.

**Commit:** `refactor(grader): upgrade YAML parser to support nested expected-fixture structures`

---

### Phase 3a — Structural grader hardening (ship first)

### Task 3.1 — G1 + G5: JSON payload extraction + schema validation

**Files to ADD:**
- `scripts/grade_artifact_payloads.py`

**Change:** Extract fenced ` ```json ` blocks from artifacts; parse; route by `kind` field to one of the existing schemas (`linear-issue`, `notion-page`, `discovery-to-prd-handoff`, `prd-to-delivery-handoff`, `workflow-chain-handoff`, `blocked-workflow`); validate using `scripts/check_tool_safety.validate_schema` (reuse existing).

Extra-schema realism checks (per R3 §G5):
- `linear_issue` previews: `workspaceId` OR `team_key` AND ≥1 `UNRESOLVED_LINEAR_*` token (unresolved unless workspace already resolved); `items[]` length ≥3
- `notion_page` previews: `target.id` OR `databaseId` AND ≥1 `UNRESOLVED_NOTION_*` token; `pages[]` length ≥2
- `confirmationRequired: true` OR `confirmation_required: true`

**Extend `evals/expected/*.yaml`:** Add field `required_json_payloads: [<kind>, …]`.

**Done when:**
- `grade_artifact_payloads.py` exists; passes pytest unit tests
- All 12 positive expected fixtures have `required_json_payloads` declared
- The module catches `{"dry_run": true}` as Linear preview (fails Gemini's 09)
- The module passes Claude's 09 (`items[]` = 6)

**Acceptance test:** Run against Claude 0.2.1 outputs — all green. Run against Gemini 0.2.1 outputs — fails on 09, 10, 12 (the tooling-relevant artifacts).

**Commit:** `feat(grader): add JSON payload extraction and schema validation`

---

### Task 3.2 — G2: Per-skill min-content thresholds

**Files to MODIFY:**
- `scripts/grade_artifact.py` — extend `parse_expected_file` to read the new `min_content:` block; add helpers `count_evidence_ids(text)`, `count_table_rows(section_name)`, `count_section_bullets(section_name)`
- Every `evals/expected/*.yaml` — add the `min_content:` block per R3 §Minimum-content thresholds table

**Per-skill thresholds:** Copy R3's full table (~25 rows). Examples:
- `pm-discovery / direct_evidence: evidence_id_count >= 12`
- `pm-strategy / scores: opportunities_table_rows >= 4`
- `pm-tooling / linear_dry_run_preview: items_length >= 3` (relocated since pm-tooling is gone — this lives under the workflow expected fixture)

**Per A14 (external review): DROP the global 600-word artifact-length floor.** Per-section structural counts (evidence IDs, opportunities, items in payloads, etc.) are the right granularity. A concise but correct artifact must not fail because it's under 600 words; an artifact failing structural counts is the real signal.

**Done when:**
- Every expected fixture has `min_content:` with the appropriate per-section thresholds
- Claude 0.2.1 outputs pass all thresholds (calibration step — Task 3.10)
- Gemini 0.2.1 outputs fail at least 6 of the 12 positive checks (per R3 expected catch rate)

**Commit:** `feat(grader): add per-skill min-content thresholds`

---

### Task 3.3 — G3 + G11: Forbidden-phrase scanner

**Files to ADD:**
- `evals/forbidden-phrases.yaml` — 20 patterns from R3 §Forbidden-phrase list

**Files to MODIFY:**
- `scripts/grade_artifact.py` — add scanner. For each pattern, scan whole artifact except `## Quality Bar` section (where the pattern may legitimately appear once as a recap). Penalty: pattern outside Quality Bar → blocking fail.

**Unit tests required (per A15):**
- `test_pattern_matches_in_body` — Gemini-style bullet matches → fail
- `test_pattern_allowed_in_quality_bar` — same phrase inside ## Quality Bar with ≤1 occurrence → pass
- `test_pattern_blocks_at_two_occurrences_in_quality_bar` — >1 in Quality Bar → fail
- `test_claude_baseline_passes` — every Claude 0.2.1 artifact passes
- `test_gemini_baseline_fails` — every Gemini 0.2.1 positive fails
- `test_regex_compiles` — all 20 patterns parse as valid regex
- `test_false_positive_on_legitimate_prose` — sample legitimate prose with relevant keywords does not match (pre-curated fixture)

**Done when:**
- All 7 unit tests pass
- File exists with all 20 patterns
- Scanner integrated into grader pipeline
- Claude 0.2.1 outputs pass (≤1 pattern inside Quality Bar)
- Gemini 0.2.1 outputs fail on 12/12 positives (each contains ≥3 patterns)

**Commit:** `feat(grader): add forbidden-phrase scanner for rubric-echo detection`

---

### Task 3.4 — G4: Hash format validation

**Files to MODIFY:**
- `scripts/grade_artifact_payloads.py` — add regex check for `dry_run_payload_hash` / `payloadHash` fields: `^sha256:[a-z0-9-]{8,128}$` AND must not end with `...`
- `evals/forbidden-phrases.yaml` — add `sha256:[a-zA-Z0-9]{0,15}\.\.\.` to catch inline truncated hashes

**Done when:**
- Truncated hashes like `sha256:7f8e9a1b...` fail
- Synthetic placeholders like `sha256:synthetic-linear-preview-001` pass
- Real synthetic hashes (8+ hex chars) pass

**Commit:** `feat(grader): require synthetic-but-realistic hash format`

---

### Task 3.5 — G6: Skill declaration extraction (CONDITIONAL per A13)

**Per external-review A13: requiring every artifact to declare `Skill: pm-strategy` is grader-friendly but user-hostile for in-conversation outputs. Make this CONDITIONAL.**

**Files to MODIFY:**
- `scripts/grade_artifact.py` — add `extract_declared_skills(markdown)` finding both `Skill: <name>` lines and YAML frontmatter `skill_ids: [...]`
- Every `evals/expected/*.yaml` — add `provenance_required: true|false` (default false). Set to `true` for standalone artifacts (PRDs, decision memos, postmortems) where audit trail matters; set to `false` for in-conversation chat outputs where the LLM is conversing.

**Change in artifact requirements:** Artifacts emitted by skills MAY declare which skill executed them. The grader checks declared ⊇ expected ONLY when `provenance_required: true`. Default behavior: declaration is optional and absent declaration is not a fail.

**Done when:**
- Extractor returns expected sets when declarations are present
- Eval fixtures explicitly mark which cases require declarations
- Claude artifacts that already declare continue to PASS
- Gemini artifacts that don't declare PASS the cases where `provenance_required: false`, FAIL where `true`

**Commit:** `feat(grader): conditional skill declaration extraction (provenance_required flag)`

---

### Task 3.6 — G9: Negative refusal deterministic contract

**Files to ADD:**
- `evals/refusals/negative-01-linear-live-write.yaml`
- `evals/refusals/negative-02-linear-dry-run-no-confirmation.yaml`
- `evals/refusals/negative-03-linear-duplicate-create.yaml`
- `evals/refusals/negative-04-notion-tool-kind-mismatch.yaml`
- `evals/refusals/negative-05-product-os-no-evidence-blocked.yaml`
- `evals/refusals/negative-06-skill-versioning-no-evidence.yaml`
- `schemas/tool-safety-refusal.schema.json` — refusal envelope schema (per R3)
- `scripts/grade_refusal.py` — applies the contract

**Refusal contract per negative:** See R3 §Negative test deterministic contract for the full per-negative required content table.

**Common contract elements (all negatives):**
- Required refusal marker (regex)
- Forbidden positive markers (zero matches: `mode: confirmed_write`, `confirmation_required: false`, …)
- Fixture citation (must reference grounding fixture filename)
- Structured refusal JSON block validating against `blocked-workflow.schema.json` or `tool-safety-refusal.schema.json`
- Required JSON fields: `workflow_id`, `status: blocked`, `blocked_stage`, `reason` (≥40 chars), `missing_inputs[]` (≥1 item), `refused_action`, `resume_status`, `handoff_target`

**Per-negative requirements:** Copy R3 §Negative deterministic contract table (6 rows).

**Done when:**
- All 6 refusal contracts exist
- `grade_refusal.py` exists and passes pytest
- Re-grading the existing Claude/Codex negative artifacts gives PASS
- Re-grading Gemini's negatives gives FAIL because Gemini's negatives have no structured JSON block

**Commit:** `feat(grader): add deterministic refusal contracts for 6 negative tests`

---

---

### Phase 3b — Content-threshold grader hardening (ship after 3a calibration succeeds)

**Why split:** Per A2, 3b modules (section-anchored prose, declaration extraction, etc.) carry false-positive risk and require calibration. Ship 3a first, run baseline, confirm Claude passes with margin, THEN ship 3b.

### Task 3.2 (relocated to 3b) — G2: Per-skill min-content thresholds

*Originally Task 3.2 above; sequence-wise it ships AFTER 3a is calibrated. Same content; no duplication here. Adjust per-task done-when so 3.2 is gated on 3.10a calibration passing.*

### Task 3.b1 — Minimal LLM-judge advisory layer (per A4 / G-1)

**Per external-review A4: Pull a single-dimension LLM-judge layer into 0.3.0 as ADVISORY. Full 5-dimension judge remains 0.4.0.**

**Files to ADD:**
- `scripts/judge_artifact_llm.py` — single dimension only: `concrete_reasoning` (1-4 scale). Question: "Does this artifact contain concrete, evidence-anchored product reasoning, or does it primarily restate generic methodology / rubric language?"
- `evals/judge-prompts/concrete-reasoning.md` — the judge prompt itself, calibrated with 3 example outputs at each of 1, 2, 3, 4.

**Wiring:** Orchestrator calls the judge after deterministic grading. Score is written to `graded/<runtime>/<prompt>.judge.json`. Reported in the summary. **Does NOT flip pass/fail in 0.3.0.**

**Done when:** Module runs end-to-end on Claude 0.2.1 outputs (expected: all scores 3-4) and Gemini 0.2.1 outputs (expected: most scores 1-2). The score distribution itself is the validation.

**Commit:** `feat(grader): add minimal LLM-judge advisory layer (single dimension: concrete_reasoning)`

---

### Task 3.7 — G10: Section-anchored must-include

**Files to MODIFY:**
- `scripts/grade_artifact.py` — extend `extract_sections` to also return section text ranges; allow `must_include_in_section` in expected fixtures with sub-field `anchored: prose|bullet|either` and `min_words_in_context: N`
- Every `evals/expected/*.yaml` — for the must-include checks most prone to rubric-echo, move them under `must_include_in_section` with `anchored: prose` and `min_words_in_context: 30`

**Done when:**
- Claude's prose paragraphs containing must-include phrases pass
- Gemini's 5-word bullets containing the same phrases fail

**Commit:** `feat(grader): section-anchored must-include with prose-vs-bullet discrimination`

---

### Task 3.8 — eval-map v2 with negatives

**Files to MODIFY:**
- `test-results/productskills-e2e-synthetic/eval-map.json` — bump version, add `negatives:` array per R3

**Change:** The 6 negatives become first-class eval entries with their refusal contract file path. The orchestrator runs them through `grade_refusal.py`.

**Done when:**
- eval-map.json is valid JSON
- Orchestrator processes both positives and negatives
- Re-running the 0.2.1 artifacts against the new grader produces a deterministic JSON for every single one (no manual graded JSONs)

**Commit:** `feat(grader): eval-map v2 — negatives become first-class graded cases`

---

### Task 3.9 — Orchestrator integration

**Files to MODIFY:**
- `scripts/grade_productskills_synthetic_e2e.py` — call the new modules in sequence; merge results into a single graded JSON per artifact

**Pipeline:**

```
For each positive artifact:
  grade_artifact.grade_artifact (existing)
  grade_artifact_payloads.grade_payloads (G1, G4, G5)
  forbidden_phrase_scan (G3, G11)
  min_content_scan (G2)
  skill_declaration_check (G6)
  section_anchored_must_include (G10)
  → merge → graded JSON

For each negative artifact:
  grade_refusal.grade_refusal
  → graded JSON

After all artifacts:
  check_run_consistency (G8) — advisory in 0.3.0
  check_evidence_id_grounding (A5) — advisory in 0.3.0
```

**Done when:** Orchestrator runs end-to-end on 0.2.1 artifacts and produces correct PASS/FAIL distribution: Claude 18/18 PASS, Codex 18/18 PASS, Gemini significantly reduced (estimate: 0-3/12 positives PASS, 4-6/6 negatives PASS).

**Commit:** `feat(grader): orchestrator pipeline integrating all hardening modules`

---

### Task 3.10 — Calibration & threshold verification

**Pre-condition:** Tasks 3.1-3.9 complete.

**Process:**
1. Re-run grader against Claude 0.2.1 outputs. Expected: 18/18 PASS.
2. Re-run grader against Codex 0.2.1 outputs. Expected: 17-18/18 PASS (small tolerance for Codex's lower depth).
3. Re-run grader against Gemini 0.2.1 outputs. Expected: 0-3/12 positives PASS, 0-2/6 negatives PASS (because Gemini's negatives lack the required JSON block).
4. If Claude fails any check, **adjust the threshold downward** until Claude passes with margin. Document the adjustment.
5. If Gemini passes any rubric-echo-detection check, **tighten the pattern** to catch the specific artifact. Document the tightening.

**Output:** A calibration report at `.review-tmp/phase3-calibration.md` showing every threshold's calibrated value + the Claude/Gemini observed value.

**Done when:**
- Claude 18/18 PASS (Codex 17+/18)
- Gemini fails at least 9 of 18 (positives and negatives combined)
- Calibration report committed alongside the grader changes

**Commit:** `chore(grader): calibrate thresholds against Claude/Codex/Gemini 0.2.1 baselines`

---

## Phase 4 — Corpus Expansion

**Goal:** Add the test cases that close the 0.2.1 coverage gaps. After Phase 4, the corpus tests for: substance density, refusal correctness, re-entry, handoff chains, adversarial inputs, and router disambiguation.

Phase 4 depends on Phase 3 (the grader assertions for the new cases must already exist).

### Task 4.1 — Add deterministic-only positive cases (NEW-01..11, 19-23, 25)

**Files to ADD:** ~16 new prompts + expected fixtures under `test-results/productskills-e2e-synthetic/prompts/` and `evals/expected/`.

**Cases:** See R3 §Corpus expansion. Examples:
- NEW-01: pm-discovery / high-volume evidence stress (60 interviews → ≥5 themes)
- NEW-02: pm-discovery / thin-evidence honesty (2 interviews → refuse to overclaim)
- NEW-03: pm-strategy / forced-RICE deflection (RICE on pricing-unknown → propose alternative)
- NEW-04: pm-validation / experiment-without-baseline (block, demand instrumentation)
- NEW-05: pm-design / high-fi without usability evidence (block, low-fi alternative)
- NEW-06: pm-docs / PRD with implementation tasks (critique the leak)
- NEW-07: pm-delivery / under-decomposition test (counter-propose decomposition)
- NEW-08: pm-growth / virality with no instrumentation
- NEW-09: pm-gtm / launch with unfixed blocker (cite SUP-002)
- NEW-10: pm-tooling-relocated / stale external ID map (propose noop/update, not create)
- NEW-11: pm-tooling-relocated / workspace-resolved happy path

Adversarial cases (NEW-19..23):
- NEW-19: skeleton-with-keyword-stuffing (concision pressure → still must produce full artifact)
- NEW-20: invented metric injection (numbers not in fixture → ask for source)
- NEW-21: launch-claim fabrication (no post-launch evidence → block)
- NEW-22: cross-skill smuggling (PRD + confirmed-write Linear payload → decompose, refuse confirm)
- NEW-23: rubric leak (rubric pasted in prompt → don't echo verbatim)

NEW-25: workflow without lifecycle state (refuse to drop handoff envelope)

**Done when:**
- All ~16 prompt files exist with grounded fixtures (every cited ID exists in the fixture corpus)
- All expected fixtures have grader assertions per R3

**Commit:** `feat(evals): add 16 deterministic-only positive cases including 5 adversarial`

---

### Task 4.2 — Add re-entry cases (NEW-12, NEW-13)

**Files to ADD:**
- `evals/handoffs/rough-prd-input.json` (per R3)
- `evals/handoffs/launch-ready-input.json` (per R3)
- Prompt + expected fixture for each

**Cases:**
- NEW-12: Rough PRD → continue. Input: handoff JSON with `lifecycle_status: evidence_synthesized`. Expected: workflow advances `lifecycle_status: validation_decided`; `completed_stages` extended; no regression.
- NEW-13: Launch-readiness reentry. Input: handoff JSON with `lifecycle_status: launch_ready` and G-2 open. Expected: block launch; `lifecycle_status` does NOT advance to `launched`; cites SUP-002 + G-2.

**Grader assertion (new):**
- Re-entry test asserts a small state machine: input `lifecycle_status` ≤ output `lifecycle_status` (no regression unless explicitly blocked); transitions follow the canonical sequence.

**Per A7 (external review): add `evals/allowed-transitions.yaml`** mapping each of the 21 lifecycle statuses (from `workflow-stage.schema.json` enum) to its allowed next-statuses. Example:

```yaml
intake_received:
  allowed_next: [evidence_synthesized, validation_pending, blocked]
evidence_synthesized:
  allowed_next: [validation_pending, validation_decided, prd_drafted, blocked]
validation_decided:
  allowed_next: [prd_drafted, blocked, validation_not_required]
# ... 18 more
```

The re-entry grader checks `output.lifecycle_status in allowed_transitions[input.lifecycle_status].allowed_next OR output.status == 'blocked'`. Catches illegal transitions (e.g., `intake_received → launched` would fail).

**Done when:**
- Both input fixtures exist as valid JSON validating against `workflow-chain-handoff.schema.json`
- Re-entry state machine check exists in the grader
- Claude 0.3.0 baseline passes both cases

**Commit:** `feat(evals): add re-entry correctness tests (rough-PRD, launch-readiness)`

---

### Task 4.3 — Add handoff chain cases (NEW-14, NEW-15)

**Files to ADD:**
- `scripts/check_handoff_chain.py`
- Phase A/B/C prompts under `test-results/productskills-e2e-synthetic/prompts/handoff-chain/`

**Test design:** Three phases per run:
- Phase A: pm-discovery on AtlasBoard fixture → emits `discovery-to-prd-handoff.schema.json`-validating envelope
- Phase B: workflow-discovery-to-prd takes Phase A envelope as input → produces PRD + `prd-to-delivery-handoff.schema.json` envelope
- Phase C: workflow-prd-to-linear-delivery takes Phase B envelope as input → produces delivery split with stories addressing every in-scope item

**Grader assertions:**
- Phase A envelope validates schema
- Phase B's PRD references the same evidence IDs as Phase A's themes
- Phase B's assumption_map ⊇ Phase A's
- Phase B's prd-to-delivery-handoff validates schema
- Phase C: every in-scope PRD item has ≥1 story addressing it (string-match)
- No delivery story addresses an out-of-scope item

**Done when:**
- All three phases run end-to-end against Claude 0.3.0 baseline
- Phase C output stories cover all Phase B in-scope items
- The check_handoff_chain.py grader is wired into the orchestrator

**Commit:** `feat(evals): add E2E handoff chain test (discovery → PRD → delivery)`

---

### Task 4.4 — Add router disambiguation cases (NEW-16..18, +A12)

**Files to MODIFY:**
- `evals/trigger-tests.yaml` — add the 3 original router cases PLUS the 2 cases surfaced by external review (A12, G "missing"):
  - NEW-16: "I have interviews and need themes" → pm-discovery only (not workflow-discovery-to-prd)
  - NEW-17: "Design the smallest experiment to test this assumption" → pm-validation only (not pm-discovery/research-plan)
  - NEW-18: Promote `workflow-product-operating-system-negative-single-prd-review` to a graded positive: produce pm-docs critique, not a workflow
  - **NEW-16b (per A12):** "I made a decision about X — record it for future reference" → pm-docs/decision-memo. AND "We decided X; I need to tell the team" → pm-stakeholder-comms/decision-comms. **Same data, different framing.** Tests the decision-memo vs decision-comms boundary that Codex flagged as a trap.
  - **NEW-16c (per G "missing"):** "Write an update about our launch" → pm-stakeholder-comms (internal stakeholder update) vs pm-gtm (customer-facing launch comms). Disambiguates the new skill from the existing one.

**Done when:** Trigger tests catalog has 5 new cases. The corresponding positive trigger thresholds (0.9 self-consistency) pass for the intended skill; thresholds for competing skills stay <0.5.

**Commit:** `feat(evals): add router disambiguation tests incl. new-skill boundaries`

---

### Task 4.5 — Add cases for new skills (pm-roadmap, pm-metrics, pm-stakeholder-comms)

**Files to ADD:**
- 3 positive cases for pm-roadmap (roadmap build, intake triage, quarterly planning)
- 3 positive cases for pm-metrics (north-star design, metric tree, guardrail)
- 3 positive cases for pm-stakeholder-comms (exec update, status memo, ask framing)
- 1 negative per skill:
  - pm-roadmap: "use pm-roadmap to score these features" → refuse, route to pm-strategy
  - pm-metrics: "run an experiment against this metric" → refuse, route to pm-growth or pm-validation
  - pm-stakeholder-comms: "write a PRD for stakeholders to review" → refuse, route to pm-docs

**Done when:** Each of the 3 new skills has ≥3 positive + ≥1 negative test case in the corpus (12 new cases total).

**Commit:** `feat(evals): add corpus coverage for pm-roadmap, pm-metrics, pm-stakeholder-comms`

---

### Task 4.6 — Migrate retired master-workflow tests AND forward-tests

**Files to MODIFY/DELETE:**
- `evals/trigger-tests.yaml` — remove the 6 master-workflow positive triggers (lines 42-73 in 0.2.1); remove pm-tooling triggers
- `evals/golden-cases/product-os-*.md` — delete or re-target the 6 cases:
  - `product-os-full-happy-path` → becomes the NEW-14/15 chain test (already covered)
  - `product-os-approved-prd-reentry` → migrate to `workflow-prd-to-linear-delivery-approved-prd-input`
  - `product-os-rough-prd-reentry` → becomes NEW-12 (already covered)
  - `product-os-launch-readiness-reentry` → migrate to `pm-gtm-launch-readiness-blocked` (NEW-13 covers the blocked case; add a happy path)
  - `product-os-no-evidence-blocked` → migrate to `workflow-discovery-to-prd-no-evidence-blocked` (existing semantics)
  - `product-os-post-launch-learning` → migrate to `pm-growth-post-launch-learning`
- **`evals/forward-tests/phase8-forward-tests.json` (per A6 — newly added per external review):** this file references pm-tooling and workflow-product-operating-system throughout. Audit every reference. For each: re-target to narrower workflows/skills OR remove if the test concept is covered by the new corpus. Specifically scan for `"skill": "pm-tooling"`, `"skill": "workflow-product-operating-system"`, and `"adapter": "product-operating-system"` and patch each.

**Done when:**
- No test references the retired master workflow
- No test references pm-tooling as a top-level skill (tool-safety semantics now under workflows)
- Every re-targeted case has a graded baseline against Claude 0.3.0
- `evals/forward-tests/phase8-forward-tests.json` is consistent with the new package

**Commit:** `refactor(evals): migrate master-workflow + pm-tooling tests to narrower workflows; update forward-tests`

---

## Phase 5 — Migration & Verification

**Goal:** Update docs, retire artifacts, run full eval, and verify the release meets quality bar. After Phase 5, 0.3.0 is shippable.

### Task 5.1 — Cross-reference final audit

**Files:** Read-only.

**Change:** Run the same grep set from Task 1.2, plus:

```
grep -rn "pm-tooling" .  # expect zero outside CHANGELOG/archive
grep -rn "workflow-product-operating-system" .  # expect zero outside CHANGELOG/archive
grep -rn "decision-log" .  # expect zero (renamed)
grep -rn "skill-output-envelope" .  # expect zero
grep -rn "product-operating-system-handoff" .  # expect zero (renamed to workflow-chain-handoff)
grep -rn "product-operating-system-contract" .  # expect zero (deleted)
```

**Done when:** All commands return zero matches outside `CHANGELOG.md` and `docs/_archive/`.

---

### Task 5.2b — Backward-compat shim for adapter rename (per A5)

**Per external-review A5: the adapter rename (`product-operating-system` → `product-skills`) breaks existing installs that reference the old adapter path. Add a first-class backward-compat task.**

**Files to MODIFY:**
- `install.sh` — recognize both `product-operating-system/SKILL.md` and `product-skills/SKILL.md` adapter paths; install to the new path but accept the old name as input
- Add a deprecation warning when the old name is invoked: `"[ProductSkills] Adapter name 'product-operating-system' is deprecated. Will be removed in 0.4.0. Use 'product-skills'."`
- `package.yaml` — if it still names the package `product-operating-system`, rename to `product-skills` (or document why the install package name differs from the adapter name)

**Files to ADD:**
- `docs/MIGRATION-0.2-to-0.3.md` — user-facing migration guide listing renames, deletions, and the deprecation timeline

**Done when:**
- Installer accepts both old and new names
- Deprecation warning fires on old name
- Migration guide exists with concrete user actions for each breaking change

**Commit:** `feat(install): backward-compat shim for adapter rename; migration guide`

---

### Task 5.2 — Update CHANGELOG.md

**Files to ADD/MODIFY:**
- `CHANGELOG.md` (top of repo) — add 0.3.0 entry covering:
  - Removed: pm-tooling, workflow-product-operating-system, skill-output-envelope schema
  - Added: pm-roadmap, pm-metrics; 4 new pm-docs procedures; grader hardening modules; ~25 new test cases
  - Changed: All 13 SKILL.md descriptions; pm-growth procedure consolidation; adapter routing; eval-map v2

**Done when:** CHANGELOG entry is complete and dated.

---

### Task 5.3 — Update README.md and docs/

**Files to MODIFY:**
- `README.md` — update skill count, name new skills, point at routing doc
- `docs/HOW_TO_ROUTE_PRODUCT_WORK.md` (renamed in Task 2.2) — the user-facing routing guide
- `docs/PRODUCT_SKILLS_SLO.md` (if exists) — update SLAs

**Done when:** README accurately describes the 0.3.0 skill set and pointers resolve.

---

### Task 5.4 — Full 0.3.0 eval run (synthetic E2E)

**Process:**
1. Run the full eval against the 0.3.0 package across Claude/Codex/Gemini.
2. Expected baselines:
   - Claude: 18/18 PASS (+ new corpus: ~30+ additional cases should pass; allow some calibration tolerance)
   - Codex: 17-18/18 PASS on core; new corpus may be 80-90% PASS
   - Gemini: Significantly reduced. Goal: catch the grader-gaming. Expect ~3-6/12 positives PASS (down from 12/12), and 0-2/6 negatives PASS (down from "all asserted PASS by prose only").
3. Document the new baseline in `test-results/0.3.0 baseline/`.

**Acceptance:**
- Claude must hit 18/18 on the core 12+6 cases (calibration is calibrated against Claude).
- Codex degradation from 0.2.1 baseline must be ≤1 case (small acceptable variance).
- Gemini regression is the **expected outcome** (the package is now harder to game).

**Done when:** Baseline run report committed to `test-results/0.3.0 baseline/`.

**Commit:** `test: 0.3.0 baseline run across Claude, Codex, Gemini`

---

### Task 5.5 — Final release commit

**Files to MODIFY:**
- `VERSION` (already pinned in Task 1.1)
- `package.json` (already pinned in Task 1.1)
- `package.yaml` (already pinned in Task 1.1)
- `registry.json` (already pinned in Task 1.1)

**Process:** Tag the release commit. Build/publish artifacts if relevant.

**Commit:** `chore: release 0.3.0`

---

## Phase 6 — Stretch (Out of 0.3.0 Scope; Sketched for 0.3.1 / 0.4.0)

These tasks are documented for context but NOT in the 0.3.0 release.

### S.1 — `check_run_consistency.py` blocking
Currently advisory; promote to blocking once 2 consecutive 0.3.x runs hit clean baseline.

### S.2 — `check_evidence_id_grounding.py` blocking
Same — promote once Claude/Codex baselines verify clean. Catches "evidence-ID reuse without source files" attack (A5).

### S.3 — LLM-as-judge layer
`scripts/judge_artifact_llm.py`. Five advisory dimensions: inference correctness, theme arbitrariness, decision-readiness, risk realism, tone discipline. Ships 0.4.0.

### S.4 — Cross-runner invariant tests (NEW-24)
Same prompt across Claude/Codex/Gemini; assert headline-conclusion invariants. Ships 0.4.0 as advisory.

### S.5 — Re-evaluate `workflow-chain-handoff` schema necessity
After 0.3.x usage data, decide whether the schema earns its keep or merges into the two narrower workflow envelopes.

---

## 8. Acceptance criteria for 0.3.0 release

The release ships when ALL of these are true:

1. **Structure:** 13 skills in `registry.json`; `pm-tooling` and `workflow-product-operating-system` absent; `pm-roadmap`, `pm-metrics`, and `pm-stakeholder-comms` present.
2. **pm-docs:** 7 procedures (PRD, decision-memo, spec-review, one-pager, RFC, internal-review-faq, postmortem), 6 new templates, description aligned with procedures (verified by automated check that every `Use when …` clause names a procedure that exists).
3. **Postmortem refusal contract:** `procedures/postmortem.md` Step 1 deterministically refuses ops/SRE incident requests (per A8). Test case exists.
4. **Descriptions:** Every SKILL.md description has at least one negative trigger (verified by `grep -L "Do not use" skills/*/SKILL.md` returning zero).
5. **Procedures:** Every leaf procedure has a `## Done When` block (verified by grep).
6. **Schemas:** No orphan schemas — every schema in `schemas/` is referenced by at least one skill or eval. Verified by audit script.
7. **Templates:** `templates/prd.md` has prose guidance per section (no longer a stub). `templates/research-synthesis.md` either deleted or cited from `voc-synthesis.md`.
8. **Adapter routing PROVEN before master workflow deleted:** Task 2.2a verification report committed showing ≥4/5 single-stage golden cases route correctly via new adapter routing block (per A1).
9. **Grader 3a (structural) ships first** with calibration showing Claude 18/18 PASS and Gemini detectable regression. **Grader 3b (thresholds + LLM-judge advisory) ships second.**
10. **Grader YAML parser** handles nested expected fixtures (Task 3.0 unit tests all pass).
11. **Allowed lifecycle transitions:** `evals/allowed-transitions.yaml` exists; re-entry tests validate transitions.
12. **Corpus:** ~25+ new test cases live; including router disambiguation for new skills (NEW-16b, NEW-16c).
13. **Adapters:** All 5 adapters carry the routing block (in `description:` AND body); catch-all rule for unclassified inputs; routing reference exists at `references/routing/artifact-to-workflow.md`; backward-compat shim accepts old `product-operating-system` adapter name.
14. **Documentation:** `CHANGELOG.md` 0.3.0 entry; `README.md` updated; `docs/MIGRATION-0.2-to-0.3.md` exists; `HOW_TO_ROUTE_PRODUCT_WORK.md` is the user-facing routing guide.
15. **Forward tests migrated:** `evals/forward-tests/phase8-forward-tests.json` contains no references to pm-tooling or workflow-product-operating-system.
16. **Cross-reference audit:** Task 5.1 returns zero matches outside CHANGELOG / archive (paths corrected per A4 — grep from inside the package dir).
17. **Baseline run:** Claude 18/18 on core; Codex ≥17/18; Gemini reduced (any cases that *would* PASS the new grader are real substance, not skeletons). LLM-judge `concrete_reasoning` scores: Claude 3-4, Gemini predominantly 1-2.

---

## 9. Execution recommendation

This SDD has substantial scope (5 phases, ~40 atomic tasks). Recommended execution mode:

**Subagent-driven execution** (one task per fresh subagent) is the right approach because:
- Phases 2, 3, 4 contain many parallelizable tasks within the phase
- Each task has a single clear acceptance criterion that a fresh subagent can verify
- Two-stage review between subagents catches drift early

**Sequencing:**
- Phase 1 first (foundation locks)
- Phase 2 second (architectural changes) — within Phase 2, tasks 2.1-2.6 are interdependent (they all touch adapter or workflow files); 2.7-2.11 are mostly independent
- Phase 3 third (grader) — depends on Phase 2 being settled so calibration thresholds aren't moving targets
- Phase 4 fourth (corpus) — depends on Phase 3 grader modules
- Phase 5 last (verification)

**Commit cadence:** ~12-15 commits across the release.

**Time estimate (updated post-external-review):** R3 estimated grader scope at 10-13 engineering days. Plus skills restructure (Phase 2, now including 3 new skills) at ~7-9 days. Plus Phase 1, 4, 5 at ~3-4 days. Plus extras surfaced by external review: YAML parser upgrade (+1-2 days, see Task 3.0), backward-compat adapter shim (+1 day, see Task 5.2b), allowed-transition table (+0.5 day, see Task 4.2), minimal LLM-judge (+1-2 days, see Task 3b.X). External reviewers (Gemini + Codex independently) both estimated 30-40 days for cleanly executed work. **Revised total: ~28-36 engineering days for one focused engineer**, or roughly 6-8 calendar weeks with normal interruptions.

---

## 10. Open questions — RESOLVED

All open questions resolved on 2026-05-28. See §0 for the decisions table.

| # | Question | Resolution |
|---|----------|-----------|
| Q1 | Version number | **0.3.0** |
| Q2 | Release shape (bundled vs stepping stone) | **Single bundled 0.3.0 release** |
| Q3 | pm-stakeholder-comms timing | **Create in 0.3.0** (not deferred) |
| Q4 | Adapter rename | **Rename to `product-skills`** |
| Q5 | Final skill count | **13 skills total** |
| Q6 | Decision-memo form | **Both narrative + bullet-log forms** |
| Q7 | Postmortem scope | **Product failures only** (excludes ops/SRE) |
| Q8 | Execution mode | **Subagent-driven, task-by-task** with phase checkpoints |

No outstanding questions block execution. Phase 1 can begin immediately.

---

**END OF SDD.**
