# Metric Design

Methods reference for `pm-metrics` procedures. Covers north-star principles, leading-vs-lagging, input/output decomposition, Goodhart's-law guards, and common pitfalls.

## North-star principles

A north-star is the single metric the team uses to evaluate whether the product is delivering value. Four properties separate a useful north-star from a vanity number:

1. **User-outcome anchored.** Reflects something the user actually does or receives, not something the team produces. "Weekly active campaigns sent" beats "campaigns built feature parity."
2. **Mechanically tied to value.** Moving the metric mechanically requires the team to deliver value; gaming it is harder than delivering. If the metric can be moved by support-driven sign-ups, it is not a north-star.
3. **Measurable.** Defined by a precise formula against current or scoped instrumentation. If you cannot count it today, name the instrumentation work.
4. **Single.** Teams that "have three north-stars" have no north-star. The north-star is the metric that wins a coin flip; the others are inputs or guardrails.

## Leading vs lagging

- **Leading metrics** move first, give fast feedback, but can mislead about durable value (e.g., activation rate). Use as the anchor when feedback cadence matters more than long-term truth.
- **Lagging metrics** are the durable truth (e.g., M3 retention, annual revenue per user) but move slowly. Use as the anchor when the team can wait for signal.

A typical pattern: lagging north-star paired with leading input metrics in the tree, paired with leading guardrails for fast tripwires.

## Input/output decomposition

The tree below the north-star is mostly: how does this metric *mechanically* combine from inputs? Formulas like:

```
NS = ∑ (input_A × input_B) – churn_C
```

are the goal. A tree of adjacent metrics that "feel related" is not a metric tree — it is a dashboard.

## Common pitfalls

### Goodhart's law — the metric becomes the target

> When a measure becomes a target, it ceases to be a good measure.

If the team can move the metric without delivering value, the metric is gameable. Guard with negative sanity scenarios in `north-star-design` and with paired guardrails in `guardrail-design`.

**Common gameable shapes:**

- "Logins per week" — moved by re-auth bugs, push notifications, sign-out-on-purpose patterns.
- "Time in app" — moved by friction, not by value.
- "Trial sign-ups" — moved by acquisition spend, not by product fit.

### Invented baselines

A frequent failure: the team writes a metric tree with target values but no cited baselines. Numbers like "improve activation from 35% to 50%" without a source for "35%" are decoration. Procedures REFUSE to ship invented numbers; flag "baseline missing" instead, and route to `kpi-review` or instrumentation.

### Industry-benchmark invocation without source

"Industry typical activation is 25%." Cite the source or do not write it. Categories vary by an order of magnitude across industries; ungrounded benchmarks anchor decisions to noise.

### "Engagement" as a metric

"Engagement" is not a metric. It is a category of metrics. If a stakeholder asks for "engagement," route through `north-star-design` to extract the underlying user-outcome they care about.

### Too many guardrails

If the team has more than ~6 guardrails per primary metric, the guardrails are noise. Distill to the few that would actually pause or rollback the change.

## Cross-references

- `skills/pm-strategy` — the goal artifact that pm-metrics decomposes.
- `skills/pm-growth` — uses the tree to find leverage; does not design the tree.
- `skills/pm-docs/procedures/prd.md` — "Success Metrics" section cites this skill's outputs.
- `references/methods/evidence-grading.md` — applies when reviewing the source for any baseline claim.
