# Runtime Meta-Prompts

Use these prompts to run the same synthetic ProductSkills E2E pack across different LLM runtimes and store comparable generated artifacts plus result files.

The full pack includes both positive prompts under `prompts/` and runtime-facing negative safety prompts under `negative-prompts/`.

## Files

- `evaluate-productskills-end-to-end.md`: recommended single prompt for Codex, Claude, and Gemini to evaluate skill coverage, stage outputs, end-to-end usefulness, and product-organization readiness.
- `run-in-codex.md`: paste into Codex to create `productskills-e2e-synthetic/generated/codex/*.md`, `graded/codex/*.json`, and a smoke summary in `results/codex-run-2026-05-27.md`.
- `run-in-claude.md`: paste into Claude to create `productskills-e2e-synthetic/generated/claude/*.md`, `graded/claude/*.json`, and a smoke summary in `results/claude-run-2026-05-27.md`.
- `run-in-gemini.md`: paste into Gemini to create `productskills-e2e-synthetic/generated/gemini/*.md`, `graded/gemini/*.json`, and a smoke summary in `results/gemini-run-2026-05-27.md`.
- `compare-runtime-results.md`: paste into any ProductSkills-enabled runtime after all three result files exist to create `productskills-e2e-synthetic/results/runtime-comparison-2026-05-27.md`.

## Safety

All prompts require dry-run behavior and prohibit live Notion, Linear, GitHub, npm, or network writes.

PASS requires generated artifacts plus passing grader JSON for mapped core prompts. Summary-only run files are smoke evidence only.

## Recommended Order

1. Paste `evaluate-productskills-end-to-end.md` into Codex.
2. Paste `evaluate-productskills-end-to-end.md` into Claude.
3. Paste `evaluate-productskills-end-to-end.md` into Gemini.
4. Run `compare-runtime-results.md` after all runtime-specific result files exist.
