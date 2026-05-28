# Package Installer Phase 3/4 Agent Prompt

Use this prompt to start the next implementation session.

```text
You are implementing ProductSkills package installer Phases 3 and 4.

Repository:
/Users/pilawski/My_projects/skillsos/Design Docs Product

Base branch:
feat/initial-product-os-package

Remote:
https://github.com/Michal-Pi/ProductSkills.git

Current state:
- Phase 1 is merged and pushed to `feat/initial-product-os-package`.
- Phase 2 is merged and pushed to `feat/initial-product-os-package`.
- Phase 2 commit: `5d9a658 feat: add installer update and uninstall`.
- The installer currently supports `install`, `update`, `uninstall`, `validate`, and `status`.
- The installer is dependency-free Node.js and uses only built-in Node modules.
- Existing installer tests live in `tests/installer.test.mjs`.
- Design and planning docs used during package construction may be untracked. Preserve them and do not revert unrelated changes.
- Do not make live Notion or Linear writes.
- Do not install dependencies unless the user explicitly approves.
- Do not publish to npm, create release tags, or push release artifacts unless the user explicitly asks.

Read first:
- docs/PACKAGE_INSTALLER_SDD.md
- docs/LOCAL_INSTALLATION.md
- package.json
- VERSION
- package.yaml
- registry.json
- bin/product-skills.mjs
- adapters/claude/SKILL.md
- adapters/codex/SKILL.md
- adapters/codex/AGENTS.md
- adapters/cursor/product-operating-system.mdc
- adapters/gemini/GEMINI.md
- tests/installer.test.mjs
- scripts/check_package.py
- scripts/run_trigger_evals.py
- scripts/check_tool_safety.py
- scripts/check_forward_tests.py

Implementation scope:
Implement Phase 3 and Phase 4 from `docs/PACKAGE_INSTALLER_SDD.md`.

Phase 3 deliverables:
1. Add distribution readiness without publishing:
   - npm package metadata review and hardening;
   - package file inclusion controls, preferably via `files` in `package.json`;
   - dry-run packaging validation such as `npm pack --dry-run` or equivalent;
   - no runtime dependency installation.
2. Add `install.sh` for shell-based bootstrap:
   - non-destructive by default;
   - supports dry-run;
   - delegates to `bin/product-skills.mjs`;
   - checks Node.js and Git availability;
   - does not install dependencies or mutate shell profiles.
3. Add release metadata scaffolding:
   - changelog or release notes entry for installer phases;
   - documented release checklist;
   - version consistency checks across `VERSION`, `package.json`, `package.yaml`, and `registry.json`.
4. Add checksum support where practical:
   - generate local checksums for packed release artifacts or package-store snapshots;
   - validate checksum generation deterministically in tests;
   - do not require signing infrastructure unless explicitly approved.
5. Update docs:
   - installation from a local checkout;
   - installation through package manager after publication;
   - release dry-run procedure;
   - rollback guidance.

Phase 4 deliverables:
1. Cursor user-scope hardening:
   - capability-detect supported Cursor global rule locations if possible;
   - keep graceful failure when detection is unavailable;
   - never guess and write into an undocumented user directory without a clear check.
2. Gemini hardening:
   - keep marker-managed `GEMINI.md` behavior;
   - add compatibility checks for user and repo scope;
   - document Gemini extension packaging as deferred unless implementation is clearly low-risk.
3. Codex hardening:
   - keep Agent Skills mode and `AGENTS.md` fallback;
   - add adapter compatibility checks for both modes;
   - do not implement Codex plugin packaging unless the plugin surface is stable and documented locally.
4. Adapter compatibility tests:
   - verify generated adapter paths and marker contents for all supported runtime/scope pairs;
   - verify unsupported pairs fail or skip gracefully with actionable messages;
   - verify repeated install/update/uninstall remains idempotent;
   - verify dry-run performs zero filesystem mutations.
5. Improve status/validate reporting as needed:
   - include unsupported/skipped runtime details;
   - keep `--json` stable and machine-readable;
   - avoid breaking existing tests unless the output contract is intentionally versioned.

Important safety constraints:
- Keep all AI/provider API calls out of the client and out of installer behavior.
- Do not read, write, or copy `.env` files.
- Do not make live Notion or Linear writes.
- Do not delete user files except under explicit uninstall flags.
- Preserve marker-managed shared files by editing only the ProductSkills marker block.
- Preserve non-generated dedicated adapters unless explicit `--force` is provided.
- Keep `--trust-source` separate from `--force`; `--force` must not silently authorize execution of validation scripts from untrusted sources.
- Maintain rollback behavior for failed updates.

Tests to add or update:
- npm/package dry-run artifact contents exclude ignored construction docs, `.env*`, `.product-skills/`, pycache, and generated eval results.
- `install.sh --dry-run` performs no filesystem mutation.
- version consistency check passes and fails on intentional mismatch.
- checksum generation is deterministic.
- Cursor user-scope detection succeeds when a supported test fixture is present and fails gracefully when absent.
- Gemini user/repo compatibility checks preserve existing `GEMINI.md`.
- Codex `skills` and `agents` adapter modes both validate.
- `uninstall --runtime all --scope user` skips unsupported runtimes without aborting earlier removals.
- update rollback remains covered.

Validation required before final response:
- python3 scripts/check_package.py .
- python3 scripts/run_trigger_evals.py .
- python3 scripts/check_tool_safety.py .
- python3 scripts/check_forward_tests.py .
- python3 -m py_compile scripts/check_package.py scripts/run_trigger_evals.py scripts/grade_artifact.py scripts/check_tool_safety.py scripts/check_forward_tests.py
- node --check bin/product-skills.mjs
- node --test tests/installer.test.mjs
- any new package/distribution validation command added during implementation
- dry-run smoke tests for:
  - install from checkout;
  - update from checkout;
  - uninstall adapter-only;
  - uninstall with package-store removal;
  - package/distribution dry-run;
  - Cursor user-scope unsupported/detected behavior.

Review required:
- Run Claude read-only review before committing important changes:
  `claude -p "Review the current git diff against the ProductSkills installer SDD. Do not modify files. Focus on Phase 3/4 distribution, runtime hardening, data-loss risks, security risks, missing error handling, and test gaps. Return blocking issues, non-blocking suggestions, test gaps, and questions."`
- Accept or reject each finding explicitly.
- Patch accepted blocking findings before committing.

Commit rules:
- Use Conventional Commits.
- Prefer one logical commit for Phase 3 and one logical commit for Phase 4 if the work is large.
- Do not commit ignored design/planning docs unless the user explicitly asks.
- Do not commit `.product-skills/`, packed tarballs, generated checksum output, or local package stores unless the file is intentionally part of release scaffolding.
- Do not tag, publish, or create GitHub releases unless explicitly asked.

Final response should include:
- branch and commit(s);
- files added or changed;
- implemented Phase 3 items;
- implemented Phase 4 items;
- validation commands and results;
- Claude review result and accepted/rejected findings;
- remaining deferred items, especially real npm publishing, signing, Gemini extension packaging, and Codex plugin packaging if not implemented.
```
