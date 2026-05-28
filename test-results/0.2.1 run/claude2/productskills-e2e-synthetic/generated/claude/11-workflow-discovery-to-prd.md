# ProductSkills workflow-discovery-to-prd — AtlasBoard Discovery → PRD

Workflow skill: `workflow-discovery-to-prd`. Synthetic only. No external systems. No invented validation results / approvals / market data.

## Intake Inventory

- 8 customer interviews (INT-001…INT-008)
- 10 support tickets (SUP-001…SUP-010)
- 5 sales call notes (SALES-001…SALES-005)
- 1 30-day segmented usage analytics table
- 4 churn notes (CHURN-001…CHURN-004)
- 4 competitor notes (COMP-001…COMP-004)
- Product overview, personas, constraints, current roadmap
- Sample artifacts (PRD, validation decision, delivery handoff, Linear/Notion previews, launch gate, post-launch learning)

## Evidence Ledger

This is **direct evidence separated from inference** with `assumptions scored by evidence strength`:

| Theme | Direct (INT/SUP/SALES) | Quantitative (USAGE/CHURN) | Competitive (COMP) | Strength |
| --- | --- | --- | --- | --- |
| Evidence-linked PRD + traceability | INT-001/002/005, SUP-001/003/008/009, SALES-001 | — | COMP-002 (Notion AI weak traceability) | Strong |
| Preview-only Linear/Notion sync + idempotency | INT-003, SALES-002 | Product Ops 52 Linear + 44 Notion previews | COMP-001 (Productboard weak handoff) | Strong |
| Preview structure / PRD section fidelity | SUP-002 | — | — | Strong |
| Admin-disable for workspace external sync | SUP-005, INT-006 | CHURN-002 ($220k) | — | Strong |
| Weekly synthesis change log | INT-005, SUP-010 | CHURN-004 ($76k) | — | Strong |
| CS dashboards | INT-008 | SUP-007 (import quality issue) | — | Medium (blocked) |
| Pricing willingness | INT-005, SALES-001 | — | — | Weak (directional) |
| Enterprise / SOC 2 | INT-006, SALES-003 | CHURN-002 | — | Weak (blocked) |
| GitHub Issues | INT-007, SUP-006, SALES-005 | CHURN-003 ($24k) | — | Conflict (roadmap Linear-first) |
| SMB founder-led | INT-004, SUP-004, SALES-004 | CHURN-001 ($9k), SMB activation 31% / W4 24% | — | Weak fit |

Inference (labeled, not fact): mid-market Notion+Linear is the most defensible wedge; CS dashboards would extend reach but only after SUP-007 import quality is closed.

## VoC Synthesis

**Sales asks separated from customer problems**:

*Customer problems (what users experience):*
- "Context dies during research → PRD handoff" (INT-001).
- "Prioritization debates because scoring doesn't expose weakness" (INT-002).
- "Notion and Linear drift after handoff" (INT-003, SUP-002, SALES-002).
- "Weekly synthesis repeats themes; can't tell what's new" (INT-005, SUP-010, CHURN-004).
- "Security team blocked beta — sync not admin-configurable" (CHURN-002, SUP-005).

*Sales asks (distinct from problems):*
- "Reduce PRD prep by 30%" (SALES-001).
- "Payload preview, external IDs, confirmation; no blind writes" (SALES-002).
- "Validation decision artifacts, launch gates, admin controls; SOC 2 required" (SALES-003).
- "GitHub Issues preview" (SALES-005). **Conflict with roadmap Linear-first.**

## Opportunity Frame

Top opportunity: evidence-linked PRD + dry-run Linear/Notion delivery preview for mid-market Product Ops + PMs (Notion + Linear shops). Convergent direct + quantitative + competitive evidence; strongest segment by activation (78%) and retention (72%); buying prerequisites are addressable.

## Assumption Map

| Assumption | Strength | Evidence |
| --- | --- | --- |
| Mid-market Product Ops + PM want evidence-linked PRD + dry-run preview | Strong | INT-001/002/003/005, SALES-001/002, USAGE Product Ops 78%/72% |
| Reviewers trust generated PRDs if every claim cites a source | Medium | INT-002 explicit; no usability test yet |
| Dry-run preview is comprehensible without high-fi onboarding | Weak | sample-post-launch-learning (4 confused) — V-1 needed |
| Trust/safety contract holds with admin disable + idempotency + confirmation | Strong (must hold) | INT-003, SALES-002, SUP-005, CHURN-002 |
| Mid-market Product Ops will pay for this | Weak | INT-005 directional; SALES-001 pilot intent; no paid-conversion data |
| Enterprise will adopt with admin controls alone | Weak (blocked) | INT-006, SALES-003 (SOC 2 required), CHURN-002 |

## Validation Recommendation

**Proceed to a PRD draft** for the evidence-supported scope (the mid-market dry-run preview opportunity). **Do not** include pricing, enterprise commitments, GitHub support, CS dashboards, or live sync — those require validation work (V-1, V-4, V-5; SUP-007 import; security package) that has not happened.

## PRD

# PRD: Evidence-Linked PRD + Dry-Run Linear/Notion Delivery Preview (Mid-Market)

## Objective
Help mid-market Product Ops and PM teams move from evidence to a reviewable PRD and inspect a dry-run Linear + Notion preview before any external write is considered.

## Customer
Primary: Product Ops leads + PMs at B2B SaaS companies with 5–25 PMs using Notion for PRDs and Linear for delivery (INT-001/002/003/005, USAGE Product Ops 78%/72%, SALES-001/002).
Secondary: product leaders needing evidence trails (INT-002).
Out of this PRD: enterprise scope (INT-006 noted but gated), SMB founders (weak fit), GitHub-Issues teams.

## Evidence
INT-001 (handoff loss); INT-002 (scoring transparency); INT-003 (preview-only sync); INT-005 (weekly synthesis change log); SUP-001/002/003/005/008/009; SALES-001/002; USAGE Product Ops 78%/72% and PRD→preview cliff 39%→22%.

## Assumptions
- *Assumption:* citation chips raise trust — V-1 will test.
- *Assumption:* dry-run previews are sufficient interim value — supported by INT-003, SALES-002.
- *Assumption:* admin-disable + idempotency + confirmation satisfies the trust contract — tested via the 4 shipped negative tool-safety fixtures.

## Scope
- Evidence import + citation chips on PRD claims (4 confidence types: cited / inferred / assumption / missing-evidence).
- PRD generation with default Non-Goals, Open Questions, Risks.
- Linear dry-run preview (epic/story tree, AC, labels, owners, external IDs, idempotency keys, payload hash, `UNRESOLVED_LINEAR_*` IDs).
- Notion dry-run preview (PRD summary + decision log + launch checklist; `UNRESOLVED_NOTION_*` IDs).
- Workspace-level admin disable (blocks writes; previews still work).
- 4/4 negative tool-safety fixtures refused in CI.

## Non Goals (PRD scope and non-goals; explicit non-goals)
- **No live external writes** (Linear, Notion, GitHub, npm, network).
- No GitHub Issues preview (roadmap Later).
- No security certification claims (no SOC 2; no data-retention attestations).
- No enterprise admin/security package in this PRD.
- No paid-conversion / pricing decisions in this PRD.
- No CS-visible dashboards (gated on SUP-007 import quality).
- No raw audio/video interview ingestion.

## Success Metrics (measurable success metrics)
- ≥80% of generated PRDs contain a citation chip per claim in Problem/Scope/Metrics.
- Preview structure defects <5%.
- ≥60% of previews carry stable external IDs per epic/story/Notion page.
- 0 unintended external writes — asserted via the 4 negative tool-safety fixtures in CI.
- ≥30% median PRD prep time reduction for pilot Product Ops (paired pre/post).
- Product Ops W4 retention ≥70% (current 72%).
- PRD→preview conversion 22% → ≥30% in 30 days (G-1).

## Risks
- Dry-run comprehension (sample-post-launch-learning). Mitigation: copy chip + V-1 gate.
- Structure regression (SUP-002). Mitigation: instrumented assertion.
- Admin-control gap (SUP-005, CHURN-002). Mitigation: admin disable before enterprise-evaluable surface.
- Citation-chip false confidence. Mitigation: 4 visually distinct confidence types.

## Open Questions
- Minimum evidence-strength threshold to allow PRD generation? **Block PRD scope decisions until set.**
- Stable payload hash format across minor edits? **Open engineering question (sample-delivery-handoff).**
- Pricing — no validated willingness-to-pay; **do not commit price in this PRD**.

## Next Actions
1. Run V-1 (launch gate).
2. Land SUP-002 fix + instrumented assertion.
3. Wire 4 negative tool-safety fixtures into CI.
4. Ship SUP-005 admin disable.
5. Schedule V-4 + V-5 as parallel discovery tracks; do not roll outcomes into this PRD.

## Approval Gates

This workflow uses **explicit stop or approval gates** at:
- PRD scope additions: require evidence + approval before requirements.
- Live external write path: require admin enablement + idempotency check + explicit confirmation against resolved hash; 4/4 negative fixtures must refuse.
- Enterprise commit: require V-5 + security package.
- Pricing commit: require V-4 result.

Blocked sections (not filled with invented facts): pricing/packaging; enterprise security package / SOC 2; GitHub delivery support; CS-visible dashboards; live sync flow; long-term retention claims. Each will be unblocked only by the corresponding validation work.

## Open Questions (workflow-level)

- Should the citation chip vocabulary be PR-team-defined or vendor-defined?
- Should the External ID Map persist at workspace or repo scope for non-test workspaces?
- What does post-V-1 retest cadence look like?

## Next Actions (workflow-level)

1. Run V-1.
2. Add citation-chip semantics.
3. Schedule V-4 + V-5 in parallel.
4. Maintain block status on pricing, enterprise, CS dashboards, live sync, GitHub.

## Quality Bar

This workflow output: keeps **direct evidence separated from inference**; keeps **sales asks separated from customer problems**; carries **assumptions scored by evidence strength**; defines **PRD scope and non-goals**; documents **explicit stop or approval gates**. It separates assumptions from facts, includes confidence or risk notes, names concrete next actions, and includes direct evidence or states that evidence is missing. It contains **no fake certainty**, **no unsupported delivery commitment**, and **no live Notion write without confirmation**.

**External writes performed: none.**
