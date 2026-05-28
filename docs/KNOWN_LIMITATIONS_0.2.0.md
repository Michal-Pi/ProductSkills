# Known Limitations 0.2.0

0.2.0 is suitable for local controlled use and beta refinement. It is not yet
ready to claim category leadership or broad production reliability.

## Runtime Evidence

- The synthetic E2E harness is wired, but actual Codex, Claude, and Gemini
  runtime outputs still need to be captured under
  `test-results/productskills-e2e-synthetic/generated/<runtime>/`.
- Negative prompts 13-18 are currently manual adversarial smoke coverage until
  they are mapped to deterministic fixtures.
- Runtime-emitted Notion or Linear payloads must be converted into
  `tool-safety-fixtures/*.json` before the tool-safety grader can score them.

## Scale Evidence

- Scale prompts 01-08 need fresh measured runtime outputs against
  `corpus-unlabeled` before prompt 09 breakpoint summaries should be treated as
  release evidence.
- Existing breakpoint result files are historical/projection artifacts.
- Large-corpus scoring now has split ground truth v2, but grading and
  cross-runtime comparison still require stored generated artifacts.

## Runtime Surfaces

- Codex skill visibility depends on the target Codex runtime loading
  `.codex/skills/*/SKILL.md`.
- Gemini extension visibility depends on Gemini CLI extension discovery under
  `~/.gemini/extensions/`.
- Cursor user-scope installation is supported only when a supported global
  rules directory can be detected or provided with
  `PRODUCT_SKILLS_CURSOR_USER_RULES_DIR`.

## Tooling

- ProductSkills continues to require dry-run previews and explicit user
  confirmation before live Notion, Linear, or other external writes.
- The installer validates package structure and adapters, but it does not prove
  that a runtime UI has reloaded newly installed skills/extensions.
