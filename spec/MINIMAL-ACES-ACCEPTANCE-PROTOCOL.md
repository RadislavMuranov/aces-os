# Minimal ACES Acceptance Protocol

**Status:** IMPLEMENTED — repository protocol artifact  
**Research status:** CLOSED  
**Authorization:** repository implementation + local verification only  
**Scope:** ACES-level acceptance boundary for state transitions

---

## 1. Purpose

This artifact implements the already-fixed Minimal ACES Acceptance Protocol without reopening its semantic definition.

The protocol defines the boundary by which a verified, provenance-bound state transition may become authoritative `AcceptedState`.

It does not authorize production/runtime integration or external digital-world execution.

---

## 2. Upstream prerequisites

The acceptance kernel operates only after these ACES semantics are established:

```text
Identity
→ Target Binding
→ Authority / Policy
→ Temporal / Causal Binding
```

These are upstream prerequisites, not additional primitives of the minimal kernel.

---

## 3. Minimal acceptance kernel

```text
StateTransition
+
ProvenanceBoundEvidence
+
Verification(PASS)
+
Authority-bearing Acceptance
→ AcceptedState
```

### StateTransition

An explicit transition from one state to another.

### ProvenanceBoundEvidence

Evidence reconstructibly bound to the subject, transition, and canonical source/history.

### Verification(PASS)

An independent determination that the retained evidence satisfies the applicable verification specification.

### Authority-bearing Acceptance

The legitimate authority-controlled operation that promotes the verified transition into authoritative ACES state.

### AcceptedState

The authoritative state admitted by ACES after the required transition, provenance, verification, and acceptance conditions are satisfied.

---

## 4. Acceptance is not verification

The following responsibilities remain distinct:

```text
VerificationSpec
VerifierIdentity
VerificationResult
AcceptanceAuthority
```

In particular:

```text
Verification(PASS) ⇏ AcceptedState
```

Verification establishes that specified conditions were satisfied.

Acceptance establishes that the corresponding transition is authorized to become authoritative state.

---

## 5. Acceptance binding

```text
AcceptanceBinding =
{
    canonical_ref,
    authority_ref,
    capability_ref,
    policy_ref,
    verification_context_ref
}
```

Where:

- `canonical_ref` identifies the canonical reality being transitioned.
- `authority_ref` identifies the authority domain responsible for acceptance.
- `capability_ref` identifies the delegated right permitting the action.
- `policy_ref` identifies the policy/version governing admissibility.
- `verification_context_ref` binds acceptance to the exact verification context.

---

## 6. Minimal invariants

```text
ExecutionResult       ⇏ AcceptedState
VerificationResult    ⇏ AcceptedState
Verification(PASS)    ⇏ AcceptedState
Authority / Policy    ⇏ AcceptedState
StateTransition       ⇏ AcceptedState
```

Therefore:

```text
AcceptedState
⇒
ProvenanceBoundHistory
∧ ValidTransition
∧ Verification(PASS)
∧ Authority-bearing Acceptance
```

And:

```text
NoHistory ⇒ NoAcceptedState
```

---

## 7. Non-collapse requirement

The implementation MUST NOT hide the acceptance boundary inside:

- verification;
- execution;
- capability;
- policy;
- state-transition mechanics.

The prohibited implicit semantic path is:

```text
VerifiedResult → AcceptedState
```

The explicit promotion boundary remains:

```text
Verified
+
Provenance-bound
+
Valid Transition
+
Authorized Acceptance
→ AcceptedState
```

The implementation may use one technical operation internally, but its semantics MUST preserve this distinction.

---

## 8. Semantic pilot boundary

The repository artifact implements the protocol semantics established by AP-001.

AP-001 demonstrated:

```text
PASS
∧ ValidAcceptanceBinding
∧ AuthorityAcceptance
⇒ AcceptedState
```

while:

```text
PASS
∧ ¬ValidAcceptanceBinding
⇒ ¬AcceptedState
```

The pilot remains semantic evidence; this artifact does not reinterpret it as production evidence.

---

## 9. Authorization boundary

### AUTHORIZED

- Repository implementation of this protocol artifact.
- Local verification of the repository artifact and its fixed invariants.

### NOT AUTHORIZED

- Production/runtime integration.
- ACES ↔ Orca ↔ DSH activation.
- External digital-world execution.
- Canon promotion.
- Claims of production effectiveness.

---

## 10. Epistemic boundary

Repository implementation success does not establish production/runtime effectiveness.

Local verification establishes only that this repository artifact contains and preserves the fixed protocol semantics checked by the local verification procedure.

It does not establish that an integrated runtime prevents all prohibited transitions.

---

## 11. Canonical relationship

Notion remains the semantic/governance fixation record.

This file is the repository implementation artifact corresponding to that already-fixed semantic record.

No new semantic authority is created by this file.

---

## 12. Implementation closure condition

This first implementation step is complete only when the repository artifact is committed and independently read back from the repository, with the required protocol invariants confirmed present.

