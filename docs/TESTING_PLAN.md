# Testing Plan

## Test Layers

### 1. Structural Validation

Run on every change:

```bash
python3 scripts/check_package.py .
```

Checks:

- Manifest exists and references valid roots.
- Registry skill IDs match folders.
- Every skill has `SKILL.md`.
- Frontmatter contains `name` and `description`.
- Skill folder name matches `name`.
- Trigger tests include should-fire and should-not-fire cases.
- Referenced templates and references exist.

### 2. Trigger Evals

Purpose: ensure the right family skill triggers and obvious non-matches do not.

Minimum bar:

- Family skills: >=90% correct selection.
- Router, if enabled: >=95% correct selection.

Trigger cases must include:

- Direct artifact requests.
- Ambiguous PM requests.
- Tooling requests.
- Negative controls that sound PM-adjacent but should not trigger.

Run:

```bash
python3 scripts/run_trigger_evals.py .
```

The Phase 5 runner is deterministic and standard-library only. It is a proxy regression scaffold for trigger surfaces, not proof of real model-router quality. It checks registered skill descriptions against `evals/trigger-tests.yaml`, enforces family and workflow self-consistency thresholds, and fails on high-risk false positives in negative controls.

Do not tune the matcher and then treat the same prompts as independent evidence. Later forward testing should add held-out prompts that are not used to tune `scripts/run_trigger_evals.py`.

### 3. Artifact Golden Cases

Golden cases compare outputs against rubrics, not exact text.

Initial cases:

- VoC synthesis from messy interview notes.
- Evidence-backed PRD.
- Prioritization method selection.
- PRD to Linear delivery breakdown.
- Growth loop diagnosis.
- Launch readiness.

Run:

```bash
python3 scripts/grade_artifact.py --case prd-generation evals/artifact-fixtures/passing-prd-generation.md
```

The Phase 6 artifact grader is deterministic and standard-library only. It checks a generated artifact against `evals/expected/<case>.yaml`, validates referenced rubric IDs from `evals/artifact-quality-rubrics.yaml`, verifies required sections, checks must-include concepts, and fails on must-not-include behavior.

`scripts/check_package.py` also smoke-tests the versioned passing and failing grader fixtures under `evals/artifact-fixtures/`.

### 4. Tool-Safety Tests

For Notion/Linear:

- Missing workspace bootstrap should produce setup instructions, not a failed write.
- External write requests must produce preview payloads.
- Re-run with same artifact ID must update mapped IDs, not duplicate.
- Partial batch failure must leave a checkpoint.

Run:

```bash
python3 scripts/check_tool_safety.py .
```

The Phase 7 runner is deterministic and standard-library only. It validates Notion and Linear fixture payloads against the local schemas, enforces dry-run-only behavior during evals, checks confirmation questions, verifies idempotency and external ID map duplicate prevention, rejects secret-like workspace fields, and checks partial-failure checkpoint structure.

### 5. Human Review

For each release candidate, run a PM review:

- Is the output actually useful to a senior PM?
- Does it cite evidence and assumptions?
- Does it avoid fake certainty?
- Does it separate discovery from delivery commitments?
- Does it make the next action obvious?

### 6. Forward Tests

Forward tests use fresh-context style prompts without expected-answer fixture paths, rubric names, or skill IDs in the user prompt.

Run:

```bash
python3 scripts/check_forward_tests.py .
```

The Phase 8 runner validates that every registered skill and initial workflow has a realistic prompt, required resource paths exist, captured observations are recorded, answer-key leakage is absent, and the deterministic trigger proxy routes the prompt to the intended skill. It is still a regression scaffold, not a substitute for real independent-agent forward tests.

## Test Infrastructure

Recommended repo additions over time:

- `scripts/check_package.py`: structural validation.
- `scripts/run_trigger_evals.py`: trigger eval runner.
- `scripts/grade_artifact.py`: rubric-based artifact grader.
- `scripts/check_tool_safety.py`: Notion/Linear dry-run safety fixture validator.
- `scripts/check_forward_tests.py`: fresh-context prompt and capture validator.
- `evals/trigger-tests.yaml`: trigger cases.
- `evals/golden-cases/`: source inputs.
- `evals/expected/`: expected qualities and rubric notes.
- `evals/tool-safety-fixtures/`: Notion/Linear safety cases.
- `evals/forward-tests/`: fresh-context prompt captures.
- `evals/results/`: ignored generated output.
- `docs/SCHEMA_SUBSET.md`: local schema keyword support for standard-library validators.

## Release Gate

Do not tag a release until:

- Structural validation passes.
- Trigger evals pass threshold as regression checks, not as router-quality proof.
- Golden cases have been reviewed.
- Forward tests include fresh-agent or adversarial review beyond deterministic proxy checks.
- No external write workflow can execute without preview and confirmation.
- Docs and examples match the current package.
