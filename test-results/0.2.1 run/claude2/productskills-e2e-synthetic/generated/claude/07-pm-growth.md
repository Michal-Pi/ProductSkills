# ProductSkills pm-growth — AtlasBoard Activation + Retention Diagnosis

Skill: `pm-growth`. Synthetic only. No external systems. No invented paid-conversion / CAC / LTV / long-term retention.

## Growth Model

AtlasBoard is a **product-led growth (PLG) workspace tool** with collaborative-team value. The relevant loop is value-driven, not virality-driven, so this analysis focuses on **activation and retention consideration** rather than acquisition (no acquisition data in the pack).

> Import evidence → synthesize opportunities → review/generate PRD → run delivery preview → export/share → second user joins → new evidence imported → repeat.

The funnel is the gating substrate; segment data tells us where it's healthy and where it isn't.

## Segment

| Segment | n | Activation | W4 Retention | Linear preview | Notion preview | Status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| **Product Ops** | 18 | **78%** | **72%** | 52 | 44 | Healthy — defend |
| **Mid-market PM** | 46 | 63% | 58% | 38 | 29 | Healthy but trailing |
| **Enterprise PMO** | 7 | 57% | 64% | 11 | 9 | Small n; admin-control gap likely material |
| **SMB founder-led** | 34 | **31%** | **24%** | 2 | 4 | Unhealthy — weak fit (INT-004, SUP-004, CHURN-001); do not invest |

Activation event (from USAGE Funnel Definitions, used as-is): workspace imports ≥10 evidence items, generates ≥3 opportunities, and creates or reviews ≥1 PRD within 7 days.

## Bottleneck

The largest single funnel cliff is **PRD-create-or-review (39%) → Run preview (22%) = −17pp**. This is the highest-leverage bottleneck.

## Evidence

- USAGE funnel: 100 → 62 → 71 → 54 → 47 → 39 → **22** → 51 (W4 return among preview-runners). The 39→22 drop is the largest.
- SUP-002 (BuildLoop, Product Ops, $142k ARR): Linear dry-run preview groups stories under one epic instead of preserving PRD sections — structural defect that discourages preview adoption.
- sample-post-launch-learning: among workspaces that *do* preview, 12/18 (67%) export markdown — value-capture post-first-preview is good. The problem is the gate between PRD and first preview, not the value after it.
- CHURN-004 (MarketPulse, mid-market, $76k): weekly synthesis didn't differentiate changed signals — adjacent retention risk pointing to the same insight (output quality drives next loop turn).
- INT-003 / SALES-002: trust contract (preview-only + idempotency + confirmation) is a prerequisite for any future live-sync growth claim.

## Hypotheses

- **H1:** Fixing SUP-002 + adding an in-PRD preview entry banner lifts PRD→preview conversion from 22% → ≥35% in Product Ops + Mid-market.
- **H2:** A "what changed since last week" diff on the weekly synthesis raises mid-market PM W4 retention from 58% → ≥65%.
- **H3:** A direct "invite reviewer" prompt at PRD-create lifts invite-second-user from 62% → ≥70%.
- **H4:** Prompting to re-preview after PRD edits raises W4 return among preview-runners from 51% → ≥60%.

## Experiments

### G-1 — Fix the PRD→preview cliff (SUP-002 + entry banner)
- Hypothesis: H1.
- Target metric: `prd_to_first_preview_7d` per workspace.
- Guardrail metric: `preview_structure_defect_reported` <5% (PRD success metric); `preview_blocked_live_write_attempt` baseline unchanged or lower.

### G-2 — Weekly synthesis change log (closes CHURN-004 risk)
- Hypothesis: H2.
- Target metric: W4 retention, mid-market PM segment.
- Guardrail metric: synthesis email open rate ≥ baseline; unsubscribe ≤ baseline.

### G-3 — Second-user activation (collaboration loop)
- Hypothesis: H3.
- Target metric: `second_user_invited_7d`.
- Guardrail metric: no decrease in PRD-create completion; invited users actually join.

### G-4 — Preview export → return (deepen value for already-converted)
- Hypothesis: H4.
- Target metric: W4 return rate among preview-runners.
- Guardrail metric: preview-runner count not artificially inflated; no double-counting.

## Metrics

- Funnel: `workspace_created`, `second_user_invited`, `evidence_imported`, `opportunity_generated`, `prd_created_or_reviewed`, `preview_generated{tool}`, `w4_return`.
- Quality: `preview_structure_defect_reported`, `preview_exported{tool,format}`, `notion_preview_kind_mismatch_detected`.
- Safety: `preview_blocked_live_write_attempt{fixture}`, `external_write_attempted{outcome}` (must never fire with `succeeded` outside future confirmed-write path).
- Retention substrate: `w4_return`, `synthesis_email_open`, `synthesis_email_unsubscribe`.

## Decision Thresholds

Each experiment has an explicit **experiment decision rule**:

- **G-1:** ≥30% conversion → ship + iterate; 25–29% → ship + UX work; <25% → investigate (likely workflow integration, not UX).
- **G-2:** ≥+5pp W4 → ship to all segments; +2 to +5pp → iterate on diff quality; <+2pp → revisit content design.
- **G-3:** ≥70% invite-second-user → ship; 65–69% → ship + monitor; <65% → test alternate prompt placement.
- **G-4:** ≥60% W4 return among preview-runners → ship; lower → test other triggers.

Each experiment includes a **guardrail metric** (named above per experiment) so growth lifts that hurt quality or safety are rejected.

## Product vs Missing-Instrumentation

**Product opportunities (act now):** G-1, G-2, G-3, G-4 — clear product levers grounded in cited evidence.

**Missing instrumentation (block claims):**
- Paid conversion — no instrumentation; do **not** claim conversion rates.
- CAC / LTV / ARPU — no acquisition or revenue data; **block**.
- Long-term retention beyond W4 — pack only has W4.
- `preview_exported{format}` and `preview_shared{channel}` — not yet instrumented; needed before quantitatively optimizing G-4.
- Persona tags per user — current cohort dashboard is workspace-level; add persona tags to attribute SMB low-activation cause.

## Cannot Conclude (out of scope for this diagnosis)

- Viability at any specific price — V-4 not run.
- Long-term retention — no data beyond W4.
- Enterprise PMO representativeness — n=7.
- Whether live sync would lift retention — **blocked** until trust/safety gate (admin disable + idempotency map + payload hashing + 4/4 negative tool-safety fixtures) closes. Any "live sync increases retention" claim is unsupported and unsafe. This diagnosis is **not** acquisition-only — the constrained loops here are activation and retention, and the experiments target them directly, not acquisition.

## Quality Bar

This artifact covers **activation and retention consideration**; each experiment specifies a **guardrail metric** and an **experiment decision rule**. It treats activation/retention as the constrained loops — there is **no acquisition-only recommendation** when activation or retention is constrained, and there is **no experiment without measurable threshold**. It separates assumptions from facts, includes confidence or risk notes, names concrete next actions, and includes direct evidence or states that evidence is missing.

**External writes performed: none.**
