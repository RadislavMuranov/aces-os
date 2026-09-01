# Evidence / Verification Hardening Contract v0.1

**Status:** FROZEN  
**Date:** 2026-09-01  
**Branch:** `feature/evidence-verification-hardening`  
**Base:** `55b788ea76fce2fa52d1a33842c9916f5861ae04`

## Chain

```text
Authorization → ASA → ExecutionAdapter → Observed Result
        → Evidence → Trusted Verifier → AcceptedState
```

## Rules

1. `ExecutionResult.success ≠ AcceptedState`
2. Evidence binds: task_id, request_id, operation, resource, scope, result_fingerprint, provenance
3. Verifier must be in trusted VerifierRegistry (`trusted=True`)
4. Verification requires exact binding match
5. AcceptedState only if: SUCCEEDED + evidence exists + match + trusted verifier + non-replay
6. Fail-closed: missing/malformed/mismatch/unknown/untrusted/replay/store unavailable
7. Evidence/Verification does not authorize, does not create capability, does not bypass ASA

## Legacy API

`apply_verification(passed=True, verifier_id=...)` **without** `evidence_id` + `verification_service` + binding fields **MUST NOT** establish AcceptedState.

## Deferred

Cryptographic evidence signatures / out-of-band verifier PKI.
