# Product Postmortem

## Goal

Produce a structured product-failure postmortem after a shipped feature underperforms, a launch misses its success criteria, scope is mis-shipped, or a feature is sunset — naming contributing causes, classifying them, defining corrective actions with owners and due dates, and answering "what would have changed our decision if known earlier." This skill covers **product failures only**; ops/SRE incidents (outages, latency regressions, security breaches) are eng-owned and explicitly refused here.

## Step 1 — SRE-incident refusal contract (load-bearing)

Before doing any other work, scan the user's request text for these keywords:

- `outage`, `downtime`
- `SLA`, `SLO`
- `auth failure`, `authentication failure`, `authorization failure`
- `latency regression`, `latency`, `p99`, `p95`
- `on-call`, `oncall`, `pager`, `paged`
- `infrastructure incident`, `infra incident`
- `security breach`, `data breach`, `vulnerability`, `CVE`

If any keyword matches, the procedure REFUSES and emits the following structured envelope, then STOPS. Do not proceed to product-postmortem flow.

```json
{
  "status": "blocked",
  "reason": "This request describes an operations / SRE / infrastructure / security incident, not a product failure. Product postmortems cover features that underperformed, mis-shipped scope, or were sunset; they do not cover outages, downtime, SLO breaches, auth failures, latency regressions, on-call incidents, infrastructure failures, or security breaches. Those are owned by engineering and SRE.",
  "route_to": "engineering-owned-postmortem-templates",
  "missing_inputs": ["product-failure-context-instead-of-ops-incident"],
  "resume_hint": "Re-classify the request: if a shipped product feature failed to hit its success criteria (adoption, retention, monetization, satisfaction), restate the failure in product terms and re-invoke. If the failure is an ops incident, route to engineering's incident-review process."
}
```

The caller may re-classify and resume; that is why the envelope is structured.

If no keyword matches, continue to Step 2.

## Input expected (when not refused)

- The feature, launch, or sunset under review
- Timeline of what happened (factual events with dates, not interpretive narrative yet)
- Success criteria the feature failed to hit (target metrics, adoption thresholds, satisfaction bars from `pm-metrics` or the original PRD)
- Available adoption / quality / customer-feedback data
- The original decision artifact (PRD, decision memo, RFC) that scoped the feature
- Optional: external context (market shift, dependency failure) — kept separate from internal contributing causes

## Output produced

A filled `../../../templates/postmortem.md` with: feature/launch identity, factual timeline, success criteria vs actual, ≥3 contributing causes classified by category, corrective actions per cause with owner + due date, "what would have changed our decision if known earlier" answered explicitly, and exportable lessons.

## Steps

2. After the Step 1 refusal contract clears, restate the feature, launch, or sunset under review. Include the owning team, ship date, and the success criteria the feature failed to hit (cited from the original PRD or pm-metrics tree).
3. Build a factual timeline. Each row: date, event, source. Events are observable (shipped, instrumented, support tickets opened, retro held); interpretations belong in the causes section, not the timeline.
4. Compare success criteria to actuals. Cite the source data — adoption dashboard, retention cohort, NPS run, support ticket volume. If a success criterion was never measurable, name that as a contributing cause (metric gap, route to `pm-metrics`).
5. Identify at least three contributing causes. Classify each into one of: **decision** (the wrong bet was chosen), **evidence** (the evidence used to choose was thin, biased, or misread), **execution** (the right bet was chosen but build / launch / rollout was flawed), **external** (market shift, dependency failure, regulatory change). Each cause must be supported by a timeline event or data point.
6. For each cause, define a corrective action: what changes structurally so this class of failure becomes less likely. Each corrective action gets a named owner and a due date. "Be more careful next time" is not a corrective action.
7. Answer "what would have changed our decision if known earlier?" explicitly. Name the missing piece of evidence or the missing analysis. This is the single most exportable lesson.
8. Forbid scapegoating language. Causes are about systems and decisions, not about named individuals' competence. If a named person appears as a cause, rewrite to name the *role*, *process*, or *information gap* instead.
9. List exportable lessons: which other teams or product areas should know what was learned. Distribute the postmortem accordingly.

## Distinct from

- `../../pm-gtm/SKILL.md` post-launch-review — that artifact is adoption-focused and assumes the launch succeeded; postmortem assumes it underperformed.
- `../../pm-growth/SKILL.md` experiment-readout — that artifact is bounded to a single experiment's learnings; postmortem covers the shipped feature lifecycle.
- Eng-owned incident postmortems — see Step 1.

## Links

- Template: `../../../templates/postmortem.md`
- Reference: `../../../references/methods/evidence-grading.md`
- Reference: `../../../references/checklists/docs-quality.md`
- Adjacent: the spec-review procedure in this skill (run on draft postmortem to catch scapegoating language and unsupported causes)

## Done when

- Step 1 refusal contract was applied; either the procedure refused and stopped, OR the request cleared and the product-postmortem flow ran.
- The timeline is factual: each row is an observable event with a date and source; no interpretive language.
- Success criteria vs actual is documented with cited source data; metric gaps are named explicitly.
- ≥3 contributing causes are named and each is classified as `decision` / `evidence` / `execution` / `external`.
- Each contributing cause maps to at least one corrective action with a named owner and a calendar-date due date.
- "What would have changed our decision if known earlier" is answered with a concrete missing piece of evidence or analysis.
- No scapegoating language: roles, processes, and information gaps are named — not individual competence.
- Exportable lessons are listed with the teams or product areas that should receive them.
