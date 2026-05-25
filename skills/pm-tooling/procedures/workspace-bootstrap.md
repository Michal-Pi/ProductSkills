# Workspace Bootstrap

Use before preparing Notion or Linear writes for a workspace.

## Steps

1. Ask for or discover workspace, database, team, and project identifiers.
2. Validate workspace shape against `../../../schemas/product-os-workspace.schema.json`.
3. If no workspace file exists, return a safe bootstrap preview for `.product-os/workspace.json` with `version: 1` and an empty or user-confirmed `workspaces` list.
4. Record conventions in `.product-os/workspace.json` only when the user confirms the exact content.
5. Do not store API tokens, secrets, or credentials in `.product-os/workspace.json`.
6. Do not guess IDs when multiple targets are plausible.
7. If tools are unavailable, produce setup instructions and dry-run payloads.

## Output

Return required identifiers, known identifiers, missing identifiers, proposed safe workspace file content, and setup next action.
