# Sample Launch Readiness Gate

## Release

AtlasBoard Linear/Notion Dry-Run Delivery Preview

## Status

Conditional. Launch only after blockers are resolved.

## Ready

- Approved PRD exists.
- Primary target segment is defined as mid-market Product Ops and PM teams using Notion plus Linear.
- Release messaging can be framed as dry-run preview, not live sync.
- Initial success metrics are defined.

## Blockers

- SUP-002 preview grouping defect must be fixed or explicitly scoped out.
- SUP-005 admin disable control must be available before enterprise-facing launch.
- Usability test has not verified that users understand dry-run vs live sync.
- Support needs enablement for "preview only" questions.

## Risks

- Users may think preview means records were synced.
- Enterprise prospects may infer security readiness that does not exist.
- Productboard/Jira/GitHub users may misunderstand target support.

## Required Launch Copy Guardrails

- Say "preview Linear and Notion payloads before sync."
- Do not say "sync automatically."
- Do not say "writes to Linear" or "publishes to Notion."
- Do not claim SOC 2, live rollback, or GitHub support.
