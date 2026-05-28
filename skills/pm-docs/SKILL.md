---
name: pm-docs
description: Author and review durable product artifacts — PRDs, decision memos, RFCs, one-pagers, internal-review FAQs, and product postmortems — with explicit evidence, assumptions, scope, and quality review. Use when the user asks to write or review a PRD, decision memo, ADR, RFC, vision one-pager, internal-review/objection FAQ, or product postmortem, or to spec-review any product document for quality. Do not use for stakeholder updates or exec status memos (route to pm-stakeholder-comms), release notes or launch comms (route to pm-gtm), market briefs or MRDs (route to pm-strategy), engineering SDDs or technical specs (out of scope — covered by prd-to-delivery-handoff), or for running the discovery-to-PRD workflow end-to-end (route to workflow-discovery-to-prd, which delegates the PRD writing back to pm-docs).
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# PM Docs

Author durable product artifacts that can survive review by product, design, engineering, GTM, and leadership — and review any product artifact (including external/inherited ones) against a universal quality bar. This skill owns artifact **form, quality, and review**; it does not own the upstream reasoning that produced the evidence (that is pm-discovery, pm-strategy, pm-validation, pm-design) or the downstream socialization (that is pm-stakeholder-comms, pm-gtm).

## Core Procedures

- Use `procedures/prd.md` for product requirements documents (standalone or as the writing step inside `workflow-discovery-to-prd`).
- Use `procedures/decision-memo.md` for durable product decisions — supports both narrative memo form and bullet-log entry form; the procedure selects the form from the user request.
- Use `procedures/spec-review.md` for PRD, RFC, one-pager, decision memo, postmortem, internal-review FAQ, or external-spec review. This is the universal quality gate and MAY be cited by other skills.
- Use `procedures/one-pager.md` for leadership-facing vision briefs, bet briefs, or narrative pitches with a single explicit ask.
- Use `procedures/rfc.md` for proposals under async review — problem + proposal + ≥2 alternatives including do-nothing, with a named decision deadline.
- Use `procedures/internal-review-faq.md` for internal objection-handling / Working-Backwards FAQs that harden a PRD, launch plan, or one-pager before review. Internal-facing only — customer FAQs are out of scope and launch FAQs route to pm-gtm.
- Use `procedures/postmortem.md` for product-failure postmortems (feature underperformed, scope mis-shipped, sunset). The procedure refuses ops/SRE incidents at Step 1 and routes them to engineering-owned templates.

## Templates

- `../../templates/prd.md` — PRD output template (all 14 sections, prose guidance per section).
- `../../templates/decision-memo.md` — narrative decision memo (multi-section, ≥30 lines).
- `../../templates/decision-log-entry.md` — bullet decision-log entry (3-5 lines, append-to-log shape with supersedure rule).
- `../../templates/one-pager.md` — one-pager / vision brief (≤500 words, narrative-first).
- `../../templates/rfc.md` — RFC with tradeoff matrix and convert-to-PRD path.
- `../../templates/internal-review-faq.md` — internal objection-handling FAQ.
- `../../templates/postmortem.md` — product-failure postmortem (out of scope: ops/SRE incidents).

## References

- Use `../../references/methods/evidence-grading.md` when grading evidence behind any claim.
- Use `../../references/checklists/docs-quality.md` before finalizing any artifact.

## Method Selection

Pick the procedure based on what the artifact is for, not just its surface shape:

- **PRD** when scope is committed (or about to be) and engineering / design / GTM need a durable contract. Standalone requests land here directly; discovery-driven requests land here via `workflow-discovery-to-prd`.
- **RFC** when the change is a *proposal under async review*, not yet a committed scope decision. After approval, the RFC may convert into a PRD (the convert-to-PRD path is noted in the RFC itself).
- **One-pager** when the audience is leadership and the goal is to frame a bet or opportunity narratively — single ask, ≤500 words. If the artifact needs solution detail, it has outgrown the one-pager and should be a PRD.
- **Decision memo** when a durable product decision needs an audit trail: what was decided, by whom, with what evidence, against what alternatives, with what revisit trigger. Narrative form for individual high-stakes decisions; bullet-log form for running logs / lightweight decisions.
- **Internal-review FAQ** before a PRD / launch / one-pager review, to surface and steelman the objections reviewers will raise. Internal-facing only — customer FAQs are out of scope; launch / press FAQs route to pm-gtm.
- **Postmortem** after a shipped feature underperforms, mis-ships scope, or is sunset. Product failures only — ops/SRE incidents are refused at Step 1 and routed to engineering-owned templates.
- **Spec review** when reviewing any of the above (or someone else's artifact). Also the universal quality gate other skills MAY cite before finalizing their own artifacts.

## Done When standard

Every artifact pm-docs produces meets the universal quality bar — the spec-review procedure encodes the same rubric, and the per-procedure Done When blocks customize it for that artifact:

- **Explicit evidence** — every material claim is cited and graded H / M / L per `../../references/methods/evidence-grading.md`, or explicitly marked as an assumption.
- **Separated assumptions** — assumptions are listed separately from open questions and from confirmed facts.
- **Scoped non-goals** — non-goals are explicit and each names a reason. Missing non-goals are a scope ambiguity, not a clean artifact.
- **Measurable success metrics** — metrics carry baseline + target + window, OR explicitly flag a metric gap routed to pm-metrics. Unfalsifiable success criteria are blocking.
- **Named open questions** — every unresolved gap names an owner and a target close date; open questions are never silent.

When all five conditions hold and the spec-review pass returns no unresolved blocking findings, the artifact is ready to ship.
