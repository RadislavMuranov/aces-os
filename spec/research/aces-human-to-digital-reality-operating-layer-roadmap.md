# ACES Human-to-Digital Reality Operating Layer

## Fundamental Priority Research & Realization Roadmap

**Status:** FUNDAMENTAL PRIORITY RESEARCH — ACTIVE
**Date:** 2026-09-03
**Branch:** `architecture/priority-realization-roadmap-v2`

## 1. Fundamental Research Question

> **Какой программный слой должен существовать между человеком и распределённым цифровым миром, чтобы человек выражал намерение и принимал значимые решения, но не был вынужден вручную переводить это намерение между приложениями, интерфейсами, схемами, правилами, паролями и процедурами?**

The research objective is to determine and then implement the minimum software layer that removes the human from the role of manual middleware between human intent and distributed digital reality, while preserving necessary human authority, responsibility, control, safety and accountability.

## 2. Research Hypothesis

> **ACES OS — Human-to-Digital Reality Operating Layer:** программный слой, который компилирует человеческое намерение в безопасные, управляемые и проверяемые изменения цифровой реальности, скрывая паразитическую операционную сложность от человека.

This is a research hypothesis, not yet a final frozen architectural claim. It must be validated through implementation evidence and controlled experiments.

## 3. Core Architectural Hypothesis

```text
                  HUMAN
                    │
             Intent / Goal
                    │
                    ▼
        ┌─────────────────────┐
        │      ACES OS        │
        │                     │
        │ Human Reality Layer │
        │ Intent              │
        │ Context             │
        │ Semantic Model      │
        │ Authority / Policy  │
        │ Digital World Model │
        │ Connector Fabric    │
        │ Reconciliation      │
        │ Evidence            │
        │ Verification        │
        │ Accepted State      │
        └──────────┬──────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
      Gmail      GitHub     Notion
      Calendar   CRM        Kaiten
        │          │          │
        └──────────┼──────────┘
                   ▼
             DIGITAL WORLD
```

The architecture must be treated as a layered system rather than a monolithic agent.

## 4. Fundamental Problem: Human as Middleware

The baseline process to be studied is:

```text
Human
  ↓
Intent
  ↓
Manual Translation
  ↓
Application A
  ↓
Manual Interpretation
  ↓
Application B
  ↓
Manual Reconciliation
  ↓
Decision
  ↓
Manual Verification
```

Research must identify which steps are necessary human judgment and which are parasitic operational work that software should absorb.

## 5. Research and Realization Roadmap

### R0 — Research Contract

**Objective:** define exactly what must be proven.

Research:
- human-as-middleware problem definition;
- necessary versus parasitic friction;
- context switching;
- repeated data entry;
- authentication and credential burden;
- application-specific rules and schemas;
- cross-system translation;
- reconciliation;
- manual verification;
- human responsibility boundaries.

**Gate:** a falsifiable problem definition and measurable baseline.

### R1 — Human Middleware Research

Study how humans currently translate intent into distributed digital operations. Map representative real workflows end-to-end and identify where humans act as integration, orchestration, reconciliation, authentication, validation and state-synchronization machinery.

### R2 — Parasitic Friction Taxonomy

Establish a formal taxonomy of parasitic friction and distinguish it from necessary friction. The target is not zero friction; it is removal of friction that contributes no necessary human judgment or control.

### R3 — Digital Frontier Census

Research existing technologies attempting to solve adjacent parts of the problem:
- human-computer interfaces;
- digital assistants;
- RPA and browser automation;
- iPaaS and workflow automation;
- agent runtimes and harnesses;
- APIs, OpenAPI and JSON Schema;
- MCP and A2A;
- WebDriver/browser control;
- durable execution and workflow systems;
- IAM, authorization and policy engines;
- semantic layers and knowledge graphs;
- entity resolution;
- event/state/reconciliation systems;
- enterprise control planes.

Rule: no architectural conclusion without implementation evidence.

### R4 — Gap Analysis

Determine which capabilities already exist, which remain fragmented, and which require a new ACES composition.

Required matrix dimensions:
- capability;
- existing implementation;
- human involvement remaining;
- security boundary;
- provenance;
- verification;
- canonical-state handling;
- ACES gap.

Primary question:

> Is there already a complete software layer that transforms Human Intent into coherent Digital Reality without making the human the manual integration engine?

### R5 — ACES Boundary

Define the minimum unique ACES architectural boundary.

Preliminary candidate:

```text
Human
   │
   ▼
INTENT
   │
   ▼
ACES
   ├── Context
   ├── Semantic Model
   ├── Digital World Model
   ├── Authority
   ├── Policy
   └── Connector Resolution
   │
   ▼
Execution
   │
   ▼
Digital World
   │
   ▼
Observation
   │
   ▼
Evidence
   │
   ▼
Verification
   │
   ▼
Accepted State
   │
   ▼
ACES Reality
```

This boundary must remain compatible with the established ACES Authority principle: Authority remains above transport and is never delegated to a connector, protocol, agent, harness or tool.

### R6 — Digital World Model (P0)

Define what ACES means by Digital World and model cross-system entities and relationships.

Initial semantic candidates:

`Person, Organization, Project, Task, Document, Message, Conversation, Event, Appointment, File, Repository, Issue, Decision, Payment, Credential, Permission, Workflow, Resource`

Example relations:

```text
Person ──participates──> Project
Project ──contains─────> Task
Task ──references──────> Document
Document ──stored_in────> Repository
Message ──about────────> Project
Event ──involves───────> Person
```

Architectural invariants:
- DWOM ≠ Knowledge;
- Digital World State ≠ World Model State ≠ Semantic Reality;
- Reconciliation ≠ Truth;
- Source Authority ≠ ACES Authorization Authority.

### R7 — Connector Fabric

Build a protocol-independent Connector Plane for reaching the Digital World.

```text
             ACES
               │
       Connector Fabric
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
 Local       Native      Direct
                         Connector
               │
              MCP
               │
        Other protocols
               │
        Browser / CLI
               │
          Digital World
```

Connector choice is a transport/capability decision, not an authority decision.

Preserve the established principle:

> **CLA-first, Authority-above-transport.**

### R8 — Semantic / Context Compiler

Develop the hypothesis of an **Intent → Digital Reality Compiler**.

Target pipeline:

```text
Human Intent
      ↓
ACES Intent IR
      ↓
Context Resolution
      ↓
Entity Resolution
      ↓
Capability Resolution
      ↓
Policy / Authority
      ↓
Execution Plan
```

Universal semantic abstractions must not erase source-specific semantics:

`Universal Semantic Model ↔ Domain Model ↔ Source-Specific Model ↔ Raw API/UI`

### R9 — Authority / Policy

Integrate the already established ACES authority boundary.

Distinguish strictly:

`Capability ≠ Permission ≠ Approval ≠ Execution ≠ Verification ≠ Acceptance ≠ Canonicality`

ACES decides under policy:
- who/what may act;
- what may be attempted;
- scope and budget;
- required evidence;
- required verification;
- whether escalation is required;
- whether a resulting state may become canonical.

### R10 — Execution Plane Integration

Do not create a competing ACES Agent merely to solve execution.

The current execution architecture remains:

```text
ACES Authority / Governance
          ↓
        Orca
          ↓
        DSH
          ↓
       Agents
          ↓
       Models
```

ACES supplies intent, context, authority, constraints, capability scope, budgets and verification requirements. External execution returns actions, receipts, observations, failures, evidence and verification artifacts.

### R11 — Reconciliation Engine (P0)

Treat the Digital World as distributed, heterogeneous and potentially contradictory.

Required functions:
- source provenance;
- source authority;
- freshness;
- conflict detection;
- entity resolution;
- state reconciliation;
- uncertainty representation;
- explicit unresolved/conflict states.

Never silently convert reconciliation into truth.

### R12 — Evidence → Verification → Accepted State

This is the convergence boundary of the Execution Plane and Digital World Plane.

```text
EXECUTION PLANE ──────────────┐
                              ▼
                           EVIDENCE
                              │
DIGITAL WORLD PLANE ──────────┤
                              ▼
                        VERIFICATION
                              │
                              ▼
                       ACCEPTED STATE
                              │
                              ▼
                        ACES REALITY
```

Canonical transition:

`INTENT → AUTHORIZATION → CONNECTOR → EXECUTION → OBSERVATION → EVIDENCE → VERIFICATION → ACCEPTANCE → CANONICAL REALITY`

### R13 — Reality Layer

Only after the underlying semantic, authority, connector, reconciliation and verification mechanisms are evidenced should the human-facing Reality Layer be realized.

Reality Layer is an architectural human-facing abstraction, not merely a UI skin. It hides the internal topology and operational complexity of the Digital World while preserving necessary human control and visibility.

### R14 — Semantic Compression

Research and implement bidirectional semantic compression.

Expansion:

```text
1 human intention
        ↓
10 applications
        ↓
37 operations
        ↓
12 notifications
        ↓
8 states
```

ACES should expand one high-semantic-density human intent into machine operations, then compress distributed observations back into a coherent human-understandable state.

Target:

`Human Intent → ACES → Coherent Digital Reality`

and

`Human Meaning → Machine Operations → Digital World → Coherent Human State`

### R15 — Measurable Human Friction

Turn the principle into measurable engineering criteria.

Candidate HCF dimensions:
- human steps avoided;
- interfaces hidden;
- schemas hidden;
- context switches avoided;
- repeated decisions eliminated;
- memory burden eliminated;
- errors prevented.

Optimization is constrained by:
- Human Control;
- Safety;
- Authority;
- Observability;
- Reversibility;
- Verification;
- Accountability.

Primary invariant:

> **ACES должен минимизировать паразитическую когнитивно-операционную нагрузку при сохранении необходимого человеческого контроля.**

### R16 — Vertical Slice

Implement one complete end-to-end scenario:

```text
Human Intent
      ↓
ACES Intent IR
      ↓
Context
      ↓
DWOM
      ↓
Policy
      ↓
Connector
      ↓
Execution
      ↓
Digital World
      ↓
Observation
      ↓
Evidence
      ↓
Verification
      ↓
Accepted State
      ↓
Human Reality Layer
```

The vertical slice must demonstrate that the human no longer performs the integration/reconciliation work manually.

### R17 — Failure-First / Adversarial Experiments

Deliberately test:
- wrong context;
- conflicting sources;
- stale state;
- insufficient authority;
- wrong recipient/entity;
- partial execution;
- timeout;
- duplicate action;
- unavailable external system;
- model hallucination;
- tool-reported success with failed desired state;
- unexpected external state change.

Required explicit outcomes include:

`UNKNOWN | CONFLICT | UNVERIFIED | REJECTED | ESCALATE`

### R18 — HDE-003 Human-Middleware Experiment

Run a controlled comparison.

**Control:** human manually executes an end-to-end distributed workflow.

**Experiment:** human supplies intent to ACES and ACES performs the governed translation/execution/reconciliation/verification path.

Measure:
- human actions;
- interfaces touched;
- context switches;
- elapsed time;
- data manually entered;
- micro-decisions;
- errors;
- manual reconciliation;
- hidden assumptions;
- cognitive load;
- control retained;
- correctness and verification quality.

Success is not maximum automation. Success is measurable removal of parasitic human middleware work without unacceptable loss of control or correctness.

### R19 — Architectural Freeze

Only after R0–R18 evidence exists, freeze:

**ACES OWNS**
- Intent;
- Context;
- Digital World Model;
- Authority;
- Policy;
- Connector selection;
- Evidence;
- Verification;
- Acceptance;
- Canonical State;
- Human Reality Layer.

**ACES DOES NOT NEED TO OWN**
- foundation models;
- agent intelligence;
- execution runtime;
- every connector implementation;
- every application;
- every workflow engine;
- every protocol.

### R20 — Production Architecture

After architectural freeze, consolidate the proven layers into production ACES:

```text
                  HUMAN
                    │
                    ▼
            ┌───────────────┐
            │ REALITY LAYER │
            └───────┬───────┘
                    │
              HUMAN INTENT
                    │
                    ▼
            ┌───────────────┐
            │ INTENT ENGINE │
            └───────┬───────┘
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
      CONTEXT              DWOM
          │                   │
          └─────────┬─────────┘
                    ▼
             POLICY/AUTHORITY
                    │
                    ▼
           CONNECTOR FABRIC
                    │
             ┌──────┴──────┐
             ▼             ▼
        DIGITAL WORLD   EXECUTION
             │             │
             └──────┬──────┘
                    ▼
                 EVIDENCE
                    │
                    ▼
               VERIFICATION
                    │
                    ▼
              ACCEPTED STATE
                    │
                    ▼
              ACES REALITY
```

### R21 — Scale

Scale only after the semantic architecture and vertical slice are proven:

`1 connector → 5 → 10 → 100 → ecosystem`

Connector count is not itself a success metric. Semantic coverage, friction reduction, safety, correctness, provenance and retained human control are primary metrics.

## 6. Canonical Research Sequence

```text
R0  Problem Definition
 ↓
R1  Human Middleware Research
 ↓
R2  Parasitic Friction Taxonomy
 ↓
R3  Digital Frontier Census
 ↓
R4  Gap Analysis
 ↓
R5  ACES Boundary
 ↓
R6  Digital World Model
 ↓
R7  Connector Fabric
 ↓
R8  Semantic / Context Compiler
 ↓
R9  Authority / Policy
 ↓
R10 Execution Plane Integration
 ↓
R11 Reconciliation Engine
 ↓
R12 Evidence / Verification / AcceptedState
 ↓
R13 Reality Layer
 ↓
R14 Semantic Compression
 ↓
R15 Human Friction Metrics
 ↓
R16 Vertical Slice
 ↓
R17 Failure / Adversarial Experiments
 ↓
R18 HDE-003 Human Middleware Experiment
 ↓
R19 Architectural Freeze
 ↓
R20 Production Architecture
 ↓
R21 Scale
```

## 7. Core Success Criterion

> **Сколько паразитической работы между человеческим намерением и цифровой реальностью ACES способен устранить, не забирая у человека необходимую власть, ответственность и контроль?**

This is the primary research and engineering criterion for the Human-to-Digital Reality Operating Layer.

## 8. Architectural Position

ACES OS SHALL NOT compete with the execution frontier by becoming merely another Agent or Harness.

ACES SHALL provide the software layer that allows a human to express intent and retain significant decisions while ACES absorbs parasitic operational complexity across heterogeneous digital systems.

The execution frontier remains an external substrate. ACES governs the boundary at which external capabilities and executions are authorized, evidenced, independently verified, accepted and, only when policy permits, promoted into canonical ACES Reality.

The established principle **CLA-First, Authority-Above-Transport** remains in force. No connector, protocol, agent, harness or tool receives ACES Authority merely by technical capability or integration status.

## 9. Status and Gates

- **Research status:** ACTIVE
- **Priority:** FUNDAMENTAL / P0
- **Hypothesis status:** OPEN — requires evidence
- **Implementation status:** ROADMAP DEFINED; realization proceeds sequentially
- **No premature architectural freeze:** R19 is the freeze gate
- **Execution architecture:** preserve ACES → Orca → DSH → Agents → Models unless new evidence changes it
- **Digital World priorities:** DWOM + Connector Fabric + Reconciliation Engine are P0
- **Acceptance boundary:** Evidence → Verification → Accepted State

## 10. Completion Condition

The research is complete only when:

1. the Human Middleware problem is operationally defined;
2. existing frontier technologies have been studied with implementation evidence;
3. the ACES gap is demonstrated rather than assumed;
4. the minimum ACES boundary is specified;
5. DWOM, Connector Fabric and Reconciliation are implemented sufficiently for a vertical slice;
6. Intent → Digital Reality compilation is demonstrated;
7. Authority/Policy remains independent of transport and execution;
8. Evidence → Verification → Accepted State is demonstrated;
9. HCF is measured;
10. HDE-003 provides controlled evidence of reduced human middleware work;
11. failure-first tests demonstrate fail-closed behavior;
12. only then is the architecture frozen and scaled.
