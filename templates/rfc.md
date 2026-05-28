# RFC — Request for Comments

> Output template for `pm-docs/rfc`. Problem and proposal are separate sections — do not collapse. Replace placeholder text in italics.

## Header

- **Title:** _short, action-oriented (e.g., "Adopt event-sourced billing for enterprise tier")_
- **Author:** _PM (single owner)_
- **Status:** _draft | under review | decided_
- **Created:** _YYYY-MM-DD_
- **Review window:** _start YYYY-MM-DD → end YYYY-MM-DD_
- **Decision needed by:** _YYYY-MM-DD (concrete calendar date — "soon" is not acceptable)_
- **Approvers (decision authority):** _named people whose sign-off is required_
- **Reviewers (input wanted, not gating):** _named people whose feedback is desired_

## Problem

_The problem in 3-5 sentences. Cite evidence (interview IDs, support tickets, analytics, market signals). If the problem is conjecture, mark it explicitly and route to `pm-discovery` before posting._

- **Evidence:** _<EVID-ids or source links>, grade H / M / L_

## Proposal

_The change being proposed in 3-5 sentences. State separately from the problem — reviewers must be able to agree on the problem while disagreeing with the proposal._

## Alternatives considered

_At least two alternatives, including "do nothing." For each: 2-3 sentence summary, expected impact, cost, key risk, reason not chosen. Strawmanned alternatives are a quality-fail._

### Alternative A: Do nothing

- **Summary:** _what happens if we do not act_
- **Expected impact:** _quantified if possible_
- **Cost:** _opportunity cost, not zero_
- **Key risk:** _what worsens_
- **Reason not chosen:** _why this is unacceptable_

### Alternative B: _<name>_

- **Summary:** _…_
- **Expected impact:** _…_
- **Cost:** _…_
- **Key risk:** _…_
- **Reason not chosen:** _…_

### Alternative C: _<name>_ (optional)

- _…_

## Tradeoff matrix

| Dimension | Proposal | Alt A (do nothing) | Alt B | Alt C |
|---|---|---|---|---|
| _User impact_ | _cite or "gut-feel — to validate"_ | _…_ | _…_ | _…_ |
| _Engineering cost_ | _…_ | _…_ | _…_ | _…_ |
| _Time to ship_ | _…_ | _…_ | _…_ | _…_ |
| _Reversibility_ | _…_ | _…_ | _…_ | _…_ |
| _Dependency surface_ | _…_ | _…_ | _…_ | _…_ |

_Cite each cell's source where possible. Gut-feel cells must be flagged._

## Convert-to-PRD path

_If approval is expected to commit scope: which PRD inherits this proposal, what scope it commits, which open questions still need answers before PRD authoring begins. Otherwise: "No PRD conversion expected — this RFC documents a process / norm change."_

## Open questions

- _Question 1 — owner if known_
- _Question 2 — owner if known_

## Sources

- _Linked evidence behind the problem and tradeoff cells_
