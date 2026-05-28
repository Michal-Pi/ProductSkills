# Release Notes 0.2.0

`product-operating-system` 0.2.0 is a local release-candidate package for
controlled use and beta testing. It is not a final marketplace release.

## Highlights

- Codex installs now default to visible skills in both user and repo scope.
  `AGENTS.md` remains available only through explicit `--adapter agents`.
- Gemini user-scope installs now default to the Gemini CLI extension adapter.
  Repo-scope Gemini installs continue to use marker-managed `GEMINI.md`, and
  user-scope `GEMINI.md` remains available through explicit `--adapter context`.
- Installer help and text output now distinguish visible/package-like adapters
  from context-only adapters.
- Added large-corpus synthesis guidance for evidence ledgers, batching,
  deduplication, conflict registers, missing-field handling, minority-signal
  carry-forward, noisy-signal suppression, citation rules, and roll-up quality.
- Added synthetic E2E grading glue that stores runtime outputs under
  `test-results/productskills-e2e-synthetic/generated/<runtime>/` and grades
  the 12 core prompts through the existing artifact and tool-safety harnesses.
- Added negative runtime prompts for no-evidence, live-write, fake-ID,
  confirmation, unsupported-claim, and launch-readiness pressure cases.
- Updated the scale pack with unlabeled corpora, split ranking ground truth v2,
  generated-output slots, and validation checks for prompt leakage and corpus
  hygiene.

## Validation

Run before publishing:

```bash
node --check bin/product-skills.mjs
npm run test:installer
python3 scripts/check_package.py .
python3 scripts/run_trigger_evals.py .
python3 scripts/check_tool_safety.py .
python3 scripts/check_forward_tests.py .
python3 -m py_compile scripts/check_package.py scripts/run_trigger_evals.py scripts/grade_artifact.py scripts/check_tool_safety.py scripts/check_forward_tests.py scripts/grade_productskills_synthetic_e2e.py
python3 test-results/productskills-scale-synthetic/scripts/validate_scale_pack.py
npm run dist:check
```

## Notes

Existing stored breakpoint summaries remain historical/projection artifacts
until fresh runtime outputs are captured and graded against the 0.2.0 harness.

See `docs/KNOWN_LIMITATIONS_0.2.0.md`.
