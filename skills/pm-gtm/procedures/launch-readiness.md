# Launch Readiness

Use when assessing whether a feature or product is ready to launch.

## Steps

1. Choose launch type using `../../../references/methods/launch-planning.md`.
2. Define audience, customer impact, rollout, support, and enablement needs.
3. Check product readiness, known limitations, risks, and mitigation.
4. Confirm messaging, channels, owners, and timing.
5. Define success metrics and post-launch review date.
6. Recommend launch, beta, staged rollout, hold, or deprecate.

## Output

Use `../../../templates/launch-plan.md` for the launch plan narrative; the structured launch-readiness gate artifact conforms to `../../../schemas/launch-readiness-gate.schema.json` (use `../../../templates/launch-readiness-gate.md` to fill it). The `approval_gate` field is optional with enum `[pending, granted, rejected]`; treat absent as `pending` for safety.

## Done when

- At least four launch gates are named (e.g., product readiness, support and docs, messaging, instrumentation, legal or compliance, rollout plan), each with an explicit closure criterion and an owner.
- Audience, customer impact, channels, timing, and enablement needs are populated with concrete values; items inherited from other artifacts cite their source.
- Success metrics with baselines or targets are stated, and a post-launch review date is set; risks and limitations have mitigation or an explicit acceptance note.
- When any launch gate cannot be closed and no mitigation is available, the procedure refuses to recommend "launch" and routes to beta, staged rollout, or hold with the unmet gate named.
