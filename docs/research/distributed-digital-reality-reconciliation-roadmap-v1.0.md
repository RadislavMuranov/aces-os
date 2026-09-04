# ACES OS — Distributed Digital Reality Reconciliation Roadmap v1.0

**Status:** FROZEN RESEARCH BASELINE / NOT CANON
**Date:** 2026-09-04
**Branch:** `research/ddr-reconciliation-roadmap-v1`
**Parent control roadmap:** `docs/architecture/ACES-OS-PRIORITY-REALIZATION-ROADMAP-v2.0.md`

## 0. Purpose

This document freezes the research finding that ACES must be able to reason about a Digital World observed and changed through heterogeneous, independently authenticated agents, connectors, execution environments, and representations.

The problem is **not** solved merely by placing records in one ACES database. The central problem is maintaining a provable chain from distributed observations and actions to an identity-bound, provenance-bound, temporally grounded, conflict-aware and explicitly accepted Digital World state.

This is a research baseline, not a claim that ACES is architecturally necessary. Any future claim of necessity requires a fresh falsification/minimality test.

## 1. Problem statement

Observed pattern:

```text
ChatGPT  -> Notion A
Grok     -> Notion B
Claude   -> Notion C
Local    -> Obsidian
Codex    -> GitHub
...
          ↓
     many agents
     many contexts
     many connector instances
     many identities
     many execution planes
     many representations
          ↓
       ACES State
```

The unresolved question is:

> How can ACES determine whether these observations refer to the same human, same connector/account, same external object, same temporal state, same action lineage and same accepted reality — without treating a connector response or an agent report as truth by default?

## 2. Research finding frozen

The current evidence supports the following narrower finding:

**Distributed digital reality is an explicit reconciliation problem at the boundary between agents, connectors, external systems and ACES epistemic state.**

The finding is stronger than a storage problem and weaker than a proven architectural-necessity claim.

### Required distinctions

```text
Tool exists             != authenticated connector
Authentication          != authority
Agent identity          != human identity
Connector identity      != external object identity
Object identity         != canonical target
Observation             != evidence accepted by ACES
Evidence                != verification
Verification            != acceptance
Acceptance              != truth in the external world
Digital World State     != World Model
Digital World State     != Semantic Reality
Reconciliation result   != truth arbitration
Execution success       != verified state
```

## 3. External standards considered

The research baseline incorporates existing standards rather than inventing replacements:

- W3C PROV for provenance representation.
- SPIFFE/SPIRE-style workload identity for cryptographically verifiable workload identity.
- OAuth/OIDC and platform-specific authorization for delegated access.
- MCP for tool/data interoperability where appropriate.
- A2A for agent-to-agent interoperability.
- OpenTelemetry for execution/observability telemetry.
- Event sourcing / append-only evidence patterns for reconstruction.
- Distributed-systems techniques such as causal ordering, conflict detection and convergence where useful.

These components solve important subproblems but do not, individually, establish ACES AcceptedState or epistemic authority. W3C PROV explicitly models entities, activities and agents and their provenance; SPIFFE provides portable cryptographic workload identity; MCP provides transport-level authorization mechanisms; A2A provides interoperability between independent agents. citeturn0search8turn0search1turn0search9turn0search3

## 4. Canonical research pipeline

```text
Human Intent
    ↓
Agent / Execution Context
    ↓
Connector Observation or Authorized Action
    ↓
Identity Binding
    ↓
Provenance Capture
    ↓
Target / Object Binding
    ↓
Temporal Binding
    ↓
Evidence
    ↓
Conflict Detection / Reconciliation
    ↓
Verification
    ↓
Acceptance
    ↓
Accepted Digital World State
    ↓
Knowledge / Memory / World Model
```

No stage may silently substitute for another stage.

## 5. Roadmap

### RDR-00 — Research Baseline Freeze

**Goal:** freeze terminology, scope and non-claims.

**Output:** this roadmap + protocol pack.

**Gate:** no implementation until the protocol pack is reviewed and accepted as the active research execution plan.

### RDR-01 — Connector Reality Inventory

**Goal:** enumerate every relevant connector/execution channel and distinguish tool presence from observed authentication, identity, authority and reachability.

**Input:** connector registry and live read-only observations.

**Output:** Connector Reality Record.

**Pass:** every claimed connector property has direct evidence or is explicitly UNKNOWN.

### RDR-02 — Actor / Workload Identity Binding

**Goal:** establish who/what performed or supplied an observation.

**Output:** identity-bound observation envelope.

**Pass:** actor identity, workload/agent identity, connector instance and identity scope are distinguishable.

### RDR-03 — External Object / Target Binding

**Goal:** determine whether two observations refer to the same external object.

**Output:** Target Binding Record with source-native identifier, scope, locator and confidence.

**Pass:** same-object claims are evidence-backed; unresolved identity remains UNKNOWN/AMBIGUOUS.

### RDR-04 — Provenance Chain

**Goal:** bind each observation/action to source, actor, connector, time, operation and derivation.

**Output:** immutable Evidence/Provenance record.

**Pass:** an independent reviewer can reconstruct how the observation entered ACES.

### RDR-05 — Temporal / Causal Ordering

**Goal:** distinguish stale, concurrent, superseding and causally dependent observations.

**Output:** temporal relation set.

**Pass:** state precedence is never inferred from arrival order alone.

### RDR-06 — Cross-Connector Reconciliation

**Goal:** compare observations referring to the same target across independent connectors.

**Output:** Reconciliation Record preserving every conflicting observation.

**Pass:** conflicts are explicit; reconciliation does not silently become truth arbitration.

### RDR-07 — Authority / Policy Separation

**Goal:** separate external source authority from ACES authorization authority.

**Output:** policy evaluation record.

**Pass:** a source's ability to report or mutate its own system never grants it ACES authority.

### RDR-08 — Evidence → Verification → Acceptance

**Goal:** establish the only promotion path into AcceptedState.

**Output:** verification and acceptance records.

**Pass:** no observation, model output, connector success or agent completion can mint AcceptedState directly.

### RDR-09 — Accepted Digital World State

**Goal:** define the minimal state representation ACES can safely rely on.

**Output:** AcceptedState contract for digital-world facts.

**Pass:** every accepted state element points to evidence, verification and target identity.

### RDR-10 — Mutation Gate

**Goal:** prevent writes when identity, target, authority, lineage, current state or verification is unresolved.

**Output:** deterministic pre-mutation decision.

**Pass:** unresolved reality causes BLOCK / ESCALATE, not best-effort mutation.

### RDR-11 — Adversarial / Chaos Verification

**Goal:** reproduce the observed multi-agent/multi-connector failure modes.

**Required scenarios:** wrong connector instance; stale object; duplicate object; ambiguous target; different authenticated identities; missing auth; split execution environment; conflicting observations; replay; delayed observation; successful action with unverified external state.

**Pass:** all unresolved cases fail closed and remain traceable.

### RDR-12 — Minimality / Necessity Test

**Goal:** determine whether existing combinations of standards and infrastructure can satisfy the complete contract without a new ACES-specific layer.

**Pass:** only after an explicit comparative implementation and failure analysis.

### RDR-13 — Architecture Decision

Possible outcomes:

```text
A. Existing stack sufficient
B. Existing stack + thin ACES coordination sufficient
C. New ACES reconciliation boundary necessary
D. Research inconclusive
```

No outcome is predetermined.

### RDR-14 — Implementation Contract

Only if RDR-12/RDR-13 justify it, freeze executable contracts for the minimum required reconciliation kernel and integrate with the existing ACES P0 roadmap.

## 6. Global gates

```text
G-RDR-0  Baseline integrity
G-RDR-1  Identity integrity
G-RDR-2  Target integrity
G-RDR-3  Provenance integrity
G-RDR-4  Temporal integrity
G-RDR-5  Reconciliation integrity
G-RDR-6  Authority integrity
G-RDR-7  Verification integrity
G-RDR-8  AcceptedState integrity
G-RDR-9  Mutation safety
G-RDR-10 Adversarial integrity
G-RDR-11 Minimality / necessity
G-RDR-12 Architecture decision
```

A failed gate blocks dependent work.

## 7. Fail-closed statuses

```text
ACCEPTED
REJECTED
UNVERIFIED
CONFLICT
UNKNOWN
AMBIGUOUS
STALE
ESCALATE
BLOCKED
```

Only `ACCEPTED` may promote an observation into the relevant AcceptedState, and only after the required verification contract succeeds.

## 8. Research invariants

1. No mutation under unresolved reality.
2. No identity by tool presence alone.
3. No same-object claim without target evidence.
4. No canonicality by connector preference alone.
5. No truth by model consensus.
6. No AcceptedState by execution success.
7. No source authority → ACES authorization escalation.
8. No cross-context continuity claim without explicit binding evidence.
9. Preserve conflicting observations; do not erase them through reconciliation.
10. ACES may accept a state as operationally relied-upon without claiming omniscient truth about the external world.
11. All protocol failures must be observable and replayable.
12. BASTION remains out of scope.

## 9. Relationship to ACES P0 roadmap

This research roadmap is subordinate to the existing ACES realization roadmap and does not replace it.

It operationalizes the P0 Axis-B requirement for:

```text
DWOM + Connector Fabric + Reconciliation Engine
```

while preserving the canonical convergence boundary:

```text
Evidence → Verification → AcceptedState
```

No PR merge, Canon promotion, BASTION integration or runtime production claim is authorized by this document.

## 10. Exit condition

The research is complete only when ACES can answer, with evidence:

```text
WHO observed/acted?
WHAT connector and external system?
WHICH exact object/target?
WHEN?
FROM WHICH state?
UNDER WHICH authority/policy?
WHAT happened?
WHAT evidence proves it?
WHAT conflicts exist?
WHAT was verified?
WHAT was accepted?
WHAT remains unknown?
```

If any required answer is unavailable, the corresponding state remains explicitly unresolved.
