# Experiment Design

Use when a product question can be answered with a bounded experiment.

## Steps

1. State hypothesis and assumption.
2. Identify audience and sample constraints.
3. Choose the smallest credible method.
4. Define primary metric, guardrail metric, minimum detectable signal if known, and duration.
5. Decide what result means ship, iterate, research, or stop.
6. Note ethical, privacy, support, and brand risks.

## Output

Use `../../../templates/experiment-brief.md`.

## Done when

- The hypothesis is written as IF/THEN/BY (intervention, expected effect, mechanism); the underlying assumption being tested is named.
- Audience, sample constraints, primary metric, guardrail metric, and duration are populated; minimum detectable signal is calculated or explicitly marked "unknown - underpowered" rather than omitted.
- A decision rule maps each plausible outcome to ship, iterate, research, or stop; ethical, privacy, support, and brand risks are listed with mitigation or an explicit acceptance.
- When the assumption is too unbounded for a single experiment to invalidate, the procedure refuses to launch and proposes a smaller question or a different method (interview, fake-door, prototype test) instead.
