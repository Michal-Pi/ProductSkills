# Generated Runtime Artifacts

Store actual runtime outputs here before grading. Summary-only run files do not belong in this directory.

Required layout:

```text
generated/<runtime>/<prompt-id>.md
generated/<runtime>/tool-safety-fixtures/<case>.json
```

Examples:

```text
generated/codex/01-pm-discovery.md
generated/claude/09-pm-tooling.md
generated/gemini/tool-safety-fixtures/linear-preview-dry-run.json
```

The markdown file must be the artifact produced by the runtime for the prompt, not a pass/fail summary. Tool-safety fixture JSON files are optional and should be added when a tooling prompt emits structured Linear or Notion payloads that can be represented with the existing `schemas/tool-safety-fixture.schema.json` shape.
