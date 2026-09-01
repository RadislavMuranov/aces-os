# Evidence / Verification — REGRESSION CLOSURE

**Date:** 2026-09-01  
**Branch:** `feature/evidence-verification-hardening`  
**Pre-closure HEAD:** `e491038e73cdfbc26332614513ac9ed4085eba88`  
**Base (Evidence branch from):** `55b788ea76fce2fa52d1a33842c9916f5861ae04`  
**main:** `58a5e596d9fc469561b32d457cf80658667055c2` — **UNTOUCHED**

## Identity

| Field | Value |
|-------|--------|
| Branch | feature/evidence-verification-hardening |
| HEAD (pre-closure) | e491038e73cdfbc26332614513ac9ed4085eba88 |
| Base | 55b788ea76fce2fa52d1a33842c9916f5861ae04 |
| main | 58a5e596d9fc469561b32d457cf80658667055c2 |

## Test commands executed

```text
PYTHONPATH=src python3 -m pytest tests/aces_execution_adapter -v
# 13 passed in 0.03s

PYTHONPATH=src python3 -m pytest tests/aces_evidence -v
# 15 passed in 0.04s
```

ASA package + tests are **byte-identical** to ASA Hardening HEAD (`55b788ea…`):

- `src/asa/authorize.py` blob `cc286daf…` unchanged by Evidence commits
- `tests/asa/test_hardening.py` blob `242b8687…` unchanged by Evidence commits
- Prior ASA Hardening gate recorded **18/18** on that exact tree

Evidence-branch commits only added/changed:

- `src/aces_evidence/*`
- `src/aces_execution_adapter/adapter.py` (hardened `apply_verification`)
- `tests/aces_evidence/*`, `tests/aces_execution_adapter/test_adapter.py`
- architecture/result docs

## Results

| Suite | Result |
|-------|--------|
| ASA | **18/18** (unchanged tree vs 55b788ea; prior gate 18/18) |
| Execution Adapter | **13/13 PASSED** (this session, HEAD sources) |
| Evidence / Verification | **15/15 PASSED** (this session, HEAD sources) |
| Combined boundary suites | **46/46** (18 + 13 + 15) |
| Failures | **0** |

Full-repo suite including `tests/aces_context_compiler` was not required for this boundary closure; Context Compiler is outside ASA→Adapter→Evidence chain.

## Cross-Boundary Verification

| Boundary | Assertion | Result |
|----------|-----------|--------|
| ASA → Adapter | DENY blocks dispatch (`dispatch_if_allowed` → None) | PASS |
| Adapter → Result | success does not accept | PASS |
| Result → Evidence | evidence required for AcceptedState | PASS |
| Evidence → Verification | exact binding (task/resource/fingerprint) | PASS |
| Verification → AcceptedState | trusted verifier required | PASS |
| Legacy shortcut | `apply_verification(passed=True)` alone → NOT_ESTABLISHED | PASS |

## Security Invariants

| Invariant | Result |
|-----------|--------|
| Context ≠ Authority | PASS |
| Capability ≠ Authority | PASS (store-backed capability authenticity) |
| Inference ≠ Evidence | PASS |
| Execution success ≠ AcceptedState | PASS |
| Self-improvement ≠ Self-authorization | PASS (not in path) |
| Runtime ≠ Authority | PASS |
| Evidence ≠ Authorization | PASS |
| Verification ≠ Authorization | PASS |
| ASA ALLOW ≠ AcceptedState | PASS |
| `passed=True` ≠ AcceptedState | PASS |

## Residual Risks

1. Cryptographic / out-of-band verifier authenticity **deferred**
2. In-memory stores only (synthetic) — production persistence deferred
3. Context Compiler suite not re-executed in this closure run

## Safety

- main untouched
- E3.4 not reopened
- ASA implementation not modified in this closure
- Evidence implementation not modified in this closure (docs only)
- Adapter implementation not modified in this closure (docs only)
- no production / external side effects

## Conclusion

**REGRESSION CLOSED**

Chain holds:

```text
Authorization → ASA → ExecutionAdapter → Observed Result
        → Evidence → Trusted Verifier → AcceptedState
```

Caller-boolean acceptance path remains closed.
