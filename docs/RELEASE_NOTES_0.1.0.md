# Release Notes 0.1.0

## Status

`product-operating-system` 0.1.0 is a local release-candidate package for controlled use and beta testing. It is not a final marketplace release.

## What Is Included

- Nine PM family skills:
  - `pm-discovery`
  - `pm-strategy`
  - `pm-validation`
  - `pm-design`
  - `pm-docs`
  - `pm-delivery`
  - `pm-growth`
  - `pm-gtm`
  - `pm-tooling`
- Two initial end-to-end workflows:
  - `workflow-discovery-to-prd`
  - `workflow-prd-to-linear-delivery`
- Workflow handoff contracts and schemas for discovery-to-PRD and PRD-to-delivery.
- Notion and Linear dry-run-first tooling contracts.
- Templates for PRDs, delivery handoffs, launch plans, research synthesis, validation plans, experiments, epics, stories, and growth models.
- Deterministic validation scripts using only Python standard library:
  - `scripts/check_package.py`
  - `scripts/run_trigger_evals.py`
  - `scripts/grade_artifact.py`
  - `scripts/check_tool_safety.py`
  - `scripts/check_forward_tests.py`
- Dependency-free installer CLI for local package-store installation, update,
  validation, status, and uninstall.
- Distribution readiness scaffolding:
  - npm package metadata and explicit package file inclusion controls;
  - `install.sh` shell bootstrap that delegates to the Node.js CLI;
  - `product-skills dist-check` for version consistency, npm pack dry-run, and
    deterministic snapshot checksum reporting;
  - `product-skills checksum` for deterministic package-store checksums.
- Runtime packaging:
  - Codex plugin manifest at `.codex-plugin/plugin.json`;
  - Gemini CLI extension adapter support through `--adapter extension`.
- Versioned eval fixtures for triggers, artifacts, tool safety, and forward-test prompts.

## Quality Gates

The current release-candidate gate is:

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
```

Trigger and forward-test pass rates are regression scaffolds, not proof of real router quality. They should be supplemented with real fresh-agent testing before a broader release.

## Primary Use Cases

- Turn messy customer evidence into an evidence-backed PRD.
- Review and repair weak PRDs.
- Convert approved PRDs into epics, stories, acceptance criteria, and Linear dry-run payloads.
- Prepare safe Notion and Linear previews without live writes.
- Diagnose product growth, validation, delivery, and GTM questions using structured procedures.

## Known Limitations

See `docs/KNOWN_LIMITATIONS_0.1.0.md`.

## Next Work

The next recommended milestone is real-use beta and refinement. Construction
and planning docs remain outside packaged release artifacts unless a maintainer
explicitly opts into shipping them.
