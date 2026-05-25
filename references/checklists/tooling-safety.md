# Tooling Safety Checklist

Use this checklist before preparing or executing external tool payloads.

- Payload starts as `mode: dry_run`.
- Target workspace, team, database, or page is explicit.
- Payload validates against the relevant schema.
- Idempotency key or local artifact ID is included.
- Existing external ID map is checked before create operations.
- User confirmation is tied to the exact target and idempotency key.
- No API tokens, secrets, or credentials are written to `.product-os/` files.
- Batch writes update the external ID map after each confirmed write.
