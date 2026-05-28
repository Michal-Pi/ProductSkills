# Graded Runtime Results

Store deterministic grader output here. A PASS claim for the synthetic E2E pack requires both:

- a generated artifact under `generated/<runtime>/<prompt-id>.md`;
- a grader result under `graded/<runtime>/<prompt-id>.json` showing `"passed": true`.

Tooling prompts may also have `graded/<runtime>/tool-safety.json` when the runtime output includes structured Linear or Notion dry-run payload fixtures.
