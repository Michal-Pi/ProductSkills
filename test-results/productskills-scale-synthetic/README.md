# ProductSkills Scale Synthetic Test Pack

This pack stress-tests ProductSkills beyond the small curated E2E suite. It uses deterministic synthetic AtlasBoard corpora at increasing sizes to find where product reasoning, citation discipline, workflow routing, and dry-run tooling safety degrade.

All data is fictional. Do not use real customer data, secrets, API keys, private business information, or external systems.

## What This Tests

- Whether ProductSkills can handle hundreds or thousands of evidence items.
- Whether planted opportunities are recalled without inventing unsupported opportunities.
- Whether citations still point to evidence that supports the claim.
- Whether conflicting and minority high-risk signals survive summarization.
- Whether the system blocks when pricing, security, workspace IDs, launch readiness, or paid-conversion data is missing.
- Whether Linear and Notion behavior remains dry-run-first at scale.
- Whether outputs remain useful for product organizations, not just complete-looking templates.

## Structure

```text
productskills-scale-synthetic/
  README.md
  generator-config.json
  corpus/
    scale-*/
  corpus-unlabeled/
    scale-100/
    scale-500/
    scale-1000/
    scale-5000/
  ground-truth/
    scale-100/
    scale-500/
    scale-1000/
    scale-5000/
  prompts/
  graders/
  edge-cases/
  scripts/
  results/
```

Each `corpus/scale-*` directory includes:

- `interviews.md`
- `support_tickets.md`
- `sales_notes.md`
- `churn_notes.md`
- `competitor_notes.md`
- `usage-analytics.md`
- `product-context.md`

Each `corpus-unlabeled/scale-*` directory includes the same source files with prompt-visible opportunity IDs, duplicate labels, conflict labels, and missing-field labels removed. Use the unlabeled corpus for measured discovery and strategy reliability runs; reserve the labeled corpus for debugging, grader development, and regression diagnosis.

Each `ground-truth/scale-*` directory includes `planted-ground-truth.json` with:

- planted opportunity counts
- expected top opportunities
- split ranking truth: `top_by_frequency`, `top_by_arr`, `top_by_strategic_weight`, `risky_minority`, and `noise_controls`
- evidence-to-opportunity map
- known conflicts
- known missing evidence
- known duplicates
- required blocked decisions
- tooling safety traps

## Scale Levels

| Scale | Purpose |
| --- | --- |
| `scale-100` | Sanity check. Should fit comfortably in most contexts. |
| `scale-500` | Medium-context stress. Tests citation and conflict retention. |
| `scale-1000` | Large corpus. Tests staged summarization and evidence maps. |
| `scale-5000` | Breakpoint test. Should force batching, compression, and explicit limits. |

## Expected Failure Modes

The tests are designed to reveal:

- Generic summaries that ignore planted ground truth.
- Unsupported citations.
- Dropped minority signals with high ARR or high risk.
- Overweighting noisy frequent low-value requests.
- Unsafe claims that dry-run previews created real Linear/Notion records.
- PRD or launch conclusions based on missing security, pricing, or paid-conversion data.
- Stage outputs that cannot be reused by the next workflow step.

## Large-Corpus Protocol

Scale runs at 500+ rows must use the ProductSkills large-corpus synthesis protocol:

- batch summaries;
- source-ID `evidence_ledger`;
- dedupe table;
- conflict register;
- missing-field table;
- minority-signal carry-forward;
- noisy-signal suppression;
- representative citations in narrative and exhaustive source-ID coverage in working ledgers at 1000+ rows;
- final roll-up with source counts before and after dedupe, ARR sums from supplied data only, confidence, conflicts, duplicates removed, and missing-field counts.

Do not grade scale reliability from breakpoint projections alone. Store actual generated outputs for prompts `01` through `08` under `results/generated-outputs/` and grade those artifacts.

## Generate Or Regenerate Corpora

```bash
python3 test-results/productskills-scale-synthetic/scripts/generate_scale_corpus.py
```

The generator is deterministic. It uses the seed in `generator-config.json` and rewrites the labeled corpora, unlabeled corpora, and ground-truth JSON files.

## How To Run

1. Start with `prompts/01-scale-discovery.md` on `scale-100`.
2. Repeat on `scale-500`, `scale-1000`, and `scale-5000`.
3. Grade with `graders/scale-rubric.md`.
4. Run `prompts/07-scale-full-workflow.md` to test stage-to-stage handoffs.
5. Run `prompts/08-scale-adversarial-edge-cases.md` to test safety and edge behavior.
6. Run `prompts/09-scale-breakpoint-evaluation.md` to find the first scale where quality materially degrades.

No prompt requires external writes.
