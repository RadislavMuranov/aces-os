# ACES OS — MASTER CONTROL PROTOCOL

**Status:** FIXED FOR RECONCILIATION
**Date:** 2026-09-01
**Repository:** `RadislavMuranov/aces-os`
**Branch:** `feature/master-control-protocol`
**Base main at reconciliation:** `58a5e596d9fc469561b32d457cf80658667055c2`

## 1. Purpose

This document defines the reconciled control boundary for ACES OS after consolidation of the current Canon, Schema/System Prompt lineage, E1/E2/E3 evidence, DSH reverse-engineering, DeepMind self-improvement research, Universal Harness architecture, and P0.3.2 infrastructure constraints.

It is a control specification, not evidence of implementation or production readiness.

## 2. Authoritative status

- Canon 22: retained.
- System Prompt v1: retained as current implementation baseline.
- Schema v1.0: retained and frozen.
- E1 Constitutional Reconciliation: PASS.
- E2 Connector Evidence: retained with its documented evidence limitations.
- E3 Experiment 001: CONDITIONAL PASS.
- E3 B/T runs: 3 / 3.
- E3 median weighted HIW: 16 -> 7 (~56% directional reduction).
- E3 critical safety events: 0.
- Connector Value: SUPPORTED.
- Connector Generality: UNPROVEN.
- Canon Promotion: NOT AUTHORIZED.
- E3.1 Durable Minimal Context Compiler: next engineering gate.
- P0.3.2 qualified GUI-host dependency: hard infrastructure boundary where applicable.
- Production: BLOCKED until required gates pass.

## 3. Immutable invariants

```text
Context != Authority
Capability != Authority
Inference != Evidence
Execution success != AcceptedState
Self-improvement != Self-authorization
```

These invariants constrain all future implementation and evaluation.

## 4. ACES ownership boundary

ACES owns:

- Semantic Reality and semantic coordination;
- context compilation;
- intent representation;
- decision coordination;
- authority evaluation;
- provenance;
- verification;
- AcceptedState;
- control-plane policy.

External systems may provide specialized execution substrates:

- agent runtimes;
- process/workflow runtimes;
- MCP and API connectors;
- browser/computer drivers;
- durable execution;
- observability.

External execution capability must not be interpreted as ACES authority.

## 5. Universal Harness architectural decomposition

The H0-H12 model is an architectural decomposition, not twelve independently authorized implementation projects:

```text
H0  Semantic Reality
H1  Context Harness
H2  Intent Harness
H3  Decision Harness
H4  Process Harness
H5  Agent Harness
H6  Connector Fabric
H7  Digital World Driver
H8  Product Visualization
H9  Execution Harness
H10 Verification Harness
H11 Evidence Harness
H12 Authority / Security Boundary
```

Semantic Reality remains the candidate source of truth; process, product, and knowledge representations are projections unless explicitly promoted by Canon.

## 6. DSH boundary

DeepSeek Harness (DSH) is treated as an adaptable execution substrate. It is not an ACES trust root, authority source, or semantic source of truth.

The ACES integration boundary is:

```text
ACES control / semantics
        -> Execution Adapter
        -> DSH or another runtime
        -> external execution
        -> observation
        -> evidence / verification
        -> AcceptedState
```

## 7. Controlled self-improvement boundary

DeepMind research is retained as a precedent for self-play, evaluation-driven learning, and iterative policy improvement. It does not establish ACES autonomy by itself.

ACES evolution remains governed:

```text
Experience
  -> Evaluation
  -> Candidate Change
  -> Constitutional Gate
  -> Promotion
```

Learning cannot grant authority.

## 8. Evidence boundary

E3 established a directional experimental signal for Context Compiler value. It did not establish Connector Generality, production readiness, autonomous authority, or Universal Harness validity.

No architectural assertion may be promoted to experimental fact without reconstructable evidence.

## 9. Required implementation sequence

```text
E3.1 Durable Minimal Context Compiler
  -> E3.2 Replication
  -> E3.3 Interruption / Recovery
  -> E3.4 Bounded Authorized Write
  -> Universal Harness / Execution Adapter
  -> ASA hardening
  -> Evidence / Verification hardening
  -> Knowledge / Memory / World Model
  -> Controlled Self-Evolution
  -> E4 Canon Promotion Gate
```

No later stage authorizes bypass of an earlier evidence gate.

## 10. E3.1 contract boundary

The minimal compiler must implement only:

```text
SOURCE STATE
  -> NORMALIZE
  -> PROVENANCE BIND
  -> UNCERTAINTY PRESERVE
  -> CONFLICT EXPOSE
  -> CONTEXT PACKAGE
```

It must not silently add a general memory system, broad knowledge graph, long-horizon autonomous planner, or unrelated ACES functionality.

## 11. Safety veto

Any of the following is a critical event and vetoes productivity PASS for the affected workflow:

- unauthorized action;
- owner-boundary violation;
- provenance loss;
- uncertainty suppression;
- verification bypass;
- unrecoverable state;
- audit gap.

## 12. Infrastructure boundary

Where an experiment requires a qualified human-operated GUI host, the absence of such infrastructure is an execution blocker. A container, `/dev/kvm`, package manager, headless browser, mock, or synthetic harness does not by itself satisfy the qualified GUI-host requirement.

No real-user data or production access is authorized solely to compensate for missing infrastructure.

## 13. Control-plane discipline

- Work must remain on the designated feature/evolution branch until explicitly promoted.
- `main` must not be mutated by this fixation.
- Historical SHAs must not be treated as current state when repository verification shows otherwise.
- Failed, partial, blocked, and recovered trajectories must remain visible in evidence.
- Criteria must not be changed after observing experimental results.
- No PASS may be declared without the required evidence.

## 14. Current gate

```text
MASTER CONTROL RECONCILIATION
        -> FIXATION
        -> INDEPENDENT AUDIT
        -> E3.1
```

The current artifact does not itself authorize implementation beyond the next approved gate.

## 15. Explicit non-claims

This protocol does not claim:

- Connector Generality is proven;
- Universal Harness is proven;
- DSH is the ACES runtime of record;
- GUI infrastructure is available;
- production readiness exists;
- autonomous consequential writes are authorized;
- Canon Promotion has occurred.

## 16. Acceptance criterion for the next transition

The next transition is valid only when the repository contains an independently auditable E3.1 implementation specification and the implementation is limited to the frozen minimal Context Compiler boundary.
