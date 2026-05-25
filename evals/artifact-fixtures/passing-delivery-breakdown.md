# Source Outcome

Convert the approved onboarding PRD into delivery-ready work while preserving user value, non-goals, risks, and tool safety.

# Epics

Includes epics or stories:

- Epic 1: Owner assignment during workspace setup.
- Epic 2: Teammate invite status and first-action reminder.

# Stories

- As an admin, I can assign a setup owner so the team knows who completes onboarding.
- As an invited teammate, I can see the next required action so I can complete my first useful step.

# Acceptance Criteria

Includes acceptance criteria:

- Given an admin assigns an owner, when the workspace is saved, then the owner is visible in setup status.
- Given a teammate invite is pending, when the reminder window is reached, then one reminder is queued.
- Edge cases or failure states where relevant: expired invites, removed teammates, duplicate reminders, and missing owner permissions are handled.

# Dependencies

Identifies dependencies or open questions: event tracking for first teammate action, notification service capacity, and product analytics naming need confirmation.

# Dry Run Payloads

Dry-run Linear payload preview:

- mode: dry-run
- payload type: Linear issue preview
- idempotency key: onboarding-owner-assignment-v1
- action: update existing issue when an external ID mapping is present

The dry-run payload is shown before write. Live writes are disabled during evals.

# Confirmation Question

Explicit confirmation before write is required: confirm the target Linear workspace, issue payload, idempotency key, and dry-run payload hash before any write.

Rollback is not overstated; if a write is confirmed later, revert steps are manual issue edits or follow-up updates.
