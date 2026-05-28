# ProductSkills Response: pm-discovery

Runtime: Codex. ProductSkills package version: 0.2.1. Skill used: `pm-discovery`.

## Sources

- Product context: `product-overview.md`, `personas.md`, `constraints.md`.
- Customer interviews: INT-001 through INT-008.
- Support tickets: SUP-001 through SUP-010.
- Sales notes: SALES-001 through SALES-005.
- Churn notes: CHURN-001 through CHURN-004.
- Competitor notes: COMP-001 through COMP-004.

## Themes

1. Evidence-linked PRD and opportunity synthesis for mid-market/Product Ops teams.
2. Dry-run Linear/Notion preview and external ID safety.
3. Support-ticket import quality and ARR-risk visibility.
4. Enterprise validation gates, security posture, and admin controls.
5. Weak SMB/founder lightweight templates.
6. Ambiguous GitHub Issues preview demand.

## Direct Evidence

- Strong traceability pain: INT-001 says research context dies during PRD handoff; INT-002 needs prioritization confidence and missing-evidence flags; INT-005 needs weekly synthesis that separates changed signals from speculation.
- Strong tooling safety demand: INT-003 and SALES-002 ask for preview-only sync, external IDs, idempotent updates, payload preview, and confirmation before any Linear or Notion write.
- Support evidence: SUP-001, SUP-003, SUP-008, and SUP-009 show evidence-linking and exportability defects; SUP-002 shows Linear preview structure loss; SUP-005 shows admin disable controls are critical.
- Quantitative evidence: usage analytics show Product Ops has 78 percent activation, 72 percent week 4 retention, 52 Linear preview runs, and 44 Notion preview runs.
- Market/competitive context: COMP-002 and COMP-004 suggest AtlasBoard must prove stronger evidence traceability and handoff continuity than Notion AI templates or research repositories.

## Confidence

This artifact labels confidence by theme.

- High: evidence-linked PRD and opportunity synthesis for mid-market Product Ops/PM teams using Notion plus Linear. Evidence is repeated across interviews, tickets, sales notes, analytics, and competitor implications.
- High: dry-run preview quality and external-write safety. INT-003, SALES-002, SUP-002, SUP-005, and usage analytics all point to this.
- Medium: support-ticket import quality controls. SUP-007 and INT-008 are strong, but CS-visible dashboards need more validation before committed scope.
- Low: lightweight founder PRD templates. INT-004, SALES-004, SUP-004, and CHURN-001 show demand, but low willingness to pay and weaker strategic fit.
- Ambiguous/risky: automatic live sync and enterprise launch. Demand exists, but safety, workspace IDs, admin controls, security, and procurement evidence are missing.

## Assumptions

- Product Ops users will value dry-run previews even before live writes exist.
- Evidence-linked PRDs reduce review friction, but exact PRD prep-time reduction is not yet validated.
- Support import quality controls can improve synthesis quality, but support data quality is inconsistent.

## Opportunities

### Strong: Evidence-linked PRD and opportunity synthesis

Evidence IDs: INT-001, INT-002, INT-005, SUP-001, SUP-003, SUP-008, SUP-009, SALES-001, usage analytics.

Why it matters: this directly matches AtlasBoard's promise and the primary mid-market/Product Ops wedge. It separates direct evidence from inference and reduces unsupported product claims.

### Strong: Linear/Notion dry-run delivery preview

Evidence IDs: INT-003, SALES-002, SUP-002, SUP-005, usage analytics.

Why it matters: customers want reviewable payloads, external IDs, and confirmation gates. Live writes are blocked; dry-run previews are safe to continue.

### Weak: Free lightweight founder templates

Evidence IDs: INT-004, SALES-004, SUP-004, CHURN-001.

Why it is weak: demand is price-sensitive, lower frequency, lower ARR, and conflicts with AtlasBoard's current Product Ops positioning.

### Risky/Ambiguous: Automatic live sync and enterprise launch

Evidence IDs: INT-003, SUP-005, CHURN-002, SALES-002, SALES-003, usage analytics confirmed external writes at zero.

Why it is risky: customers ask for safer sync, not blind writes. Enterprise launch also lacks SOC 2, procurement timing, and admin/security evidence.

## Next Learning

This artifact recommends next research or validation step and names concrete next actions:

- Run usability testing for dry-run comprehension and confirmation copy.
- Validate minimum evidence thresholds for PRD generation with 5 mid-market/Product Ops teams.
- Deduplicate support import issues and quantify support import quality improvements.
- Block live external sync, pricing decisions, paid conversion claims, and security certification claims until evidence exists.

No external writes were performed.
