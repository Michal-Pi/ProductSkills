---
name: pm-validation
description: Product validation workflows for assumption mapping, problem validation, solution validation, experiment design pre-build, Teresa Torres-style opportunity solution trees, riskiest-assumption testing, and validation decisions (proceed / iterate / kill / needs more evidence). Use when the user asks to validate an idea, test whether a problem is real, test a prototype, map assumptions, design the smallest pre-build experiment, or decide whether evidence is sufficient to commit scope. Do not use for production experiments against shipped features (route to pm-growth); for designing the metric the experiment moves (route to pm-metrics); or for usability testing UX patterns (route to pm-design).
allowed-tools: [Read, Write, Edit, Grep, Glob]
---

# PM Validation

Turn uncertainty into explicit assumptions, tests, and decision rules.

## Core Procedures

- Use `procedures/assumption-map.md` for what-must-be-true analysis.
- Use `procedures/problem-validation.md` to test whether the problem is real and important.
- Use `procedures/solution-validation.md` to test whether the solution works for a validated problem.
- Use `procedures/experiment-design.md` for test plans and success criteria.

## References

- Use `../../references/frameworks/continuous-discovery.md` for opportunity solution trees.
- Use `../../references/methods/evidence-grading.md` when choosing validation confidence and next tests.
- Use `../../references/checklists/validation-method-coverage.md` before finalizing validation plans.
- Use `../../templates/validation-plan.md` or `../../templates/experiment-brief.md` for structured outputs.

## Quality Bar

Every validation plan must include the assumption, test method, audience, success metric, guardrail, and decision rule.
