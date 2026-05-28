# Spec Review

## Goal

Review any product artifact — PRD, RFC, one-pager, decision memo, postmortem, internal-review FAQ, or an external/inherited spec — for quality. This procedure is the **universal quality gate** for the package; it MAY be cited by other skills before they finalize their artifacts. Reviewing your own draft before sharing it is also a valid invocation.

> **Note:** This procedure MAY be cited by other skills as the universal quality gate before finalizing artifacts. It is not pm-docs-specific; the rubric and severity scale travel.

## Input expected

- The artifact to review (markdown, link, or inline text)
- Optional: the artifact's intended audience (engineering, leadership, GTM, customer-facing peer review)
- Optional: the decision stakes (low / medium / high) — calibrates which findings are blocking vs. improvements
- Optional: the artifact's template (pm-docs prd / rfc / one-pager / decision-memo / postmortem / internal-review-faq, or a stated external shape) — drives the per-section checklist

## Output produced

A review document containing:

- Findings by severity (blocking / improvement / nit), each with a concrete suggested fix
- Missing-sections list (template sections that are empty or absent)
- Risky-assumption list (claims asserted as fact without grounding)
- Sampled evidence claims (representative high-stakes claims checked against cited sources — not exhaustive)
- A single recommendation: **revise** (blocking issues remain), **validate** (gaps need evidence before ship), **align** (cross-functional disagreement to resolve), or **proceed** (ready to ship)

## Severity rubric

The review classifies every finding into exactly one of three severities:

- **blocking** — The artifact cannot ship as-is. Triggers: a required section is missing or empty, a load-bearing claim is fabricated or contradicted by cited evidence, scope and non-goals are mutually inconsistent, the success metric is unfalsifiable, the artifact misrepresents the source corpus or invents citations, or the artifact violates the underlying procedure's Done When conditions. Blocking findings must be resolved or explicitly documented as open questions before the artifact ships.
- **improvement** — The artifact can ship, but quality is materially weaker without the fix. Triggers: an answer is vague where specificity would help, evidence is ungraded, an alternative was acknowledged but not steelmanned, a risk is named without a mitigation, prose is unnecessarily long or jargon-heavy in a section where leaders will skim.
- **nit** — Style, polish, or formatting. Triggers: typo, inconsistent capitalization, ordering of sections that the template allows either way, single word choices. Nits are recorded but do not affect the recommendation.

## Steps

1. Confirm the artifact's template and intended audience. If unknown, infer from the artifact's shape; if it cannot be inferred, the first finding is "artifact lacks identifiable shape — name the template before reviewing further."
2. Walk every required section of the template's checklist. For each section: present? non-empty? answers the section's question? Missing or empty sections become blocking findings.
3. Check evidence: is every material claim either cited (with grade) or explicitly named as an assumption? Ungraded evidence claims become improvements; uncited assertions of fact become blocking.
4. Sample a representative subset of high-stakes claims (top 3-5) and check the cited sources actually support the claim. Full evidence verification is out of scope; sampling catches the worst cases.
5. Check scope-vs-non-goals coherence. A scope claim contradicted by a non-goal is a blocking finding; an ambiguous boundary is an improvement.
6. Check the success-metric / acceptance-criteria specificity. Metrics without baseline + target + window are blocking unless the artifact explicitly flags a metric gap.
7. Check for forbidden patterns: scapegoating (in postmortems), strawmanned alternatives (in RFCs), generic "anticipated questions" lifted from a rubric (in FAQs), unfalsifiable success criteria (in PRDs).
8. Classify every finding into blocking / improvement / nit per the rubric above.
9. Produce a single recommendation: revise / validate / align / proceed. If any blocking findings remain unresolved and undocumented as open questions, the recommendation must be revise or validate (not proceed).

## Calling-skill protocol

Other skills citing this procedure pass: the artifact, the template name, the stakes level. They receive: the findings, the recommendation, and (if any) the list of open questions to fold back into the source artifact. Skills MAY treat blocking findings as gating; the rubric does not force gating, it provides the classification.

## Links

- Reference: `../../../references/checklists/docs-quality.md`
- Reference: `../../../references/methods/evidence-grading.md`

## Done when

- Every required section of the artifact's template is checked, present-or-absent recorded.
- Each finding has a severity (blocking / improvement / nit) AND a concrete suggested fix — findings without a fix are notes, not findings.
- A single recommendation is given: revise / validate / align / proceed.
- A representative subset of high-stakes claims has been sampled against cited sources (not all claims — sampling is sufficient).
- Blocking findings either get resolved in the source artifact OR are explicitly documented as open questions with owner + target close date before the recommendation can be `proceed`.
