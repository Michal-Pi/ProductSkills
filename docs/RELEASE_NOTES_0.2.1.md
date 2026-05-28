# Release Notes 0.2.1

`product-operating-system` 0.2.1 is a local release-candidate package for
controlled use and beta testing. It is not a final marketplace release.

## Hotfix

- Fixed `product-skills update` source resolution when running a newer CLI from
  `npx`. If the installed package metadata points at an older cached npm package
  root, update now prefers the newer current CLI package source when its version
  differs from the installed package store.
- Added regression coverage for installing from a fake `0.1.0` source and then
  updating from the newer CLI package without passing `--source`.

## Includes 0.2.0 Changes

- Codex installs default to visible skills in both user and repo scope.
- Gemini user-scope installs default to the Gemini CLI extension adapter.
- Installer help and output distinguish visible/package-like adapters from
  context-only adapters.
- Large-corpus synthesis guidance, synthetic E2E grading glue, negative runtime
  prompts, scale-pack unlabeled corpora, split ranking ground truth v2, and
  scale validation scaffolding are included.

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

See `docs/KNOWN_LIMITATIONS_0.2.1.md`.
