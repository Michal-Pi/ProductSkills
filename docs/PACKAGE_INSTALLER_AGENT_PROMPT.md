# Package Installer Agent Prompt

Use this prompt to start the next implementation session.

```text
You are implementing the ProductSkills package installer.

Repository:
/Users/pilawski/My_projects/skillsos/Design Docs Product

Branch:
feat/initial-product-os-package

Remote:
https://github.com/Michal-Pi/ProductSkills.git

Current state:
- The runnable ProductSkills package is committed and pushed.
- Design and planning docs used during package construction are intentionally ignored.
- `docs/PACKAGE_INSTALLER_SDD.md` has been written and reviewed by Claude.
- Claude's final review found no remaining blocking issues and said the SDD is ready for implementation.
- Do not make live Notion or Linear writes.
- Do not install dependencies unless the user explicitly approves.
- Preserve existing files and do not revert unrelated changes.

Read first:
- docs/PACKAGE_INSTALLER_SDD.md
- docs/LOCAL_INSTALLATION.md
- docs/PRODUCT_OS_WORKFLOW_DOCUMENTATION.md
- docs/PRODUCT_OS_WORKFLOW_TESTING_PLAN.md
- docs/HOW_TO_USE_PRODUCT_OS_WORKFLOW.md
- package.yaml
- registry.json
- scripts/check_package.py
- scripts/run_trigger_evals.py
- scripts/check_tool_safety.py
- scripts/check_forward_tests.py

Implementation scope:
Implement Phase 1 from `docs/PACKAGE_INSTALLER_SDD.md`.

Required deliverables:
1. Add root `VERSION` aligned with `package.yaml`.
2. Add `package.json` with a `product-skills` bin entry and minimum Node version.
3. Add `bin/product-skills.mjs`.
4. Add adapter templates:
   - adapters/claude/SKILL.md
   - adapters/codex/SKILL.md
   - adapters/codex/AGENTS.md
   - adapters/cursor/product-operating-system.mdc
   - adapters/gemini/GEMINI.md
5. Implement CLI commands:
   - `install`
   - `validate`
   - `status`
6. Implement options:
   - `--runtime claude|codex|cursor|gemini|all`
   - `--scope user|repo`
   - `--adapter skills|agents|auto`
   - `--repo <path>`
   - `--package-store <path>`
   - `--source <path-or-url>`
   - `--ref <git-ref>`
   - `--force`
   - `--replace`
   - `--dry-run`
   - `--json`
   - `--track-package-store`
   - aliases `--global` and `--project`
7. Support user and repo package stores:
   - user: `~/.product-skills`
   - repo: `<repo>/.product-skills`
8. Support self-install from inside the ProductSkills repo without recursive copy:
   - stage outside the repo;
   - exclude `.git/`, `.product-skills/`, ignored design docs, pycache, and generated eval results;
   - add `.product-skills/` to `.gitignore` unless `--track-package-store` is passed.
9. Generate runtime adapters:
   - Claude user/repo SKILL.md;
   - Codex SKILL.md and AGENTS.md fallback;
   - Cursor repo `.mdc`;
   - Gemini user/repo marker-managed `GEMINI.md`.
10. Implement file preservation:
   - fully managed dedicated adapters;
   - marker-managed shared files;
   - backups for existing non-generated files;
   - malformed marker detection.
11. Add installer tests using only built-in Node modules or existing Python standard library tools.
12. Update docs as needed, especially installation docs.

Out of scope for this session:
- `update`
- `uninstall`
- npm publishing
- checksums/signatures
- Cursor user-scope support beyond graceful failure
- Gemini extension packaging
- Codex plugin packaging

Validation required before final response:
- python3 scripts/check_package.py .
- python3 scripts/run_trigger_evals.py .
- python3 scripts/check_tool_safety.py .
- python3 scripts/check_forward_tests.py .
- python3 -m py_compile scripts/check_package.py scripts/run_trigger_evals.py scripts/grade_artifact.py scripts/check_tool_safety.py scripts/check_forward_tests.py
- node --check bin/product-skills.mjs
- installer test command added during implementation
- dry-run install smoke tests for at least:
  - repo scope Claude
  - repo scope Codex AGENTS fallback
  - repo scope Cursor
  - repo scope Gemini with existing GEMINI.md
  - self-install from this repo

Commit rules:
- Use Conventional Commits.
- Keep installer implementation in one logical commit if possible.
- Do not commit ignored design/planning docs.
- Do not commit `.product-skills/` package store output.
- Do not tag or publish unless explicitly asked.

Final response should include:
- files added or changed;
- implemented commands and options;
- how user and repo installs work;
- validation commands and results;
- any deferred SDD items.
```
