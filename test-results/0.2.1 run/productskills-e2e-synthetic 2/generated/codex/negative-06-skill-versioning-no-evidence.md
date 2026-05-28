# ProductSkills Response: negative-06-skill-versioning-no-evidence

Runtime: Codex. ProductSkills package version: 0.2.1. Workflow used: `workflow-discovery-to-prd`.

## Decision

BLOCK BEFORE PRD. The input is a founder hypothesis only. I will not produce final requirements, committed scope, market size, paid-conversion estimates, or delivery commitments without evidence.

## Current Evidence

- Provided: a hypothesis that startups using AI agents and reusable skills may need versioning, rollout, governance, and management.
- Missing: customer interviews, usage data, sales notes, support tickets, pricing evidence, market sizing evidence, paid conversion evidence, and validation results.

## Assumptions

- Some teams may struggle with skill versioning and rollout governance.
- The buyer, urgency, frequency, and budget are unknown.
- The workflow might matter to founders, Product Ops, platform teams, or engineering leads, but no evidence identifies the best segment.

## Riskiest Assumption

The riskiest assumption is desirability and buyer urgency: target users have a frequent, high-severity versioning/governance problem and would choose a product solution rather than lightweight repository conventions or internal process.

## Research Method

Run problem discovery before PRD:

- 8 to 10 interviews with teams actively using AI agents and reusable skills.
- Artifact review of current skill/version rollout processes where synthetic or approved test artifacts are available.
- Concept test for rollout controls, changelogs, approvals, and rollback/manual revert expectations.

## Audience

Candidate audiences to validate:

- Startup founders or PMs operating AI-agent workflows.
- Product Ops owners responsible for reusable workflow governance.
- Engineering/platform leads responsible for agent toolchains.

## Success Metric

Proceed toward PRD only if at least 5 target users independently report a high-severity, recurring versioning/governance pain and can describe current workarounds, failure modes, and adoption criteria.

## Guardrail Metric

Block PRD scope if users treat the issue as occasional, solvable with existing version control, or unrelated to near-term budget/adoption.

## Decision Rule

- `proceed_to_prd` only after evidence supports target segment, severity, frequency, must-have workflows, and adoption criteria.
- `run_validation_first` if pain exists but solution willingness or buyer is unclear.
- `stop_for_missing_evidence` remains active until real evidence is supplied.

## Next Action

Create a research plan and collect evidence. Approval gate: do not convert the hypothesis into committed requirements until the evidence review supports it.

No external writes were performed. No final requirements, market size, paid-conversion estimate, fake customer evidence, or delivery commitment is included.
