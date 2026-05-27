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

### Candidate Plan

1. Re-test current Codex adapter behavior on a clean machine:
   - user scope with `--adapter skills`;
   - repo scope with `--adapter skills`;
   - repo scope with `--adapter agents`;
   - `--adapter auto` for both scopes.
2. Verify which install locations Codex surfaces in the skills UI.
3. Decide the new default:
   - likely prefer visible skills as the default Codex adapter;
   - keep AGENTS.md as an explicit `--adapter agents` mode.
4. Update CLI help and install output to explain the difference.
5. Add tests that assert Codex defaults and output copy match the intended UX.
6. Update `docs/LOCAL_INSTALLATION.md` with platform-specific Codex guidance.

