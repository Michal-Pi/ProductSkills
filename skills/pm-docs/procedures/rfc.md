# RFC

## Goal

Author a Request for Comments — a structured async-review artifact that proposes a product or process change, separates problem from proposal, documents alternatives (including do-nothing), and names approvers + a decision deadline. The RFC is the shape of a *proposal under review*, not a committed PRD; if approved, it may convert into a PRD.

## Input expected

- The change proposed in one sentence
- The problem it solves (with cited evidence where possible)
- Alternatives considered — at minimum two, including "do nothing"
- Tradeoffs per alternative (costs, risks, reversibility)
- Who needs to weigh in (named approvers and reviewers, distinguished)
- Review window (start / end dates) and decision-needed-by date
- Optional: convert-to-PRD path if approval is expected

## Output produced

A filled `../../../templates/rfc.md` with: title, status (draft / under review / decided), problem section, proposal section, ≥2 alternatives (one of which is "do nothing"), tradeoff matrix, decision-needed-by date, named approvers and reviewers, and a convert-to-PRD note when applicable.

## Steps

1. Set status to `draft` while authoring; the author flips to `under review` when posting. `decided` is set only when the named approver records a decision.
2. Write the problem section first. Cite evidence (interview IDs, support tickets, analytics, market signals). If the problem is conjecture, mark it explicitly and route to `pm-discovery` before posting — RFCs without grounded problems generate unproductive comment threads.
3. Write the proposal section *separately* from the problem. Problem and proposal must not collapse into one paragraph; reviewers must be able to disagree with the proposal while agreeing on the problem.
4. List alternatives — at minimum two, including "do nothing." For each alternative: a 2-3 sentence summary, expected impact, cost, key risk, and reason it was not chosen. Strawmanned alternatives are a quality-fail.
5. Build the tradeoff matrix. Rows = alternatives; columns = the dimensions that matter for this decision (user impact, engineering cost, time to ship, reversibility, dependency surface). Cite each cell's source where possible; gut-feel cells are flagged.
6. Name approvers explicitly (people whose sign-off is required) and reviewers explicitly (people whose input is wanted but not gating). Mixing the two stalls the decision.
7. Set the decision-needed-by date. RFCs without a deadline drift; if the change does not actually need a decision by a date, the artifact is closer to a one-pager — route accordingly.
8. If approval is expected to lead to scoped work, write a convert-to-PRD note: which PRD inherits this proposal, what scope it commits, and which open questions still need answering before PRD authoring begins.
9. Run the spec-review pass before posting — at minimum check evidence grading and that each alternative is steelmanned.

## Links

- Template: `../../../templates/rfc.md`
- Reference: `../../../references/checklists/docs-quality.md`
- Reference: `../../../references/methods/evidence-grading.md`
- Adjacent: the spec-review procedure in this skill (run before posting); the prd procedure (post-approval conversion target)

## Done when

- Problem and proposal are separate, non-collapsing sections.
- ≥2 alternatives are documented, including an explicit "do nothing" with stated cost.
- The tradeoff matrix has named dimensions and each cell is either cited or explicitly marked "gut-feel — to validate."
- Review window and decision-needed-by date are present and concrete (calendar dates, not "soon").
- Approvers and reviewers are listed as distinct sets; every approver has decision authority noted.
- A convert-to-PRD path is noted if approval is expected to commit scope; otherwise the RFC explicitly states "no PRD conversion expected."
- The artifact carries a status field (`draft` / `under review` / `decided`) and a single owner.
