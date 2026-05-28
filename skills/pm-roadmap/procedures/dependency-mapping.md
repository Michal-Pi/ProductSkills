# Dependency Mapping

## Goal

Surface cross-initiative dependencies (shared surfaces, sequencing constraints, upstream/downstream team commitments) before a quarterly commitment or roadmap publication, so dependencies are explicit risks rather than silent assumptions.

## Input expected

- Candidate set of bets (typically committed + stretch from `quarterly-planning`, or a draft roadmap slate from `roadmap-build`)
- Surface inventory: shared systems and concerns that any initiative could touch (auth, data model, infra, design system, billing, on-call rotation, customer comms, regulatory surface, API contracts)
- Optional: team org chart (who owns which surface)
- Optional: prior commitments from upstream teams (eng-infra, platform, design)

## Output produced

- A dependency map with two views:
  - **Bet → surfaces touched** (per-bet: which shared systems / which other team's surface)
  - **Surface → bets contending** (per-surface: which bets contend, what the contention is, sequencing implication)
- A risk register entry per contention with severity (blocking / slowing / aware) and a proposed resolution (sequence, deconflict, owner sync, cut)
- A "must-confirm-with-owner" list — bets whose dependency on another team has not been explicitly confirmed
- Recommended changes to roadmap or quarter commitment based on findings

## Steps

1. For each bet, list every shared surface it touches. Err toward over-listing — silent dependencies are the failure mode.
2. Group by surface to see contention. A surface touched by ≥2 bets in the same time-slice is the focus.
3. For each contention, classify:
   - **Sequencing dependency:** Bet A must ship before Bet B (e.g., schema change blocks downstream feature).
   - **Resource dependency:** Both bets need the same scarce team (e.g., 1 infra engineer can't support both in the same quarter).
   - **Design/UX dependency:** Same user-facing surface; design coherence requires coordination.
   - **Data dependency:** One bet depends on data only available after another ships.
4. For each contention, propose a resolution: re-sequence, split a bet, add owner-sync ritual, cut the lower-priority bet, or accept the risk with a documented mitigation.
5. Identify dependencies on upstream teams (platform, design system, infra). For each, mark whether the upstream commitment is confirmed (cite the source) or unconfirmed (add to must-confirm-with-owner).
6. Recommend roadmap changes if findings warrant. The output is advisory; the roadmap owner decides.

## Links

- Reference: `../../../references/methods/roadmap-methods.md`
- Upstream: `../../pm-roadmap/procedures/quarterly-planning.md` or `../../pm-roadmap/procedures/roadmap-build.md` (run dependency-mapping after a candidate slate exists)
- Downstream: revised roadmap-build output incorporating sequencing changes

## Done when

- Every bet in the candidate set has a list of touched surfaces (or an explicit "no shared surfaces touched" assertion).
- Every surface touched by ≥2 bets has a classified contention type and a proposed resolution.
- Every upstream-team dependency is marked confirmed (with cited source) or unconfirmed (with owner named for follow-up).
- Risk register entries have a severity label (blocking / slowing / aware) and a resolution recommendation.
- The must-confirm-with-owner list is non-silent: every unconfirmed dependency is named.
