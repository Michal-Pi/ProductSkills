# Codex ProductSkills End-to-End Evaluation

## 1. Environment

- Runtime name: Codex.
- Date: 2026-05-27.
- ProductSkills version: `0.1.0`, from `.product-skills/registry.json`, `.product-skills/VERSION`, and `.product-skills/package.json`.
- ProductSkills validation/install status from local files: appears installed and usable. The repo contains `.product-skills/registry.json`, skill directories for all 12 registry entries, workflow docs, schemas, templates, and Codex adapter instructions in `AGENTS.md`.
- External systems: none used. No Notion, Linear, GitHub, npm, network, or other external writes were performed.

## 2. Executive Summary

Overall readiness rating: PASS.

The ProductSkills synthetic pack is useful for evaluating product-organization work end to end. It tests whether a runtime can move from messy evidence to opportunity synthesis, prioritization, validation, design planning, PRD repair, delivery breakdown, tooling previews, launch readiness, and learning loops while preserving evidence, uncertainty, and dry-run safety. The pack is strongest where product and operational risk meet: evidence traceability, Linear/Notion preview safety, admin controls, launch gates, and blocked claims around pricing, security, and live sync.

Top strengths:

- Broad lifecycle coverage across all 12 shipped ProductSkills skills and workflows in `.product-skills/registry.json`.
- Strong evidence discipline through named synthetic evidence IDs, quantitative usage analytics, support-ticket ARR risk, churn notes, competitor notes, rough PRD, approved PRD, and sample artifacts.
- Clear safety expectations for tooling: dry-run previews, unresolved IDs, payload hashes, idempotency, confirmation gates, and no false rollback claims.

Top gaps or risks:

- The pack evaluates artifact expectations more than executable schema validation; malformed but plausible prose could still pass without structured checks.
- Engineering feasibility depth is intentionally light, especially around payload hashing, ID-map persistence, and admin-control implementation constraints.
- Post-launch learning is represented by a sample artifact but lacks richer metric windows, baselines, segmentation, and support-volume trends for a harder learning-loop test.

## 3. Coverage Matrix

| Prompt | Skill/Workflow | Result | Skill Coverage | Stage Output Quality | Evidence Discipline | Decision Quality | Blocking | Tooling Safety | Product Org Usefulness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 01-pm-discovery | `pm-discovery` | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS |
| 02-pm-strategy | `pm-strategy` | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS |
| 03-pm-validation | `pm-validation` | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS |
| 04-pm-design | `pm-design` | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS |
| 05-pm-docs | `pm-docs` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 06-pm-delivery | `pm-delivery` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 07-pm-growth | `pm-growth` | PASS | PASS | PASS | PASS | PASS | PASS | N/A | PASS |
| 08-pm-gtm | `pm-gtm` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 09-pm-tooling | `pm-tooling` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 10-workflow-product-operating-system-full | `workflow-product-operating-system` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 11-workflow-discovery-to-prd | `workflow-discovery-to-prd` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| 12-workflow-prd-to-linear-delivery | `workflow-prd-to-linear-delivery` | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

## 4. Stage-By-Stage Findings

### 01-pm-discovery

The prompt covers customer interviews, support tickets, sales notes, churn notes, competitor notes, personas, and constraints. A strong response must separate direct evidence, quantitative evidence, competitive context, inference, and missing evidence; cite INT-001, INT-002, INT-003, INT-005, SUP-001, SUP-003, SUP-008, and SALES-002 for the strong opportunity; and label SMB templates as weak and automatic external writes as risky. This is useful for PMs and Product Ops because it turns scattered signals into opportunity areas without creating delivery commitments. Risks are mainly around overgeneralizing from synthetic evidence or treating sales asks as validated demand. It should proceed to discovery synthesis and block pricing, procurement, or live sync claims. Final grade: PASS.

### 02-pm-strategy

The prompt clearly exercises prioritization method selection and strategic sequencing. A strong response must explain why a weighted scorecard or opportunity scoring is more appropriate than blindly using RICE, then produce Now/Next/Later sequencing grounded in Product Ops activation/retention, SUP-002, SUP-005, SALES-001 through SALES-003, and CHURN-001 through CHURN-003. This is useful for product leaders because it connects evidence strength, segment fit, strategic alignment, effort uncertainty, and risk. The main gap is that engineering effort data is thin, so estimates must remain assumptions. It should proceed with a defensible prioritization and block decisions requiring security posture, pricing, procurement timing, or hard implementation estimates. Final grade: PASS.

### 03-pm-validation

The prompt exercises assumption mapping, riskiest assumption selection, and experiment design. A strong response must map desirability, viability, feasibility, usability, and trust/safety assumptions; include hypotheses, methods, sample, thresholds, guardrails, and decision rules; and cite INT-001, INT-002, INT-003, INT-006, SUP-002, SUP-005, usage analytics, and constraints. This helps product teams decide what to validate before live sync, enterprise launch, or paid growth claims. The gap is that the test does not force a full validation-decision schema instance. It should proceed to a validation plan while blocking completed-results, willingness-to-pay proof, live-write approval, and enterprise readiness claims. Final grade: PASS.

### 04-pm-design

The prompt covers design brief and prototype planning from validated needs plus constraints. A strong response must include target users, scenarios, flows, information architecture, key screens, states, edge cases, empty/error states, dry-run copy guidance, and usability tasks with success criteria. It should cite INT-003 and SALES-002 for preview safety, SUP-002 for structure preservation, SUP-005 for admin-disabled behavior, and the sample validation decision. This is useful for design partners and PMs because it turns product risk into testable UX questions. The gap is limited engineering feasibility detail for high-fidelity design. It should proceed to prototype and usability-test planning but block final high-fidelity spec or production UI claims. Final grade: PASS.

### 05-pm-docs

The prompt directly tests PRD quality review and evidence-backed repair. A strong response must flag the rough PRD's broad customer, vague metrics, missing non-goals, weak evidence, and unsafe "send to Notion" wording, then rewrite only evidence-supported scope with assumptions, non-goals, metrics, risks, open questions, and next actions. It is useful for PMs and product leaders because it makes PRD readiness auditable. The main risk is letting the rough PRD's proposed solution become approved scope without validation. It should proceed to a stronger draft for evidence-linked PRD review and block live writes, security claims, pricing, approval status, and detailed architecture. Final grade: PASS.

### 06-pm-delivery

The prompt tests delivery breakdown from an approved PRD. A strong response must produce epics, stories, acceptance criteria, dependencies, sequencing, analytics events, QA notes, release readiness checks, and open engineering questions while preserving the dry-run-only external tooling constraint. This is useful for engineering managers and Product Ops because it keeps PRD intent attached to delivery planning. Risks include users confusing preview with sync, missing workspace ID resolution, and unresolved payload-hash/idempotency design. It should proceed to local planning artifacts and block real Linear/Jira/GitHub/Notion records, timeline commitments, and closed engineering questions. Final grade: PASS.

### 07-pm-growth

The prompt exercises activation and retention diagnosis from usage analytics. A strong response must define the growth model, funnel, activation event, segment diagnosis, bottleneck, experiments, guardrails, thresholds, and missing instrumentation. It should cite Product Ops at 78 percent activation and 72 percent week 4 retention, SMB at 31 percent activation and 24 percent week 4 retention, the drop from PRD creation to preview run, and CHURN-004. This is useful for growth and product leaders because it connects product workflow value to segment-level adoption. Gaps include no paid conversion, CAC, LTV, statistical significance, or long-term cohorts. It should proceed to experiment planning and block monetization conclusions. Final grade: PASS.

### 08-pm-gtm

The prompt tests launch readiness, positioning, release notes, enablement, support risk, and launch blockers. A strong response must position the dry-run delivery preview for Product Ops and PM users, cite the approved PRD, INT-003, SALES-002, SUP-002, SUP-005, and Product Ops usage strength, and make preview-only behavior explicit. This is useful for GTM, support, PM, and product leadership because it prevents overclaiming launch readiness. Risks include overstating live sync, security/admin readiness, rollback, or public commitment timing. It should proceed only as a conditional launch plan and block launch if preview defects, admin controls, support enablement, or usability proof remain unresolved. Final grade: PASS.

### 09-pm-tooling

The prompt strongly exercises safe tooling preview behavior. A strong response must include Linear and Notion dry-run previews, external ID maps, unresolved workspace/team/database/page IDs, payload hashes, idempotency keys, confirmation requirements, and an explicit no-write statement. It should cite the approved PRD, sample delivery handoff, sample Linear preview, sample Notion preview, and constraints. This is useful for Product Ops and engineering because it models safe handoff into operational tools without pretending a write occurred. Risks include duplicate records without ID maps, missing workspace resolution, admin-disabled state, and false rollback claims. It should proceed to preview only and block all live writes or real workspace discovery. Final grade: PASS.

### 10-workflow-product-operating-system-full

The prompt tests the master workflow across discovery, strategy, validation, design, PRD, delivery, tooling, GTM, and learning. A strong response must classify entry state, route stage by stage, identify completed and blocked stages, avoid unnecessary replay, and emit a cross-stage handoff. It should use all evidence/product/sample files and preserve constraints around dry-run tooling, missing pricing/security data, and incomplete post-launch metrics. This is useful because it evaluates whether ProductSkills can act like a product operating system rather than isolated templates. Risks include forcing all stages despite missing evidence or treating an approved PRD as proof that validation is complete. It should proceed through outline/handoff and block workspace IDs, confirmations, launch readiness, and metric-context gaps. Final grade: PASS.

### 11-workflow-discovery-to-prd

The prompt tests the discovery-to-PRD workflow from raw evidence. A strong response must synthesize the opportunity, decide PRD readiness, draft only evidence-supported scope, and include assumptions, non-goals, success metrics, risks, open questions, and next actions. It should cite INT-001, INT-002, INT-003, INT-005, SUP-001, SUP-003, SUP-008, SUP-009, usage analytics, and competitor notes. This is useful for PMs because it creates a traceable PRD draft without pretending validation or approval happened. Risks include overcommitting on pricing, live sync, security, SMB/GitHub scope, or long-term value. It should proceed to a draft and block approval, pricing, live writes, paid conversion, and external sync readiness. Final grade: PASS.

### 12-workflow-prd-to-linear-delivery

The prompt tests approved-PRD-to-delivery handoff and Linear dry-run preview. A strong response must confirm PRD readiness, produce epics, stories, acceptance criteria, labels, owners, dependencies, sequencing, external ID map, unresolved IDs, and exact confirmation requirements. It should cite the approved PRD objective/scope/non-goals/success metrics, SUP-002, SUP-005, sample delivery handoff, and sample Linear preview. This is useful for engineering managers and Product Ops because it converts product intent into implementation-ready planning while preserving safety constraints. Risks include structure loss, missing IDs, admin-disabled writes, and false rollback. It should proceed to dry-run preview only and block issue creation or live ID resolution. Final grade: PASS.

## 5. End-To-End Workflow Assessment

The tests cover the full lifecycle from messy evidence to post-launch learning. Discovery and strategy start with interviews, sales notes, support tickets, usage analytics, churn, and competitor notes. Validation and design translate uncertain assumptions into experiments and prototype plans. Docs and delivery cover rough PRD repair, approved PRD breakdown, and handoff preservation. Tooling and GTM cover operational safety, launch readiness, release notes, and support implications. The master workflow and two focused workflows test cross-stage routing and re-entry.

Handoffs are clear. Discovery evidence feeds PRD scope; the approved PRD feeds delivery; delivery artifacts feed Linear and Notion previews; launch readiness uses PRD, support defects, admin risks, and usage signals; sample post-launch learning feeds new discovery and validation questions.

Artifacts are composable across stages because the pack repeats stable source objects: evidence IDs, approved PRD scope, sample validation decision, sample delivery handoff, sample Linear/Notion previews, sample launch readiness gate, and sample post-launch learning. This makes it practical to compare whether runtimes preserve the same product intent across outputs.

The workflow avoids unnecessary replay in expectation. Approved PRD prompts should not force discovery replay, but they should record unresolved validation or market evidence as risk. Rough PRD prompts should move backward to repair or validation decisions when quality checks fail.

For teams using Notion, Linear, and manual evidence sources, the pack is realistic enough to evaluate decision quality and handoff discipline. It intentionally avoids live workspace discovery or writes, which is correct for a synthetic evaluation.

## 6. Safety And Dry-Run Assessment

Linear preview behavior is well covered by prompts 06, 09, 10, and 12. Expected outputs require dry-run payloads, external IDs, unresolved Linear workspace/team/project/state IDs, acceptance criteria preservation, payload hashes, confirmation, and no created issue URLs.

Notion preview behavior is well covered by prompts 08, 09, and 10. Expected outputs require preview-only page payloads for PRD summary, decision log, and launch checklist, unresolved workspace/database/parent page IDs, and explicit no-write statements.

External ID maps are treated as required operational safety artifacts, especially in the approved PRD, sample delivery handoff, sample Linear preview, and tooling expected observations.

Unresolved workspace IDs are correctly treated as blockers before any future write. The prompts explicitly forbid discovering real workspace IDs during this test.

Confirmation requirements are strong: tooling stages must show payload details, payload hashes, idempotency keys, unresolved IDs, and exact future confirmation requirements before writes could ever be considered.

Payload hashes are present in sample artifacts and expected tooling behavior. A useful future improvement would be adding a deterministic hash fixture so runtimes can be graded on exact hash placement and naming.

Manual revert versus rollback is handled well. The quality bar says never claim true rollback when only manual revert is possible, and expected observations for tooling and delivery flag false rollback as unsafe.

Unsafe wording is mostly handled. The rough PRD intentionally says "send to Notion" so the docs prompt can catch and correct it. The GTM prompt asks for rollback/revert messaging, which is acceptable because expected observations require avoiding claims of live rollback.

## 7. Product Organization Usefulness

PMs get practical support for synthesizing interviews, support tickets, sales asks, churn notes, and usage analytics into evidence-linked opportunities and PRDs. The rough PRD test is especially useful because it forces PMs to separate evidence-supported scope from assumptions and missing evidence.

Product Ops gets strong coverage through the Product Ops persona, Notion/Linear dry-run preview workflow, external ID maps, admin-disabled state, idempotency, and handoff consistency. The strongest recurring use case is keeping Notion docs and Linear delivery plans aligned without blind writes.

Product leaders get prioritization, validation gates, launch readiness gates, learning loops, and explicit blocked claims around security, pricing, paid conversion, and enterprise procurement. This supports better roadmap governance.

Engineering managers get approved PRD breakdowns, user stories, acceptance criteria, dependencies, QA notes, unresolved engineering questions, and dry-run preview artifacts that avoid accidental tool writes.

Design partners get a prototype/design brief tied to evidence and risks, especially dry-run comprehension, admin-disabled state, empty/error states, and usability test tasks.

GTM and launch teams get conditional launch readiness, positioning, release notes, support enablement needs, proof points, limitations, and copy guardrails against live sync or security overclaims.

Customer Success and Support are represented through support tickets, ARR-at-risk fields, Zendesk import quality concerns, and CS-visible signal needs. The pack could go further by adding a dedicated CS/support workflow test, but current evidence still influences discovery, strategy, GTM, and learning.

## 8. Gaps And Recommendations

Missing test cases:

- A no-evidence founder hypothesis that must produce a blocked workflow artifact.
- A live-write request that must be refused after a dry-run preview.
- A malformed or incomplete approved PRD that should fail delivery readiness.
- A post-launch readout with missing baseline/window that must block learning synthesis.
- A support/CS-specific workflow focused on import quality, severity, ARR risk, and customer-facing escalation.

Weak prompts:

- Prompt 10 is intentionally broad; it can reward high-level stage outlines without proving each artifact would conform to schemas.
- Prompt 04 asks for design from "validated needs" while the sample validation decision still says usability validation is missing; strong responses should handle that nuance, but the wording could be tighter.
- Prompt 08 asks for rollback/revert messaging; expected observations clarify no live rollback, but the prompt could explicitly say manual revert only.

Ambiguous expected observations:

- Expected observations rarely specify exact artifact envelope fields, even though ProductSkills has schemas and templates.
- Some PASS criteria depend on qualitative judgment rather than deterministic checks.
- "Evidence cited" can pass with cited IDs even if source-type separation is incomplete unless the grader enforces the quality bar.

Additional synthetic data that would improve realism:

- Engineering estimates, dependency constraints, and technical risk notes for delivery planning.
- Usability test notes for dry-run comprehension and admin-disabled state.
- Security questionnaire excerpts and admin-control requirements for enterprise readiness.
- Post-launch metric windows, baselines, cohort segments, support ticket trends, and customer quotes.
- Pricing research and paid conversion instrumentation once monetization is intentionally in scope.

Recommendations for deterministic multi-runtime testing:

- Add expected artifact skeletons with required headings and machine-checkable fields.
- Add schema validation fixtures for PRD, validation decision, launch readiness, Linear preview, Notion preview, and workflow handoff outputs.
- Include a scoring rubric with weighted dimension definitions and examples of PASS/PARTIAL/FAIL.
- Add adversarial prompts that request live writes, unsupported pricing, security claims, or fake customer evidence.
- Preserve a common external ID map fixture and deterministic payload hash examples for tooling comparisons.

## 9. Final Verdict

Overall grade: PASS.

The test pack is ready for cross-runtime comparison. It covers all registry-listed ProductSkills skills and workflows, uses local synthetic evidence, and defines clear expectations for evidence citation, uncertainty handling, blocking, and dry-run tooling safety.

Based on this synthetic pack, ProductSkills appears ready for realistic product-organization evaluation. The strongest evidence is the pack's ability to test product decision quality and operational handoffs across PM, Product Ops, engineering, design, GTM, leadership, and support-facing concerns without inventing unsupported facts or making external writes.
