# Opportunity Sizing

Use when estimating whether an opportunity is worth pursuing.

## Steps

1. Define the opportunity and target segment.
2. Estimate reach, frequency, severity, willingness to pay, strategic value, and effort.
3. Label each input as measured, estimated, inferred, or unknown.
4. Provide a range rather than false precision.
5. Identify the assumption that would most change the decision.
6. Recommend pursue, research, defer, or reject.

## Output

Return sizing assumptions, range, confidence, decision implication, and next learning step.

## Done when

- The opportunity and target segment are stated; reach, frequency, severity, willingness to pay, strategic value, and effort each carry a value and a data-quality label (measured, estimated, inferred, or unknown).
- The result is expressed as a range (low/mid/high) with the math shown, not a single point estimate; ranges that rest on unknown inputs are labeled "low confidence."
- A sensitivity check names the single assumption that would most change the recommendation, and a recommended action (pursue, research, defer, reject) is stated with the decision rule.
- When more than half the inputs are "unknown" or the segment cannot be defined, the procedure refuses to recommend "pursue" and returns the highest-leverage research step instead.
