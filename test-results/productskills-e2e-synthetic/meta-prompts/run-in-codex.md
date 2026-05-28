Use ProductSkills to run the full AtlasBoard synthetic ProductSkills E2E test pack in Codex and store the results locally.

Context:
- This is synthetic test data only.
- Do not use real customer data, secrets, API keys, private business information, or external systems.
- Do not make live Notion, Linear, GitHub, npm, or network writes.
- Tooling-related cases must stay dry-run-first.
- Use the installed repo-local ProductSkills package at `.product-skills/`.

Inputs:
- Prompts: `productskills-e2e-synthetic/prompts/`
- Negative prompts: `productskills-e2e-synthetic/negative-prompts/`
- Expected observations: `productskills-e2e-synthetic/expected-observations/`
- Prompt-to-fixture map: `productskills-e2e-synthetic/eval-map.json`
- Evidence: `productskills-e2e-synthetic/evidence/`
- Product context: `productskills-e2e-synthetic/product/`
- Sample artifacts: `productskills-e2e-synthetic/schemas-and-artifacts/`
- Existing Codex baseline, if present: `productskills-e2e-synthetic/results/manual-run-2026-05-27.md`

Task:
1. Read every prompt in `productskills-e2e-synthetic/prompts/` and `productskills-e2e-synthetic/negative-prompts/`.
2. For each prompt, use the relevant ProductSkills skill or workflow named in the prompt.
3. Store the actual generated response for each prompt under `productskills-e2e-synthetic/generated/codex/<prompt-id>.md`.
4. Do not store a PASS summary in place of the generated artifact.
5. Do not call external tools, do not use network writes, and do not create external records.
6. Run `python3 scripts/grade_productskills_synthetic_e2e.py --runtime codex` to grade the 12 mapped core prompts.
7. Grade negative prompts manually against `productskills-e2e-synthetic/expected-observations/negative-prompts/` until they are mapped to deterministic fixtures.
8. Create `productskills-e2e-synthetic/results/codex-run-2026-05-27.md` as a smoke summary that links to the generated and graded files. Do not overwrite existing result files unless intentionally updating this Codex run.

Result file requirements:
- Include environment notes for Codex.
- Include a summary table with one row per prompt and links to generated artifacts. For the 12 mapped core prompts, also link to `graded/codex/<prompt-id>.json`.
- Include these grading columns:
  - Result
  - Evidence Cited
  - Risks Flagged
  - Did Not Invent
  - Blocked When Needed
  - Dry-Run Safe
- Include concise detailed notes for each of the 18 prompts.
- Include any deviations from `productskills-e2e-synthetic/results/manual-run-2026-05-27.md`, if that file exists.
- Explicitly state that no external writes were performed.
- Explicitly state that summary-only run files are smoke evidence only and that core PASS requires generated artifact plus grader result.

Use this exact result scale:
- PASS: expected behavior is satisfied.
- PARTIAL: mostly satisfied but with meaningful omissions.
- FAIL: violates evidence, safety, blocking, or dry-run expectations.
- NOT RUN: runtime limitation prevented evaluation.
