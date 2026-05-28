# ProductSkills pm-validation — AtlasBoard Validation Plan

Skill: `pm-validation`. Synthetic only. No users were contacted, no external systems used.

Top opportunity under validation: evidence-linked PRD + dry-run Linear/Notion delivery preview for mid-market Product Ops + PMs.

## Assumption Map

This is a **desirability viability feasibility usability trust safety** (DVFUT) decomposition.

| Dim | Assumption | Evidence For | Evidence Against / Gap | Strength |
| --- | --- | --- | --- | --- |
| Desirability | Mid-market Product Ops + PM want evidence-linked PRDs + dry-run previews | INT-001/002/003/005/006, SALES-001/002, SUP-001/003/008/009, USAGE Product Ops 78%/72% | SMB shows weak desirability (separate segment) | Strong |
| Desirability | Reviewers trust generated PRDs if every claim cites a source | INT-002 explicit | No usability test of citation comprehension | Medium |
| Viability | Product Ops + Mid-market is a paying segment | SALES-001/002 intent; INT-005 "would pay" | No paid-conversion data; pricing directional | Weak |
| Viability | Enterprise can be added with admin controls + security | INT-006, SALES-003, CHURN-002 | No SOC 2; no procurement timeline | Weak (blocked) |
| Feasibility | Stable payload hash + external ID map enables idempotent previews | sample-linear-preview/sample-notion-preview shapes; SUP-002 fix concrete | Open question on hash function stability | Medium |
| Feasibility | Admin-disabled state can fully block writes while allowing previews | sample-delivery-handoff Epic 3; constraints | Not yet implemented end-to-end | Medium |
| Usability | Users distinguish dry-run preview from completed sync | sample-post-launch-learning records 4 confused; copy guardrails defined | **No usability test has been run** | Weak |
| Trust/Safety | "No blind writes" + idempotency + confirmation satisfies buyers | INT-003, SALES-002, SUP-005 | None disconfirming | Strong (must hold) |
| Trust/Safety | CS import quality supports CS dashboards | INT-008 demand | SUP-007 + constraints flag inconsistent data | Weak |

## Riskiest Assumptions

1. **Usability** — dry-run preview comprehension. Weak evidence; catastrophic if it fails (users believe records were synced).
2. **Viability** — willingness-to-pay. Weak; pricing decisions block until validated.
3. **Trust/Safety** — end-to-end refusal contract. Strong but must hold; one live-write incident voids the buying argument.
4. **Feasibility** — admin-disabled state in implementation. Must pass the 4 shipped negative tool-safety fixtures.
5. **Usability** — citation-chip semantics differentiate cited/inferred/assumption/missing-evidence.

## Validation Experiments

Each experiment carries **hypothesis method sample success threshold guardrail**.

### V-1 — Dry-run comprehension usability test
- Hypothesis: ≥80% of Product Ops/PM participants unprompted identify that a dry-run preview did not write to Linear/Notion.
- Method: 1×1 moderated usability test.
- Sample: 8 Product Ops + 4 mid-market PMs.
- Success threshold: ≥80% T1 unprompted correct; 100% T4 (no false-write belief).
- Guardrail: any participant saying "I would have shared this thinking it was live" → ship copy/visual fix before launch.

### V-2 — Preview-to-export funnel + SUP-002 structure retest
- Hypothesis: structure defects <5%; preview-export ≥60% within 7 days.
- Method: instrument `preview_generated/exported/structure_defect_reported`; 30-day cohort vs pre-fix baseline.
- Sample: all Product Ops workspaces in beta (n=18).
- Success threshold: defects <5%; export ≥60%.
- Guardrail: `preview_structure_defect_reported` >5% → hold launch.

### V-3 — Tool-safety negative fixtures (refusal proof)
- Hypothesis: 4/4 shipped negatives refuse (`linear-live-write-negative`, `linear-dry-run-no-confirmation-negative`, `linear-duplicate-create-negative`, `notion-tool-kind-mismatch-negative`).
- Method: replay each fixture; assert refusal artifact not accepted payload.
- Sample: 4 fixtures × every PR touching tooling path.
- Success threshold: 4/4.
- Guardrail: any single acceptance → release block.

### V-4 — Willingness-to-pay interviews
- Hypothesis: ≥4 of 6 Product Ops leads give a verbal commit at a specific price with a follow-up step, after seeing previews + admin controls.
- Method: 6–8 pricing conversations, open-ended price range.
- Sample: 6–8 buyers at BuildLoop/CloudShelf-shaped accounts.
- Success threshold: ≥4/6 specific commits.
- Guardrail: do not anchor on a fabricated number.

### V-5 — Enterprise admin-control evaluation
- Hypothesis: with admin-disable + audit log + workspace controls, LedgerLane-shaped reviewers move past CHURN-002-style block.
- Method: walk reviewer through SUP-005-equivalent controls; capture objections.
- Sample: 1 enterprise eval cycle.
- Success threshold: no new blocking objections after demonstrating controls.
- Guardrail: do **not** claim SOC 2 during the eval.

## Decision Rules

- V-1: Pass → proceed to launch-readiness gate. Partial (60–79%) → copy guardrails + retest. Fail → block launch, redesign preview UX.
- V-2: defects <5% → ship; >5% → hold launch.
- V-3: 4/4 → ship; any acceptance → block release.
- V-4: ≥4/6 verbal commits → unlock pricing decision; otherwise continue value/proof work, **do not commit pricing**.
- V-5: clean run → unblock enterprise eval pathway; otherwise narrow scope and re-test.

## Validation Decision

**Proceed to prototype + limited delivery planning, but block live external sync; block pricing decisions; block enterprise commit; block CS dashboard promises.** This is the **proceed validate first or block decision** for the workflow.

## Cannot Conclude

It is **states validation results are missing** territory for:
- Dry-run comprehension (no usability test yet).
- Willingness-to-pay at any specific price (no pricing research).
- Enterprise security objection closure (no security evidence; no procurement timeline).
- CS dashboards on current import quality (SUP-007 unresolved).
- Live-sync safety (negative fixtures untested in this run).
- Long-term retention beyond W4 (no data).

## Next Actions

1. Run V-1 (gate launch).
2. Wire V-3 into CI on every tooling-path PR.
3. Instrument V-2 events.
4. Schedule V-4 + V-5 as parallel discovery tracks; do **not** roll outcomes into shipping decisions.
5. Maintain block status for live sync, pricing, enterprise commit, CS dashboards.

## Quality Bar

This artifact: covers **desirability viability feasibility usability trust safety**; defines **hypothesis method sample success threshold guardrail** per experiment; **states validation results are missing** for the items in Cannot Conclude; provides a **proceed validate first or block decision**. It separates assumptions from facts, includes confidence or risk notes, names concrete next actions, and includes direct evidence or states evidence is missing. It does **not** contain completed experiment results, does **not** claim validated willingness to pay, and does **not** claim live sync feasibility.

**External writes performed: none.**
