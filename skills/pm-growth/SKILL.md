---
name: pm-growth
description: Product growth workflows for growth models, growth loops, activation, retention, monetization, lifecycle strategy, product-led growth, funnel-stage diagnostics, experiment backlogs, experiment readouts, post-launch metric loops, and Reforge-style growth/product analysis. Use when the user asks to improve growth, activation, retention, conversion, monetization, expansion, PLG, lifecycle, run a growth experiment, write an experiment readout, or diagnose a post-launch learning loop. Do not use for designing the metric tree the experiments target (route to pm-metrics); for prioritization across non-growth bets (route to pm-strategy); or for customer-facing launch comms (route to pm-gtm).
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# PM Growth

Diagnose growth systems and turn bottlenecks into product experiments.

## Core Procedures

- Use `procedures/growth-model.md` to map the product growth model.
- Use `procedures/growth-loop-diagnosis.md` to diagnose loops and bottlenecks across stages.
- Use `procedures/funnel-stage-analysis.md` for a focused single-stage analysis — pass `stage: activation | retention | monetization` as a parameter. (Replaces the previous activation-analysis / retention-analysis / monetization-analysis procedures, which differed only by stage parameter.)
- Use `procedures/plg-motion.md` for product-led growth and sales-assist handoff questions.
- Use `procedures/lifecycle-experiment.md` for designing a growth experiment.
- Use `procedures/experiment-readout.md` for writing up a completed experiment with decision and downstream implications.

## References

- Use `../../references/frameworks/growth-models.md` for growth loops, lifecycle, PLG, and stage-specific frameworks.
- Use `../../references/checklists/growth-method-coverage.md` before finalizing growth recommendations.
- Use `../../templates/growth-model.md` for model outputs.
- Use `../../templates/experiment-brief.md` for experiments and their readouts.

## Method Selection

- Bottleneck is unclear; "growth is slow" symptom → `growth-loop-diagnosis` (cross-stage diagnosis).
- Bottleneck is named and lives at a specific funnel stage → `funnel-stage-analysis` with `stage: activation | retention | monetization`.
- Question is about PLG vs sales-assist motion → `plg-motion`.
- Ready to design an experiment with hypothesis + primary metric + decision rule → `lifecycle-experiment`.
- An experiment finished and the team needs the readout + decision → `experiment-readout`.
- Whole-product growth shape needs mapping (loops, lifecycle, monetization model) → `growth-model`.

## Output Standard

Growth outputs must identify target metric, current bottleneck, affected segment, loop/funnel stage, experiment hypothesis, guardrail metric, and decision rule. Every primary-metric claim has a baseline + cited source; invented numbers are refused.

## Guardrails

- Post-launch signals feed back into discovery. When `experiment-readout` or `funnel-stage-analysis` surfaces an opportunity for new product investigation (a segment underserved, a value hypothesis disconfirmed, a new bottleneck), the output explicitly names the discovery input that should follow and recommends routing it to `pm-discovery`.
- Every experiment readout requires a pre-stated decision rule; rules retrofitted after the result are refused (see `procedures/experiment-readout.md` refusal contract).
- No baseline or industry benchmark is invented. Every claim has a cited source.
