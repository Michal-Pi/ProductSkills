# Acceptance Criteria

Use when writing or reviewing acceptance criteria.

## Steps

1. Define the user-visible behavior.
2. Include primary success path.
3. Include edge cases, permissions, empty states, errors, and failure states where relevant.
4. Identify instrumentation or audit requirements.
5. Make each criterion observable and testable.
6. Avoid implementation-only criteria unless the product behavior requires them.

## Output

Return acceptance criteria grouped by story or scenario.

## Done when

- Each story has at least three distinct acceptance-criterion bullets covering the primary success path; every epic carries at least one edge-case bullet (permission, empty state, error, or failure).
- Each criterion is observable and testable from the user's perspective; implementation-only criteria are removed or flagged with the product behavior that requires them.
- Instrumentation, audit, or analytics requirements named in the steps are either listed as their own criterion or explicitly marked "not required."
- When inputs are missing user-visible behavior or scenario context, the procedure stops and returns the missing context as open questions rather than inventing criteria.
