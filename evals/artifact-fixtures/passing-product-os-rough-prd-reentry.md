# entry_classification

Lifecycle status is prd_review_required. This is a rough PRD re-entry, so the workflow starts with a readiness check and does not start earlier stages unless the artifact fails review.

# prd_readiness_review

The readiness check reviews customer problem, scope, non-goals, assumptions, risks, success metrics, and open questions.

# evidence_and_validation_decision

Direct evidence separated from inference. Assumptions are separate from facts. Validation decision is run_validation_first for unsupported claims that drive scope, while low-risk copy and structure repairs can proceed.

# unsupported_claims

Unsupported claims include vague metric impact, unverified user pain, and solution certainty not backed by direct evidence.

# repair_plan

Repair adds non-goals, success metrics, evidence confidence, assumption notes, and concrete next actions before approval.

# approval_gates

Approval gate asks whether to run validation or explicitly accept risk before treating scope as delivery-ready.

# handoff

Handoff target is pm-docs for PRD repair or pm-validation for the riskiest assumption. Lifecycle status and next action make the output resumable.
