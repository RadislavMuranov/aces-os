# ACES Integration & Authority Principle

## CLA-First, Protocol-Independent Authority

**Status:** PROPOSED CANONICAL ARCHITECTURAL PRINCIPLE  
**Date:** 2026-09-03  
**Branch:** `architecture/priority-realization-roadmap-v2`

## 1. Authority Supremacy

**ACES SHALL NOT delegate Authority to any connector, protocol, transport, agent, harness, tool or external execution runtime.**

Authority is an ACES-owned architectural concern and remains above the integration layer.

Therefore:

`Authority ≠ Connector ≠ Protocol ≠ Capability ≠ Execution`

No protocol, including MCP, may by itself establish Epistemic Authority, Decision Authority, Execution Authority, Acceptance Authority or Canonicality within ACES Reality.

## 2. MCP Is Not an Authority Mechanism

**MCP is a capability transport and interoperability mechanism, not an ACES Authority mechanism.**

MCP authorization may determine whether a client or principal is permitted to access a resource or invoke a capability within the MCP interaction model. It does not determine whether ACES should authorize the intended action, consider the resulting effect permissible or correct, accept the result as evidence, or accept the resulting state as canonical ACES Reality.

MCP therefore remains subordinate to the ACES Authority Boundary.

## 3. CLA-First Security Optimization

**ACES SHALL prefer the most direct, local, native, first-party or otherwise controlled integration mechanism when it objectively provides an adequate integration path.**

Preferred ordering:

`LOCAL → NATIVE / FIRST-PARTY → DIRECT CONNECTOR → MCP → OTHER PROTOCOL / BRIDGE`

This ordering is a **security and architectural optimization**, not an absolute prohibition against MCP.

Its purpose is to minimize unnecessary trust boundaries, credential propagation, token exposure, confused-deputy opportunities, protocol hops, attack surface, opaque intermediate components, provenance ambiguity and operational complexity.

ACES SHALL avoid introducing MCP merely where an equivalent or superior controlled CLA path already exists.

## 4. CLA-First Is Not CLA-Only

**CLA-first SHALL NOT be interpreted as CLA-only.**

MCP MAY be used when it provides material value that is not adequately provided by the available CLA path, including interoperability, capability availability, ecosystem leverage, deployment practicality, portability, operational economics, standardized integration, or materially lower implementation complexity.

The decision to use MCP remains subject to ACES Policy, Authorization, Security, Provenance, Verification and Acceptance requirements.

## 5. Connector Plane

ACES SHALL maintain a protocol-independent Connector Plane:

```text
                 ACES AUTHORITY
                       │
             ┌─────────▼─────────┐
             │ Capability Router │
             │ / Connector Plane │
             └─────────┬─────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
       LOCAL        NATIVE        MCP
          │            │            │
          └────────────┼────────────┘
                       │
                 DIGITAL WORLD
```

The Connector Plane determines **how ACES reaches the digital world**. It does not determine **whether ACES is authorized to accept what happens there as canonical reality**.

## 6. Authority Boundary

The canonical ACES control flow is:

```text
             ACES AUTHORITY
                    │
        ┌───────────┴───────────┐
        │                       │
    AUTHORIZATION           POLICY
        │                       │
        └───────────┬───────────┘
                    │
              CONNECTOR PLANE
                    │
       ┌────────────┼────────────┐
       │            │            │
     Local        Native        MCP
       │            │            │
       └────────────┼────────────┘
                    │
                EXECUTION
                    │
               OBSERVATION
                    │
                 EVIDENCE
                    │
              VERIFICATION
                    │
               ACCEPTANCE
                    │
             CANONICAL REALITY
```

Canonical transition:

**INTENT → AUTHORIZATION → CONNECTOR → EXECUTION → OBSERVATION → EVIDENCE → VERIFICATION → ACCEPTANCE → CANONICAL REALITY**

No connector or protocol may bypass the Authority, Evidence, Verification or Acceptance boundaries.

## 7. Security Invariant

ACES SHALL treat additional integration layers as additional security and epistemic boundaries.

> **The existence of a standardized protocol is not sufficient justification for introducing it into the execution path.**

Where a direct and adequately governed CLA path exists, introducing MCP solely for convenience SHALL be considered an unnecessary architectural and security dependency.

## 8. Architectural Invariant

**ACES does not delegate Authority to the integration protocol.**

**ACES chooses the transport according to architectural optimality, security, capability and interoperability requirements, while Authority always remains above the transport layer.**

This applies equally to Local connectors, Native APIs, First-party integrations, SDKs, REST/GraphQL, MCP, browser automation, CLI interfaces, future protocols, external agents and external harnesses.

No integration mechanism receives ACES Authority merely by being native, local, standardized, trusted by a vendor, or technically capable.

## 9. Final Principle

### **CLA-First, Authority-Above-Transport**

**ACES SHALL prefer the most direct, local, native, first-party or otherwise controlled integration mechanism that adequately satisfies its capability, security, provenance, observability and governance requirements. MCP SHALL be treated as an interoperability/capability transport mechanism rather than an Authority mechanism. MCP MAY be used where its material interoperability or capability value justifies the additional boundary. Regardless of transport, all Authority, Policy, Evidence, Verification, Acceptance and Canonical Reality decisions remain under ACES control.**

## 10. Core Invariant

> **MCP is never Authority. CLA-first is security optimization, not protocol absolutism. Authority remains transport-independent and ACES-owned.**
