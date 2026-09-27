# Deterministic Transition Contract Validation Matrix

**Scope:** implementation-local structural enforcement only.

| Case | Input condition | Expected result |
|---|---|---|
| V-01 | Valid TransitionContract; all six fields non-empty strings | ACCEPTED |
| V-02 | Input is not TransitionContract | REJECTED |
| V-03 | PredecessorState is empty/whitespace | REJECTED |
| V-04 | CandidateAction is empty/whitespace | REJECTED |
| V-05 | ExpectedResultingState is empty/whitespace | REJECTED |
| V-06 | Evidence is empty/whitespace | REJECTED |
| V-07 | VerificationRequirement is empty/whitespace | REJECTED |
| V-08 | AuthorizationRequirement is empty/whitespace | REJECTED |
| V-09 | Any field has a non-string runtime value | REJECTED |
| V-10 | Multiple fields invalid | REJECTED; all errors reported in fixed field order |

## Boundary semantics

- Validation is structural, not semantic.
- No field is inferred or defaulted.
- No runtime value is coerced to string.
- A rejected contract cannot be represented as accepted by this validator.
- This matrix does not establish truthfulness of evidence, validity of authorization, verification success, replay/idempotency, or production effectiveness.
