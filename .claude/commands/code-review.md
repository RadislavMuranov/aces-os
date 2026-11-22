---
description: Evidence-based code review of the current change set.
argument-hint: [--fix]
disable-model-invocation: true
context: fork
---

Review the current change set only. Do not modify files unless $ARGUMENTS contains --fix.

1. Establish repository identity, HEAD, and working-tree state. Inspect the actual diff against the correct base.
2. Read changed files and relevant callers, dependencies, and tests. Separate pre-existing defects from regressions introduced by this change.
3. Search the full class of every confirmed finding and inspect analogous call sites. Do not repeat findings already reported in the current review.
4. Prioritize correctness, data integrity, money/pricing, other people's data, authentication, credentials, authorization, and security boundaries.
5. Report each finding with severity, exact file and line, and one concise sentence describing impact and evidence.
6. Keep style observations separate; maximum three for the entire review.
7. Do not infer a defect from a missing test alone. State what was and was not verified.

Output: findings (highest severity first), pre-existing findings, style notes (0–3), inspected scope, exact tests and raw output, remaining unknowns.

If --fix is present, minimally correct confirmed findings, add regression tests, run the narrowest relevant tests, and re-review the diff. Do not commit or push.
