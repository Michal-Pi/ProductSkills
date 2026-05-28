# Product Operating System Skills

`product-operating-system` is a Product Management skillset for AI assistants. It turns messy product inputs into evidence-backed decisions and tool-ready artifacts across discovery, strategy, validation, growth, documentation, delivery, launch, and Notion/Linear workflows.

## Current Status

This repo is at local release-candidate preparation for `0.2.1`. The package is suitable for controlled local use and beta refinement, but it should not yet claim category leadership or broad production reliability.

Release-candidate docs:

- `docs/RELEASE_NOTES_0.2.1.md`
- `docs/KNOWN_LIMITATIONS_0.2.1.md`
- `docs/LOCAL_INSTALLATION.md`
- `docs/RELEASE_CANDIDATE_CHECKLIST.md`

The original design specs live in:

- `product-management-skills-package-final.md`
- `product-management-skills-package-design.md`

The package scaffold starts with family-level skills to avoid trigger competition:

- `pm-discovery`
- `pm-strategy`
- `pm-validation`
- `pm-design`
- `pm-docs`
- `pm-delivery`
- `pm-growth`
- `pm-gtm`
- `pm-tooling`
- `workflow-product-operating-system`
- `workflow-discovery-to-prd`
- `workflow-prd-to-linear-delivery`

`pm-router` remains optional and should only ship after trigger evals prove it improves routing.

## Implementation Process

1. Implement the family skills with lean `SKILL.md` files and procedure references.
2. Add templates and schemas for core artifacts.
3. Add deterministic validation scripts.
4. Add trigger evals and golden artifact cases.
5. Test skills against realistic PM tasks.
6. Add Notion/Linear MCP tooling only after workspace bootstrap and idempotency are reliable.
7. Promote high-volume procedures into standalone atomic skills only after trigger evals justify it.

## Local Validation

Run the full local gate:

```bash
python3 scripts/check_package.py .
python3 scripts/run_trigger_evals.py .
python3 scripts/grade_artifact.py --case prd-generation evals/artifact-fixtures/passing-prd-generation.md
python3 scripts/grade_artifact.py --case delivery-breakdown evals/artifact-fixtures/passing-delivery-breakdown.md
python3 scripts/check_tool_safety.py .
python3 scripts/check_forward_tests.py .
python3 -m py_compile scripts/check_package.py scripts/run_trigger_evals.py scripts/grade_artifact.py scripts/check_tool_safety.py scripts/check_forward_tests.py
```

The validators check package structure, trigger-regression fixtures, artifact-grader fixtures, dry-run tool-safety fixtures, forward-test prompt coverage, and Python syntax.

Trigger and forward-test results are regression scaffolds, not proof of real model-router quality.

## Product Operating System Workflow

Phase 12 added the master workflow spine:

- Documentation: `docs/PRODUCT_OS_WORKFLOW_DOCUMENTATION.md`
- Testing plan: `docs/PRODUCT_OS_WORKFLOW_TESTING_PLAN.md`
- Usage plan: `docs/HOW_TO_USE_PRODUCT_OS_WORKFLOW.md`

Use `workflow-product-operating-system` when a product artifact may need routing across discovery, validation, PRD, delivery, tool preview, launch readiness, or post-launch learning.

## Installation

After publication, the npm package name is `@pm-musketeers/product-skills` and
the installed CLI command is `product-skills`. Until publication is complete,
see `docs/LOCAL_INSTALLATION.md` for local install and release-candidate
instructions.
