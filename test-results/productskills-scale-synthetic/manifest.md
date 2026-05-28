# Scale Pack Manifest

## Generated Corpora

| Directory | Evidence Items | Ground Truth |
| --- | ---: | --- |
| `corpus/scale-100` | 100 | `ground-truth/scale-100/planted-ground-truth.json` |
| `corpus/scale-500` | 500 | `ground-truth/scale-500/planted-ground-truth.json` |
| `corpus/scale-1000` | 1000 | `ground-truth/scale-1000/planted-ground-truth.json` |
| `corpus/scale-5000` | 5000 | `ground-truth/scale-5000/planted-ground-truth.json` |

## Unlabeled Corpora

| Directory | Evidence Items | Purpose |
| --- | ---: | --- |
| `corpus-unlabeled/scale-100` | 100 | Prompt-visible labels removed for measured runs. |
| `corpus-unlabeled/scale-500` | 500 | Prompt-visible labels removed for measured runs. |
| `corpus-unlabeled/scale-1000` | 1000 | Prompt-visible labels removed for measured runs. |
| `corpus-unlabeled/scale-5000` | 5000 | Prompt-visible labels removed for measured runs. |

## Planted Opportunities

| ID | Expected Classification |
| --- | --- |
| `OPP-STRONG-001` | Strong: evidence-linked PRD and opportunity synthesis |
| `OPP-STRONG-002` | Strong: dry-run Linear/Notion delivery preview |
| `OPP-RISKY-001` | Risky: automatic live sync to external tools |
| `OPP-RISKY-002` | Risky: enterprise launch with incomplete security evidence |
| `OPP-WEAK-001` | Weak: free lightweight founder PRD templates |
| `OPP-AMBIG-001` | Ambiguous: GitHub Issues delivery preview |
| `OPP-DATA-001` | Strong: support-ticket import quality controls |
| `NOISE-LOW-001` | Noise: low-value cosmetic requests |

## Required Blocking Decisions

- Live Notion or Linear writes.
- Enterprise security certification claims.
- Paid conversion claims.
- Pricing decisions.
- Workspace ID resolution against real systems.

## Ground-Truth Ranking Buckets

Do not use `expected_top_opportunities` as the only grading target. Each generated truth file now splits opportunity expectations into:

- `top_by_frequency`;
- `top_by_arr`;
- `top_by_strategic_weight`;
- `risky_minority`;
- `noise_controls`.
