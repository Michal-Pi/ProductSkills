# ProductSkills pm-gtm — AtlasBoard Launch Readiness + Release Notes

Skill: `pm-gtm`. Synthetic only. **Nothing was published. No users were contacted. No live sync, security certification, or external write is claimed.**

## Launch Type

**Conditional preview release** of AtlasBoard's Linear/Notion Dry-Run Delivery Preview. This is **not** a live-sync launch. The release surfaces preview-only artifacts; live writes remain disabled. Launch is gated on six blockers (see Rollout below). Status: **CONDITIONAL** until all blockers close.

## Audience

- **Primary:** Lena (Product Ops Lead) — mid-market B2B SaaS, Notion + Linear shops (INT-003, SALES-002, USAGE Product Ops 78%/72%).
- **Primary:** Maya (Senior PM) — mid-market PM workflow (INT-001, SALES-001, SUP-001).
- **Secondary:** Elise (VP Product) — validation/launch-gate visibility (INT-006).
- **Customer impact:** Product Ops + Mid-market PM teams get a reviewable Linear/Notion preview directly from an approved PRD, without risking what's already in Linear/Notion. Customer impact is **positive value-capture for already-converted workspaces** and a **reduced risk** for security-sensitive evaluators (admin disable is shipped before any write surface).
- **Out of scope for this release:** Priya (founder/PM); enterprise security/procurement buyers (gated on security package); GitHub-Issues teams.

## Positioning

- One-sentence promise: "Inspect what would sync to Linear and Notion — without risking what's there."
- Three proof points (synthetic): preview-only with idempotency keys (INT-003, SALES-002); workspace-level admin disable (SUP-005, CHURN-002 root-cause closure at the *control* level); refusal of all 4 shipped negative tool-safety fixtures in CI.
- Anti-positioning (what we explicitly do **not** promise): live sync, SOC 2, GitHub support, paid-conversion-driven outcomes.

## Channels

- In-product banner for Product Ops + Mid-market PM workspaces post-rollout.
- 1-page "Preview vs Live Write" explainer (gated; not published until V-1 passes).
- ≤4-min demo recording (gated until launch).
- Internal Support macro + KB article.

**No release notes are published yet — DRAFT only.** Distribution begins after the six launch blockers close.

## Enablement

- Sales / CS scripted answer: "Most common question — 'did this actually create the Linear issue?' Answer: **No.** Point users to the header chip and Future-Write Blockers panel."
- Support macro + KB article ready before launch.
- Internal demo recording (≤4 min) covers preview → export → External ID Map → Future-Write Blockers panel.
- PR copy lint enforced (forbidden phrases: `sync automatically`, `writes to Linear`, `publishes to Notion`, `SOC 2`, `GitHub support`).

## Support Plan

- Support staffed for week-1 surge of "did this actually create the issue?" questions; mitigation = scripted answer + KB.
- Escalation path for any incident where a user reports they believed a preview was a real write (treat as a P1 comprehension defect; trigger V-1 retest before further rollout).
- Customer impact mitigation per risk (see Risks below): **mitigation or fallback for risky launches** is defined per risk, not generic.

## Rollout

Conditional, phased:

- **Phase 1:** Enable for Product Ops segment workspaces (n=18) once SUP-002 fix is verified.
- **Phase 2:** Expand to Mid-market PM segment.
- **Phase 3 (post-launch):** Re-evaluate Enterprise PMO — gated on admin-control + security evidence (V-5 + security package).

**Launch blockers (must close before Phase 1):**

| Blocker | Source | Gate criterion |
| --- | --- | --- |
| SUP-002 preview grouping defect | SUP-002 ($142k) | Cohort defect rate <5% over 7 days |
| SUP-005 admin disable | SUP-005 ($310k); CHURN-002 ($220k lost) | Toggle propagates; previews still work; writes blocked |
| V-1 dry-run comprehension usability test | sample-post-launch-learning (4 confused) | T1 ≥80% unprompted correct; 100% T4 (no false-write belief) |
| Support enablement | sample-launch-readiness-gate | Macro + KB article live |
| 4/4 negative tool-safety fixtures refused in CI | tool-safety-fixtures | All four return refusal artifact, not accepted payload |
| Launch copy guardrails enforced in lint | sample-launch-readiness-gate | Forbidden phrases blocked in PR check |

## Risks

Each risk has an explicit **mitigation or fallback for risky launches**:

- **Dry-run comprehension** (sample-post-launch-learning: 4 confused users). *Mitigation:* copy chip + V-1 gate. *Fallback:* if V-1 lands 60–79%, ship copy guardrails + retest; below 60%, redesign preview UX before launch.
- **Structure regression** (SUP-002). *Mitigation:* instrumented assertion + cohort dashboard. *Fallback:* hold Phase 1 if defect rate exceeds 5%.
- **Admin-control gap** (SUP-005, CHURN-002). *Mitigation:* admin disable shipped before any enterprise-evaluable surface. *Fallback:* withhold enterprise-facing comms entirely; this is also why Phase 3 is gated separately.
- **Customer impact of false-write belief.** *Mitigation:* T4 success criterion is 100%; *fallback:* any single failure on T4 is a launch blocker (treat as unsafe).
- **Misreading by Productboard/Jira/GitHub-using prospects.** *Mitigation:* explicit Limitations section in release notes; *fallback:* sales answer points to roadmap order and Linear-first tradeoff.

## Success Metrics

- ≥80% of Phase-1 workspaces generate ≥1 preview within 14 days.
- Preview structure-defect rate <5%.
- 0 unintended external writes (`external_write_attempted{succeeded}` must never fire outside the future confirmed-write path).
- Support volume on "did this actually create?" <10% of Phase-1 workspaces by week 4.
- W4 return among Phase-1 preview-runners ≥55% (calibrated from USAGE baseline 51%).

## Post Launch Review

This release plugs into a **post-launch learning loop**: feed `preview_generated`, `preview_exported`, `preview_blocked_live_write_attempt`, `support_did_this_create_inquiry`, and `w4_return` events back into the discovery substrate. Re-route the cohort signal into `pm-discovery` as a new evidence source; re-enter the workflow at `evidence_synthesized` after Phase 1.

Re-baselining cadence: cohort review at 14 days and 30 days post-launch; if any metric fails the threshold, hold the next phase.

## DRAFT Release Notes (not published)

> **DRAFT — not for distribution.** Nothing has been sent.
>
> **For:** Product Ops + PMs at mid-market B2B SaaS teams using Notion + Linear.
> **What it does:** Generate a dry-run preview of how an approved PRD would appear in Linear (epics + stories + AC) and Notion (PRD summary + decision log + launch checklist). Inspect the full payload before any external write is considered.
> **What it does not do:** No live Linear/Notion/GitHub/npm writes. No automatic workspace discovery. No security certification.
> **Limitations:** No GitHub Issues. No SOC 2. No paid-conversion reporting. Dry-run comprehension is gated on V-1.
> **Rollback:** Manual revert only — no true rollback is promised.

This DRAFT carries **no roadmap promises in release notes** beyond the conditional phased rollout already defined here, and **no unsupported claims** (every line is grounded in cited evidence or labeled as out-of-scope).

## Quality Bar

This artifact addresses **customer impact**, provides **mitigation or fallback for risky launches** per risk, and defines a **post-launch learning loop**. It separates assumptions from facts, includes confidence or risk notes, names concrete next actions, and includes direct evidence or states that evidence is missing. There are **no unsupported claims** (SOC 2 / live rollback / GitHub support are explicitly excluded) and **no roadmap promises in release notes** (only the conditional phased rollout, with gates).

**External writes performed: none. Nothing was published.**
