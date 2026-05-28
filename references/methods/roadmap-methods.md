# Roadmap Methods

Choose the roadmap shape based on the team's commitment style, audience, and planning cadence. Use this reference from `skills/pm-roadmap/procedures/roadmap-build.md` and `skills/pm-roadmap/procedures/quarterly-planning.md`.

## Shapes

### Now-Next-Later

Three bands instead of dates. Each band has a confidence floor: Now = high confidence + sized; Next = medium confidence + sized; Later = directional, often unscoped.

**Use when:**
- Team works in short cycles and dislikes hard-date commitments
- Audience is mostly internal (eng + design + adjacent PMs)
- Strategy is stable but tactical sequencing changes weekly

**Avoid when:**
- Stakeholders need a date for revenue, GTM, or contract reasons (use quarterly time-sliced instead)

### Quarterly time-sliced

Roadmap is organized by Q1 / Q2 / Q3 / Q4 (or whatever cadence the company uses). Each slice has explicit committed + stretch sets.

**Use when:**
- Quarterly OKR or planning rhythm exists
- GTM, finance, or executive audience needs date-bound expectations
- Team can produce reliable velocity estimates from prior quarters

**Avoid when:**
- Team is brand-new with no velocity baseline (use Now-Next-Later for 1-2 quarters first to calibrate)

### Theme-based

Roadmap is organized by theme (customer-job or strategic pillar). Time-slicing is secondary. Used when sequencing within a theme matters more than cross-theme synchronization.

**Use when:**
- Strategy is theme-driven and the question is depth within a theme, not breadth across
- The team can pick up the next bet within a theme as capacity frees up

**Avoid when:**
- Cross-theme dependencies dominate (use time-sliced + dependency-mapping)

### Capacity-aware (shared-engineering)

Explicitly models team utilization, including teams shared across initiatives. Surfaces over-allocation visually.

**Use when:**
- ≥1 engineering team is shared across product surfaces
- Quarter-to-quarter velocity has historically slipped due to invisible overcommitment

**Avoid when:**
- Team is dedicated; capacity arithmetic is trivial

## Confidence bands (use everywhere)

| Band | Means | Required artifacts |
|---|---|---|
| **High** | Scoped, sized, dependencies known | Prioritization entry + sizing estimate + dependency map row (resolved or accepted) |
| **Medium** | Scoped, sized, ≥1 unresolved dependency | Prioritization entry + sizing estimate + dependency map row (with named risk) |
| **Low** | Unscoped OR unsized OR strategic fit weak | Prioritization entry only — flag for discovery / sizing before commit |

## Capacity arithmetic (recommended default)

```
discretionary_capacity = (headcount × weeks_in_slice × velocity_factor)
                        - leave
                        - KTLO_overhead
                        - locked_commitments_capacity
                        - slack_buffer (≥ 15% of net)
```

Cite every input. "Roughly 4 engineer-weeks" is not capacity; "(2 engineers × 4 weeks × 0.75 velocity) − 1 week leave = 5 engineer-weeks" is.

## Slack buffer

Reserve ≥15% of net capacity for unplanned work + carry-over. Roadmaps that allocate 100% of capacity slip predictably. The slack is not "padding" — it is the allocation for the work the team will discover during the slice.

## Cross-references

- Prioritization upstream: `references/frameworks/prioritization-models.md` and `skills/pm-strategy/procedures/prioritization.md`
- Evidence grading for intake: `references/methods/evidence-grading.md`
- Large-corpus synthesis for noisy intake backlogs: `references/methods/large-corpus-synthesis.md`
- Metric anchors: `skills/pm-metrics` (when present)
