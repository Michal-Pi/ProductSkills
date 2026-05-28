# Wireframe Brief

Use when turning product intent into a design exploration brief.

## Steps

1. State user, goal, scenario, and job.
2. Define scope and non-goals.
3. List required states, empty states, errors, permissions, and edge cases.
4. Include content requirements and data dependencies.
5. Identify assumptions and validation questions.
6. Define review criteria.

## Output

Return a brief with user goal, flows, states, content, constraints, success criteria, and open questions.

## Done when

- User, goal, scenario, and job-to-be-done are each populated (no placeholders), and scope plus non-goals are stated explicitly.
- Required states (empty, error, permission, edge) are enumerated, and content requirements plus data dependencies are listed; missing data is flagged as an open question rather than glossed.
- Assumptions and validation questions are recorded, and review criteria the designer's output will be judged against are stated.
- When the originating product intent or target user is missing, the brief refuses to specify flows and returns the missing context as the first deliverable.
