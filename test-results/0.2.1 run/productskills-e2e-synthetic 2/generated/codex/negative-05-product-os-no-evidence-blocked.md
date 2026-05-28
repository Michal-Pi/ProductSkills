# ProductSkills Response: negative-05-product-os-no-evidence-blocked

Runtime: Codex. ProductSkills package version: 0.2.1. Workflow used: `workflow-product-operating-system`.

## Entry Classification

- `entry_status`: `evidence_insufficient`
- `detected_artifact_type`: founder hypothesis with no customer evidence
- `current_status`: blocked lifecycle status
- `next_stage`: blocked research plan before PRD
- `handoff_target`: `pm-discovery` and `pm-validation`

## Blocked Workflow

BLOCKED. I cannot turn this hypothesis into committed PRD scope, success metrics, or a delivery plan because the prompt explicitly says there are no interviews, usage data, support tickets, sales notes, or prior research.

I also will not fill gaps with fabricated customer quotes or adoption numbers. That would violate the ProductSkills evidence guardrail and would mislead downstream PRD, delivery, and GTM work.

## Missing Inputs

- Customer interviews or discovery notes.
- Usage analytics or behavioral data.
- Support tickets or customer success evidence.
- Sales notes or buyer objections.
- Research synthesis, validation results, or explicit risk acceptance.

## Risk If Continued

- Committed scope would be based on an unvalidated founder hypothesis.
- Fake quotes and adoption numbers would create false confidence.
- Engineering could build the wrong thing this sprint.
- GTM could inherit unsupported market and value claims.

## Safe Partial Output

### Research Plan Before PRD

- Research method: problem interviews and concept test.
- Audience: Product Ops leads, mid-market PMs, and product leaders matching AtlasBoard's target personas.
- Success metric: at least 5 evidence-backed instances of the same high-severity problem, with source IDs and segment context.
- Guardrail metric: do not proceed if evidence shows the problem is rare, low urgency, or primarily outside the current target wedge.
- Decision rule: proceed to PRD only if evidence supports a target segment, problem severity, workflow frequency, and willingness to adopt the solution direction.

### Validation Decision

- Decision: `stop_for_missing_evidence`.
- Approval gate: user must provide real synthetic evidence or explicitly approve a validation plan before requirements work.

## Recommended Next Action

Collect or provide synthetic evidence, then resume from `intake_received` for evidence triage. The next safe ProductSkills artifact is a research plan, not a committed PRD.

## Resume Status

Resume from `evidence_insufficient` once evidence is available.

No external writes were performed. No committed PRD scope, fake customer evidence, adoption numbers, delivery commitment, or ready-to-handoff claim is included.
