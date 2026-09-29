# Minimal ACES Acceptance Protocol

**Protocol ID:** MAP-001  
**Status:** FORMALLY FIXED  
**Research status:** CLOSED  
**Semantic scope:** ACES-level acceptance boundary for digital-world state transitions.

## 1. Purpose

Define the minimum semantic boundary required for a digital-world transition to become authoritative ACES `AcceptedState`.

This protocol is not an execution framework and is independent of any particular model, agent, harness, connector, or tool protocol.

## 2. Upstream ACES prerequisites

The acceptance kernel operates only after the existing ACES semantic prerequisites are established:

```text
Identity
→ Target Binding
→ Authority / Policy
→ Temporal / Causal Binding
```

These are upstream ACES responsibilities. They are not additional primitives of the minimal acceptance kernel.

## 3. Minimal semantic kernel

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

An explicit transition from a prior state to a proposed or resulting state.

### ProvenanceBoundEvidence

Evidence reconstructibly bound to the relevant subject, target, transition, source/history, and verification context.

### Verification(PASS)

An independent determination that the retained evidence satisfies the applicable verification specification.

### Authority-bearing Acceptance

The legitimate ACES-controlled operation that promotes the verified transition into authoritative ACES state.

Acceptance is a semantic control-plane responsibility. It may be implemented compositionally; it must not be semantically hidden inside execution, verification, policy evaluation, or generic state-transition mechanics.

### AcceptedState

The authoritative state admitted by ACES after the acceptance boundary has been satisfied.

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

Verification establishes that specified conditions were satisfied. Acceptance establishes that the corresponding transition is legitimately promoted to authoritative state.

## 5. Minimal invariants

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

## 6. Non-collapse requirement

The acceptance boundary MUST remain semantically explicit.

An implementation MUST NOT rely on an implicit rule equivalent to:

```text
VerifiedResult → AcceptedState
```

If implementation combines verification, authorization, transition commit, and acceptance into one technical operation, the semantic acceptance boundary remains distinct and reconstructible.

## 7. Authority binding

Acceptance preserves the existing ACES authority chain at the point where a verified transition becomes authoritative state.

A conceptual acceptance binding is:

```text
AcceptanceBinding = {
    canonical_ref,
    authority_ref,
    capability_ref,
    policy_ref,
    verification_context_ref
}
```

This does not create a new authority model. It binds acceptance to the already-established ACES identity, target, authority, policy, and verification semantics.

## 8. Relation to the ACES execution stack

```text
ACES
 ↓
Orca
 ↓
DSH
 ↓
AgentRun / Session
```

Execution-layer components produce or mediate execution. They do not become authoritative acceptance authorities merely by producing a successful result.

Existing primitives remain complementary where applicable:

```text
Model          → COMPLEMENTARY
Context        → COMPLEMENTARY
Reasoning      → COMPLEMENTARY
Tool Protocol  → COMPLEMENTARY
State          → ACES-OWNED
Agent Loop     → COMPLEMENTARY
Memory         → COMPLEMENTARY
Verification   → ACES-OWNED
Harness        → COMPLEMENTARY
Evidence       → ACES-OWNED
```

This classification is semantic, not a claim that other systems lack state, verification, or evidence mechanisms. ACES-owned means that their authoritative composition and acceptance semantics belong to ACES.

## 9. External architectural corroboration

Independent open-source systems examined during research reproduce the same boundary in different domains: verification evidence does not by itself change accepted state; an attributed/authorized decision or committed transition is required to promote a verified result into authoritative state.

This corroboration supports the ACES semantic conclusion but is not a dependency of the protocol.

## 10. Formal closure

The Minimal ACES Acceptance Protocol is formally fixed at the semantic level.

No additional research or local test is required to establish this atomic semantic conclusion. Future implementation or test gaps are evidence/implementation limitations unless contradictory evidence appears.

Canonical invariant:

```text
ExecutionResult ⇏ AcceptedState
```

Canonical promotion condition:

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
