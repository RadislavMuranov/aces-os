# ASA Hardening Contract v0.1

**Status:** FROZEN  
**Date:** 2026-09-01  
**Branch:** `feature/asa-hardening`  
**Base:** `feature/execution-adapter` @ `5fc7b1028de55ea90c80432562c5d0bfaeb4014e`  
**Lineage:** ASA-004 authorization core (`asa-004-authorization-core`)

## Separation (MUST NOT collapse)

```text
Authentication of authority  →  is this grant store-backed under known Authority?
Authorization semantics      →  does it permit exact op/resource/scope/time/principal?
Execution                    →  may ExecutionAdapter dispatch?
Verification                 →  did the external world match the claim? (DEFERRED)
AcceptedState                →  only after independent verification (NOT this gate)
```

## Authority authenticity (this gate)

Trust root for this gate (explicit, non-cryptographic):

- Capability body is loaded from **CapabilityStore** (not client-forged body).
- `issued_under_authority` and policy authority must be in **AuthorityRegistry**.
- Unknown capability_id → DENY (`INVALID_CAPABILITY`) — forged id fails.
- Structural `AuthorizationRecord` alone is **not** proof of authenticity.

**Deferred to later gate:** cryptographic signature / out-of-band approval binding.  
**Trust assumption:** store integrity + registry membership. Acceptable only for synthetic/local boundary proof.

## Decision vocabulary

Canonical: `ALLOW` | `DENY` (ASA-004).

Handoff maps:

- `ALLOW` → `may_dispatch=True`
- `DENY` → `may_dispatch=False` (ExecutionAdapter MUST NOT be called)

## Fail-closed (non-exhaustive)

unknown identity/authenticator · invalid capability · unknown authority · expired ·
revoked · scope/op/resource/principal mismatch · missing policy · policy engine error ·
revocation store unavailable · audit unavailable → **DENY**, no dispatch.

## Verification boundary (residual)

`apply_verification(passed=True)` remains caller-trusted on ExecutionAdapter.  
ASA Hardening does **not** claim independent evidence.  
**Next gate candidate:** Evidence / Verification hardening.

## Non-goals

Enterprise IAM · PKI · full policy engine (ASA-006) · production security certification ·
Canon Promotion · modifying Execution Adapter internals · E3.4 re-open.
