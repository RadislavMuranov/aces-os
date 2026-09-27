# Typed Transition Contract + Deterministic Fail-Closed Validator

**Status:** IMPLEMENTATION — AUTHORIZED / BOUNDED  
**Authorization:** IMPLEMENTATION AUTHORIZATION — 2026-09-27  
**Scope:** repository-local contract and structural validator only.

## Purpose

Move transition semantic-completeness checking from executor-mediated interpretation to a deterministic rejection boundary.

## Contract

A transition candidate is structurally complete only when all six required fields are present as non-empty strings:

1. PredecessorState
2. CandidateAction
3. ExpectedResultingState
4. Evidence
5. VerificationRequirement
6. AuthorizationRequirement

The implementation deliberately does **not** decide whether the supplied evidence is truthful, whether verification actually passes, whether authorization is substantively valid, whether replay is idempotent, or whether the resulting state is safe. Those remain outside this bounded implementation scope and remain UNKNOWN where not established.

## Fail-closed behavior

Validation returns ACCEPTED only when the value is an instance of the typed contract and every required field is a non-empty string after whitespace trimming.

Any type mismatch or empty/whitespace-only required field produces REJECTED.

No coercion, inference, defaulting, or probabilistic interpretation is permitted.

Validation errors are deterministic and emitted in fixed contract-field order.

## Explicit non-goals

- runtime ACES/Orca/DSH integration;
- production activation or deployment;
- MAS implementation;
- provider selection;
- replay/idempotency semantics (CE-13);
- evidence-truthfulness verification (CE-14);
- production prevention-effectiveness claims;
- Canon promotion.

## Verification target

The initial implementation is a minimal structural enforcement boundary. Passing its tests establishes only that the local implementation deterministically accepts structurally complete contracts and rejects the tested malformed forms. It does not establish production effectiveness.
