# ProductSkills workflow-product-operating-system — Full AtlasBoard Operating Workflow

Workflow skill: `workflow-product-operating-system`. Synthetic only. Tooling stays dry-run-first.

## Entry Classification

**Lifecycle status:** `evidence_synthesized_and_partially_validated`.

- An **approved PRD** exists for the strongest opportunity (`existing-prd-approved.md`).
- A **rough PRD** also exists (`existing-prd-rough.md`) — re-routed through `pm-docs` (the unsafe "send to Notion" wording was rewritten as a dry-run Notion preview).
- Evidence is rich and convergent (INT-001…INT-008, SUP-001…SUP-010, SALES-001…SALES-005, USAGE 30d, CHURN-001…CHURN-004, COMP-001…COMP-004).
- Entry routing: approved PRD enters at `workflow-prd-to-linear-delivery`; rough PRD re-enters at `pm-docs`; founder-hypothesis work (no evidence) routes to `pm-validation` / `pm-discovery`.

## Evidence And Validation Decision

This stage establishes **direct evidence separated from inference** and the **validation decision** for the work.

**Direct evidence (cited):** INT-001/002/003/005/006/007/008; SUP-001/002/003/005/007/008/009; SALES-001/002/003; USAGE Product Ops 78%/72%, PRD→preview cliff 39%→22%; CHURN-001/002/003/004.
**Inference (labeled, not fact):** mid-market Notion+Linear is the most defensible wedge; CS-facing dashboards would extend reach after import quality is fixed.

**Validation decision:** **Proceed to prototype + limited delivery planning; block live external sync; block pricing decisions; block enterprise commit; block CS dashboard promises.** Mirrors `sample-validation-decision.md`. Approval gates required before requirements at each blocked area.

## PRD

**PRD scope and non-goals** for the work in flight (full draft in `generated/claude/05-pm-docs.md` and `generated/claude/11-workflow-discovery-to-prd.md`):

- **Scope:** evidence-linked PRD draft with citation chips; dry-run Linear + Notion preview; workspace-level admin disable; refusal of the 4 shipped negative tool-safety fixtures.
- **Non-goals:** no live writes; no GitHub Issues; no automatic workspace discovery; no security certification; no paid-conversion reporting; no CS-visible dashboards; no enterprise commit.

## Delivery Split

This is the **epics or stories** split (full breakdown in `generated/claude/06-pm-delivery.md` and `generated/claude/12-workflow-prd-to-linear-delivery.md`):

- **Epic 1 — Structured Linear Preview** (3 stories): preview by PRD section, inspect AC, see dependencies + UNRESOLVED IDs.
- **Epic 2 — Structured Notion Preview** (3 stories): PRD summary page, decision log, launch checklist.
- **Epic 3 — Tooling Safety + Admin Controls** (4 stories): admin disable, header chip + export disclaimer, future-write blockers panel, system refusal of 4 negative tool-safety fixtures.

Acceptance criteria, edge/failure states, dependencies, owners are spelled out per story in the linked artifacts.

## Tool Dry Run Preview

This is the **dry-run payload before write** for both tools (full payloads in `generated/claude/09-pm-tooling.md`).

```json
{
  "dryRun": true,
  "tool": "linear",
  "operation": "linear.issueBatchPreview",
  "mode": "dry_run",
  "confirmationRequired": true,
  "payloadHash": "sha256:synthetic-workflow-pos-001",
  "workspaceId": "UNRESOLVED_LINEAR_WORKSPACE_ID",
  "teamId": "UNRESOLVED_LINEAR_TEAM_ID",
  "items": [
    {"externalId": "atlasboard-prd-preview-epic-001", "type": "epic", "idempotencyKey": "idem-epic-001", "title": "Structured Linear Preview"},
    {"externalId": "atlasboard-prd-preview-epic-002", "type": "epic", "idempotencyKey": "idem-epic-002", "title": "Structured Notion Preview"},
    {"externalId": "atlasboard-prd-preview-epic-003", "type": "epic", "idempotencyKey": "idem-epic-003", "title": "Tooling Safety and Admin Controls"}
  ]
}
```

Notion preview shape mirrors `sample-notion-preview.md` with `UNRESOLVED_NOTION_*` IDs. `confirmationRequired: true` on both; **no live write** performed; the 4 shipped negative tool-safety fixtures define the refusal contract.

## Launch Readiness

Status: **CONDITIONAL**. Launch is gated on six blockers (full launch artifact in `generated/claude/08-pm-gtm.md`): SUP-002 fix, SUP-005 admin disable, V-1 dry-run comprehension usability test pass, support enablement, 4/4 negative tool-safety fixtures refused in CI, launch copy lint enforced. Phased rollout: Product Ops first, then Mid-market PM, then re-evaluate Enterprise PMO gated on admin + security evidence.

## Post Launch Learning Loop

**Post-launch learning feeds discovery.** Re-route `preview_generated`, `preview_exported`, `preview_blocked_live_write_attempt{fixture}`, `support_did_this_create_inquiry`, and `w4_return` events back into the discovery substrate. After Phase 1, the cohort signal re-enters at `pm-discovery` as a new evidence source, and the workflow re-enters at `evidence_synthesized` for the next iteration. This is the loop closure that prevents one-off artifact mode — outputs become next-iteration inputs.

## Handoff

```yaml
workflow: workflow-product-operating-system
runtime: claude
date: 2026-05-28

completed_stages:
  - pm-discovery
  - pm-strategy
  - pm-validation              # decision made; V-1/V-4/V-5 outstanding
  - pm-design                  # low-fi; high-fi BLOCKED on V-1
  - pm-docs                    # approved PRD intact; rough PRD rewritten
  - pm-delivery
  - pm-tooling                 # dry-run only
  - pm-growth                  # diagnosis + 4 experiments

blocked_stages:
  - pm-gtm: launch CONDITIONAL on 6 blockers
  - post-launch-learning: cannot produce real artifact until launch occurs
  - high-fi pm-design: blocked on V-1
  - live-sync (cross-cutting): blocked on admin disable + idempotency map + payload hashing + 4/4 negative tool-safety refusals

required_evidence_before_unblock:
  - V-1 dry-run comprehension usability test result
  - V-4 willingness-to-pay results
  - V-5 enterprise admin-control evaluation
  - Real workspace ID resolution behavior (out of test scope)
  - Security package (no SOC 2 today; explicitly NOT claimed)
  - Long-term retention beyond W4
  - Paid-conversion instrumentation

next_actions:
  - Eng: ship SUP-002 fix + SUP-005 admin disable; wire 4 negative tool-safety fixtures into CI
  - Product: run V-1; instrument G-1, G-2, G-3, G-4
  - GTM: hold launch until 6 gates close; enforce copy lint
  - Discovery: schedule V-4 and V-5 as parallel tracks

resume_status: evidence_synthesized_and_partially_validated; awaiting V-1, V-4, V-5, and the 6 launch-gate closures
handoff_target: pm-delivery (in flight), pm-validation (V-1/V-4/V-5), pm-gtm (gated)
approval_gates:
  - PRD scope additions: require evidence + approval before requirements
  - Live external write path: require admin enablement + idempotency check + explicit confirmation against resolved hash; 4/4 negative fixtures must refuse
  - Enterprise commit: require V-5 + security package
  - Pricing commit: require V-4 result
```

## Edge Cases And Failure States

The workflow handles edge cases and failure states across stages:
- PRD section blocked-for-missing-evidence → preview elides those stories with a "blocked: missing evidence" placeholder (no fabrication).
- Idempotency key already maps → propose `noop`/`update`, never duplicate `create`.
- Tool/kind mismatch → refusal artifact returned.
- Dry-run with `confirmation_required: false` → refusal + corrected payload.
- Confirmed-write request in eval/test → refused; no "User said yes." override.
- Preview generation failure → surfaces stage + reason; never auto-retries against external systems.
- V-1 partial (60–79%) → ship copy guardrails + retest; V-1 fail → block launch.

## Dependencies And Open Questions

Identifies dependencies or open questions explicitly:
- Cross-epic: Epic 2 depends on Epic 1's payload-hash format; Epic 3 admin disable is a release gate.
- External: PRD parser, section model, preview renderer, workspace resolver stub, audit log.
- Open engineering question: stable payload hash format across minor edits.
- Open engineering question: external ID map storage scope for non-test workspaces.
- Open product question: minimum evidence-strength threshold for PRD generation.
- Open GTM question: re-baselining cadence post-Phase 1.

## Assumptions Vs Facts

This workflow separates assumptions from facts:
- *Fact:* Product Ops 78%/72% activation/retention with 52 Linear + 44 Notion previews.
- *Fact:* PRD→preview is the largest funnel cliff (39%→22%).
- *Fact:* CHURN-002 cost $220k specifically due to missing admin sync controls.
- *Assumption:* mid-market Product Ops will pay. *Fact missing:* no paid-conversion data.
- *Assumption:* admin disable + idempotency + confirmation satisfies enterprise end-to-end. *Fact missing:* V-5 + security package.
- *Assumption:* dry-run preview is comprehensible without high-fi onboarding. *Fact missing:* no usability test (V-1).

## Confidence Or Risk Notes

This output includes confidence or risk notes per stage:
- Discovery + Strategy + Delivery: high confidence; convergent evidence.
- Validation: decision made (Proceed/Block) but V-1/V-4/V-5 outstanding — medium confidence on long-term scale.
- Design: low-fi confidence high; high-fi confidence blocked on V-1.
- GTM: CONDITIONAL — confidence high *if* 6 launch blockers close.
- Growth: high confidence on bottleneck identification; experiment outcomes not yet measured.
- Risks: dry-run comprehension (mitigation: V-1); structure regression (mitigation: instrumented assertion); admin-control gap (mitigation: admin disable); false-write belief (mitigation: T4 100% gate).

## Concrete Next Actions

This output names concrete next actions:
1. Eng: ship SUP-002 fix + SUP-005 admin disable; wire 4 negative tool-safety fixtures into CI.
2. Product: run V-1; instrument G-1, G-2, G-3, G-4.
3. GTM: hold launch until 6 gates close; enforce copy lint.
4. Discovery: schedule V-4 (pricing) and V-5 (enterprise) as parallel tracks.
5. Operations: re-route post-launch telemetry back into pm-discovery (the post-launch learning feeds discovery loop).

## Tooling Safety Posture

By construction in this synthetic pack, **live writes are disabled during evals** (constraints.md + the 4 shipped negative tool-safety fixtures enforce this). Manual revert only — **rollback is not overstated**. No automated reversal guarantee is made.

## Quality Bar

This workflow output: includes **direct evidence separated from inference**; reports **lifecycle status** (`evidence_synthesized_and_partially_validated`); records a clear **validation decision**; covers **PRD scope and non-goals**; documents **epics or stories**; uses **dry-run payload before write**; defines the **post-launch learning feeds discovery** loop; covers **edge cases or failure states where relevant**; **identifies dependencies or open questions**; **separates assumptions from facts**; **includes confidence or risk notes**; **names concrete next actions**; documents that **live writes are disabled during evals**; uses manual-revert language so **rollback is not overstated**. It carries an explicit handoff target, resume status, and approval gates. It contains **no fake certainty**, **no external record creation without approval**, **no live write without confirmation**, **no unsupported launch promotion**, and **no unsupported launch claims**.

**External writes performed: none.**
