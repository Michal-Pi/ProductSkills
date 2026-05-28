# Internal Review FAQ

## Goal

Produce an internal-facing Q/A document that hardens a PRD, launch plan, RFC, or one-pager by surfacing and answering the questions reviewers and stakeholders are most likely to raise — the Working-Backwards "FAQ" pattern, used pre-review to preempt objections. This is the *internal* objection-handling artifact; it is NOT a customer-facing FAQ (out of scope) and it is NOT a launch FAQ (route to `pm-gtm`).

## Input expected

- The artifact being defended (PRD / RFC / launch plan / one-pager / decision memo)
- Known objection sources: sales, customer success, engineering, leadership, finance, legal — whichever apply
- Prior questions from earlier reviews, retros, or hallway conversations
- Evidence pool used by the underlying artifact (so answers can cite, not invent)
- Optional: VoC themes from `pm-discovery/voc-synthesis` if customer-side objections are needed (but the FAQ remains internal-facing)

## Output produced

A filled `../../../templates/internal-review-faq.md` with: artifact-being-defended pointer, ≥5 Q/A pairs covering at minimum scope, evidence strength, risk, alternatives considered, and success criteria; each answer cites evidence or names the assumption; anticipated follow-ups; an explicit escalation path if a question is unresolved at review time.

## Steps

1. State the artifact being defended at the top — title, version, owner, date — so the FAQ does not drift independently of the source artifact.
2. Generate at least five Q/A pairs covering, at minimum, these dimensions: (a) scope ("why isn't X in scope?"), (b) evidence strength ("how do we know this is the right problem?"), (c) risk ("what's the biggest thing that could go wrong?"), (d) alternatives considered ("why not the obvious other approach?"), (e) success criteria ("how will we know it worked?").
3. Source questions from real reviewers. Generic "anticipated questions" lifted from a rubric are a tell of low quality — ground each question in a named reviewer's known concerns, a prior debate, or a documented stakeholder priority.
4. Steelman every objection. The strongest version of the objection must appear, not a strawman the author can easily knock down. A FAQ that exists only to defend the proposal is performative and reduces, not increases, review quality.
5. Each answer either cites evidence (graded H / M / L per `../../../references/methods/evidence-grading.md`) or explicitly names the underlying assumption — never both implicit. "We think users want this" is not an answer; "Interview corpus INT-014..018 surfaced this theme in 4 of 5 sessions (evidence: M, ungeneralized)" is.
6. Where an answer reveals a real weakness — missing evidence, unresolved tradeoff, scope ambiguity — add it to the artifact's open-questions list. The FAQ may surface fixes back into the source document.
7. Add anticipated follow-ups: which questions the author expects to deepen during review (i.e., the second-round questions reviewers will ask after the first answer).
8. Name an escalation path: if a question is unresolved at review time, who decides, by when. Unresolved questions without an escalation owner cause review drift.

## Steps for routing decisions

- Customer-facing FAQ (help docs, product education) — out of scope; this skill does not produce customer-facing FAQs.
- Launch FAQ (press, sales enablement, external messaging) — route to `../../pm-gtm/SKILL.md`.
- VoC-driven objection map (synthesizing what customers themselves have asked) — route to `../../pm-discovery/SKILL.md` and bring the synthesized themes back as evidence for this FAQ.

## Links

- Template: `../../../templates/internal-review-faq.md`
- Reference: `../../../references/methods/evidence-grading.md`
- Reference: `../../../references/checklists/docs-quality.md`
- Optional upstream: pm-discovery voc-synthesis when customer-side objections drive the FAQ — see `../../pm-discovery/SKILL.md`
- Adjacent: the spec-review procedure in this skill (run on the source artifact, not the FAQ, after FAQ surfaces weaknesses)

## Done when

- ≥5 Q/A pairs are present and cover scope, evidence strength, risk, alternatives considered, and success criteria at minimum.
- Each question is grounded in a real reviewer concern, prior debate, or documented stakeholder priority — not lifted generically from a rubric.
- Every objection is steelmanned; no strawmen.
- Each answer either cites graded evidence OR explicitly names the assumption — never implicit.
- Weaknesses surfaced by the FAQ are reflected back into the source artifact's open-questions list.
- An escalation path is named: which question is unresolved, who decides, by when.
- The artifact-being-defended is explicitly named and versioned at the top of the FAQ.
