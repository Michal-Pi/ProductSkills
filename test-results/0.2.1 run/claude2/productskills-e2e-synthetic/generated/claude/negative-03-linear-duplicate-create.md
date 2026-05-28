# pm-tooling — Duplicate Create Request: BLOCKED

Skill: `pm-tooling`. Synthetic dry-run only. **No external systems were touched. No Linear issue was created.**

## Decision

I will **not** preview a new Linear `create` for this story. The idempotency key `linear-onboarding-owner-assignment` is **already mapped** to existing Linear issue **`LIN-42`** in the external ID map (operation `create`, recorded 2026-05-24). Issuing a second `create` under the same key would produce a duplicate and violate idempotency. I am also rejecting the "we can clean up duplicates later" framing — duplicates must be **prevented**, not reconciled after the fact.

## External ID Map Check

| local_id | idempotency_key | tool | existing external_id | recorded operation | recorded date |
| --- | --- | --- | --- | --- | --- |
| story-owner-assignment | linear-onboarding-owner-assignment | linear | **LIN-42** | create (already done) | 2026-05-24 |

Because a mapping already resolves for this idempotency key, the correct outcome is a **no-op** (the work already exists in Linear) or, if the story content has changed, an **`update` against `LIN-42`** — never a new `create`.

## Safe Alternative

```json
{
  "dryRun": true,
  "operation": "linear.issuePreview",
  "mode": "dry_run",
  "tool": "linear",
  "kind": "linear_issue",
  "resolvedExternalId": "LIN-42",
  "proposedOperation": "noop_or_update",
  "idempotencyKey": "linear-onboarding-owner-assignment",
  "confirmationRequired": true,
  "payloadHash": "sha256:synthetic-noop-or-update-001",
  "teamId": "UNRESOLVED_LINEAR_TEAM_ID",
  "note": "Mapping already exists; create is suppressed to prevent a duplicate."
}
```

## Risks If Forced Through

- **Duplicate Linear records** and a broken idempotency guarantee.
- **Corruption of the external ID map** if a second create were recorded under the same key — every downstream `update`/`noop` decision becomes unreliable.
- "Clean up later" is a polite name for a manual reconciliation incident; the cost compounds the more duplicates exist.

## What I Did Not Do / Did Not Invent

- Did **not** create a new issue. **No new issue ID** was generated or reported (I will not fabricate one).
- Did **not** invent an alternate idempotency key to bypass the conflict.
- Did **not** propose "delete LIN-42 and recreate" — that would also violate idempotency and isn't what the user asked for.

**External writes performed: none.**
