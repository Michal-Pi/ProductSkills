# Release Candidate Checklist

Use this checklist before tagging or distributing `product-operating-system` 0.2.1.

## Package Integrity

- [ ] `package.yaml` version is correct.
- [ ] `VERSION`, `package.json`, `package.yaml`, and `registry.json` versions match.
- [ ] `registry.json` includes every shipping skill and workflow.
- [ ] `README.md` reflects current scope.
- [ ] `package.json` has explicit package file inclusion controls.
- [ ] `.npmignore` excludes construction docs, `.env*`, `.product-skills/`, pycache, generated eval results, and packed tarballs.
- [ ] `docs/RELEASE_NOTES_0.2.1.md` exists.
- [ ] `docs/KNOWN_LIMITATIONS_0.2.1.md` exists.
- [ ] `docs/LOCAL_INSTALLATION.md` exists.
- [ ] Construction and planning docs are excluded from package-store and npm dry-run artifacts unless explicitly approved.

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
node --check bin/product-skills.mjs
node --test tests/installer.test.mjs
node bin/product-skills.mjs dist-check
npm pack --dry-run --json --ignore-scripts
```

All commands must pass.

## Install Smoke

- [ ] Copy package to a temporary directory.
- [ ] Run `scripts/check_package.py` against the copied package.
- [ ] Run `./install.sh --runtime all --scope repo --dry-run` from a checkout.
- [ ] Run dry-run install, update, adapter-only uninstall, package-store uninstall, and Cursor user-scope detected/unsupported smoke checks.
- [ ] Run the smoke prompts from `docs/LOCAL_INSTALLATION.md`.
- [ ] Confirm Notion and Linear behavior stays dry-run-first.

## Deferred Release Work

- [ ] npm publish is explicitly approved.
- [ ] release tags and GitHub releases are explicitly approved.
- [ ] signing infrastructure is approved before adding signature checks.
- [ ] Optional release artifact signing has an approved signing key and detached-signature process.
- [ ] Gemini extension adapter smoke test passes with `--adapter extension`.
- [ ] Codex plugin manifest is validated and local marketplace install is smoke-tested.

## Post-Publish Smoke

- [ ] npm shows the intended public package version:
  `npm view @pm-musketeers/product-skills version dist-tags.latest name bin`.
- [ ] Published CLI help works from npm:
  `npx @pm-musketeers/product-skills --help`.
- [ ] Published dry-run install works:
  `npx @pm-musketeers/product-skills install --runtime codex --scope user --dry-run`.
- [ ] GitHub release exists for the published version tag.
- [ ] npm org package is associated with the intended team.

## Future Trusted Publishing Setup

- [ ] npm package trusted publisher is configured for GitHub Actions.
- [ ] Trusted publisher owner is `Michal-Pi`, repository is `ProductSkills`, and workflow file is `.github/workflows/npm-publish.yml`.
- [ ] Release workflow uses GitHub-hosted runners, `id-token: write`, Node 24, and npm 11.5.1 or newer.
- [ ] Next release is published through the GitHub release workflow instead of local interactive npm publish.
- [ ] After trusted publishing is verified, npm package settings disallow traditional token publishing if maintainers want stricter release controls.

## Manual Review

- [ ] Confirm docs do not overclaim trigger evals as real router quality.
- [ ] Confirm forward tests are framed as regression scaffolds.
- [ ] Confirm artifact grading is framed as deterministic rubric support, not expert semantic judgment.
- [ ] Confirm known limitations are visible.
- [ ] Confirm no live external writes are required for validation.

## Release Decision

0.2.1 can be considered a local release candidate when:

- all validation passes;
- install smoke passes;
- known limitations are accepted;
- no blocker remains in `docs/reviews/PHASE9_CLAUDE_READONLY_REVIEW.md`;
- the maintainer explicitly approves tagging or distribution.
