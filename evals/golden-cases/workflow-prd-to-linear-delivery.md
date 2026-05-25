# Golden Case: Workflow PRD to Linear Delivery

## Prompt

Convert a PRD for team invite activation into delivery-ready epics, user stories, acceptance criteria, dependencies, and Linear dry-run issue payloads.

Inputs include:

- Scope: invite status visibility, resend invite, expired invite handling, and admin notification.
- Non-goals: bulk CSV import, custom invite branding, and billing-seat automation.
- Risks: email deliverability, permission boundaries, and stale invite state.
- Existing external ID map contains one prior epic for invite management.
- Linear target team is Growth.

## Expected Qualities

- Reviews PRD readiness before creating stories.
- Preserves scope, non-goals, assumptions, dependencies, and risks.
- Splits work into valuable, testable stories with edge cases and failure states.
- Previews updates for existing mapped issues instead of duplicate creates.
- Produces Linear `mode: dry_run` payloads and asks for exact confirmation before any write.
