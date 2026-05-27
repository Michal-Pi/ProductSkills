# Post-Release Feedback

Capture field feedback here for later triage. Do not treat these notes as
committed decisions until they are promoted into a scoped plan.

## Feedback 1: Codex Skills Visibility

Date captured: 2026-05-27

### Feedback

ProductSkills are not visible as Codex skills after repo-scope installation
because the current Codex repo adapter writes project instructions into
`AGENTS.md`. The expected behavior is likely that ProductSkills should be
installed as visible Codex skills instead, or at least make the distinction
clear during install.

### Current Behavior

- `--runtime codex --scope user` installs the Codex skills adapter under the
  user Codex skills directory.
- `--runtime codex --scope repo` defaults to the Codex agents adapter and writes
  ProductSkills instructions into the repo `AGENTS.md`.
- `--runtime all --scope repo` therefore also writes Codex instructions into
  `AGENTS.md` by default.

### Cross-Platform Adapter Matrix

Current defaults are not conceptually consistent across runtimes. They are
runtime-native, but they mix "visible skill/rule packages" with
"shared instruction files".

| Runtime | User-Scope Default | Repo-Scope Default | Visible In Runtime UI? | Notes |
| --- | --- | --- | --- | --- |
| Claude | `~/.claude/skills/product-operating-system/SKILL.md` | `<repo>/.claude/skills/product-operating-system/SKILL.md` | Expected yes for skills-aware Claude surfaces | Consistent dedicated skills adapter in both scopes. |
| Codex | `~/.codex/skills/product-operating-system/SKILL.md` | `<repo>/AGENTS.md` | User scope yes; repo scope no | Inconsistent: repo scope defaults to shared instructions instead of visible skills. Explicit `--adapter skills` writes `<repo>/.codex/skills/...`. |
| Cursor | Supported detected global rules dir, usually `~/.cursor/rules/product-operating-system.mdc` | `<repo>/.cursor/rules/product-operating-system.mdc` | Expected yes as Cursor rules | User scope is conditional; repo scope is dedicated rules. |
| Gemini | `~/.gemini/GEMINI.md` | `<repo>/GEMINI.md` | No | Default is shared context block. Explicit `--adapter extension` writes `~/.gemini/extensions/product-skills/` and is user-scope only. |

### Consistency Assessment

- Dedicated/visible install defaults are consistent for Claude and Cursor.
- Codex is inconsistent with the user's mental model because repo scope defaults
  to `AGENTS.md`, while user scope defaults to visible skills.
- Gemini is different by platform design: the default adapter is a context file,
  not a visible skill. The visible/package-like Gemini option is the extension
  adapter, but the installer currently requires explicit `--adapter extension`
  and only supports it for user scope.
- `--runtime all --scope repo` mixes adapter concepts in one command:
  Claude skill, Codex shared `AGENTS.md`, Cursor rule, Gemini shared `GEMINI.md`.
- `--runtime all --scope user` also mixes concepts:
  Claude skill, Codex skill, Cursor conditional rule, Gemini shared `GEMINI.md`.

### Why It Matters

- `AGENTS.md` modifies project-level instructions but does not make
  ProductSkills visible in Codex's skills list.
- Users testing "skills installed successfully" expect visible skills in Codex.
- The current default can look like a failed install even when the repo adapter
  worked as designed.

### Questions To Resolve

- Should Codex repo-scope default to `--adapter skills` instead of
  `--adapter agents`?
- Should `--adapter auto` choose visible skills for Codex on both user and repo
  scope?
- Should AGENTS.md modification become an explicit opt-in adapter for users who
  want repo-local project instructions?
- Should install output warn that the agents adapter will not appear in the
  Codex skills UI?
- Are visible-skill install paths and behavior different between Codex desktop,
  Codex CLI, and repo-local Codex usage?
- Should Gemini user scope default to the extension adapter once package-style
  visibility is the release goal?
- Should `--runtime all` prefer each platform's most visible/package-like
  adapter instead of shared instruction files?

### Candidate Plan

1. Re-test current Codex adapter behavior on a clean machine:
   - user scope with `--adapter skills`;
   - repo scope with `--adapter skills`;
   - repo scope with `--adapter agents`;
   - `--adapter auto` for both scopes.
2. Re-test Gemini behavior:
   - user scope with default context file;
   - user scope with `--adapter extension`;
   - repo scope with default context file.
3. Verify which install locations each runtime surfaces in its UI:
   - Claude skills;
   - Codex skills;
   - Cursor rules;
   - Gemini extensions and context files.
4. Decide the new defaults:
   - likely prefer visible skills as the default Codex adapter;
   - keep AGENTS.md as an explicit `--adapter agents` mode.
   - decide whether Gemini should default to `--adapter extension` for user
     scope, while keeping `GEMINI.md` as an explicit context adapter.
5. Update CLI help and install output to explain the difference between visible
   runtime packages and shared instruction/context files.
6. Add tests that assert runtime defaults and output copy match the intended UX.
7. Update `docs/LOCAL_INSTALLATION.md` with platform-specific guidance.
