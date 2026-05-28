# ProductSkills pm-design — AtlasBoard Design Brief

Skill: `pm-design`. Synthetic only. No external design tools used. **No usability validation has happened.**

## Design Brief

Generate a low-fidelity design brief for the evidence-linked PRD + dry-run Linear/Notion preview experience (the approved-PRD opportunity). High-fidelity work is **blocked** until V-1 dry-run comprehension usability test passes. Every design decision below either cites evidence or is labeled as an assumption — **design decisions cite evidence or are labeled assumptions**.

## Target Users

- **Primary:** Lena (Product Ops Lead, mid-market) — INT-003, SALES-002, USAGE Product Ops 78%/72%.
- **Primary:** Maya (Senior PM) — INT-001, SALES-001, SUP-001.
- **Secondary:** Elise (VP Product) — INT-006 (validation/launch gates).
- **Out of scope:** Priya (founder, weak fit, INT-004/SUP-004/CHURN-001), Hannah (CS — blocked on SUP-007 import quality).

## Scenarios

1. Maya finishes an evidence-linked PRD and clicks "Preview delivery sync." She expects a Linear epic/story tree + Notion page set she can inspect **before any write**.
2. Lena reviews the same preview a day later; she needs payload hash + idempotency keys + external ID map to be stable so her review is meaningful.
3. Admin has set workspace-level "external writes disabled" — Lena can still preview; write button is disabled with rationale (not hidden).
4. A user tries to "send to Notion now" without enablement — system **blocks** with a refusal artifact (matches the 4 shipped negative tool-safety fixtures).

## Core Flows

- **Flow A — Preview generation.** PRD → Preview delivery sync → Linear tab + Notion tab; both `dryRun: true`, `confirmationRequired: true`, payload hash, idempotency keys, `UNRESOLVED_*` IDs; export `.md`/`.json`.
- **Flow B — Inspect → revise → re-preview.** Edits show a diff of changed externalIds and a new payload hash; existing external ID map preserved (no duplicate create).
- **Flow C — Admin disable.** Toggle blocks writes; previews still work; rationale text + audit-log link.
- **Flow D — Blocked live write.** Any confirmed-write attempt or `confirmation_required: false` dry-run → refusal artifact (covers the 4 negative fixtures: live-write, no-confirmation, duplicate-create, kind-mismatch).

## Information Architecture

```
Workspace
├── Evidence Library
├── Opportunities
├── PRDs
│   └── <PRD>
│       ├── Overview
│       ├── Evidence Links
│       ├── Scope / Non-Goals
│       ├── Metrics & Risks
│       └── Preview Delivery Sync   ← entry to Flow A
│           ├── Linear Preview (dry-run)
│           ├── Notion Preview (dry-run)
│           ├── External ID Map
│           └── Future-Write Blockers
└── Admin
    └── External Sync Controls
```

## Key Screens

1. **Preview entry banner** — states: ready (admin enabled), preview-only (admin disabled), partial (PRD has blocked sections).
2. **Linear Preview tab** — header chip "Dry-Run Preview · No Linear write was performed"; epic→story tree; externalId, idempotencyKey, AC; footer payload hash + UNRESOLVED IDs + confirmation notice.
3. **Notion Preview tab** — same chip; page hierarchy with externalIds; source-evidence links resolved.
4. **External ID Map drawer** — localId → existing externalId → operation; explicit "would be a duplicate create" rows pointing to existing record.
5. **Future-Write Blockers panel** — checklist: resolve workspace/team/state/label IDs · confirm payload + hash · admin permits · persist external ID map · idempotency check.
6. **Admin disable state** — write button disabled, rationale text, audit-log link.

## States

- Empty, Loading, Success, Partial (some sections blocked-for-missing-evidence), Error, Admin-disabled, Blocked-live-write.

Includes **empty states and error states** explicitly:
- Empty: "No preview yet. Generate one to inspect what would sync if enabled."
- Error: "Preview generation failed at <stage>. No external writes were attempted. Details: <reason>." Never auto-retry against an external system.

## Edge Cases

- Idempotency key already maps → propose `noop`/`update`, never duplicate `create` (matches `linear-duplicate-create-negative`).
- Tool/kind mismatch (Notion preview with Linear payload) → refuse, do not silently re-label (matches `notion-tool-kind-mismatch-negative`).
- Dry-run with `confirmation_required: false` → reject + return corrected payload (matches `linear-dry-run-no-confirmation-negative`).
- Confirmed-write request in eval/test → refuse; no "User said yes." override (matches `linear-live-write-negative`).
- PRD section blocked-for-missing-evidence → preview elides those stories with a "blocked: missing evidence" placeholder.
- Admin disables external writes mid-session → in-flight preview still completes; write button transitions to disabled with rationale.

## Dry Run Copy

The phrase **"Dry-Run Preview · No Linear/Notion write was performed"** appears on every preview header AND every exported artifact's first line — **dry-run status is unmistakable**.

- Use "would create" / "would update" — never "created" / "synced" / "published" in preview UI.
- "Confirm" buttons reserved for the future write path; preview tabs use "Export" / "Copy payload" only.
- Admin-disabled copy: "External writes disabled by workspace admin." Not "feature unavailable."
- Refusal artifacts: lead with what was refused + why, then the safe alternative.

## Usability Test Plan

Includes **usability test tasks and success criteria** (V-1 from the validation plan):

- **T1:** "You ran Preview delivery sync. Tell me what happened in Linear and Notion." Success: participant says "nothing was sent; this is a preview" unprompted (≥80%).
- **T2:** "Show me where AtlasBoard would create a new Linear issue vs update an existing one." Success: ≥75% identify External ID Map and noop/update rows.
- **T3:** "Admin has disabled external writes. What can you still do?" Success: participant identifies previews still work and explains why writes are blocked.
- **T4:** "Try to send this to Linear now." Success: 100% correctly interpret the refusal artifact — false-write belief is a launch blocker.

## Validation Gaps

High-fidelity design and shipped UI are **blocked** by:
- No usability test has been run yet (V-1 outstanding).
- No accessibility audit (defer high-fi until contrast/keyboard targets defined).
- No internationalization scope.
- Admin-disable audit-log artifact format is an open engineering question (`sample-delivery-handoff`).

## Quality Bar

This artifact: includes **design decisions cite evidence or are labeled assumptions**; makes **dry-run status is unmistakable**; covers **empty states and error states**; provides **usability test tasks and success criteria**. It does **not** report completed usability tests (V-1 is *proposed*), does **not** make production UI decisions, and does **not** describe live external integration behavior. It separates assumptions from facts, includes confidence or risk notes, names concrete next actions, and includes direct evidence or states that evidence is missing.

**External writes performed: none.**
