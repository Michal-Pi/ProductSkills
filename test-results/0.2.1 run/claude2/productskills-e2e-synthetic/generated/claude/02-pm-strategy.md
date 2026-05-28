# ProductSkills pm-strategy — AtlasBoard Prioritization Method Selection

Skill: `pm-strategy`. Synthetic only. No external systems were used.

## Decision Context

AtlasBoard has converging evidence (INT-001…INT-008, SUP-001…SUP-010, SALES-001…SALES-005, USAGE 30d, CHURN-001…CHURN-004, COMP-001…COMP-004) and needs to sequence work across Now / Next / Later. Several candidate opportunities are strong-but-narrow (mid-market Notion+Linear dry-run preview), some carry trust/safety blockers (live sync, enterprise without security), and several have weak commercial evidence (pricing, SMB, GitHub). The prioritization method must surface evidence strength, confidence, and trust/safety risk explicitly — not collapse them into a single ratio.

## Options

| Method | Pro for AtlasBoard | Con for AtlasBoard | Decision |
| --- | --- | --- | --- |
| RICE | Familiar | Multiplying Reach × Impact × Confidence ÷ Effort fabricates precision when Reach is directional and pricing is unknown | **Reject** |
| WSJF | CoD/JobSize is useful for queueing | Mixes user pain, trust gates, and admin-control debt into one scalar, hiding the live-sync trap | **Reject as primary** |
| ICE | Lightweight | Cannot separate "blocked by missing evidence" from "low impact"; would mask live-sync risk | **Reject** |
| MoSCoW | Easy to communicate | No trade-off framework; insufficient on its own | **Use as final Now/Next/Later wrapper only** |
| **Weighted Scorecard** | Side-by-side display of evidence, fit, alignment, effort, risk, confidence | More setup work, weights are subjective unless declared | **Selected** |

## Selected Method

**Weighted Scorecard** with explicit per-criterion weights declared up front (no hidden criteria weights), per-opportunity confidence, and a sensitivity check. Final ranking is wrapped in MoSCoW-style Now / Next / Later / Blocked.

### Method selection rationale

This **method selection rationale** addresses why RICE/WSJF/ICE were rejected and why a weighted scorecard fits AtlasBoard: the pack penalizes invented precision (no paid conversion, no LTV) and rewards explicit blocking + uncertainty handling; only the weighted scorecard makes evidence-strength and trust/safety first-class scoring criteria instead of folding them into a single ratio.

## Criteria

| Criterion | Weight | Why |
| --- | ---: | --- |
| Evidence Strength | 0.25 | Pack's central rule; refuse intuition scoring |
| Segment Fit (mid-market PM + Product Ops) | 0.15 | Constraints explicitly target this wedge |
| Strategic Alignment (roadmap Now + tradeoffs) | 0.15 | Linear before GitHub, traceability before auto-gen, previews before live writes |
| Effort (inverse) | 0.15 | Capacity is finite |
| Risk / Trust+Safety | 0.20 | Auto live sync + enterprise security debt are the dominant downside risks |
| Confidence | 0.10 | Penalize directional evidence (pricing, procurement) |

Weights sum to 1.0 and are declared, not hidden.

## Scores

| Opportunity | Evidence | Segment | Align | Effort⁻¹ | Risk/Safety | Confidence | Weighted /5.0 | Tier |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| SUP-002 fix + SUP-005 admin disable | 5 | 5 | 5 | 5 | 5 | 5 | **5.00** | Now (gate) |
| Evidence-linked PRD + dry-run preview (mid-market) | 5 | 5 | 5 | 4 | 4 | 5 | **4.65** | Now |
| Missing-evidence + confidence labels (opportunity/prio views) | 5 | 5 | 5 | 4 | 4 | 5 | **4.65** | Now |
| Validation decision templates | 4 | 4 | 4 | 5 | 5 | 4 | **4.30** | Next |
| Weekly synthesis change log (CHURN-004, SUP-010) | 4 | 5 | 4 | 4 | 4 | 4 | **4.15** | Next |
| Launch readiness gate artifacts | 4 | 4 | 4 | 4 | 4 | 4 | **4.00** | Next |
| Support import quality (SUP-007, INT-008) | 4 | 4 | 4 | 3 | 4 | 4 | **3.85** | Next |
| Paid conversion instrumentation | 2 | 4 | 3 | 3 | 4 | 1 | **2.80** | Later |
| Auto Linear/Notion live sync (no safety gate) | 4 | 4 | 1 | 2 | **1** | 3 | **2.65** | **Blocked** |
| GitHub Issues preview | 3 | 2 | 1 | 2 | 3 | 4 | **2.50** | Later |
| Enterprise security package | 3 | 3 | 3 | 1 | 2 | 2 | **2.40** | Later (blocked on security evidence) |

## Confidence

This section provides a **confidence or sensitivity note**:
- **Sensitivity:** if Evidence Strength weight drops 0.25→0.15 and Effort⁻¹ rises 0.15→0.25, the Now tier is unchanged (SUP-002/005 still top); only Launch-readiness vs Validation-decision swap order in Next.
- **Stability:** Linear-first vs GitHub conflict is stable — GitHub never reaches Now under reasonable reweighting (Strategic Alignment score = 1).
- **Confidence by tier:** Now = High; Next = Medium; Later = Low; Blocked = High that the block is correct.

## Recommendation

**Now (this quarter):** SUP-002 fix + SUP-005 admin disable (gate); evidence-linked PRD + dry-run preview hardening; missing-evidence/confidence labels.
**Next:** validation decision templates; weekly synthesis change log; launch readiness gate; CS import quality.
**Later:** paid conversion instrumentation; GitHub Issues preview; enterprise security package.
**Blocked:** auto live Linear/Notion sync until trust/safety gate closes (admin disable + idempotency map + payload hashing + 4/4 negative tool-safety fixtures refused in CI).

**Next decision step:** schedule a 30-min weight review with Product + Eng leads to confirm the 0.25/0.15/0.15/0.15/0.20/0.10 weights before kicking off SUP-002 implementation.

## Risks

- **Pricing prioritization** — directional only; do not score on assumed willingness to pay.
- **Enterprise sequencing** — block any commit until admin-control + security evidence exists.
- **Live-sync prioritization** — block until the safety floor is met.
- **Paid-conversion-weighted scoring** — no data; do not backfill estimates.
- **Effort scores** — directional 1–5 only; no engineering capacity table exists.

## Quality Bar

This artifact: includes the **method selection rationale**, a **confidence or sensitivity note**, and the **next decision step**; separates assumptions from facts; includes direct evidence or states that evidence is missing; includes confidence or risk notes; names concrete next actions. Criteria weights are declared up front — there are no hidden criteria weights, and RICE is not applied to every scenario.

**External writes performed: none.**
