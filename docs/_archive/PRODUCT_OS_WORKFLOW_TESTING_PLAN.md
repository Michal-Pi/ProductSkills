# Product Operating System Workflow Testing Plan

## Purpose

This plan tests the Phase 12 master workflow assets and keeps the existing package validation intact.

The test strategy is deterministic first:

- structure checks;
- trigger regression checks;
- artifact golden-case grading;
- tool-safety fixtures;
- forward-test prompt coverage;
- Python syntax checks.

These tests are regression scaffolds. They do not prove real model-router quality or senior PM judgment by themselves.

## Full Validation Gate

Run from the package root:

```bash
python3 scripts/check_package.py .
python3 scripts/run_trigger_evals.py .
python3 scripts/check_tool_safety.py .
python3 scripts/check_forward_tests.py .
python3 scripts/grade_artifact.py --case prd-generation evals/artifact-fixtures/passing-prd-generation.md
python3 scripts/grade_artifact.py --case delivery-breakdown evals/artifact-fixtures/passing-delivery-breakdown.md
python3 scripts/grade_artifact.py --case skill-versioning-no-evidence evals/artifact-fixtures/passing-skill-versioning-no-evidence.md
python3 scripts/grade_artifact.py --case product-os-full-happy-path evals/artifact-fixtures/passing-product-os-full-happy-path.md
python3 scripts/grade_artifact.py --case product-os-no-evidence-blocked evals/artifact-fixtures/passing-product-os-no-evidence-blocked.md
python3 scripts/grade_artifact.py --case product-os-rough-prd-reentry evals/artifact-fixtures/passing-product-os-rough-prd-reentry.md
python3 scripts/grade_artifact.py --case product-os-approved-prd-reentry evals/artifact-fixtures/passing-product-os-approved-prd-reentry.md
python3 scripts/grade_artifact.py --case product-os-launch-readiness-reentry evals/artifact-fixtures/passing-product-os-launch-readiness-reentry.md
python3 scripts/grade_artifact.py --case product-os-post-launch-learning evals/artifact-fixtures/passing-product-os-post-launch-learning.md
python3 -m py_compile scripts/check_package.py scripts/run_trigger_evals.py scripts/grade_artifact.py scripts/check_tool_safety.py scripts/check_forward_tests.py
```

## What Each Layer Covers

### Structural Validation

Command:

```bash
python3 scripts/check_package.py .
```

Covers:

- registry and package integrity;
- skill frontmatter;
- workflow procedure and contract availability;
- broken resource references;
- method checklists;
- golden-case expected fixtures;
- tool-safety fixture behavior;
- forward-test coverage;
- Product OS workflow assets and canonical lifecycle statuses.

### Trigger Regression

Command:

```bash
python3 scripts/run_trigger_evals.py .
```

Covers:

- positive routing for the master workflow;
- rough PRD re-entry;
- launch readiness re-entry;
- post-launch learning re-entry;
- negative cases where narrow `pm-docs` or `pm-tooling` should win.

### Product OS Artifact Grading

Commands:

```bash
python3 scripts/grade_artifact.py --case product-os-full-happy-path evals/artifact-fixtures/passing-product-os-full-happy-path.md
python3 scripts/grade_artifact.py --case product-os-no-evidence-blocked evals/artifact-fixtures/passing-product-os-no-evidence-blocked.md
python3 scripts/grade_artifact.py --case product-os-rough-prd-reentry evals/artifact-fixtures/passing-product-os-rough-prd-reentry.md
python3 scripts/grade_artifact.py --case product-os-approved-prd-reentry evals/artifact-fixtures/passing-product-os-approved-prd-reentry.md
python3 scripts/grade_artifact.py --case product-os-launch-readiness-reentry evals/artifact-fixtures/passing-product-os-launch-readiness-reentry.md
python3 scripts/grade_artifact.py --case product-os-post-launch-learning evals/artifact-fixtures/passing-product-os-post-launch-learning.md
```

Covers:

- full lifecycle happy path;
- no-evidence blocked state;
- rough PRD re-entry;
- approved PRD re-entry without forced validation replay;
- launch readiness re-entry;
- post-launch learning loop.

### Tool Safety

Command:

```bash
python3 scripts/check_tool_safety.py .
```

Covers:

- Notion and Linear dry-run behavior;
- confirmation questions;
- idempotency keys;
- external ID map update previews;
- rejected live-write fixtures during evals.

### Forward Tests

Command:

```bash
python3 scripts/check_forward_tests.py .
```

Covers:

- realistic fresh-context style prompts;
- every registered skill and workflow;
- answer-key leakage checks;
- deterministic route agreement;
- required resource path availability.

## Manual Smoke Tests

Run these prompts after installation or major workflow edits.

### Full Workflow

```text
Take this product work from idea to launch. We have interview notes, support tickets, analytics notes, and an approved direction. Classify the entry point, decide whether validation is needed, draft or review the requirements, split delivery, prepare safe tool previews, check launch readiness, and define post-launch learning.
```

Expected behavior:

- routes to `workflow-product-operating-system`;
- emits lifecycle status and handoff target;
- separates direct evidence from inference;
- uses validation decisioning;
- keeps tool writes dry-run first;
- includes launch readiness and learning loop.

### Approved PRD Re-Entry

```text
I have an approved PRD and need the next product workflow step. Continue into delivery readiness, story split, tool dry-run preview, launch readiness, and post-launch learning. Do not make us replay validation if approval and readiness checks pass.
```

Expected behavior:

- uses `approved_for_delivery`;
- marks validation not required when checks pass;
- records earlier evidence gaps as risks;
- does not force discovery replay.

### No-Evidence Blocked State

```text
I have a founder hypothesis for a startup product but no interviews, usage data, sales notes, support tickets, or prior research. Run the workflow and tell me whether we can create committed PRD scope.
```

Expected behavior:

- returns blocked or evidence-insufficient status;
- produces a research or validation plan;
- does not create committed PRD scope.

## Pass Criteria

- All commands in the full validation gate pass.
- Product OS artifact fixtures score 4/4 or meet the expected fixture requirements.
- No workflow output implies live Notion or Linear writes during evals.
- Future-state re-entry does not force validation replay when readiness checks pass.
- Blocked outputs are resumable and useful.

## Known Test Limits

- Trigger and forward tests are deterministic proxy checks.
- Artifact grading checks structure and concepts, not deep PM judgment.
- Live Notion and Linear integrations are not exercised.
- Fresh independent-agent testing is still required before broad release claims.
