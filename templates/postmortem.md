# Product Postmortem

> Output template for `pm-docs/postmortem`. **Out of scope:** ops/SRE incidents — see eng-owned templates. (Outages, downtime, SLA/SLO breaches, auth failures, latency regressions, on-call incidents, infrastructure incidents, and security breaches are refused at the procedure level.) Replace placeholder text in italics.

## Header

- **Feature / launch / sunset under review:** _name_
- **Owning team:** _team_
- **Ship date:** _YYYY-MM-DD_
- **Postmortem author:** _PM_
- **Postmortem date:** _YYYY-MM-DD_
- **Source decision artifact:** _link to PRD / decision memo / RFC that scoped this feature_
- **Postmortem participants:** _named people who contributed_

## Summary

_2-3 sentences. What shipped, what success criteria it failed to hit, what the team is changing as a result. The TL;DR a leader can read in 30 seconds._

## Factual timeline

_Each row is an observable event with a date and a source. Interpretations belong in the causes section below, not here._

| Date | Event | Source |
|---|---|---|
| _YYYY-MM-DD_ | _shipped to GA_ | _release notes link_ |
| _YYYY-MM-DD_ | _adoption dashboard instrumented_ | _dashboard link_ |
| _YYYY-MM-DD_ | _first support escalation_ | _ticket #_ |
| _YYYY-MM-DD_ | _retro held_ | _retro notes link_ |

## Success criteria vs actual

_Compare what the PRD / decision said success looked like to what actually happened. Cite source data. If a success criterion was never measurable, name that as a contributing cause (metric gap)._

| Criterion | Target | Actual | Source |
|---|---|---|---|
| _Activation rate among <segment>_ | _e.g., ≥35% by week 4_ | _e.g., 18% by week 6_ | _dashboard link_ |
| _NPS movement_ | _e.g., +3_ | _e.g., −1_ | _NPS run link_ |
| _Support ticket volume_ | _e.g., ≤baseline_ | _e.g., +40%_ | _support dashboard_ |

## Contributing causes (≥3, classified)

_Each cause must be supported by a timeline event or data point. Classify each as `decision` / `evidence` / `execution` / `external`. No scapegoating — name the role, process, or information gap, not individual competence._

### Cause 1 — _<short name>_

- **Class:** _decision | evidence | execution | external_
- **Description:** _2-3 sentences_
- **Supported by:** _timeline event or data citation_

### Cause 2 — _<short name>_

- **Class:** _…_
- **Description:** _…_
- **Supported by:** _…_

### Cause 3 — _<short name>_

- **Class:** _…_
- **Description:** _…_
- **Supported by:** _…_

## Corrective actions

_For each contributing cause, what changes structurally so this class of failure becomes less likely. Each action has a named owner and a calendar-date due date. "Be more careful next time" is not a corrective action._

| Cause | Corrective action | Owner | Due |
|---|---|---|---|
| _Cause 1_ | _structural change_ | _name_ | _YYYY-MM-DD_ |
| _Cause 2_ | _…_ | _…_ | _…_ |
| _Cause 3_ | _…_ | _…_ | _…_ |

## What would have changed our decision if known earlier

_The single most exportable lesson. Name the missing piece of evidence or the missing analysis explicitly. If the answer is "nothing would have changed our decision," say so — that is also a valid finding (it means the failure mode was unforeseeable or the bet was correct in expectation)._

## Exportable lessons

_Which other teams or product areas should know what was learned, and how the postmortem will reach them._

| Lesson | Distribute to | Channel |
|---|---|---|
| _Lesson 1_ | _team / area_ | _doc / forum / 1:1_ |

## Sources

- _Original PRD / decision memo / RFC link_
- _Adoption / quality / customer-feedback data links_
- _Retro notes link_
