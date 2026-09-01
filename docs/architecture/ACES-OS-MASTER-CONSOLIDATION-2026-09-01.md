# ACES OS — MASTER CONSOLIDATION

**Date:** 2026-09-01
**Status:** RECONCILED / PRE-CANONICAL
**Branch:** `evolution/karpathy-agent-native-priority`

## 1. Purpose

This document consolidates the ACES OS architecture established across the current evolution line, including the ACES foundation, governance/epistemics, DeepMind self-improvement research, and DSH reverse-engineering.

It is a consolidation artifact, not an automatic Canon promotion.

## 2. Master model

ACES OS is a local-first cognitive/execution operating layer and CONNECTOR between human intent, knowledge, agents, and the Digital World. It is not itself a replacement for the underlying applications or an autonomous authority.

```text
Human Intent
  -> Understand
  -> Context
  -> Authorize
  -> Decide
  -> Compile
  -> Execute
  -> Observe
  -> Evidence
  -> Verify
  -> Accept
  -> Memory
  -> Learn
  -> Constitutional Gate
  -> next state
```

## 3. Planes

1. **Constitution / Governance:** Constitution, Policy, Authority, approval and immutable boundaries.
2. **Epistemic:** Evidence, Provenance, Verification, Knowledge, Memory, World Model.
3. **Decision / Compiler:** Intent, Decision, Authorization, Context Compiler, effective capability scope.
4. **Execution:** Execution Adapter, DSH/runtime, agents, tools, sessions, sandbox.
5. **Reality / Connector:** files, web, applications, APIs and external systems.

These planes MUST remain conceptually and authoritatively distinct.

## 4. Core invariants

```text
Context != Authority
Capability != Authority
Inference != Evidence
Execution success != AcceptedState
Self-improvement != Self-authorization
```

Unknown or unavailable critical authorization/provenance/audit state is fail-closed.

## 5. Runtime acceptance

```text
S0
 -> Decision (E=PASS, A=PASS)
 -> Transition
 -> Execution
 -> Result
 -> Verification PASS
 -> AcceptedState S1
```

Execution alone never creates an AcceptedState.

## 6. ASA

The authorization model uses minimal primitives: Identity, Principal, Capability, Resource, Operation, Scope, Policy, Authority, Decision, Provenance, Audit, Revocation and Expiration.

Operations include READ, CREATE, UPDATE, DELETE, EXECUTE, EXPORT, IMPORT, DELEGATE, AUTHORIZE and REVOKE.

Unknown identity, invalid/expired/revoked capability, missing policy, unavailable policy engine, unavailable audit or unavailable provenance are fail-closed conditions.

ASA is specified but not yet implemented in the repository.

## 7. Context Compiler

The minimum compiler contract is:

```text
SOURCE STATE
 -> NORMALIZE
 -> PROVENANCE BIND
 -> UNCERTAINTY PRESERVE
 -> CONFLICT EXPOSE
 -> CONTEXT PACKAGE
```

The compiler must preserve owner boundaries, source references, uncertainty and conflicts. It must not invent missing state, silently resolve conflicts or turn inference into observation.

The E3 experiment produced the first empirical signal for this mechanism: median weighted HIW 16 versus 7 across 3 baseline and 3 treatment runs, approximately 56% directional reduction, with zero critical safety events. This is a narrow experimental result, not a universal 56% claim.

## 8. DSH relationship

DSH is an adaptable execution substrate candidate, not an ACES authority layer.

```text
ACES -> ExecutionAdapter -> DSH / other runtime
```

DSH mechanisms may be adopted, adapted, replaced, forked or ablated as ACES evolves. ACES must not derive authority from DSH or GitHub administration.

## 9. DeepMind-derived learning line

AlphaGo established a human-scaffolded baseline. AlphaGo Zero demonstrated self-play learning from rules without human game data; AlphaZero generalized the approach across games. The architectural lesson adopted for ACES is controlled self-improvement through generated experience and evaluation, subject to immutable governance.

```text
Minimal admissible knowledge
 -> experience generation
 -> evaluation
 -> learning
 -> stronger policy/capability
 -> constitutional gate
 -> new cycle
```

MuZero is retained as a future research direction for learned world models and planning; it is not a current ACES implementation requirement.

## 10. Controlled self-evolution

Mutable knowledge, policy, capability and strategy may evolve only inside immutable governance boundaries. Learning does not grant authority.

## 11. Evidence status

- E1 Constitutional Reconciliation: PASS.
- E2 connector evidence: historical evidence basis exists in the evolution record; repository artifact named `E2-CONNECTOR-EVIDENCE-RESULT-2026-09-01.md` was not found during current repository audit and must not be fabricated.
- E3 Experiment 001: CONDITIONAL PASS according to the recorded result artifact.
- E3 durable runtime implementation: not yet present.
- E3 replication/recovery/bounded-write evidence: not yet sufficient.
- Canon Promotion: NOT AUTHORIZED.

## 12. Engineering rule

Architecture is not implementation. Implementation is not verification. Verification is not Canon promotion. Every transition requires its own evidence gate.
