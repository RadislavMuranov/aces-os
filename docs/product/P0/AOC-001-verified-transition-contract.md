# AOC-001 — Verified Transition Acceptance Contract

Status: draft (RAD-7 slice) · Code: `src/acceptance/accept-verified-transition.ts` (core), `src/acceptance/transition-decision.ts` (decision surface)
Scope: one local verified-transition path. Not a universal workflow engine. Old branches and production-provider integrations stay out of this slice.

## Inputs

`StateTransition` (transition_ref, canonical_ref, has_history), `VerificationResult` (status PASS|FAIL, verification_context_ref), `AcceptanceBinding` (canonical_ref, authority_ref, capability_ref, policy_ref, verification_context_ref), `AuthorityAcceptance` (accepted + authority_ref/capability_ref/policy_ref when accepted).

## Success result

`{ accepted: true, decision: AcceptedState }` — typed ACCEPTED decision carrying canonical_ref, transition_ref and the full acceptance_binding (correlation/evidence binding).

## Rejection taxonomy

| reason | when | maps to core guard |
|---|---|---|
| `MISSING_HISTORY` | `transition.has_history === false` | `if (!transition.has_history) return null` |
| `VERIFICATION_FAIL` | `verification.status !== "PASS"` | `if (verification.status !== "PASS") return null` |
| `MISSING_BINDING` | `binding === null` | `if (!binding) return null` |
| `EMPTY_BINDING_REF` | any binding ref is `""` | `if (Object.values(binding).some((ref) => ref.length === 0)) return null` |
| `AUTHORITY_DENY` | `authority.accepted === false` | `if (!authority.accepted) return null` |
| `BINDING_MISMATCH` (field) | binding ref ≠ matching input ref (canonical, authority, capability, policy, verification_context) | the five comparison guards |
| `EVALUATION_ERROR` | guards passed but core returned null (should be unreachable; fail-closed) | defensive |

Rejections carry `detail` and, for `BINDING_MISMATCH`/`EMPTY_BINDING_REF`, the offending `field`.

## Fail-closed rules

1. Unknown or incomplete policy evaluation is NOT a permission: it must be modeled upstream as `accepted:false`, which lands as `AUTHORITY_DENY`.
2. A rejection never triggers an external side effect. `decideVerifiedTransition` is pure; callers perform I/O only on `accepted:true`.
3. The core `acceptVerifiedTransition` stays the single acceptance authority; the decision wrapper mirrors its guard order and delegates the accept path to it, so the contract cannot drift from the code.

## Local end-to-end scenario (RAD-10/RAD-11 acceptance)

1. Compose a valid transition + PASS verification + complete binding + accepting authority → expect `accepted:true` with matching `decision.acceptance_binding`.
2. Mutate exactly one input per case (no history / FAIL verification / null binding / one empty ref / denied authority / each of the five ref mismatches) → expect the corresponding rejection reason.
3. Run: `node --test tests/accept-verified-transition.test.ts tests/transition-decision.test.ts` — all green with exit code 0.
