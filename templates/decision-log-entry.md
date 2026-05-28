# Decision Log Entry

> Output template for `pm-docs/decision-memo` (bullet-log form). A single 3-5 line entry designed to be appended to a running decision-log file. The narrative form is `templates/decision-memo.md`; use that when the decision warrants a full memo. Replace placeholder text in italics.

## Entry shape

Each decision-log entry is 3-5 lines with the load-bearing fields compressed into a stable row. Append entries chronologically to a single running log; do not interleave with narrative memos.

### Append-to-log format

```
- [YYYY-MM-DD] DECISION-<id>: <one-sentence decision>.
  Owner: <name + role>. Options considered: <opt A>, <opt B> (selected: <opt>).
  Rationale: <≤1 sentence>. Evidence: <EVID-ids, grades>. Expected outcome: <metric/baseline → target / by date>.
  Revisit: <date | metric threshold | event>. Upstream: <link to prioritization / RFC if any>.
```

Five lines maximum. Every load-bearing field appears even compressed. If a field requires more than the line allows, the decision warrants the narrative form instead — route to `templates/decision-memo.md`.

## Example entries (illustrative — replace with real decisions)

```
- [2026-05-14] DECISION-014: Defer SSO claims-mapping editor to Q4.
  Owner: Maya Chen (PM, Identity). Options considered: build now, defer to Q4, vendor (selected: defer).
  Rationale: Enterprise demand confirmed but Q3 capacity committed to billing migration.
  Evidence: SAL-014, SAL-022, INT-031 (grade A); capacity model 2026-05 (grade A).
  Expected outcome: enterprise activation +8% in Q4 (baseline 22%, target 30%, by 2026-12-31).
  Revisit: 2026-10-01 capacity review, or if ≥3 enterprise deals slip on SSO gap before then.
  Upstream: pm-strategy/prioritization-2026-Q3-run.

- [2026-05-21] DECISION-015: Adopt event-sourced billing schema for enterprise tier.
  Owner: Maya Chen (PM, Billing). Options considered: event-sourced, current schema + migrations, vendor (selected: event-sourced).
  Rationale: Audit / restate-history requirement from contracted enterprise customers; vendor cost projection too high at our scale.
  Evidence: SAL-019 (grade A), finance projection 2026-05 (grade A), spike report SPK-008 (grade B).
  Expected outcome: zero-billing-restatement incidents in 12 months (baseline 4/year, target 0, by 2027-06-30).
  Revisit: 2027-Q2 review, or earlier if migration ships >6 weeks late.
  Upstream: RFC-2026-014.
```

## Header (when starting a new log file)

- **Log name:** _e.g., Atlas product decision log 2026_
- **Owner:** _PM or PM lead maintaining the log_
- **Append rule:** _new entries at the bottom; never edit prior entries — supersede them with a new entry that links back_
- **Narrative-form pointer:** _decisions warranting more than 5 lines route to `templates/decision-memo.md`_

## Supersedure rule

If an entry needs to change after being appended, do not edit it. Append a new entry with `Supersedes: DECISION-<id>` and update the prior entry's status to `superseded by DECISION-<new-id>` in a one-line comment beneath the original entry. This preserves the audit trail.
