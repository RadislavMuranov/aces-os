# ACES OS — UNIVERSAL HARNESS / DIGITAL REALITY CONTROL STACK

**Status:** CANDIDATE — architectural realization principle; not a new Canon layer
**Date:** 2026-08-31
**Authority:** Subject to ACES OS Master Control Protocol and existing Canonical Authority

## 1. Purpose

Define the proposed ACES Universal Harness as an integration and coordination principle for ACES OS. It does not replace existing runtimes, automation engines, process engines, connector systems, agent SDKs, browser drivers, UI builders, or observability systems.

ACES coordinates specialized external mechanisms while owning the semantic, authority, context, intent, provenance, verification, and accepted-state contracts.

## 2. Canonical architectural thesis

> ACES OS is not an automation platform. It is a semantic control interface over the digital world.

> ACES Universal Harness coordinates existing agents, workflows, processes, connectors, browsers, applications and execution runtimes without becoming the source of their domain semantics.

> One Semantic Reality → Multiple Projections → Multiple Execution Mechanisms → One Verified Reality State.

These statements are CANDIDATE architectural principles pending reconciliation with the governing Canon and Master Control Protocol.

## 3. Core distinction

External systems answer specialized execution questions:

- Agent runtimes → how to reason and use tools
- Workflow systems → how to automate workflows
- Process engines → how to execute processes
- Connector systems → how to reach applications
- MCP → how tools/resources can be exposed through a protocol
- Browser/computer drivers → how to operate digital interfaces
- Durable execution systems → how execution survives retries, waits, failures, and restarts
- Observability systems → how execution is traced and evaluated
- Design/UI systems → how representations are constructed

ACES answers the higher-order coordination question:

> How does a human manage digital reality through one friendly interface while preserving semantics, authority, state, evidence, verification, and feedback?

## 4. Semantic Reality as source of truth

```text
                    SEMANTIC REALITY
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 PROCESS PROJECTION  PRODUCT PROJECTION  KNOWLEDGE PROJECTION
        │                  │                  │
        ▼                  ▼                  ▼
 process execution       UI/product          knowledge views
```

BPMN-like process representations, product/UI representations, and knowledge views are projections of Semantic Reality rather than independent sources of truth.

## 5. H0–H12 Universal Harness

### H0 — Semantic Reality
Source of truth: objects, relations, context, state, projects, tasks, decisions, evidence, processes, metrics, policies, roles, memory, and business logic.

### H1 — Context Harness
Collects and scopes the context required for a specific operation.

### H2 — Intent Harness
Transforms human intent into structured, actionable intent.

### H3 — Decision Harness
Determines what should happen, whether it is permitted, who/what should execute it, which mechanism should be used, and the appropriate autonomy level.

### H4 — Process Harness
Represents and executes deterministic and human/agent processes. Process models are executable projections, not semantic authority.

### H5 — Agent Harness
Uses AI reasoning where deterministic mechanisms are insufficient. Agents are execution mechanisms, not the ultimate system authority.

### H6 — Connector Fabric
Provides interoperable access to digital services through multiple connector protocols and mechanisms. MCP is one protocol within the fabric, not the fabric itself.

### H7 — Digital World Driver
Supports API, MCP, browser, computer, file, shell, database, cloud/SaaS, messaging, code, and human execution modes where authorized.

### H8 — Product Visualization Layer
Projects Semantic Reality into user-facing product/UI representations using design intent and machine-readable design memory.

### H9 — Execution Harness
Provides durable, resumable, retryable, observable, permission-aware execution and compensation/reversal where feasible.

### H10 — Verification Harness
Determines whether the observed result satisfies the intended contract and required invariants.

### H11 — Evidence Harness
Captures execution trace, provenance, audit data, results, proof, and state transition evidence.

### H12 — Authority / Security Boundary
Determines whether an operation is authorized under the applicable identity, capability, scope, policy, authority, revocation, and protected-artifact rules.

## 6. Canonical reality-management loop

```text
REALITY
   ↓
SEMANTIC MODEL
   ↓
INTENT
   ↓
DECISION
   ↓
AUTHORIZED EXECUTION
   ↓
DIGITAL WORLD
   ↓
OBSERVED RESULT
   ↓
VERIFICATION
   ↓
EVIDENCE
   ↓
ACCEPTED STATE
   ↓
UPDATED REALITY
```

The loop is incomplete unless the resulting state is observed and verified.

## 7. Universal Connector Fabric

```text
                 ACES CONNECTOR FABRIC
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
         MCP            API          BROWSER
          │              │              │
          └──────────────┼──────────────┘
                         ▼
              DIGITAL WORLD SERVICES
```

The architecture must not equate MCP with the entire connector architecture. Protocol, authentication, capability discovery, authorization, execution, provenance, and verification remain separable concerns.

## 8. Execution selection

For a user-level intent such as “send this to the client”, ACES may select among API, MCP, browser, computer, or human execution based on availability, authority, reliability, policy, risk, and required evidence.

The user should not need to understand the underlying mechanism unless the decision requires disclosure or approval.

## 9. External systems as specialized subsystems

ACES should prefer integration/adaptation over rebuilding mature infrastructure. Candidate external classes include agent runtimes, workflow engines, process engines, connector platforms, browser drivers, durable-execution runtimes, observability platforms, and design systems.

This is an architectural constraint, not a commitment to any particular vendor.

## 10. Authority and verification

No external runtime becomes ACES authority merely because it executes an action. External systems are execution substrates. ACES authority and verification remain governed by ACES contracts and the applicable Master Control Protocol.

```text
Human / Canonical Authority
            ↓
     ACES Authority
            ↓
     Decision / Policy
            ↓
 Authorized Execution
            ↓
 External Runtime
            ↓
 Evidence / Verification
            ↓
     Accepted State
```

## 11. Relationship to Evolution Control

The Universal Harness is not itself an autonomous self-modification mechanism. Evolution of its scaffolding, skills, hooks, policies, or adapters must follow the existing evolution governance and observed-failure requirements.

In particular:

```text
Observed reality
      ↓
Failure / opportunity
      ↓
Candidate change
      ↓
Controlled verification
      ↓
Decision
      ↓
Authorized realization
```

No architectural expansion is justified merely because a new tool or trend exists.

## 12. Architectural non-goals

ACES does not become:

- a new Zapier;
- a new n8n;
- a new BPMN engine;
- a new browser automation framework;
- a new agent SDK;
- a new UI builder;
- a new MCP implementation merely for protocol ownership;
- a new observability platform.

ACES owns semantic coordination, authority, context, intent, provenance, verification, and accepted-state integration.

## 13. Candidate mapping model

Future implementation work should maintain an explicit mapping:

```text
ACES primitive
   ↓
external capability
   ↓
adapter / connector
   ↓
contract
   ↓
authority boundary
   ↓
evidence
   ↓
verification
```

No external capability should be adopted solely by feature similarity; it must be evaluated for semantic fit, authority, failure semantics, evidence quality, and integration cost.

## 14. Research and trend resilience

The harness must be resilient to rapid changes in LLMs, agent runtimes, protocols, and tooling. External technology trends are evidence for evaluation, not automatic reasons to change Canon.

```text
NEW TREND
   ↓
OBSERVE
   ↓
CLASSIFY
   ↓
EVALUATE AGAINST REALITY
   ↓
EXPERIMENT / ABLATION WHEN JUSTIFIED
   ↓
EVIDENCE
   ↓
DECISION
   ↓
ONLY THEN REINTRODUCE NECESSARY CONTROL
```

## 15. Current status

**CANDIDATE.** This document records a proposed architectural realization principle discovered during corpus archaeology and current technology analysis. It must not be promoted to Canonical status until reconciled against the authoritative ACES Constitution, existing canonical evolution mechanisms, Master Control Protocol, Canon Gate, Realization Roadmap, and verified runtime evidence.

**Reality precedes canon.**
