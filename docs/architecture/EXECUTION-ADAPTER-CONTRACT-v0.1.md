# Execution Adapter Contract v0.1

**Status:** FROZEN for Universal Harness / Execution Adapter gate  
**Date:** 2026-09-01  
**Branch:** `feature/execution-adapter`  
**Base:** `a05c0b73714e2c30c4c55bc39b1df25e5cd173fe`

## Boundary

```text
ACES Semantic Reality
        ↓
Intent / Decision
        ↓
Authorization Boundary
        ↓
ExecutionAdapter
        ↓
Execution Runtime / Substrate  (replaceable)
        ↓
Observed Result
        ↓
Verification / Evidence
        ↓
AcceptedState
```

## Invariants

- Context ≠ Authority
- Capability ≠ Authority
- Inference ≠ Evidence
- Execution success ≠ AcceptedState
- Self-improvement ≠ Self-authorization
- DSH ≠ Authority (DSH not required; any substrate is replaceable)

## Contract fields

1. **execution request** — `ExecutionRequest`
2. **semantic intent/reference** — `intent_reference`
3. **authorized operation** — must match `AuthorizationRecord.operation`
4. **resource/scope** — exact match required
5. **runtime selection** — `runtime_id` must be registered
6. **capability handoff** — adapter calls `ExecutionRuntime.execute`
7. **execution result** — `ExecutionResult` with status + observed
8. **provenance** — adapter + approval_id + timestamps
9. **verification status** — starts PENDING/NOT_STARTED; never auto-PASS from success
10. **failure semantics** — FAILED vs REJECTED (auth)
11. **cancellation/termination** — CANCELLED reserved; runtime failure → FAILED
12. **no-authority-escalation** — missing/invalid auth → REJECTED; runtime cannot set AcceptedState

## Fail-closed

Missing authorization, operation/resource/scope/task mismatch, expired authorization, unknown runtime → `REJECTED`, `AcceptedState = NOT_ESTABLISHED`.

## Non-goals

- Full orchestration platform
- Productized DSH
- Production side effects
- Manufacturing approval or AcceptedState from capability
