# How To Use The Product Operating System Workflow

## When To Use It

Use `workflow-product-operating-system` when product work needs routing across multiple stages or when the correct next stage is ambiguous.

Good fit:

- "Take this from idea to launch."
- "What is the next product workflow step?"
- "Continue this product work from this PRD."
- "We have delivery artifacts and need launch readiness."
- "We have post-launch metrics; what should we learn and do next?"

Use a narrower skill when the task is clearly single-stage:

- `pm-docs` for a single PRD review.
- `pm-tooling` for a Linear or Notion dry-run payload only.
- `workflow-discovery-to-prd` for raw evidence into PRD.
- `workflow-prd-to-linear-delivery` for approved PRD into delivery and Linear preview.

## Basic Usage Pattern

Provide:

1. The artifact or signal you have.
2. The desired outcome.
3. Any known lifecycle state, such as rough PRD, approved PRD, delivery-ready scope, launch request, or post-launch metrics.
4. Evidence sources and confidence level when known.
5. Tooling context only if you want Notion or Linear preview.

Example:

```text
I have an approved PRD for teammate setup insights. Continue the product workflow from here. Check delivery readiness, split epics and stories, prepare Linear dry-run previews, assess launch readiness, and define the post-launch learning plan. Do not replay validation unless the readiness check fails.
```

## Expected Output

A good workflow output should include:

- entry classification;
- lifecycle status;
- evidence used;
- assumptions;
- validation decision or validation-not-required rationale;
- current artifact or blocked artifact;
- approval gates;
- next action;
- handoff target.

## Common Entry Points

### Raw Evidence

Prompt:

```text
Turn these interviews, support tickets, and analytics notes into the next product artifact. Preserve direct evidence, inference, confidence, assumptions, and approval gates.
```

Expected route:

```text
intake_received -> evidence triage -> opportunity framing -> evidence and validation decision
```

### Founder Hypothesis With No Evidence

Prompt:

```text
I have a feature idea but no customer interviews, usage data, support tickets, or sales notes. Run the workflow and tell me what can safely be produced.
```

Expected route:

```text
evidence_insufficient -> blocked workflow artifact -> research or validation plan
```

Expected behavior:

- no committed PRD scope;
- missing evidence named;
- resume status included.

### Rough PRD

Prompt:

```text
I have a rough PRD with a goal and proposed solution, but evidence is mixed and non-goals are missing. Continue from this artifact and repair what is needed.
```

Expected route:

```text
prd_review_required -> PRD readiness review -> repair or validation decision
```

### Approved PRD

Prompt:

```text
This PRD is approved and includes scope, non-goals, assumptions, risks, and metrics. Continue into delivery readiness and tool preview. Do not force validation replay.
```

Expected route:

```text
approved_for_delivery -> validation_not_required -> delivery readiness gate -> delivery split
```

### Tool Preview

Prompt:

```text
Prepare Notion and Linear dry-run previews for this approved artifact. Include target IDs, idempotency keys, payload hashes, and confirmation questions.
```

Expected route:

```text
ready_for_tool_preview -> dry-run preview -> ready_for_human_write_confirmation
```

Expected behavior:

- preview only;
- explicit confirmation required;
- no live write during evals or first pass.

### Launch Readiness

Prompt:

```text
We have delivery artifacts and want to launch in two weeks. Start at launch readiness and check audience, customer impact, enablement, support, risks, success metrics, and post-launch learning.
```

Expected route:

```text
ready_for_launch_review -> launch readiness gate -> launch_ready or blocked
```

### Post-Launch Learning

Prompt:

```text
The feature launched last month. Activation improved, support tickets dropped, but one segment still reports confusion. Synthesize learning, update assumptions, decide what to do next, and create the next discovery input.
```

Expected route:

```text
learning_loop_open -> metric readout -> customer signal -> assumption updates -> next discovery input
```

## Approval Gates

The workflow should ask before:

- promoting weak evidence into committed scope;
- accepting risk instead of running validation;
- treating an ambiguous PRD as delivery-ready;
- creating or updating external tool records;
- launching with unresolved customer, support, legal, or operational risk.

## Blocked State

If the workflow blocks, treat the output as useful work. It should tell you:

- why it stopped;
- what is missing;
- what can safely be done now;
- what risk would be created by continuing;
- which status to resume from;
- who or what should handle the next step.

## Tooling Safety

Notion and Linear outputs are dry-run first.

Before any write, the workflow must show:

- target workspace or team;
- payload summary;
- idempotency keys;
- `dry_run_payload_hash`;
- exact confirmation question.

Do not treat a preview as a completed write.
