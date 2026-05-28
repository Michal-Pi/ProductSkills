# ProductSkills 0.2.1 — Prioritized Improvements

**Audit date:** 2026-05-28
**Inputs:** four parallel sub-agent audits (prompts/design, gaps/valuation, 0.2.1 test results, collaboration/schemas/evals)
**Working copies:** `.review-tmp/{A-prompts,B-gaps,C-tests,D-collab}.md`

---

## Executive summary

Three signals converge across the four audits:

1. **The "18/18 PASS" is misleading.** The deterministic grader is a regex/section-header checker. Gemini gamed it with rubric-echo skeletons (e.g., bullet body literally reads `"includes **method selection rationale**"`) and still scored 4/4. Claude and Codex produced real artifacts; the safety floor (refusing live writes, refusing fabricated evidence) held across all three runners. But the **quality bar is silently unenforced for one of three runners** — and the grader can't tell.

2. **The skills route on noise.** `description:` fields are keyword piles. No skill has a negative trigger. The three workflow skills — and especially `workflow-product-operating-system` — share trigger surface with each other and with `pm-discovery`. A router has no decision rule. The genuinely useful entry-classification table sits inside a procedure file the router never reads at trigger time.

3. **Infrastructure is over-built relative to where contracts actually fire.** 16 schemas, 17 templates, 35 references. The "universal output envelope" is cited by exactly one skill. Five schemas (`blocked-workflow`, `launch-readiness-gate`, `post-launch-learning`, `tool-safety-fixture`, `forward-test-suite`) are orphan from skills — their templates are wired, the schemas aren't. The package has wiring at the workflow boundary but cohesion erodes inside the family skills.

The 9+3 split is **directionally correct** but carries 2-3 weak slots:
- `pm-tooling` is infrastructure, not a PM job. Its safety semantics belong inside the two workflow skills.
- `pm-docs` description promises capabilities its procedures don't deliver (SDDs, MRDs, stakeholder updates don't exist as procedures).
- `workflow-product-operating-system` is a superset trigger of the other two workflows; high routing risk.

Three high-value gaps a working senior PM hits weekly to quarterly: **roadmap/quarterly planning**, **metrics/KPI design**, **stakeholder/executive communication**.

---

## Prioritized improvement list

Tiers reflect **impact × effort**. Tier 1 fixes are mostly editorial (rewriting `description:` fields, wiring schemas, fleshing one template). Tier 2 is structural (skill consolidation, grader hardening). Tier 3 is the long-term composition question.

### Tier 1 — Ship before 0.2.2 (editorial, low effort, high impact)

| # | Change | Why | Files |
|---|--------|-----|-------|
| 1 | **Rewrite all 12 `description:` fields** to: (a) one scope sentence, (b) one explicit "Use when…" trigger, (c) **at least one negative trigger naming the nearest neighbor**. Move framework keyword lists into a `## Methods Covered` body section. | Routing is the #1 weakness. LLMs route on the whole description. No skill has a negative trigger today; the three workflows are mutually indistinguishable on description alone. | All 12 `skills/*/SKILL.md` |
| 2 | **Promote the entry-classification table** from `workflow-product-operating-system/procedures/product-operating-system.md` (lines 9-22) into the **SKILL.md body**, and re-describe the master workflow as "router for ambiguous inputs or cross-stage work — prefer `workflow-discovery-to-prd` for raw-to-PRD, prefer `workflow-prd-to-linear-delivery` for PRD-to-Linear." | The single most valuable routing artifact in the package is invisible to the router. | `skills/workflow-product-operating-system/SKILL.md` |
| 3 | **Fix `pm-docs` description-vs-procedure mismatch.** Either implement `sdd.md`, `mrd.md`, `stakeholder-update.md` procedures, OR trim the description to PRD + decision-log + spec-review only. | The current description promises capabilities the procedures don't deliver — failure mode is silent. | `skills/pm-docs/SKILL.md` + `procedures/` |
| 4 | **Wire orphan schemas next to their templates** in `workflow-product-operating-system/procedures/product-operating-system.md`: `blocked-workflow.schema.json` (Blocked State), `launch-readiness-gate.schema.json` (step 9), `post-launch-learning.schema.json` (step 10). | Five schemas exist that no skill cites; structured-output emitters have no path to the contract. | One procedure file. |
| 5 | **Decide the fate of `schemas/skill-output-envelope.schema.json`.** Either cite from every pm-* SKILL.md, or delete. | "Universal envelope" cited by exactly one skill. Pick a side. | All pm-* SKILL.md OR delete schema |
| 6 | **Flesh out `templates/prd.md`** with one-line guidance per section, modeled after `templates/research-plan.md` (the gold standard). | PRD is the most-cited template and the thinnest. Most likely artifact produced badly without scaffolding. | `templates/prd.md` |
| 7 | **Disambiguate the byte-identical adapters.** `adapters/claude/SKILL.md` and `adapters/codex/SKILL.md` are the same file. Either differentiate per host (tool perms, invocation hints) or point both at one canonical file via the installer. | Two byte-identical files implies broken intent. | `adapters/{claude,codex}/SKILL.md` |
| 8 | **Delete or wire `templates/research-synthesis.md`.** Zero references in any skill or procedure today. | Dead weight in the bundle. | `templates/research-synthesis.md` |
| 9 | **Add a leaf-procedure "Done when" block** to every `procedures/*.md` (3-5 concrete acceptance conditions). Workflow procedures already have "Completion Standard" — propagate to leaves. | Without acceptance criteria, the LLM stops at 6 bullets. This is the structural enabler of Gemini's rubric-echo failure mode (no internal stop rule = no internal quality bar). | All `skills/*/procedures/*.md` |

**Tier-1 total effort:** roughly a day of writing/editing. **Impact:** addresses every HIGH-severity finding from sub-agent A and the orphan-schema cohesion gap from sub-agent D.

---

### Tier 2 — Ship for 0.3.0 (structural)

| # | Change | Why | Files |
|---|--------|-----|-------|
| 10 | **Harden the grader against rubric-echo.** Add to `evals/expected/*.yaml`: `min_evidence_ids: N`, `min_sections_with_content: N` (each section needs >= K non-skeleton tokens), `forbidden_phrases: [...]` (catches "includes **method selection rationale**" used as content). | Gemini's `02-pm-strategy.md` is 35 lines with one scored opportunity and scored 4/4. Grader cannot distinguish skeleton from analysis. | `evals/expected/*.yaml`, `scripts/grade_productskills_synthetic_e2e.py` |
| 11 | **Bring negatives into the deterministic grader.** Add the 6 negative prompts to `eval-map.json` with machine-checkable refusal contracts (must contain BLOCKED/REFUSED, must not contain a created issue ID, must reference grounding fixture). Gemini's run shipped with **no graded JSON for any negative** — PASS asserted in prose only. | The 6 negative tests are the package's safety floor. They cannot be manually-graded-only. | `evals/eval-map.json`, grader script, expected fixtures |
| 12 | **Tighten `schemas/tool-safety-fixture.schema.json`** and `linear-issue` / `notion-page` payload validation. Replace `payloads: {type: array}` with typed inner objects. The grader should reject `{"dry_run": true}` as a "Linear preview." | Gemini's pm-tooling preview was a 2-key JSON stub. The safety-critical artifact reduced to a placeholder still scored 4/4 on tooling_safety. | `schemas/tool-safety-fixture.schema.json`, payload schemas |
| 13 | **Collapse `pm-growth` procedural redundancy.** Merge `activation-analysis.md`, `retention-analysis.md`, `monetization-analysis.md` into one `funnel-stage-analysis.md` parameterized by stage. OR add a "Method Selection" block (pm-strategy style) at SKILL.md level that names when to pick each. | Four near-identical 5-step procedures + `lifecycle-experiment.md` duplicates `pm-validation/experiment-design.md`. LLM has no rule for which to pick. | `skills/pm-growth/{SKILL.md, procedures/}` |
| 14 | **Collapse `pm-tooling` 5 procedures into 2** (`dry-run-preview.md`, `id-resolution.md`). The five share one underlying discipline (preview → resolve IDs → confirm → write → record map). | Over-decomposed; same concern fragmented into 5 files. | `skills/pm-tooling/procedures/` |
| 15 | **Add re-entry correctness eval.** Given approved-PRD input, assert `validation_decision == validation_not_required` and `entry_status == approved_for_delivery`. Today the prose rubric is satisfied even if a model replays validation. | Phase 12 invested heavily in re-entry behavior; nothing structurally enforces it. | `evals/expected/product-os-approved-prd-reentry.yaml` + fixture |
| 16 | **Add end-to-end handoff chain eval.** Emit a `discovery-to-prd-handoff` JSON from workflow-1, consume as input to workflow-2, validate the resulting `prd-to-delivery-handoff`. Only way to confirm the contracts actually compose. | The handoff contracts claim chained consumers, but the chain is never exercised end-to-end as structured data. | `evals/forward-tests/workflow-chain-handoff.json` (new) |
| 17 | **Standardize handoff-target naming.** negative-05 produced 3 different resume targets across runners (`voc-synthesis` vs `pm-discovery` vs `pm-discovery + pm-validation`). Pick one canonical name (`pm-discovery`) and pin it in the workflow procedure + contract. | Cross-runner inconsistency that the grader doesn't catch. | `workflow-product-operating-system/procedures/...`, contract docs |
| 18 | **Disambiguate `decision_status` enums from canonical lifecycle status enum.** Per-workflow `decision_status` (5 values each) overlaps names with the 21-value canonical lifecycle status. Add a mapping table OR rename to `local_decision`. | Reader/model will assume they're the same set; they aren't. | `references/workflows/workflow-lifecycle-statuses.md`, two handoff schemas |
| 19 | **Add `allowed-tools:` frontmatter** to all SKILL.md files. `pm-tooling` especially should restrict to MCP tools and forbid shell. Other family skills should mostly be read+write-file. | No tool-permission declarations anywhere. `pm-tooling` having broad implicit access is a real safety risk. | All 12 SKILL.md |
| 20 | **Add a router-disambiguation eval suite** for trigger competitions: 3 workflows vs each other, pm-discovery vs workflow-discovery-to-prd, pm-validation vs pm-discovery/research-plan. | The borderline cases identified by sub-agent A as the highest routing risk are not specifically tested today. | `evals/trigger-tests/router-disambiguation/` (new) |

---

### Tier 3 — Strategic composition (decide before 0.3.0)

These are the **trade-off decisions** the user asked about ("remove X to make space for Y"). Sub-agent B proposed dropping 3 and adding 3 to keep the slot count at 12. The proposed swap:

**Drop:** `pm-tooling`, `pm-docs`, `workflow-product-operating-system`
**Add:** `pm-roadmap`, `pm-metrics`, `pm-stakeholder-comms`

| # | Change | Argument FOR | Argument AGAINST | Recommendation |
|---|--------|--------------|------------------|----------------|
| 21 | **Drop `pm-tooling` as a top-level slot;** move its 5 procedures into `references/mcp/` as shared procedures cited by both workflow skills. | Pure infrastructure, no product reasoning. Workflows already own dry-run + confirmation. PMs don't think "I need pm-tooling," they think "send this to Linear." Removes trigger competition. | Loses the rules-only-skill discipline pattern that's the cleanest in the package. Adapter SKILL.md files refer to it as `product-operating-system`-adjacent. | **DO IT** — but keep the safety rules visible in the workflow SKILL.md bodies, not buried in references. |
| 22 | **Merge `pm-docs` into `pm-delivery`.** Move PRD + spec-review into pm-delivery. Move decision-log into pm-strategy. Move (currently fictional) stakeholder updates into a new `pm-stakeholder-comms`. | `pm-docs` only has 3 real procedures; its description promises 5+. PRD is an artifact, not a discipline — `workflow-discovery-to-prd` already orchestrates PRD creation. | Risk of `pm-delivery` becoming bloated. PRD-as-discipline is a real PM job (and is what the package wedges into the market with). | **PROBABLY** — but consider keeping pm-docs as the artifact-writing skill (PRD/spec/RFC/ADR) and trimming, rather than dissolving. The category is real; the current content is thin. |
| 23 | **Drop `workflow-product-operating-system`.** The other two workflows + a routing line in the master adapter can do the job. | Highest routing-overlap risk in the package. The router and the master workflow compete with each other and with the two narrower workflows. Phase 12 added it for re-entry behavior, but re-entry can be a procedure inside the two narrower workflows. | This is where the most design effort went. The entry-classification table is genuinely useful. Re-entry handling is non-trivial. | **DEFER until 0.4.0.** Run a forward-test that compares "narrower workflow + entry classification in adapter rules" against the master workflow. If no quality lift, drop. |
| 24 | **Add `pm-roadmap`.** Themes, sequencing, dependencies, capacity, confidence bands. Owns the "feature requests → roadmap" hero workflow the design doc named but never built. | Quarterly mandatory deliverable for every senior PM. Currently nothing produces the roadmap artifact. | Risks colonizing `pm-strategy/prioritization`. Need a clean boundary. | **DO IT** — boundary is "strategy chooses bets; roadmap sequences chosen bets into a presentable artifact." |
| 25 | **Add `pm-metrics`.** North-star metric trees, input metrics, guardrails, KPI design. | Cited as a deferred gap in `findings.md` line 64. Every other artifact loses anchoring without it (PRD "success metrics" sections are wildly variable in quality today). | `pm-growth` already touches metrics. Risk of duplication. | **DO IT** — boundary is "metrics defines the tree; growth consumes the tree to find leverage." |
| 26 | **Add `pm-stakeholder-comms`.** Exec updates, status memos, decision memos, ask framing. | Most frequent under-served PM job. The package generates artifacts but doesn't help PMs socialize them. | Risks being a wrapper around generic memo-writing. | **CONDITIONAL** — only add if pm-roadmap and pm-metrics are added first. Stakeholder comms can also live as procedures inside pm-delivery (status) + pm-gtm (launch comms). Lower priority than 24 and 25. |

**Strategic-bundle recommendation:** Do #21 (drop pm-tooling) + #24 (add pm-roadmap) + #25 (add pm-metrics). That's a 1-for-2 net add. Defer #22, #23, #26 until 0.4.0. This keeps the package focused on the wedge (evidence → PRD → delivery) while closing the two highest-leverage missing artifacts.

---

## What's working well — don't break

For balance, the audits identified patterns worth preserving and propagating:

1. **`pm-strategy`'s "Method Selection" block** — the only skill that gives the LLM an explicit decision rule for sub-procedures. Pattern to copy into `pm-growth` and `pm-discovery`.
2. **`pm-discovery`'s "Output Standard"** (`evidence_ledger` / batch / dedupe / conflict register) — gold-standard for what every artifact-producing skill should require.
3. **The three workflow procedure files** (Entry Conditions / Workflow Steps / Intermediate Artifacts / Stop Points / Fallbacks / Handoff Contract / Completion Standard) — template for what leaf procedures should aspire to.
4. **`templates/research-plan.md`** — the only template with real per-section prose guidance. Model others on this (especially `prd.md`).
5. **Schema strictness on linear-issue + notion-page** — conditional `if mode=confirmed_write then required:...` is the right safety pattern. Don't loosen.
6. **References are all load-bearing.** All 35 reference docs are cited at least once. No reference cleanup needed.
7. **Adapter design is correct** — thin shims, no logic duplication, low maintenance cost. Adapters didn't fail at all.
8. **Negative-test refusal posture** — 18/18 correct refusals across runners. The package's safety floor holds.
9. **Workflow orchestration is real, not narrative.** Workflow procedures delegate to sibling skills via explicit relative paths (15+ deep references). The composition story works.
10. **Cross-runner depth gradient is informative** (Claude > Codex >> Gemini). Use Gemini's behavior as the "shallowest plausible runtime" and harden the grader against it.

---

## Suggested execution sequence

If shipping 0.2.2 as a quick-fix release:
- All Tier-1 (#1-9). One day's work. Re-run the test suite, expect Gemini scores to drop on hardened evals — that's the point.

If shipping 0.3.0 as a structural release:
- Tier-1 done first.
- Then Tier-2 #10-12 (grader hardening) — this is the most important block because the test-suite credibility is the foundation for every future change.
- Then Tier-2 #13-20 in any order, parallelizable.
- Strategic bundle (#21 + #24 + #25) folded in once Tier-1 is settled.

Defer #22, #23, #26 to 0.4.0 after seeing forward-test data on whether the master workflow earns its slot.

---

## Open questions to decide before 0.3.0

1. **Does the package want PRD-as-artifact or PRD-as-discipline?** Determines whether `pm-docs` stays or merges.
2. **Is `workflow-product-operating-system` load-bearing or vestigial?** Need an A/B forward-test before dropping.
3. **Should the grader add an LLM-judge pass** for substance, or stay deterministic and add minimum-content thresholds? Sub-agent C leans toward both (thresholds first, LLM-judge as a secondary verifier).
4. **Should `decision_status` enums be merged with the lifecycle status enum**, or kept distinct with explicit mapping? Affects schema breaking changes.

These are decisions only the package owner can make. Audits identify them; they don't resolve them.
