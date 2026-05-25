# Tool ID Resolution

Use before any confirmed Notion or Linear write that depends on tool-specific IDs.

## Steps

1. List human-readable names in the preview, such as workspace, database, page, team, project, label, state, or owner.
2. Identify which values are already resolved IDs and which are display names only.
3. If an ID is missing or ambiguous, stop and ask for the exact target or provide setup instructions.
4. For Linear, resolve team keys to team IDs, label names to label IDs, and workflow state names to state IDs before confirmed writes.
5. For Notion, resolve workspace, database, parent page, and target page IDs before confirmed writes.
6. Include both display name and resolved ID in the dry-run preview when available.
7. Never treat a display name as a write-ready ID.

## Output

Return resolved IDs, unresolved names, ambiguity notes, and the next action needed before a confirmed write.
