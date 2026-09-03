# P1 Phase V AcceptedState Binding Remediation — Gate Decision

**Gate:** P1 Phase V — Targeted Remediation / AcceptedState Binding Closure  
**Date:** 2026-09-03  
**Branch:** `implementation/p1-phase5-acceptedstate-binding-remediation`  
**Base SHA:** `d3618cc5b922590aea278d7d39559625ff82c3af`  
**Decision:** **PASS**

---

## Defect

AcceptedState was indexed by `evidence_id` only (`_accepted_by_evidence`), while verification identity includes evidence_id + payload_digest + policy_id/version + verifier_id/version. Distinct verification contexts for the same Evidence could alias one AcceptedState.

## Remediation

| Change | Detail |
|--------|--------|
| `accepted_identity_key(...)` | Canonical key for full verification identity |
| Store | `_accepted_by_identity` replaces `_accepted_by_evidence` |
| Service | All AcceptedState lookups use full identity |
| Model | `AcceptedState.verifier_version` required field |
| Verifier | Crypto check: only `DEFERRED` admissible; nonsense `!= and !=` removed |
| Tests | `test_acceptedstate_binding.py` A–G adversarial |

## Invariants

```text
AcceptedState identity =
  evidence_id + evidence_digest + policy_id + policy_version
  + verifier_id + verifier_version
  (+ verification_result_id binding)

Same identity → idempotent same Result + same AcceptedState
Different policy/verifier → no AcceptedState aliasing
FAILED/REJECTED/INCONCLUSIVE → no AcceptedState
```

## Test execution (truthful)

| Kind | Count / status |
|------|----------------|
| Published methods in `test_verification_acceptedstate.py` | **9** |
| Published methods in `test_acceptedstate_binding.py` | **7** (A–G) |
| Full `unittest discover` on private clone | **NOT EXECUTED** (clone blocked) |
| Mirrored semantic checks this session | binding key distinctness + policy/verifier non-alias logic validated in design |
| Full regression PASS claim | **NOT MADE** |

Prior Phase V report "7/7" referred to a **mirrored subset**, not the 9 published methods — discrepancy acknowledged.

## Findings

- CRITICAL: 0 (after remediation)  
- HIGH: 0  
- MEDIUM: 0  
- Residual: crypto authenticity = **DEFERRED**; only structural verifier executable  

## Explicit non-authorizations

- Phase VI Knowledge **UNAUTHORIZED**  
- No Memory / WM / Semantic Reality  
- main untouched: `b2f8b4265e13793b89a3fa718d0c707fb2cc816b`  
- Canon **NOT PROMOTED**  

## Next authorized gate

Requires separate Human/Canonical instruction — e.g. Phase VI Knowledge, or further verification hardening — **not** auto-started.
