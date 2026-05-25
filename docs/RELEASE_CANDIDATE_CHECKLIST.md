# Release Candidate Checklist

Use this checklist before tagging or distributing `product-operating-system` 0.1.0.

## Package Integrity

- [ ] `package.yaml` version is correct.
- [ ] `registry.json` includes every shipping skill and workflow.
- [ ] `README.md` reflects current scope.
- [ ] `docs/RELEASE_NOTES_0.1.0.md` exists.
- [ ] `docs/KNOWN_LIMITATIONS_0.1.0.md` exists.
- [ ] `docs/LOCAL_INSTALLATION.md` exists.
- [ ] `docs/OPINIONATED_E2E_WORKFLOW_EXPANSION_PLAN.md` is referenced as post-0.1.0 next-work guidance.

## Validation

Run:

```bash
python3 scripts/check_package.py .
python3 scripts/run_trigger_evals.py .
python3 scripts/grade_artifact.py --case prd-generation evals/artifact-fixtures/passing-prd-generation.md
python3 scripts/grade_artifact.py --case delivery-breakdown evals/artifact-fixtures/passing-delivery-breakdown.md
python3 scripts/check_tool_safety.py .
python3 scripts/check_forward_tests.py .
python3 -m py_compile scripts/check_package.py scripts/run_trigger_evals.py scripts/grade_artifact.py scripts/check_tool_safety.py scripts/check_forward_tests.py
```

All commands must pass.

## Install Smoke

- [ ] Copy package to a temporary directory.
- [ ] Run `scripts/check_package.py` against the copied package.
- [ ] Run the smoke prompts from `docs/LOCAL_INSTALLATION.md`.
- [ ] Confirm Notion and Linear behavior stays dry-run-first.

## Manual Review

- [ ] Confirm docs do not overclaim trigger evals as real router quality.
- [ ] Confirm forward tests are framed as regression scaffolds.
- [ ] Confirm artifact grading is framed as deterministic rubric support, not expert semantic judgment.
- [ ] Confirm known limitations are visible.
- [ ] Confirm no live external writes are required for validation.

## Release Decision

0.1.0 can be considered a local release candidate when:

- all validation passes;
- install smoke passes;
- known limitations are accepted;
- no blocker remains in `docs/reviews/PHASE9_CLAUDE_READONLY_REVIEW.md`;
- the maintainer explicitly approves tagging or distribution.
