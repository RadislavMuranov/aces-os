# ACES Digital World Priority 001

**Status:** P0 / IMMEDIATE / PRIORITY #1  
**Decision:** FROZEN PRIORITY BASELINE  
**Date:** 2026-09-02

## 1. Purpose

The primary realization problem of ACES OS is not connecting a large number of applications. It is removing the human from the role of permanent middleware between a fragmented digital world.

ACES OS must therefore operate as the coordination, reconciliation, evidence, and authority layer between the human and the Digital World.

> **ACES OS — my friendliest CONNECTOR to the DIGITAL WORLD.**
>
> ACES must manage digital-world complexity instead of transferring that complexity to the human.

## 2. P0 Architectural Decision

The following capability becomes the **single highest-priority realization task** of ACES OS:

**Digital World Model + Connector Fabric + Reconciliation Engine**

This work has priority over expansion of secondary features and must be treated as the immediate execution objective.

## 3. Digital World Coverage

The canonical connector target set is:

- GitHub
- Slack
- Notion
- Obsidian
- Kaiten
- Filesystem
- Browser
- Exa / Browser Exa
- Terminal
- Cloud
- Databases
- APIs
- Applications
- Remote machines
- Google Drive
- Gmail
- NotebookLM

This list is extensible. New systems must be integrated through the same canonical object, capability, provenance, authority, and policy model rather than through bespoke user workflows.

## 4. Fundamental Principle

**Application != Source of Truth.**

External systems are sources and surfaces of:

- state
- events
- artifacts
- communications
- evidence
- execution

ACES maintains the canonical epistemic and authoritative state through its own object/provenance model.

No external application becomes an ACES trust anchor merely because it is connected or administratively powerful.

## 5. Digital World Object Model (DWOM)

ACES must represent digital reality through canonical objects rather than application-specific records.

A DWOM object is a **canonical representation of an external digital-world entity, representation, event, or observation**. It preserves external identity, source, provenance, freshness, capabilities, and references to source material without automatically becoming an ACES KnowledgeObject.

The boundary is explicit:

```text
External Representation
  -> DWOM Object
  -> Observation / Evidence
  -> Reconciliation / Decision / Verification as applicable
  -> AcceptedState
  -> KnowledgeObject (only through the existing epistemic promotion path)
```

A connector MUST NOT silently promote an external representation, DWOM object, or retrieved observation into a KnowledgeObject merely because it was retrieved or synchronized.

A KnowledgeObject remains an ACES epistemic claim governed by the Knowledge/Memory/WorldModel contract. DWOM is a digital-world representation layer, not an epistemic authority layer.

## 6. Reference / Cache / Materialization

ACES must not mirror the entire Digital World by default.

Three data modes are canonical:

1. **Reference** — retain identity and provenance of an external object.
2. **Cache** — retain only the context required for active reasoning/execution.
3. **Materialization** — persist a local/canonical artifact only when required by policy, evidence, execution, or user intent.

Default behavior is **minimal retrieval, not total synchronization**.

## 7. Demand-Driven Synchronization

ACES must not require continuous manual or indiscriminate synchronization.

Canonical flow:

```text
Human Intent
  -> Required Context
  -> Relevant Objects
  -> Relevant Sources
  -> Minimal Retrieval
  -> Reconciliation
  -> Evidence / Action
```

The system must avoid "sync everything" architecture.

## 8. Digital World Reconciliation Engine

The Reconciliation Engine is responsible for:

- discovery
- identity resolution
- change detection
- deduplication
- conflict detection
- provenance
- freshness
- source authority mapping
- reconciliation
- canonical state projection

**Reconciliation is not Truth Arbitration.** The engine may discover, compare, correlate, detect conflict, apply explicitly defined precedence/policy, and produce a reconciled or candidate digital-world state. It MUST NOT silently manufacture epistemic truth or treat its own reconciliation result as authoritative merely because it resolved a conflict.

When sources disagree, ACES must preserve the competing observations and provenance. Any precedence between sources must be explicit, scoped to the relevant domain/operation, policy-governed, and distinguishable from ACES security/authorization authority.

## 9. Authority Model

Authority remains inside ACES.

```text
Human Authority
  -> ACES ASA
  -> Policy / Capability Evaluation
  -> Connector Operation
  -> External Digital World
```

GitHub, Slack, Notion, Obsidian, Kaiten, Google Workspace, cloud systems, and other connectors are untrusted external systems from the ACES authority perspective.

**Source Authority != ACES Authorization Authority.**

A source may be authoritative for a narrowly defined external fact or operation (for example, GitHub may be authoritative for the state of a GitHub issue), but that source authority MUST NOT grant the external system authority to authorize ACES actions, issue capabilities, redefine ACES Semantic Reality, or bypass ASA/policy evaluation.

Source precedence is therefore a data/epistemic-policy property; ACES authorization is a security/authority property. They MUST remain separate.

## 10. MCP Rule

MCP is **not** the default connector architecture.

MCP may be used only when a CLA / Connector / Local / Native alternative is unavailable.

Native and local integration paths have priority.

## 11. Human Interaction Cost

The architecture must explicitly optimize for **Human Interaction Cost** in addition to compute, latency, financial cost, and risk.

The target is to eliminate parasitic work such as:

- duplicate entry
- manual synchronization
- manual reconciliation
- repeated searching
- cross-application context switching
- unnecessary archiving
- repetitive cleanup
- copying decisions between systems
- maintaining multiple representations of the same knowledge

ACES must not replace human friction with machine-generated synchronization noise.

## 12. ASPE Realization Criterion

This capability is a direct engineering realization of the **Axiom of Preservation of Psychic Energy (ASPE)**:

> The inevitability of interaction with the digital world is not a justification for expending human psychic energy.

The system succeeds only if the human no longer has to act as middleware between disconnected digital systems.

## 13. Priority Roadmap

### P0 — Immediate

- freeze this architectural decision
- define DWOM canonical object contracts
- define Connector Contract
- define Identity Mapping
- define Capability Mapping
- define Event Mapping
- define Evidence Mapping
- define Authority Mapping
- define Reconciliation Contract
- define Human Interaction Cost metrics

### P1 — First Vertical Slice

Implement and verify a representative cross-system slice using:

- Obsidian
- GitHub
- Slack
- Gmail
- Google Drive
- Kaiten

The slice must demonstrate that one logical ACES object can be discovered, referenced, reconciled, evidenced, and acted upon across multiple systems without requiring duplicate manual entry.

The slice MUST distinguish:

```text
External Representation
  -> DWOM Object
  -> Observation / Evidence
  -> Reconciliation / Candidate State
  -> explicit Decision / Verification where required
  -> AcceptedState
  -> Knowledge promotion only through the existing epistemic path
```

It MUST also demonstrate that conflicting source observations remain traceable and that any source precedence used by reconciliation is explicit and policy-scoped rather than an implicit claim of truth or security authority.

### P2 — Research / Discovery Surfaces

- Notion
- Browser
- Exa / Browser Exa
- NotebookLM

### P3 — Execution / Infrastructure Surfaces

- Terminal
- Cloud
- Databases
- APIs
- Applications
- Remote machines

## 14. Acceptance Criteria

The P0 initiative is not complete when connectors merely work.

It is complete only when the following are demonstrated:

1. One ACES object can span multiple external representations.
2. Provenance is preserved for every imported fact/state/event.
3. Conflicting sources are detected and surfaced.
4. ACES can determine which source is authoritative for a given operation/domain **without confusing source precedence with ACES authorization authority or epistemic truth**.
5. Full-world mirroring is not required.
6. Synchronization is demand-driven.
7. Human does not perform routine cross-system reconciliation.
8. Human does not have to maintain duplicate representations.
9. Connector failures fail safely and preserve uncertainty.
10. ASA remains the authority boundary.
11. MCP is used only as an exception path.
12. The resulting system measurably reduces parasitic human interaction cost.
13. DWOM retrieval/synchronization does not silently create KnowledgeObjects.
14. Reconciliation preserves competing observations and provenance when conflicts cannot be legitimately resolved.
15. Digital World State, World Model State, and Semantic Reality remain distinct layers with explicit boundaries.

## 15. World State Boundary

The term **Digital World State** denotes a reconciled or projected representation of observed external digital-world state. It is not equivalent to ACES Semantic Reality and is not itself epistemic truth.

The layers are distinct:

```text
Digital World State
= reconciled/projected representation of observed external state

World Model State
= ACES epistemic belief/probability about relevant state

Semantic Reality
= ACES canonical semantic representation maintained through the governed epistemic chain
```

Accordingly:

- **Digital World State != World Model State**.
- **World Model State != Semantic Reality**.
- **Evidence != either state**; evidence is bound observation used by verification and epistemic updates.
- **World Model != Evidence** and cannot manufacture evidence.
- **World Model != Authority** and cannot authorize actions or directly mutate/redefine Semantic Reality.
- A Digital World State projection MUST NOT by itself become Semantic Reality.
- Knowledge promotion remains governed by the existing `Evidence -> Verification -> AcceptedState -> Knowledge` path.

The canonical epistemic direction is:

```text
Digital World
  -> Observation / Evidence
  -> Verification
  -> AcceptedState
  -> Knowledge Update
  -> Semantic Reality
```

In parallel, legitimate accepted epistemic inputs may update the World Model:

```text
Accepted epistemic inputs
  -> World Model Update
  -> Belief / Projection
```

There is no direct:

```text
World Model
  -> Semantic Reality mutation
```

or:

```text
Digital World State
  -> Semantic Reality by fiat
```

## 16. Architectural Position in the Frozen Stack

```text
ACES Control / Governance / Epistemic Authority
                    |
             Execution Contract
                    |
                  Orca
                    |
                   DSH
                    |
          ACES Inference Fabric
          /       |        \
      Polza     Direct      Local
                    |
                  Models

Parallel / cross-cutting ACES layer:

Connector Fabric
       |
Digital World Object Model
       |
Reconciliation Engine
       |
Digital World State
       |
Evidence / Verification
       |
AcceptedState
       |
Knowledge / Memory / World Model
       |
Semantic Reality
```

The Digital World layer is not a peripheral integration feature. It is a primary realization layer of the ACES mission.

## 17. Immediate Execution Rule

Until this P0 initiative reaches its first verified vertical slice, new integrations and secondary features must not displace it in priority unless explicitly justified by an Architecture Decision Record.

**Priority:** P0 / BLOCKING  
**Execution mode:** immediate  
**Success condition:** ACES removes the human as digital-world middleware.
