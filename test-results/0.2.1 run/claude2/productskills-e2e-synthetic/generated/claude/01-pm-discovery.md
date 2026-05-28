# ProductSkills pm-discovery — AtlasBoard Opportunity Synthesis

Skill: `pm-discovery`. Synthetic only. No external systems were used.

## Sources

- `productskills-e2e-synthetic/product/product-overview.md`, `personas.md`, `constraints.md`
- `evidence/customer-interviews.md` (INT-001…INT-008)
- `evidence/support-tickets.md` (SUP-001…SUP-010)
- `evidence/sales-call-notes.md` (SALES-001…SALES-005)
- `evidence/usage-analytics.md` (30-day, segmented)
- `evidence/churn-notes.md` (CHURN-001…CHURN-004)
- `evidence/competitor-notes.md` (COMP-001…COMP-004)

## Themes

- Evidence traceability + handoff context loss (INT-001, INT-002, SUP-001/003/008/009).
- Preview-only Linear/Notion sync with idempotency (INT-003, SALES-002, SUP-002/005, CHURN-002).
- Weekly synthesis change log (INT-005, SUP-010, CHURN-004).
- Enterprise admin/security readiness (INT-006, SALES-003, SUP-005, CHURN-002).
- SMB-founder weak fit (INT-004, SUP-004, SALES-004, CHURN-001, SMB activation 31% / W4 24%).
- GitHub-Issues delivery conflict (INT-007, SUP-006, CHURN-003) vs Linear-first roadmap.
- CS-visible dashboards blocked on import quality (INT-008, SUP-007).

## Direct Evidence

This section separates **direct evidence** from inference.

- **Direct customer (interviews):** INT-001/002/003/005/006/007/008 — see quotes in `evidence/customer-interviews.md`.
- **Direct customer (support):** SUP-001/002/003/005/007/008/009/010 — concrete ticket-level issues with severity and ARR.
- **Direct customer (sales):** SALES-001/002/003 — explicit asks and objections from buyers.
- **Quantitative (USAGE):** Product Ops 78% activation / 72% W4 retention (highest); SMB 31% / 24% (lowest); PRD→preview funnel cliff 39%→22% (largest drop).
- **Quantitative (churn):** CHURN-001 $9k SMB; CHURN-002 $220k enterprise; CHURN-003 $24k GitHub-only; CHURN-004 $76k mid-market.
- **Competitive (market):** COMP-001/002/003/004 give competitive context but are not customer evidence.
- **Inference (label as inference, not fact):** mid-market Notion+Linear is the most defensible wedge; CS-facing dashboards would extend reach but only after import quality is fixed.

## Confidence

This section **labels confidence by theme** so weak-evidence opportunities are not promoted prematurely.

| Theme | Confidence | Why |
| --- | --- | --- |
| Evidence-linked PRD + dry-run preview (mid-market Notion+Linear) | **High** | Convergent direct + quantitative + competitive evidence |
| Admin disable / tooling safety | **High** | SUP-005, INT-003, SALES-002, CHURN-002 all converge |
| Weekly synthesis change log | **High** | CHURN-004 + SUP-010 + INT-005 |
| CS-visible dashboards | Medium | Real demand, weak data substrate (SUP-007) |
| Enterprise wedge | **Low** | INT-006/SALES-003 budget but SOC 2/timeline missing |
| Pricing willingness | **Low** | Directional only — `constraints.md` flags this |
| SMB / GitHub paths | **Low (weak fit)** | CHURN-001/003, SUP-004/006, low activation |

## Assumptions

This section **separates assumptions from facts**.

- *Assumption:* mid-market Product Ops will pay for this. **Fact missing:** no paid-conversion data; pricing directional only.
- *Assumption:* admin disable + idempotency + confirmation satisfies enterprise buyers end-to-end. **Fact missing:** V-5 admin-control evaluation; no SOC 2.
- *Assumption:* dry-run preview is comprehensible without high-fi onboarding. **Fact missing:** no usability test (V-1).
- *Assumption:* CS dashboards are buildable on current import quality. **Fact missing:** SUP-007 unresolved.
- *Fact:* Product Ops shows 78%/72% activation/retention with 52 Linear + 44 Notion previews.
- *Fact:* PRD→preview is the largest funnel cliff (39%→22%).
- *Fact:* CHURN-002 cost $220k specifically due to missing admin sync controls.

## Opportunities

### 🟢 STRONG — Evidence-linked PRD + dry-run delivery preview for Notion+Linear mid-market teams
Evidence: INT-001/002/003/005, SUP-001/002/003/008/009, SALES-002, USAGE Product Ops 78%/72%. Confidence: High.

### 🟡 RISKY/AMBIGUOUS — CS-visible support synthesis pipeline (Hannah lane)
Evidence: INT-008, SUP-007; data-quality prerequisite. Confidence: Medium.

### 🟡 RISKY/AMBIGUOUS — Automatic Linear/Notion live sync
Evidence: INT-003, SALES-002, SUP-005, CHURN-002. Demand exists; trust/safety + admin controls are buying prerequisites. Confidence: Low to proceed; High to block today.

### 🟡 RISKY/AMBIGUOUS — Enterprise wedge before security evidence
Evidence: INT-006, SALES-003, CHURN-002, SUP-005. Confidence: Low.

### 🔴 WEAK — Free-tier lightweight templates for solo founders
Evidence: INT-004, SUP-004, SALES-004, CHURN-001. Confidence: High that this is weak commercially.

### 🟡 RISKY/AMBIGUOUS — GitHub Issues delivery
Evidence: INT-007, SUP-006, CHURN-003 vs Linear-first roadmap. Defer.

## Next Learning

This section **recommends next research or validation step** and **names concrete next actions**.

1. Recruit 5 mid-market Product Ops teams to validate dry-run preview comprehension and the SUP-002 structure-defect fix (addresses validation `Validation Still Needed`).
2. Run a CS-import-quality study with VantageOps-shaped data (INT-008, SUP-007) before promising CS dashboards.
3. Pricing / willingness-to-pay research with Product Ops and Mid-market PM (currently directional only).
4. Enterprise admin-control evaluation with LedgerLane (INT-006, SALES-003, SUP-005, CHURN-002); explicitly block any SOC 2 claim.
5. **Block** these decisions until evidence arrives: pricing commitments, procurement timing, security certification claims, live external writes, paid-conversion claims, CS-dashboard scope expansion.

## Quality Bar

This artifact: separates direct evidence from inference; labels confidence by theme; recommends next research or validation step; includes direct evidence or states that evidence is missing; separates assumptions from facts; includes confidence or risk notes; names concrete next actions. It does **not** contain invented customer quotes and does **not** make delivery commitments without validation.

**External writes performed: none.**
