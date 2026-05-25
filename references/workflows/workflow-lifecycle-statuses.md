# Workflow Lifecycle Statuses

Use these statuses across Product Operating System workflows.

| Status | Meaning | Typical handoff target |
|---|---|---|
| `intake_received` | Raw product signal or artifact has been received and classified. | evidence triage |
| `evidence_insufficient` | Evidence is missing or too weak for committed scope. | research plan or validation plan |
| `evidence_synthesized` | Evidence has been summarized with confidence and gaps. | opportunity framing |
| `opportunity_framed` | Opportunity, segment, problem, and assumptions are named. | evidence decision |
| `needs_validation` | A risky assumption needs validation before commitment. | validation plan |
| `validation_not_required` | Input is already approved, already validated, or later-stage and should proceed through readiness review. | PRD, delivery, launch, or learning readiness |
| `ready_for_prd` | Evidence and decision context support PRD drafting. | PRD drafting |
| `prd_review_required` | A PRD or equivalent artifact needs quality review before delivery. | spec review |
| `prd_ready` | PRD is complete enough for approval or delivery gate. | approval or delivery gate |
| `ready_for_delivery_gate` | Scope can enter delivery readiness review. | delivery gate |
| `approved_for_delivery` | Scope is approved for delivery planning. | delivery split |
| `delivery_review_required` | Delivery artifacts need value, AC, dependency, or sequencing review. | delivery repair |
| `delivery_ready` | Delivery artifacts are ready for tool preview or launch planning. | tool preview or launch readiness |
| `ready_for_tool_preview` | Source artifact and target context are sufficient for dry-run preview. | Notion or Linear preview |
| `ready_for_human_write_confirmation` | Dry-run preview is ready for explicit user write confirmation. | human confirmation |
| `ready_for_launch_review` | Product work is ready for launch readiness review. | launch readiness |
| `launch_ready` | Launch criteria are met or explicitly accepted. | launch or handoff |
| `launched_or_handed_off` | Launch happened or ownership moved to an operating team. | post-launch learning |
| `learning_loop_open` | Post-launch metrics or signals need synthesis and decisioning. | learning synthesis |
| `blocked` | Workflow cannot safely advance without user input, evidence, approval, or target context. | user or owner |

Rules:

- Prefer the closest canonical status over local synonyms.
- Use `blocked` only when the next action is unsafe or impossible without missing input.
- Use `validation_not_required` for approved, validated, delivery, launch, or post-launch re-entry when readiness checks pass.
