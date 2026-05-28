# Competitive Evaluation

Use when assessing competitor products, positioning, packaging, or gaps.

## Steps

1. Define the customer segment and buying or usage context using `../../../references/methods/strategy-analysis.md`.
2. Select relevant competitors and alternatives, including manual workarounds.
3. Compare capabilities, pricing, positioning, distribution, proof, and switching costs.
4. Distinguish market facts from assumptions.
5. Identify strategic implications, not just feature gaps.
6. Recommend whether to compete, differentiate, partner, ignore, or research further.

## Output

Return comparison table, evidence confidence, implications, risks, and next action.

## Done when

- The comparison covers at least three competitors or alternatives (including manual workarounds when relevant), each scored across capabilities, pricing, positioning, distribution, proof, and switching costs.
- Every cell is tagged as market fact (with source) or assumption; cells with no source are explicitly labeled "unverified" rather than left as ungraded claims.
- At least one strategic implication beyond feature parity is named (positioning shift, packaging response, segment focus, distribution play), and a single recommended action (compete, differentiate, partner, ignore, research) is stated with its rule.
- When the customer segment or buying context is undefined, or when no verified evidence exists for at least one competitor row, the procedure refuses to recommend an action and returns the research gap.
