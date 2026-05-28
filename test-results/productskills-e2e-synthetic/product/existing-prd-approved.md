# Approved PRD: Linear/Notion Dry-Run Delivery Preview

## Objective

Enable Product Ops and PM teams to generate safe, reviewable Linear and Notion dry-run previews from an approved PRD before any external write is considered.

## Customer

Primary: Product Ops leads and PMs at mid-market B2B SaaS companies using Notion for PRDs and Linear for delivery.

Secondary: product leaders who need evidence that delivery plans preserve PRD intent.

## Evidence

- INT-003: BuildLoop needs preview-only sync, external ID mapping, and idempotent updates.
- SALES-002: buyer requested Linear and Notion previews and explicitly rejected blind writes.
- SUP-002: Linear preview currently groups stories under one epic, losing PRD section structure.
- SUP-005: enterprise admin needs workspace-level control over external sync actions.
- Usage analytics: Product Ops has 78 percent activation, 72 percent week 4 retention, and highest preview usage.

## Problem

Teams want AtlasBoard to help translate approved PRDs into delivery and documentation artifacts, but they will not trust the product if external tool payloads are opaque or unsafe. Existing beta previews do not preserve structure reliably and do not show enough idempotency detail.

## Assumptions

- Product Ops teams will evaluate AtlasBoard if previews are structured, inspectable, and clearly dry-run.
- Linear and Notion payload previews can create value before live writes exist.
- External ID mapping will reduce fear of duplicate issues/pages.

## Scope

- Generate a Linear dry-run preview with epics, stories, acceptance criteria, labels, owners, dependencies, and external IDs.
- Generate a Notion dry-run preview with page hierarchy, PRD summary, decision log, launch checklist, and source evidence links.
- Show payload hash, idempotency keys, unresolved target IDs, and confirmation requirements.
- Preserve PRD sections when grouping delivery work.
- Include admin-disabled state behavior that blocks write requests and still allows preview generation.

## Non-Goals

- No live writes to Linear or Notion.
- No GitHub Issues support in this release.
- No automatic workspace discovery against real external systems.
- No security certification claims.

## User Experience

1. User opens an approved PRD.
2. User selects "Preview delivery sync."
3. AtlasBoard generates Linear and Notion dry-run previews.
4. User sees unresolved workspace/team/database IDs as blockers for future writes.
5. User can export markdown or JSON preview artifacts.
6. Any write action remains disabled unless a future explicit confirmation flow is implemented.

## Success Metrics

- 80 percent of Product Ops beta users can generate a complete preview from an approved PRD without manual editing.
- Linear preview structure defects drop from current SUP-002 baseline to fewer than 5 percent of previews.
- At least 60 percent of previews include stable external IDs for every epic, story, and Notion page.
- Zero unintended external writes.

## Risks

- Users may confuse dry-run previews with completed syncs.
- Missing workspace IDs may frustrate teams expecting one-click automation.
- Preview payloads may expose sensitive text if users paste real customer data; this test pack uses synthetic data only.

## Open Questions

- Which payload fields should be mandatory for a future confirmed write?
- Should admin-disabled state hide write buttons or show disabled buttons with rationale?
- What payload hash format should be considered stable across minor text edits?

## Approval

- Product: approved for delivery planning.
- Engineering: approved for breakdown, pending technical discovery.
- GTM: release messaging should say "dry-run preview" and avoid claiming live sync.
