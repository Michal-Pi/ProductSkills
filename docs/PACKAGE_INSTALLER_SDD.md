# ProductSkills Package Installer SDD

## Status

Draft reviewed by Claude. Accepted review findings have been incorporated. Implementation should not begin until the remaining runtime-surface assumptions are confirmed during Phase 1.

## Review Resolution

Claude's read-only review found four blocking issues. Resolution:

- Codex adapter surface: defaults to Agent Skills in both scopes, with `AGENTS.md` available only as explicit fallback.
- Gemini user scope: defaults to the extension adapter, with marker-managed `~/.gemini/GEMINI.md` available through explicit `--adapter context`.
- File preservation: split dedicated fully managed adapters from marker-managed shared files.
- Self-install: specified current-checkout source handling, temporary staging, recursive-copy exclusions, and default `.product-skills/` ignore behavior.

## Purpose

ProductSkills needs a real installer and updater instead of copy-paste installation instructions.

The installer should make the package usable across:

- Claude Code;
- Codex;
- Cursor;
- Gemini CLI;
- later runtimes that can consume file-based instructions.

The installer should support both:

- user-level installation, available across projects;
- repo-level installation, committed or kept local inside one project.

The design follows the same broad pattern as GSD: a shared package directory plus thin runtime-specific adapters, with update and validation commands.

## Goals

- Install the runnable ProductSkills package into a stable location.
- Generate runtime adapters for Claude Code, Codex, Cursor, and Gemini.
- Support user and repo scopes.
- Preserve existing user files and back them up before overwrite.
- Validate package integrity after install and update.
- Support future updates without requiring manual copy commands.
- Avoid live Notion or Linear writes during install, validation, or smoke tests.
- Keep design and planning docs out of installed runtime packages unless explicitly requested.

## Non-Goals

- Do not implement live Notion or Linear integrations.
- Do not create a marketplace submission in this phase.
- Do not support every AI coding tool on day one.
- Do not require npm publishing for the first installer iteration.
- Do not replace native runtime package managers where they exist.
- Do not install dependencies without explicit user action.

## User Stories

### User-Level Install

As a PM or builder, I want to install ProductSkills once and use it across my local projects.

Example:

```bash
product-skills install --runtime codex --scope user
product-skills install --runtime claude --scope user
```

### Repo-Level Install

As a team, I want ProductSkills available inside one repository so every collaborator gets the same workflow instructions.

Example:

```bash
product-skills install --runtime cursor --scope repo
product-skills install --runtime gemini --scope repo
```

### Update

As a user, I want to update ProductSkills without losing local adapter edits.

Example:

```bash
product-skills update --scope user
product-skills update --scope repo
```

### Validate

As a maintainer, I want a fast command that verifies the installed package is complete.

Example:

```bash
product-skills validate --scope user
product-skills validate --scope repo
```

## Architecture

The installer has two layers:

1. Shared package store.
2. Runtime adapter.

The shared package store contains the full ProductSkills package:

```text
<package-store>/
  VERSION
  README.md
  package.yaml
  registry.json
  docs/
  evals/
  references/
  schemas/
  scripts/
  skills/
  templates/
```

The runtime adapter is small. It tells the runtime where the package store is and which files to read first.

This keeps updates simple: update the package store, then regenerate adapters only when adapter templates change.

The package store is fully managed by the installer. Users should not edit files under `.product-skills/` or `~/.product-skills/` directly. Customization belongs in runtime adapters or separate project instructions.

## Scope Model

### User Scope

User scope installs into the user's home directory.

Default package store:

```text
~/.product-skills/
```

Runtime adapters:

```text
~/.claude/skills/product-operating-system/SKILL.md
~/.codex/skills/product-operating-system/SKILL.md
~/.gemini/extensions/product-skills/gemini-extension.json
~/.gemini/extensions/product-skills/GEMINI.md
```

Gemini user scope may still use marker-managed `~/.gemini/GEMINI.md` with
explicit `--adapter context`.

Cursor user-level support is runtime-dependent. The installer should support `--scope user --runtime cursor` only when it can locate a supported global Cursor rules directory. Otherwise it should stop with a clear message and recommend repo scope.

### Repo Scope

Repo scope installs into the current repository.

Default package store:

```text
<repo>/.product-skills/
```

Runtime adapters:

```text
<repo>/.claude/skills/product-operating-system/SKILL.md
<repo>/.codex/skills/product-operating-system/SKILL.md
<repo>/.cursor/rules/product-operating-system.mdc
<repo>/GEMINI.md
```

Codex repo scope may still use marker-managed `<repo>/AGENTS.md` with explicit
`--adapter agents`.

Repo scope should be the default when the command is run inside a git repository and the user does not specify `--scope`.

User scope should be the default outside a git repository.

Repo-scope package stores should be ignored by default. The installer should offer to add `.product-skills/` to `.gitignore` when installing into a repo. Runtime adapters may be committed.

## Runtime Adapter Design

### Claude Code Adapter

Claude Code supports Agent Skills under user or project skill directories. The adapter should be a valid `SKILL.md`.

User path:

```text
~/.claude/skills/product-operating-system/SKILL.md
```

Repo path:

```text
<repo>/.claude/skills/product-operating-system/SKILL.md
```

Adapter content:

```md
---
name: product-operating-system
description: Product Operating System workflow for product discovery, PRDs, delivery, launch readiness, and post-launch learning. Use when product work needs routing across multiple PM lifecycle stages.
---

# Product Operating System

Use the installed ProductSkills package at:

`<package-store>`

Start with:

- `<package-store>/docs/HOW_TO_USE_PRODUCT_OS_WORKFLOW.md`
- `<package-store>/skills/workflow-product-operating-system/SKILL.md`
- `<package-store>/skills/workflow-product-operating-system/procedures/product-operating-system.md`
- `<package-store>/references/workflows/product-operating-system-contract.md`

Rules:

- Do not invent customer evidence.
- Treat validation as an evidence and routing decision, not mandatory replay.
- Use dry-run previews for Notion and Linear.
- Return blocked workflow artifacts when evidence, target IDs, or approval are missing.
```

### Codex Adapter

Codex support has two adapter modes:

1. Agent Skills mode for Codex runtimes that load `SKILL.md` folders.
2. `AGENTS.md` fallback mode for Codex runtimes that only consume repository or user instruction files.

The installer should prefer Agent Skills mode for both user and repo scope so
ProductSkills are visible as Codex skills. `AGENTS.md` is a context-only
fallback and must be selected explicitly with `--adapter agents`.

User path:

```text
~/.codex/skills/product-operating-system/SKILL.md
~/.codex/AGENTS.md
```

Repo path:

```text
<repo>/.codex/skills/product-operating-system/SKILL.md
<repo>/AGENTS.md
```

The Codex `SKILL.md` adapter content can match the Claude adapter unless runtime-specific metadata is later needed.

The Codex `AGENTS.md` fallback must use a marker-delimited block:

```md
<!-- PRODUCT_SKILLS_START -->
# ProductSkills

Use the ProductSkills package at `<package-store>`.

Read:

- `<package-store>/docs/HOW_TO_USE_PRODUCT_OS_WORKFLOW.md`
- `<package-store>/skills/workflow-product-operating-system/procedures/product-operating-system.md`

Rules:

- Do not invent customer evidence.
- Treat validation as an evidence and routing decision.
- Keep external tool actions dry-run first.
- Produce blocked workflow artifacts when evidence or approval is missing.
<!-- PRODUCT_SKILLS_END -->
```

### Cursor Adapter

Cursor should use a rule file.

Repo path:

```text
<repo>/.cursor/rules/product-operating-system.mdc
```

Adapter content:

```md
---
description: Product Operating System workflow for product discovery, PRDs, delivery, launch readiness, and post-launch learning
alwaysApply: false
---

Use the ProductSkills package at `<package-store>`.

Read first:

- `<package-store>/docs/HOW_TO_USE_PRODUCT_OS_WORKFLOW.md`
- `<package-store>/skills/workflow-product-operating-system/procedures/product-operating-system.md`

Follow these rules:

- Do not invent customer evidence.
- Treat validation as routing, not mandatory replay.
- Use dry-run previews for Notion and Linear.
- Stop with a blocked workflow artifact when required inputs are missing.
```

Cursor repo scope is required for the first implementation. Cursor user scope should be treated as optional and capability-detected.

### Gemini Adapter

Gemini CLI supports context files such as `GEMINI.md` and user-scope
extensions. The installer should default user scope to the extension adapter
because it is the closest package-like surface, while repo scope should continue
to use `GEMINI.md`.

Repo path:

```text
<repo>/GEMINI.md
```

User path:

```text
~/.gemini/extensions/product-skills/gemini-extension.json
~/.gemini/extensions/product-skills/GEMINI.md
~/.gemini/GEMINI.md with explicit --adapter context
```

Gemini installs must preserve an existing `GEMINI.md`. If the file exists, the installer should append a clearly delimited ProductSkills block unless `--force` is passed.

Block format:

```md
<!-- PRODUCT_SKILLS_START -->
# ProductSkills

Use the ProductSkills package at `<package-store>`.

Read:

- `<package-store>/docs/HOW_TO_USE_PRODUCT_OS_WORKFLOW.md`
- `<package-store>/skills/workflow-product-operating-system/procedures/product-operating-system.md`

Rules:

- Do not invent customer evidence.
- Treat validation as an evidence and routing decision.
- Keep external tool actions dry-run first.
- Produce blocked workflow artifacts when evidence or approval is missing.
<!-- PRODUCT_SKILLS_END -->
```

On update, replace only the content between these markers.

## CLI Design

Primary command:

```bash
product-skills <command> [options]
```

Commands:

```bash
product-skills install
product-skills update
product-skills validate
product-skills status
product-skills uninstall
```

Common options:

```bash
--runtime claude|codex|cursor|gemini|all
--scope user|repo
--adapter skills|agents|context|extension|auto
--repo <path>
--package-store <path>
--source <path-or-url>
--ref <git-ref>
--force
--replace
--dry-run
--json
--track-package-store
```

Aliases:

```bash
--global -> --scope user
--project -> --scope repo
```

### Install

Examples:

```bash
product-skills install --runtime codex --scope user
product-skills install --runtime claude --scope repo
product-skills install --runtime all --scope repo
```

Behavior:

1. Resolve scope.
2. Resolve package store.
3. Resolve install source.
4. Copy or clone ProductSkills package into package store.
5. Validate package store with `python3 scripts/check_package.py <package-store>`.
6. Generate runtime adapter.
7. Back up any existing adapter before overwrite.
8. Print restart or reload instructions.

Install source rules:

- If run inside the ProductSkills repository, use the current checkout as the source.
- If run outside the ProductSkills repository and `--source <path-or-url>` is provided, use that source.
- Otherwise clone from the canonical GitHub URL.
- If the package store is inside the source tree, abort unless this is the explicit self-install case handled by a temporary copy.

Self-install behavior:

- When installing repo scope from inside the ProductSkills repo, copy the package through a temporary staging directory outside the repo, then move it into `.product-skills/`.
- Do not recursively copy `.product-skills/`, `.git/`, ignored design docs, pycache, or generated eval results.
- Add `.product-skills/` to `.gitignore` unless the user passes `--track-package-store`.
- `.product-skills/` is the package installer store. It is unrelated to the existing `.product-os/` ignore entry used by product workflow state.

### Update

Examples:

```bash
product-skills update --scope user
product-skills update --scope repo --runtime all
```

Behavior:

1. Locate package store.
2. Detect installed version.
3. Check latest available version.
4. Show changelog when available.
5. Ask for confirmation unless `--force` is passed.
6. Update package store.
7. Run validation.
8. Regenerate adapters if template version changed.
9. Preserve local user edits through backup and marker-based replacement.

`--ref` semantics:

- On install, `--ref` selects the git branch, tag, or commit to install.
- On update, an existing pinned ref remains pinned unless the user passes a new `--ref`.
- Without `--ref`, update follows the latest release tag once releases exist; before releases, it follows the default branch.

### Validate

Examples:

```bash
product-skills validate --scope user
product-skills validate --scope repo
```

Behavior:

1. Locate package store.
2. Run:

```bash
python3 scripts/check_package.py <package-store>
python3 scripts/run_trigger_evals.py <package-store>
python3 scripts/check_tool_safety.py <package-store>
python3 scripts/check_forward_tests.py <package-store>
python3 -m py_compile scripts/check_package.py scripts/run_trigger_evals.py scripts/grade_artifact.py scripts/check_tool_safety.py scripts/check_forward_tests.py
```

3. Validate installed adapters exist for selected runtime.

### Status

Example:

```bash
product-skills status --scope user --runtime all
```

Output should include:

- package store path;
- installed version;
- git ref or release tag when available;
- runtime adapters installed;
- validation status;
- ignored or missing runtimes.

### Uninstall

Example:

```bash
product-skills uninstall --runtime codex --scope user
product-skills uninstall --scope repo --runtime all --remove-package-store
```

Behavior:

1. Remove selected runtime adapters.
2. Leave package store by default.
3. Remove package store only with `--remove-package-store`.
4. Preserve backups unless `--clean-backups` is passed.

## Package Store Source

Initial implementation can support GitHub clone or archive download.

Recommended first path:

```bash
git clone https://github.com/Michal-Pi/ProductSkills.git <package-store>
```

Canonical source:

```text
https://github.com/Michal-Pi/ProductSkills.git
```

Later npm path:

```bash
npx product-skills install --runtime all --scope user
```

For npm distribution, add:

```text
package.json
bin/product-skills.mjs
install.sh
adapters/
  claude/SKILL.md
  codex/SKILL.md
  cursor/product-operating-system.mdc
  gemini/GEMINI.md
```

## Versioning

Add a root `VERSION` file.

Use semantic versioning:

```text
0.1.0
```

Version sources in priority order:

1. `VERSION`
2. `package.yaml` `version`
3. git tag

The update command should treat mismatches as warnings and prefer `VERSION`.

`VERSION` should be added before implementing the installer. `package.yaml` should stay aligned with it.

## Adapter Template Variables

Adapter templates should support:

```text
{{PACKAGE_STORE}}
{{INSTALL_SCOPE}}
{{RUNTIME}}
{{VERSION}}
```

Repo-scope adapters should prefer relative paths where the runtime can resolve them reliably.

User-scope adapters should use absolute paths with `~` expanded only when the runtime supports it. Otherwise write full absolute paths.

Avoid timestamps in generated adapters. Re-running install should be idempotent when inputs have not changed.

## File Preservation

There are two adapter ownership models.

Dedicated adapter files are fully managed:

- `.claude/skills/product-operating-system/SKILL.md`
- `.codex/skills/product-operating-system/SKILL.md`
- `.cursor/rules/product-operating-system.mdc`

Shared instruction files are marker-managed:

- `AGENTS.md`
- `GEMINI.md`

Before overwriting any fully managed adapter:

1. Detect whether it exists.
2. If the file was generated by ProductSkills, replace the full file.
3. If the file exists but is not recognized as ProductSkills-generated, create a backup:

```text
<adapter>.bak.<timestamp>
```

4. Refuse overwrite unless `--force` is passed.

Dedicated adapter recognition:

- Claude and Codex `SKILL.md`: frontmatter `name: product-operating-system`.
- Cursor `.mdc`: frontmatter `description` contains `Product Operating System workflow`.
- Future templates should include a stable `Generated by ProductSkills` comment when the runtime format allows comments.

Before editing a shared instruction file:

1. If ProductSkills markers exist, replace only the content between markers.
2. If no markers exist, append a new marker-delimited block.
3. If markers are malformed, create a backup and fail with repair instructions.

For `GEMINI.md` and `AGENTS.md`, never replace the whole file unless `--force --replace` is passed.

Backup retention:

- Keep the latest five backups per adapter by default.
- `--clean-backups` may remove older backups during uninstall.

## Security

Installer safety rules:

- Do not execute package scripts during install except validation scripts explicitly documented here.
- Treat remote package validation scripts as trusted only when installed from the canonical repository and selected ref.
- For published releases, prefer signed or checksum-verified archives before running validation scripts.
- Do not read or write `.env` files.
- Do not install npm or Python dependencies without explicit user approval.
- Do not make external Notion or Linear calls.
- Do not modify auth, RLS, deployment, or infrastructure files.
- Do not delete user files without explicit `uninstall` flags.
- Print all write paths in `--dry-run`.

Installer dependencies:

- Node.js is required for the CLI. The implementation must declare a minimum supported Node version in `package.json`.
- Python 3 is required for package validation scripts.
- Git is required for clone, fetch, and update unless archive download mode is used.

Runtime safety rules:

- Notion and Linear outputs remain dry-run previews.
- Confirmed writes require exact target, payload, idempotency keys, and payload hash.
- Installer smoke tests must not trigger live external writes.

## Error Handling

Installer should fail with actionable messages for:

- missing git;
- missing Python 3;
- unsupported Node.js version;
- invalid runtime;
- unsupported runtime and scope pair;
- not inside a git repo for repo scope;
- package validation failure;
- adapter path exists and cannot be safely merged;
- malformed generated markers;
- update source unavailable;
- git clone or fetch failure.

Each error should include:

- what failed;
- path involved;
- next action.

## Test Plan

### Unit Tests

Test:

- runtime detection;
- scope detection;
- path resolution;
- adapter rendering;
- marker-based replacement;
- malformed marker detection;
- backup creation;
- version comparison;
- dry-run output.

### Integration Tests

Use temporary directories.

Cases:

- install Codex user scope;
- install Codex repo scope using default visible skills;
- install Codex repo scope using explicit `AGENTS.md` fallback;
- install Claude repo scope;
- install Cursor repo scope;
- fail gracefully for unsupported Cursor user scope;
- install Gemini repo scope with existing `GEMINI.md`;
- install Gemini user scope using default extension adapter;
- install Gemini user scope into existing `~/.gemini/GEMINI.md` with explicit `--adapter context`;
- install repo scope from inside the ProductSkills repo itself;
- update existing package store;
- validate package store;
- report status for installed package and adapters;
- uninstall adapter only;
- uninstall adapter plus package store.

Self-install assertions:

- package store excludes `.git/`;
- package store excludes `.product-skills/`;
- package store excludes ignored design docs;
- package store excludes `__pycache__/` and generated eval results;
- `.gitignore` contains `.product-skills/` unless `--track-package-store` was passed.

Error-path tests:

- unsupported runtime and scope pair returns actionable error;
- package validation failure aborts install;
- clone or archive download failure leaves no partial adapter;
- `--dry-run` performs zero filesystem mutations;
- repeated install does not duplicate `AGENTS.md` or `GEMINI.md` blocks.

### Regression Tests

The installer must run existing package validation:

```bash
python3 scripts/check_package.py .
python3 scripts/run_trigger_evals.py .
python3 scripts/check_tool_safety.py .
python3 scripts/check_forward_tests.py .
```

### Manual Smoke Tests

After install, ask the runtime:

```text
Use the Product Operating System workflow on this rough PRD. Continue from the correct lifecycle stage and do not replay validation unless the readiness check fails.
```

Expected:

- ProductSkills activates or is followed through context.
- The workflow selects a re-entry status.
- Validation is treated as routing.
- Missing evidence is not fabricated.
- Tool writes remain dry-run.

## Implementation Phases

### Phase 1: Local Installer CLI

Add:

```text
VERSION
package.json
bin/product-skills.mjs
adapters/
```

Support:

- `install`;
- `validate`;
- `status`;
- `--runtime`;
- `--scope`;
- `--dry-run`;
- self-install from the current checkout;
- Claude skills, Codex Agent Skills, explicit Codex `AGENTS.md` fallback, Cursor repo rules, Gemini repo context, and Gemini user extension adapters.

### Phase 2: Update And Uninstall

Support:

- `update`;
- `uninstall`;
- version detection;
- backup and marker replacement;
- git ref or tag update.

### Phase 3: Distribution

Support:

- npm package distribution;
- `install.sh`;
- release tags;
- changelog;
- checksums where practical.

### Phase 4: Runtime Hardening

Support:

- Cursor user-scope capability detection;
- Gemini extension compatibility hardening;
- Codex plugin packaging if the plugin surface becomes stable enough;
- Codex `AGENTS.md` fallback hardening if Agent Skills support is unavailable;
- adapter compatibility tests.

## Open Questions

- Should npm be the primary distribution channel, or should GitHub install remain primary until usage stabilizes?
- Should adapter templates be generated from a single shared template plus runtime deltas?
- How much user customization should survive adapter regeneration?
- Can the current target Codex runtime reliably load `~/.codex/skills/*/SKILL.md`, or should `AGENTS.md` fallback be the default outside this environment?
- Does the target Cursor version expose a stable user-level rule file, or is Cursor user scope unsupported?

## Recommended Defaults

- Default scope: repo inside git repo, user outside git repo.
- Default runtime: detect current runtime when possible; otherwise require `--runtime`.
- Default package store: `.product-skills` for repo, `~/.product-skills` for user.
- Default repo package-store tracking: ignored, with adapters committed if desired.
- Default update source: current git remote for development, release tag for published versions.
- Default overwrite behavior: preserve and back up, never silent overwrite.
- Default validation: run `check_package.py` after install and update.

## Definition Of Done

The installer design is ready for implementation when:

- user and repo scope behavior is explicit;
- runtime adapter paths are explicit;
- install, update, validate, status, and uninstall behavior is specified;
- file preservation rules are clear;
- security constraints are clear;
- test plan covers all supported runtimes and scopes;
- Claude review has no blocking findings or all accepted findings are patched.
