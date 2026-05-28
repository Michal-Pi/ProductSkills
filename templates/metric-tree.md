# Metric Tree

> Output template for `pm-metrics/metric-tree`. North-star at the root; decompose to actionable, instrumented leaves.

## Header

- **North-star (root):** _name + formula (link to `pm-metrics/north-star-design` output)_
- **Author:** _PM_
- **Date:** _YYYY-MM-DD_

## Tree (text form)

```
NORTH-STAR: <name>
├── L1: <input A>           formula: <A combines with B into NS via ___>
│   ├── L2: <sub-input A1>  formula: <…>
│   └── L2: <sub-input A2>  formula: <…>
├── L1: <input B>           formula: <…>
└── L1: <input C>           formula: <…>
```

## Node detail (one section per node L1 and L2)

### L1 — _<name>_

- **Formula:** _precise expression linking this node to its parent_
- **Why it drives the parent:** _one sentence_
- **Measurement status:** _measurable today / scoped instrumentation / not measurable_
- **Source events / properties:** _<EVT-id>, <PROP-id>_
- **Baseline (cited):** _value + source link; if unknown, "baseline missing — route to kpi-review"_
- **Expected sensitivity:** _how much would a 10% improvement here move the parent?_
- **Cross-dependencies:** _other nodes this node depends on or is depended on by_

(repeat for every level-1 and level-2 node)

## Investment heatmap

| Node | Expected sensitivity | Current headroom | Investment priority |
|---|---|---|---|
| _Node X_ | _high_ | _high_ | _LEVERAGE — top for pm-growth investment_ |
| _Node Y_ | _high_ | _low_ | _consider only if guardrail risk acceptable_ |
| _Node Z_ | _low_ | _high_ | _deprioritize_ |

## Instrumentation gaps

| Node | Missing event/property | Proposed owner | ETA | Unlocks |
|---|---|---|---|---|
| _Node A_ | _<event>_ | _<name>_ | _YYYY-MM-DD_ | _baseline + targeting_ |

## Cross-dependencies (edges)

- _Activation quality → Retention_ — flag for pm-growth diagnosis
- _Refer leakage → Acquisition_ — flag

## Sources

- North-star artifact: _link_
- Instrumentation schema: _link_
- Any prior metric trees: _link_
