# Release Notes

Use when writing customer-facing or internal release notes.

## Steps

1. Identify audience and release type.
2. Summarize what changed and why it matters.
3. State availability, limitations, migration steps, and support path.
4. Avoid unsupported claims or roadmap promises.
5. Include customer impact and success metric when relevant.

## Output

Return release note draft plus internal reviewer checklist.

## Done when

- The draft is audience-segmented: at least one customer-facing and one internal variant exist, or the single audience is stated explicitly with a reason the other is not produced.
- Availability, limitations, migration steps, and support path are populated; "no change" or "not applicable" is used in place of an empty field so reviewers see the omission was deliberate.
- Claims are tied to shipped behavior; benefits not backed by data are softened or removed, and no roadmap promises appear in the customer-facing variant.
- The internal reviewer checklist lists at least three named reviewers or review gates (product, support, legal/comms as appropriate); when the change set is unclear, the draft refuses to publish and returns a content-gap list instead.
