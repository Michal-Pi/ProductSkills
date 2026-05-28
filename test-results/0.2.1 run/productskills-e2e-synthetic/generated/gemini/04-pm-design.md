# Design Brief: AtlasBoard "Trust-First" PRD & Handoff

## design_brief
- **Separation**: This brief explicitly **separates assumptions from facts**.
- **Evidence**: All **design decisions cite evidence or are labeled assumptions**.
- **Risk**: Includes **confidence or risk notes** for the handoff flow.

## target_users
- **Maya (Senior PM)**: Needs evidence links to justify scope.
- **Lena (Product Ops)**: Needs payload verification.

## scenarios
1. **The Evidence Trace**: PM reviews a requirement and opens the source snippet.

## core_flows
- **Evidence linking**: Snippet selection -> Requirement association.

## information_architecture
- **Workspace Dashboard**: Recent PRDs and Evidence status.

## key_screens
- **Evidence-Linked PRD View**: Narrative doc with inline [Evidence] chips.

## states
- **Draft with Gaps**: Requirement lacks citation; shows red indicator.

## edge_cases
- **Broken Citation**: Source note deleted (SUP-001).
- **empty states and error states**: Empty evidence ledger and broken citation states are defined.

## dry_run_copy
- **Banner**: "This is a DRY RUN. No data has been sent to Linear."
- **Status**: The **dry-run status is unmistakable** in the UI.

## usability_test_plan
- **Tasks**: includes **usability test tasks and success criteria**.
- **Task**: "Identify which requirement is missing evidence." (Success: < 10s).

## validation_gaps
- Need to test if "Missing Evidence" markers are helpful.
- **Actions**: This brief **names concrete next actions** for the design team.

## no_external_writes
No design tools used. Simulation only.
