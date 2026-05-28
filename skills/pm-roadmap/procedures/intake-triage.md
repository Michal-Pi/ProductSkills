# Intake Triage (Routing)

## Goal

Triage a backlog of inbound feature requests, sales asks, support escalations, exec requests, and stakeholder notes into a routing decision per item: **ignore**, **monitor**, **research**, **validate**, **sequence** (into roadmap), or **escalate** (out-of-band: incident / legal / executive decision).

This is the "feature-requests to roadmap" hero workflow named in the 0.3.0 design — distinct from `pm-discovery/intake-triage`, which clusters raw evidence into themes. This procedure decides what to *do* with each item.

## Input expected

- A list of inbound items, each ideally with: source (support / sales / exec / interview / review / analytics), customer or stakeholder context, problem statement, requested solution, evidence link, date
- Strategy and current roadmap (used as filters)
- Optional: existing themes from `pm-discovery` and `pm-metrics` tree (used to detect "already covered" cases)

## Output produced

- A triage table filled from `../../../templates/intake-triage.md`:
  - One row per item with columns: id, source, problem (de-jargoned), requested solution (separated from problem), evidence grade (`A`–`D` per `../../../references/methods/evidence-grading.md`), strategic fit (yes/partial/no, with reason), duplicate-of (id) or unique, routing decision, next action, owner-or-driver, follow-up date
  - Summary roll-up: counts per routing decision; ARR or affected-user counts where supplied (never invented); top 3 duplicate clusters
  - "Open question / missing context" list per item where the evidence grade is `D` (insufficient)
  - Explicit "do not roadmap" set with reasons

## Steps

1. Normalize every item. Strip jargon. Separate the problem (what hurts the user) from the proposed solution (what the requester asked for). The solution is a hypothesis, not a requirement.
2. Grade evidence using the evidence-grading reference (`../../../references/methods/evidence-grading.md`). Items at grade `D` may not be sequenced; they route to `research` or `ignore`.
3. Detect duplicates and contradictions. For large or noisy backlogs (≥40 items, or many overlapping themes), apply `../../../references/methods/large-corpus-synthesis.md` and preserve dedupe table + minority-signal carry-forward.
4. Apply the routing decision tree:
   - **Ignore:** below-bar evidence AND no strategic fit.
   - **Monitor:** evidence grade C or D, but worth tracking (recurring weak signals).
   - **Research:** strategic fit unclear, or problem unclear → route to `pm-discovery`.
   - **Validate:** problem clear, solution uncertain → route to `pm-validation` to design the smallest experiment.
   - **Sequence:** evidence grade ≥B, strategic fit clear, problem and solution coherent → eligible for `pm-strategy/prioritization` then `roadmap-build`.
   - **Escalate:** outside PM scope (incidents → on-call; legal / contractual → legal; pricing concession → finance/exec).
5. Cite the strategic fit reason. "Fits strategy" without a reason is not acceptable — name the pillar or north-star input.
6. For items routed to `sequence`, flag the metric they would move (cited from `pm-metrics` if available); if no metric mapped, flag the gap.
7. Surface the top duplicate clusters in the summary so prioritization can rank the cluster, not the individual ticket.

## Links

- Template: `../../../templates/intake-triage.md`
- Reference: `../../../references/methods/evidence-grading.md`, `../../../references/methods/large-corpus-synthesis.md`
- Downstream: items routed `sequence` → `pm-strategy/prioritization` → `../../pm-roadmap/procedures/roadmap-build.md`
- Distinct from: `../../pm-discovery/procedures/intake-triage.md` (theme clustering of raw evidence)

## Done when

- Every input item has a routing decision and a one-line justification citing the rule that triggered it.
- Every `sequence` item has an evidence grade ≥B, a strategic fit reason, and either a cited target metric or a flagged metric gap.
- Every `research` and `validate` item names the downstream skill (`pm-discovery`, `pm-validation`) with a one-line handoff.
- Duplicate clusters are named and counted before prioritization runs; no item appears in the prioritization input twice under different ids.
- The "do not roadmap" set is explicit with reasons — silent drops are not allowed.
- If ≥40 items are processed, the output includes a final roll-up (counts per decision, dedupe count, missing-field count) per `large-corpus-synthesis`.
