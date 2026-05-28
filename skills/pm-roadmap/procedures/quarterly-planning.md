# Quarterly Planning

## Goal

Select the bets a team commits to next quarter, given a prioritized backlog and team capacity, leaving an explicit slack buffer and surfacing the "next quarter" candidates.

## Input expected

- Prioritized backlog (from `pm-strategy/prioritization`)
- Team capacity: headcount, expected weeks in quarter, expected leave, ongoing keep-the-lights-on overhead
- Strategic constraints: locked commitments (regulatory, executive, customer contracts), declared north-star for the quarter
- Optional: prior-quarter completion rate (informs realistic velocity assumption)

## Output produced

- A quarter commitment doc filled from `../../../templates/roadmap.md` with `time_shape: quarterly` and a single-quarter focus:
  - **Committed bets** list (with confidence band, capacity estimate, success metric, owner)
  - **Stretch bets** (would be picked up only if committed bets ship early)
  - **Slack buffer** explicit allocation (recommend ≥15% of capacity reserved for unplanned + carry-over)
  - **Not committed this quarter** list from the prioritized backlog tail with reason
  - **Next-quarter candidates** named explicitly (so they're not surprises later)
  - Locked commitments called out separately at the top so they can't be deprioritized silently

## Steps

1. Compute realistic quarter capacity. Start from headcount × weeks, subtract leave and KTLO overhead, multiply by prior-quarter completion ratio if known. Reserve ≥15% slack.
2. Subtract locked commitments first. Whatever remains is "discretionary capacity."
3. Walk the prioritized list top-to-bottom and add bets until discretionary capacity is exhausted.
4. For each committed bet, confirm: confidence band, primary success metric (cited from `pm-metrics`), owner, dependencies known.
5. If a committed bet is confidence-band low because of unresolved dependencies, either swap it for a higher-confidence next bet OR explicitly flag the risk and propose a kickoff de-risking step in week 1.
6. List stretch bets (next 2-3 from the prioritized tail) explicitly so the team knows the "if we have time" set.
7. List "not committed this quarter" with reasons (capacity, dependency, confidence, strategic fit slipped).
8. Note next-quarter candidates so the next cycle starts with a prepared shortlist, not a blank page.

## Links

- Template: `../../../templates/roadmap.md`
- Reference: `../../../references/methods/roadmap-methods.md` (quarterly time-sliced section)
- Upstream: `../../pm-strategy/procedures/prioritization.md` (must run first)
- Adjacent: `../../pm-roadmap/procedures/dependency-mapping.md` (run before this when ≥2 initiatives share surfaces)

## Done when

- Discretionary capacity is computed from headcount × weeks × completion ratio − leave − KTLO − slack, with every number cited.
- Slack buffer ≥15% is reserved and labeled.
- Every committed bet has: confidence band, primary success metric or flagged metric gap, owner, and a one-line dependency status.
- Locked commitments are listed separately at the top — they did not consume discretionary capacity silently.
- A stretch list of 2-3 named bets exists.
- "Not committed this quarter" names every prioritized bet that did not make the cut, with one-line reason.
- Next-quarter candidates are explicitly listed.
