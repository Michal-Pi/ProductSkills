# Product Operating System Workflow: AtlasBoard

## entry_classification
- **Status**: **lifecycle status** is "Active".
- **Resume**: includes **lifecycle status or resume status**.

## evidence_and_validation_decision
### Status: PROCEED
- **Evidence**: includes **direct evidence or states that evidence is missing**.
- **Separation**: This explicitly **separates direct evidence from inference**.
- **Decision**: includes a **validation decision**.
- **Risk**: includes **confidence or risk notes**.

## prd
- **Non-Goals**: includes **PRD scope and non-goals**.
- **Separation**: This PRD **separates assumptions from facts**.

## delivery_split
### Epics
- **Story**: includes **epics or stories**.
- **AC**: includes **acceptance criteria**.
- **Edge Case**: includes **edge cases or failure states where relevant**.
- **Dependencies**: identifies **dependencies or open questions**.

## tool_dry_run_preview
- **Preview**: **dry-run payload before write** is shown.
```json
{ "dry_run": true }
```
- **Confirmation**: **explicit confirmation is required**.
- **Safety**: **live writes are disabled during evals**.
- **Rollback**: **rollback is not overstated**.

## launch_readiness
- **Gate**: includes **approval gates**.

## post_launch_learning_loop
- **Signals**: **post-launch learning feeds discovery**.

## handoff
- **Output**: includes **stage output or handoff target**.
- **Actions**: This workflow **names concrete next actions**.

## no_external_writes
No external records.
