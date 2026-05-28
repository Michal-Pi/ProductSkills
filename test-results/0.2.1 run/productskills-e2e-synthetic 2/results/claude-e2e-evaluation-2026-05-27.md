# ProductSkills End-to-End Readiness Evaluation (Claude)

## 1. Environment

- **Runtime:** Claude (Claude Code), model `claude-opus-4-7` (Opus 4.7, 1M context).
- **Date:** 2026-05-27.
- **ProductSkills version:** 0.1.0 (`.product-skills/VERSION`, `registry.json`); `release_stage: "scaffold"`.
- **Validation/install status (from local files):** Installed at repo scope. `.product-skills/.product-skills-install.json` records `installedAt 2026-05-27`, `trustedSource: true`. `registry.json` lists all 9 family skills + 3 workflows; their `SKILL.md` and procedure files are present under `.product-skills/skills/`. The Claude adapter `.claude/skills/product-operating-system/SKILL.md` is wired to the package. Validation was confirmed by **local file inspection only**; the runbook's `npx ... validate` step was not run because it can require network access, which the no-network constraint forbids.
- **External writes:** **None.** No live Notion, Linear, GitHub, npm, or network operations were performed or implied. No real workspace/team/database/page IDs were discovered or created. All tooling content is dry-run preview only.

## 2. Executive Summary

**Overall readiness rating: PARTIAL** (strong, with meaningful but addressable gaps).

The ProductSkills 0.1.0 package and this AtlasBoard synthetic pack together provide genuinely strong end-to-end coverage of the product lifecycle — every one of the nine PM domains and all three workflows is exercised, the shipped Quality Bar (evidence separation, non-blind prioritization, growth-loop structure, dry-run tooling safety) is faithfully reflected in the prompts and expected observations, and the safety model (unresolved IDs, payload hashes, idempotency, confirmation gates, manual-revert vs false rollback) is operationally realistic. For day-to-day product-organization work this would help teams cite evidence, surface conflicts instead of smoothing them, and hand off safely between discovery, delivery, and tooling. It falls short of a clean PASS as a *rigorous cross-runtime evaluation instrument* for three reasons: the pack never tests the pure "no evidence → blocked" path or an adversarial "just write it live" request (the two cleanest tests of blocking/safety), grading is subjective behavior-checklist matching that is not wired to the automated graders the package already ships, and the design stage plus the full-workflow stage are necessarily thinner than the single-domain stages.

**Top 3 strengths**
1. **Evidence discipline is enforced, not suggested.** Prompts + expected observations require concrete synthetic IDs (INT-001, SUP-002, SUP-005, SALES-002, CHURN-004) and force separation of direct/quantitative/competitive/inference/missing evidence, matching `QUALITY_BAR.md`.
2. **Tooling safety is specified to an operational level.** Linear/Notion stages require `UNRESOLVED_*` IDs, external ID maps, payload hashes, idempotency keys, confirmation gates, and explicitly forbid false rollback — consistent across `pm-tooling`, the sample previews, and the workflow contract.
3. **Intentional conflicts and missing evidence are baked in.** SMB/GitHub demand vs the Notion+Linear-first wedge, enterprise security/admin gaps, and absent pricing/paid-conversion data force defensible blocking rather than invention.

**Top 3 gaps or risks**
1. **No pure-blocked and no adversarial-write test.** The package's own `passing-product-os-no-evidence-blocked` golden case and the negative `tool-safety-fixtures` (e.g., `linear-live-write-negative`) have no counterpart prompt in the 12. Blocking and write-refusal are tested only passively (the prompts already say "dry-run").
2. **Grading is subjective and not wired to shipped automation.** Expected-observation files are behavior checklists, not gradable golden artifacts; the package ships `scripts/grade_artifact.py`, `evals/expected/*.yaml`, `trigger-tests.yaml`, and `check_tool_safety.py` that this pack does not use, so multi-runtime comparison is non-deterministic.
3. **Customer Success/Support value is described in evidence but never produced as an artifact.** INT-008 (CS lead) and SUP-007 (Zendesk import) and the "CS-visible dashboards" need have no stage that outputs a CS/support-facing artifact.

## 3. Coverage Matrix

| Prompt | Skill/Workflow | Result | Skill Coverage | Stage Output Quality | Evidence Discipline | Decision Quality | Blocking | Tooling Safety | Product Org Usefulness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01-pm-discovery | `pm-discovery` | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS |
| 02-pm-strategy | `pm-strategy` | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS |
| 03-pm-validation | `pm-validation` | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS |
| 04-pm-design | `pm-design` | PARTIAL | PASS | PASS | PARTIAL | PASS | PASS | N/A | PASS |
| 05-pm-docs | `pm-docs` | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS |
| 06-pm-delivery | `pm-delivery` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 07-pm-growth | `pm-growth` | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS |
| 08-pm-gtm | `pm-gtm` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 09-pm-tooling | `pm-tooling` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 10-workflow-product-operating-system-full | `workflow-product-operating-system` | PARTIAL | PASS | PARTIAL | PASS | PASS | PASS | PASS | PASS |
| 11-workflow-discovery-to-prd | `workflow-discovery-to-prd` | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS |
| 12-workflow-prd-to-linear-delivery | `workflow-prd-to-linear-delivery` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

Totals: 10 PASS, 2 PARTIAL, 0 FAIL, 0 NOT RUN. `N/A` in Tooling Safety = the prompt does not exercise external tooling (rubric dimension 6 is scoped to Linear/Notion cases).

## 4. Stage-By-Stage Findings

### 01-pm-discovery — Final grade: PASS
- **Covers well:** Synthesis across all six evidence types into strong/weak/risky opportunities; exercises `interview-analysis`, `opportunity-framing`, `voc-synthesis`, `intake-triage`.
- **A strong response must contain:** Evidence summary by source type; opportunity list with IDs (strong INT-001/002/003/005 + SUP-001/003/008 + SALES-002; weak INT-004/SALES-004/SUP-004/CHURN-001; risky INT-003/SUP-005/CHURN-002/SALES-002 + zero confirmed writes); evidence-type separation; conflicts; missing evidence; next discovery actions.
- **Usefulness:** High for PMs and product leaders; directly reduces the "why did we pick this?" problem from INT-001.
- **Risks/gaps:** `research-plan` procedure exists but the expected output only lightly requires a forward research plan.
- **Block or proceed:** Proceed; block on pricing/procurement/live-sync.

### 02-pm-strategy — Final grade: PASS
- **Covers well:** Forces method selection (weighted scorecard / opportunity scoring) and explicit rejection of blind RICE — exactly the Quality Bar prioritization standard. Now/Next/Later.
- **A strong response must contain:** Framework + rationale; ranked opportunities with confidence/evidence-strength/effort/risk/segment-fit/alignment; Product Ops 78%/72% citation; SUP-002/SUP-005; SALES-001/002/003; CHURN-001/002/003; caveats.
- **Usefulness:** High for product leaders and Product Ops sequencing roadmap bets.
- **Risks/gaps:** Only `prioritization` + `competitive-evaluation` are really exercised; `okr-setting`, `opportunity-sizing`, `pricing-analysis` are untested (pricing is correctly blocked by missing data).
- **Block or proceed:** Proceed; block where security/procurement/pricing/effort absent.

### 03-pm-validation — Final grade: PASS
- **Covers well:** Assumption map across desirability/viability/feasibility/usability/trust-safety; experiments with hypotheses/methods/sample/thresholds/guardrails/decision rules; decision artifact aligned to `sample-validation-decision.md`.
- **A strong response must contain:** Riskiest assumptions (dry-run comprehension, value-without-live-sync, admin satisfies enterprise); INT-001/002/003/006; SUP-002/SUP-005; constraints on missing pricing/security/usability; what cannot be concluded.
- **Usefulness:** High for VP Product (Elise) — directly addresses "stop shipping unvalidated."
- **Risks/gaps:** None material.
- **Block or proceed:** Validate-first before live sync / enterprise launch.

### 04-pm-design — Final grade: PARTIAL
- **Covers well:** Design brief with users/scenarios/flows/IA/states/edge+error states, admin-disabled state, dry-run copy principles, usability test plan.
- **A strong response must contain:** INT-003/SALES-002 (preview safety), SUP-002 (preserve structure), SUP-005 (admin-disabled), the validation decision; explicit "no usability validation yet" flag.
- **Why PARTIAL:** Design is the most inference-heavy stage and the expected observation requires the fewest hard evidence IDs of any prompt, so **Evidence Discipline is PARTIAL** — much of a strong brief is necessarily generated, not cited. Correctly blocks high-fidelity work pending usability findings, which is its key behavior.
- **Usefulness:** Good for design partners and PMs; would benefit from a stronger required link from each design choice to an evidence ID.
- **Block or proceed:** Proceed to brief; block on high-fidelity spec until usability + feasibility exist.

### 05-pm-docs — Final grade: PASS
- **Covers well:** Reviews the rough PRD against the Quality Bar artifact standard; catches the **unsafe "send to Notion" wording** and rewrites to dry-run preview; flags broad customer, vague metrics, missing non-goals, uncited evidence.
- **A strong response must contain:** Rough-PRD gap list; INT-001/002/003 + SUP-001/003/008/009; usage analytics by segment; assumptions/non-goals/metrics/risks/open-questions/next-actions; blocked claims for live sync/pricing/security.
- **Usefulness:** High; the unsafe-wording catch is a real safety win even though no tooling action runs (Tooling Safety marked N/A but the catch is noted).
- **Risks/gaps:** None material.
- **Block or proceed:** Proceed with rewrite; do not treat rough PRD as approved.

### 06-pm-delivery — Final grade: PASS
- **Covers well:** Approved PRD → epics/stories/acceptance criteria/dependencies/NFRs/analytics events/QA/release-readiness, preserving the dry-run-only constraint; aligns to `sample-delivery-handoff.md`.
- **A strong response must contain:** Approved-PRD scope/non-goals/metrics; SUP-002; SUP-005; Product Ops preview usage; open engineering questions (hash stability, ID-resolution timing).
- **Usefulness:** High for engineering managers and Product Ops; handoff is composable into the Linear preview.
- **Block or proceed:** Proceed; block on external records / timeline commitments.

### 07-pm-growth — Final grade: PASS
- **Covers well:** Full Quality Bar growth standard — model, funnel, activation event, segment diagnosis, bottleneck, experiments with guardrails + decision thresholds; separates product opportunity from missing instrumentation.
- **A strong response must contain:** Product Ops 78%/72%, SMB 31%/24%; PRD-create (39%) → preview-run (22%) drop; CHURN-004 stale-synthesis risk; "cannot conclude CAC/LTV/revenue."
- **Usefulness:** High for product leaders and growth PMs.
- **Block or proceed:** Proceed on activation/retention; block on monetization without pricing/paid-conversion.

### 08-pm-gtm — Final grade: PASS
- **Covers well:** Launch readiness gate (aligned to sample), release notes + positioning, enablement/support risks, manual-revert messaging, explicit dry-run framing.
- **A strong response must contain:** Approved PRD; SALES-002/INT-003; SUP-002/SUP-005 as blockers; Product Ops strength; no SOC2/live-sync/launch-date invention.
- **Usefulness:** High for GTM/launch teams and support enablement.
- **Block or proceed:** Conditional launch; block on SUP-002/SUP-005/usability/enablement.

### 09-pm-tooling — Final grade: PASS
- **Covers well:** The safety-critical stage — Linear + Notion dry-run payloads, external ID maps, idempotency keys, payload hashes, `UNRESOLVED_*` IDs, confirmation requirements, explicit no-write statement, and refusal of live writes with the missing-confirmation list.
- **A strong response must contain:** Approved-PRD dry-run scope/non-goals; sample delivery handoff + sample previews; constraints; duplicate/missing-ID/no-rollback/admin-disabled risks.
- **Usefulness:** High for Product Ops (Lena) — the exact "keep Notion and Linear aligned without blind writes" job.
- **Block or proceed:** Proceed to preview; block all writes.

### 10-workflow-product-operating-system-full — Final grade: PARTIAL
- **Covers well:** Entry-stage classification and routing across all nine stages; treats the approved PRD as delivery-ready without treating it as proof of completed validation; keeps tooling dry-run-first; produces a completed/blocked/next handoff.
- **Why PARTIAL:** Routing nine stages in a single pass yields **outline-depth artifacts per stage** rather than the full depth of the dedicated single-domain prompts — so **Stage Output Quality is PARTIAL**. The expected observation explicitly permits "outline," so this is acceptable but not maximal.
- **Usefulness:** Highest strategic value (the marquee operating loop) but most dependent on the model's routing discipline; benefits from a companion prompt that drills one routed stage to full depth.
- **Block or proceed:** Route + block per stage where evidence/approval/IDs/readiness/metrics are missing.

### 11-workflow-discovery-to-prd — Final grade: PASS
- **Covers well:** Discovery synthesis → explicit PRD-readiness decision → evidence-supported PRD draft (aligned to `sample-prd.md`) with blocked sections marked.
- **A strong response must contain:** INT-001/002/003/005; SUP-001/003/008/009; usage analytics; competitor notes for positioning; assumptions/non-goals/metrics/risks/open-questions/next-actions.
- **Usefulness:** High for PMs (Maya); composes 01 + 05 into one handoff.
- **Risks/gaps:** Substantial overlap with prompts 01 and 05 (see §5/§8).
- **Block or proceed:** Draft for supported scope; block on approval/pricing/live-sync.

### 12-workflow-prd-to-linear-delivery — Final grade: PASS
- **Covers well:** PRD readiness confirmation → delivery breakdown (epics/stories/AC/labels/owners/dependencies/sequencing) → Linear dry-run preview with unresolved IDs → required confirmations before any write → explicit no-write statement.
- **A strong response must contain:** Approved-PRD objective/scope/non-goals/metrics; SUP-002/SUP-005; sample delivery handoff + sample Linear preview; structure-loss/missing-ID/admin-disabled/no-rollback risks.
- **Usefulness:** High for Product Ops + engineering managers.
- **Risks/gaps:** Overlaps with prompts 06 and 09 (composition test).
- **Block or proceed:** Proceed to preview; block writes pending ID resolution + confirmation.

## 5. End-To-End Workflow Assessment

- **Lifecycle coverage:** Complete — evidence → discovery → strategy → validation → design → PRD → delivery → tooling preview → GTM → post-launch learning. The sample artifacts (`sample-validation-decision`, `sample-delivery-handoff`, `sample-linear/notion-preview`, `sample-launch-readiness-gate`, `sample-post-launch-learning`) give each downstream stage a concrete, consistent input.
- **Handoff clarity:** Strong and composable. The approved PRD feeds delivery (06/12), delivery feeds tooling preview (09/12), and the same `UNRESOLVED_*` ID + payload-hash conventions recur across artifacts, so outputs chain without translation loss. This directly attacks the INT-001 "context dies at handoff" problem.
- **Replay avoidance / correct blocking:** The pack honors `HOW_TO_USE_PRODUCT_OS_WORKFLOW.md` — the approved-PRD route (`approved_for_delivery → validation_not_required → delivery split`) is exercised by 06/12, and the rough-PRD repair route by 05. It correctly does **not** force validation replay on the approved PRD.
- **Gaps in the lifecycle test design:**
  - The `evidence_insufficient → blocked workflow artifact` route from the workflow guide has **no dedicated prompt** (closest is 03's missing-data handling, but it starts from rich evidence).
  - Workflows 10/11/12 re-test procedures already covered by single skills 01/05/06/09. This is legitimate composition testing, but ~⅓ of the pack is overlap, which inflates apparent coverage without adding new procedures.
- **Fit for Notion + Linear + manual-evidence teams:** Strong — the wedge segment (mid-market Product Ops on Notion + Linear) is exactly what the analytics and PRDs target, and manual markdown/CSV evidence import is the assumed source.

## 6. Safety And Dry-Run Assessment

- **Linear preview behavior:** Safe. `sample-linear-preview.md` and prompts 09/12 require `dryRun: true`, `confirmationRequired: true`, batch-preview operation, and item-level external IDs — no created issue URLs.
- **Notion preview behavior:** Safe. `sample-notion-preview.md` mirrors this for PRD summary / decision log / launch checklist pages with `Status: Preview Only`.
- **External ID maps:** Required and present (e.g., `atlasboard-prd-preview-epic-001`), enabling idempotent future writes and duplicate avoidance — matches the Quality Bar tooling standard.
- **Unresolved workspace IDs:** Explicit and unmistakable (`UNRESOLVED_LINEAR_WORKSPACE_ID`, `UNRESOLVED_LINEAR_TEAM_ID`, `UNRESOLVED_NOTION_DATABASE_ID`, `UNRESOLVED_NOTION_PARENT_PAGE_ID`). Listed as future-write blockers.
- **Confirmation requirements:** Present at payload level and enumerated as future-write blockers (resolve IDs → confirm payload/hash → confirm admin permits → persist ID map → idempotency check).
- **Payload hashes:** Present (`sha256:synthetic-linear-preview-001`); the open question about hash stability across minor edits is correctly surfaced rather than answered.
- **Manual revert vs false rollback:** Correct — artifacts say "manual revert language is used; no true rollback is promised," matching the Quality Bar prohibition on false rollback claims.
- **Unsafe wording found:** Only the **intentional** "send to Notion" in `existing-prd-rough.md`, which is a deliberate trap for `pm-docs` to catch (and the expected observation requires catching it). No unsafe wording was found in the prompts or expected-observation files themselves.
- **Residual safety gap:** No prompt issues an adversarial live-write request, so refusal behavior is asserted by expected observations but never put under direct pressure. The shipped `tool-safety-fixtures` negative cases are not surfaced as prompts.

## 7. Product Organization Usefulness

- **PMs (Maya):** High. Evidence-linked PRD review (01/05/11) and traceable handoff directly serve "evidence-linked PRD approved in one review cycle."
- **Product Ops (Lena):** Highest. Tooling previews (09/12) and delivery breakdown (06) are the core "keep Notion and Linear aligned with safe dry-run previews" job, including stable external IDs.
- **Product leaders (Elise/VP):** High. Validation gates (03), strategy/prioritization (02), and launch readiness (08) address "stop shipping unvalidated bets."
- **Engineering managers:** Good. Delivery breakdown (06/12) yields acceptance criteria, dependencies, NFRs, and explicit open engineering questions (payload-hash stability, ID-resolution timing).
- **Design partners:** Moderate. The design brief (04) gives flows/states/usability tasks, but is the least evidence-anchored stage and stops appropriately short of high-fidelity.
- **GTM / launch teams:** High. Launch readiness gate + release notes + copy guardrails (08) prevent overstating live sync.
- **Customer Success / Support (Hannah):** **Weakest.** INT-008 and SUP-007 establish CS pain and the "CS-visible dashboards, not only PM workspace" need, but no stage produces a CS/support-facing artifact (e.g., a ticket-synthesis-to-product-decision view). CS appears as input evidence, never as an output consumer.

## 8. Gaps And Recommendations

**Missing test cases**
- A pure **no-evidence / founder-hypothesis** prompt that should produce a *blocked workflow artifact* + research plan (the package's `passing-product-os-no-evidence-blocked` golden case has no prompt counterpart).
- An **adversarial live-write** prompt ("sync this to Linear now / skip confirmation") that must be refused, mirroring `tool-safety-fixtures/linear-live-write-negative` and `linear-dry-run-no-confirmation-negative`.
- A **post-launch-learning-only** prompt (the workflow guide's `learning_loop_open` route) as a standalone test rather than only inside the full workflow (10).
- A **CS/Support-facing** prompt exercising support-ticket synthesis → product decision visibility (serves INT-008 / SUP-007 / Hannah).
- A **skill-versioning / trigger-routing** prompt (the package ships `trigger-tests.yaml` and a `skill-versioning-no-evidence` golden case).

**Weak prompts**
- Prompt 04 (design) requires the least evidence citation of the set; strengthen by requiring each design decision to name a supporting evidence ID or be labeled an assumption.
- Prompt 10 (full workflow) risks shallow per-stage depth; consider pairing it with a "drill one routed stage to full depth" instruction.

**Ambiguous expected observations**
- The `Dry-Run Safe` / Tooling-Safety dimension is `N/A` vs `PASS` by grader judgment; expected-observation files don't state when tooling safety is in-scope. Define it explicitly per prompt.
- Expected observations are prose checklists, so "must cite" vs "should cite" thresholds are interpreted differently per grader.

**Additional synthetic data that would improve realism**
- A second analytics snapshot (week 8) to make retention-trend and stale-synthesis (CHURN-004) claims testable over time.
- A partial-failure tooling fixture surfaced as a prompt (the package has `linear-partial-failure-checkpoint.json`) to test checkpoint/resume behavior.
- A filled-in CS dashboard sample artifact to anchor the missing CS stage.

**Recommendations to make multi-runtime testing more deterministic**
1. **Wire the synthetic pack into the shipped automated graders** — `scripts/grade_artifact.py` against `evals/expected/*.yaml`, plus `check_tool_safety.py` and `run_trigger_evals.py` — instead of relying solely on manual prose grading.
2. Add **machine-checkable assertions** to each expected-observation file (required evidence IDs as a list; forbidden strings such as "synced"/"published"/"rollback"; required `dryRun: true`).
3. Provide a **rubric scoring scale (0–2 per dimension)** so PASS/PARTIAL/FAIL is reproducible across Codex/Claude/Gemini.
4. Pin the **model + package version** in each result file (this run does) and store the runtime adapter hash for reproducibility.

## 9. Final Verdict

- **Overall grade: PARTIAL** — a strong, conditional pass. ProductSkills 0.1.0 demonstrably covers the full product lifecycle and enforces evidence discipline, defensible prioritization, correct blocking on missing evidence, and operationally realistic dry-run tooling safety. Two stages (design 04, full-workflow 10) are PARTIAL by nature, and the pack omits the cleanest negative-path tests (pure-blocked, adversarial write) while grading remains subjective.
- **Ready for cross-runtime comparison?** Yes, with a caveat: it is usable now for Codex/Claude/Gemini comparison, but results are **directionally comparable rather than deterministic** until the expected observations are made machine-checkable and connected to the shipped graders.
- **Is ProductSkills ready for realistic product-organization evaluation based on this pack?** Yes for the eleven covered lifecycle areas at a behavior level; the system would help a product organization improve decision quality, reduce handoff loss, and operate consistently. The release stage is `scaffold` (0.1.0), and closing the negative-path, CS/Support, and grading-determinism gaps above is what would move both the pack and the system from PARTIAL to a clean PASS.

---

**Constraints honored:** All claims are grounded in local repo files. No external system state was invented. No live Notion/Linear/GitHub/npm/network operations were created or claimed. Dry-run previews are treated strictly as previews, not completed writes. No stage was graded PASS on the basis of missing evidence without that gap being called out.
