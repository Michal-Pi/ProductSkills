# Decision Memo

> Output template for `pm-docs/decision-memo` (narrative form). Durable for-the-record artifact. Socializing the decision to stakeholders is `pm-stakeholder-comms/decision-comms`, not this. Replace placeholder text in italics.

## Header

- **Title:** _short — e.g., "Adopt event-sourced billing for enterprise tier"_
- **Decision (1 sentence):** _what was decided_
- **Decision date:** _YYYY-MM-DD_
- **Decision owner:** _name + role (decision authority)_
- **Memo author:** _PM (may be different from decision owner)_
- **Status:** _decided | revisited | superseded by <memo link>_
- **Form-selection note:** _narrative form selected; trigger keyword: "<keyword>"_
- **Upstream artifact (if any):** _link to pm-strategy prioritization run or RFC that produced the recommendation_

## Context

_3-5 sentences. What problem prompted the decision, what constraints applied, what evidence was on the table. Cite EVID-ids and source links. The reader who lands here in 6 months should understand the situation without re-reading every upstream document._

- **Evidence used:** _<EVID-ids or links>, grade H / M / L_

## Options considered

_At minimum two. No strawmen. Each option was evaluated against the same evidence._

### Option A — _<name>_

- **Summary:** _2-3 sentences_
- **Evidence supporting:** _<EVID-ids>, grade H / M / L_
- **Expected cost / effort:** _engineer-weeks or relative size_
- **Key risk:** _the strongest reason this could go wrong_

### Option B — _<name>_

- **Summary:** _…_
- **Evidence supporting:** _…_
- **Expected cost / effort:** _…_
- **Key risk:** _…_

### Option C — _<name>_ (optional)

- _…_

## Selected option and rationale

_Which option won and why, in ≤2 sentences. Link to the prioritization artifact if applicable. "Selected option won because <evidence + tradeoff>" — not "because it felt right."_

## Assumptions

_Claims taken as true without proof. List separately from risks._

- _Assumption 1_
- _Assumption 2_

## Risks

_Things that could invalidate the decision. List separately from assumptions._

- _Risk 1_
- _Risk 2_

## Expected outcome

_The metric this decision is supposed to move. Cite `pm-metrics` if a metric tree exists; if not, flag the gap rather than fabricate._

- **Metric:** _name (cited)_
- **Baseline:** _current value_
- **Target:** _expected value_
- **Window:** _by when the movement is expected_

## Revisit trigger

_A date, a metric threshold, or an event that triggers re-evaluation. "Revisit when convenient" is not acceptable._

- _e.g., "If activation rate among <segment> stays below 25% by 2026-09-01, re-open this decision."_
- _e.g., "Revisit at the Q4 strategy review regardless of metrics."_

## Open questions

- _Question 1 — owner if known_
- _Question 2_

## Sources

- _Linked evidence corpus_
- _Linked upstream prioritization artifact or RFC_
- _Linked metric tree from pm-metrics_
