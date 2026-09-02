# ACES OS — Priority Realization Roadmap v2.0

**Status:** FROZEN / CANONICAL REALIZATION ROADMAP  
**Date:** 2026-09-02  
**Supersedes (as control roadmap):** `docs/architecture/ACES-OS-MASTER-ROADMAP-v1.0.md`  
**Does not delete:** Roadmap v1.0 historical lineage  
**Does not implement:** DWOM / Connector Fabric / Reconciliation Engine runtime  
**Does not merge:** PR #4  
**main:** untouched by this fixation

---

## 0. Purpose

This document is the **single canonical realization roadmap** for ACES OS after reconciliation of:

1. Priority Realization Roadmap v1.0 (sequential gate list G0–G11)
2. Frozen P0 decision: **Digital World Model + Connector Fabric + Reconciliation Engine = P0 / IMMEDIATE / PRIORITY #1**
3. Completed execution / authority / epistemic gates (E3.x, Execution Adapter, ASA, Evidence/Verification, Knowledge/Memory/World Model)
4. G2-R1 verification-closure status (**BLOCKED** — environment; not falsely promoted to PASS)
5. PR #4 architectural PASS boundaries (unmerged)

Architecture is not implementation. Implementation is not verification. Verification is not Canon promotion.

---

## 1. Frozen P0 decision (priority baseline)

```text
Digital World Model + Connector Fabric + Reconciliation Engine
= P0 / IMMEDIATE / PRIORITY #1
```

Source of truth for the decision text:

- `spec/ACES-DIGITAL-WORLD-PRIORITY-001.md`
- branch: `feature/digital-world-reconciliation-priority`
- HEAD (PR #4 head): `68389673a7459d674440c7a362645c70bc645526`
- PR #4: open, **unmerged**, architecturally PASS at boundary level

### Four PR #4 boundaries (canonical)

```text
DWOM != Knowledge
Source Authority != ACES Authorization Authority
Reconciliation != Truth Arbitration
Digital World State != World Model State != Semantic Reality
```

These boundaries are binding for all subsequent realization work.

---

## 2. Three foundational axes (not a single flat sequence)

ACES realization is modeled as **three coupled axes**. They are parallel where independent and convergent where epistemic acceptance is required.

### Axis A — Cognitive / Authority / Execution

```text
Constitution
  → Authority / Policy (ASA)
  → Execution Contract
  → Orca
  → DSH (replaceable substrate)
  → Inference Fabric
  → Execution Receipt / Observed Result
```

### Axis B — Digital Reality

```text
Digital World
  → Connector Fabric
  → DWOM (Digital World Object Model)
  → Reconciliation Engine
  → Digital World State
  → Observation / Evidence (digital-world observations)
```

### Axis C — Epistemic Acceptance

```text
Execution observation + Digital-world observation
  → Evidence
  → Verification
  → AcceptedState
  → Knowledge
  → Memory / World Model
  → Semantic Reality
```

### Convergence boundary

```text
Evidence → Verification → AcceptedState
```

is the **explicit convergence boundary** between:

- execution-plane observations (Axis A receipts)
- digital-world observations (Axis B)

No axis may short-circuit this boundary.

### Explicit non-equalities (binding)

```text
Execution success != AcceptedState
DWOM object != KnowledgeObject
Digital World State != Semantic Reality
World Model != Semantic Reality mutator
World Model != Evidence
World Model != Authority
Reconciliation result != Truth
Source authority != ACES authorization authority
DSH capability != ACES Authority
Inference != Evidence
Context != Authority
Capability != Authority
Self-improvement != Self-authorization
```

---

## 3. Reality Layer

**Reality Layer** is an architectural human-facing control principle present from **P0**.

It denotes the obligation that ACES present and control interaction with the Digital World so the human is not permanent middleware.

- Architectural presence: **from P0**
- UI / product-surface realization: **may occur later** (deferred productization)
- Success criterion includes **Human Interaction Cost (HIC)** and **ASPE** (Axiom of Preservation of Psychic Energy)

Reality Layer is not postponed to “Phase 6 integration.”

---

## 4. MCP rule (unchanged)

```text
MCP only when CLA / Connector / Local / Native alternative is unavailable.
```

Native / local / CLA connector paths have priority over MCP.

---

## 5. Human Interaction Cost / ASPE (realization criteria)

Realization is incomplete if connectors merely function.

Mandatory criteria:

1. Measurable reduction of parasitic human work (duplicate entry, manual sync, re-search, context switching, cross-system reconciliation).
2. ASPE: interaction with the digital world must not force unnecessary expenditure of human psychic energy.
3. Fail-safe connector failure with preserved uncertainty.
4. Demand-driven retrieval; no default full-world mirror.

---

## 6. Mandatory first vertical slice (P1)

First mandatory multi-system vertical slice:

```text
Obsidian + GitHub + Slack + Gmail + Google Drive + Kaiten
```

Required demonstration class:

```text
External Representation
  → DWOM Object
  → Observation / Evidence
  → Reconciliation / Candidate State
  → explicit Decision / Verification where required
  → AcceptedState
  → Knowledge only via existing epistemic path
```

Conflicting observations remain traceable. Source precedence is explicit, policy-scoped, and never security/authorization authority.

---

## 7. Mapping: Roadmap v1.0 → Roadmap v2.0

Historical v1.0 gates are **preserved as lineage**, not deleted. Their control meaning is re-homed onto the three-axis model.

| v1.0 Gate | Historical meaning | v2.0 placement | Current status |
|-----------|--------------------|----------------|----------------|
| G0 Canon integrity | Canon reconciliation without retroactive mutation | Continuity / governance hygiene | PASS (historical lineage) |
| G1 E3.1 Durable Context Compiler | Minimal compiler + instrumentation | Axis A support / compiler line | PASS (implementation lineage) |
| G2 E3.2 Replication | Additional workflow replication | Evidence of connector value (limited) | CONDITIONAL PASS |
| G3 E3.3 Interruption / Recovery | Reconstruct after interruption | Axis A + C recoverability | CONDITIONAL PASS |
| G4 E3.4 Bounded Authorized Write | Explicit human-approved bounded write | Axis A authority path | CONDITIONAL PASS (closed for prior approval scope) |
| G5 Execution Adapter / DSH | Runtime-neutral adapter | Axis A Execution Contract → substrate | CONDITIONAL PASS |
| G6 ASA | Authorization authenticity boundary | Axis A Authority / Policy | CONDITIONAL PASS |
| G7 Evidence / Verification | Evidence → Trusted Verifier → AcceptedState | **Axis C convergence kernel** | CONDITIONAL PASS / regression CLOSED on Evidence lineage |
| G8 Knowledge / Memory / World Model | Downstream epistemic layers | Axis C after AcceptedState | Contract FROZEN; G2 minimal implementation CONDITIONAL PASS; **G2-R1 VERIFICATION CLOSURE = BLOCKED** |
| G9 Controlled Self-Evolution | Learning under immutable gates | Deferred post-stability | NOT STARTED |
| G10 MuZero-style research | Learned planning research | Deferred research | DEFERRED |
| G11 E4 Canon Promotion | Promotion only on sufficient evidence | Terminal governance gate | NOT AUTHORIZED |

### Critical truthful blockers (must not be rewritten)

```text
G2-R1 VERIFICATION CLOSURE = BLOCKED
Reason: authenticated exact-SHA local Git worktree unavailable in prior execution environments
NOT converted to PASS
```

```text
PR #4 = architecturally PASS at boundary level; UNMERGED
main = must remain untouched by this roadmap fixation
Canon Promotion = NOT AUTHORIZED
```

---

## 8. Completed / frozen stack (execution lineage preserved)

Frozen / accepted structural lineage (branch evidence; not main merge claims):

| Component | Representative branch / HEAD | Status |
|-----------|------------------------------|--------|
| E3 Experiment 001 | evolution lineage | CONDITIONAL PASS |
| E3.1 Context Compiler | feature/master-control-protocol lineage | PASS |
| E3.2 Replication | same lineage | CONDITIONAL PASS |
| E3.3 Interruption / Recovery | same lineage | CONDITIONAL PASS |
| E3.4 Bounded Authorized Write | same lineage | CONDITIONAL PASS (scope-closed) |
| Execution Adapter | `feature/execution-adapter` @ `5fc7b102…` | CONDITIONAL PASS |
| ASA Hardening | `feature/asa-hardening` @ `55b788ea…` | CONDITIONAL PASS |
| Evidence / Verification Hardening | `feature/evidence-verification-hardening` @ `e70ce9b5…` | CONDITIONAL PASS; regression CLOSED on lineage |
| Knowledge/Memory/WorldModel Contract v0.1 + v0.1a | `feature/knowledge-memory-worldmodel-contract` @ `f0362a21…` | FROZEN |
| Knowledge/Memory/WorldModel minimal impl | `feature/knowledge-memory-worldmodel-minimal` @ `70ae38ef…` | CONDITIONAL PASS |
| G2-R1 live Verification→Knowledge | `feature/g2r1-live-verification-knowledge` @ `62853bcf…` | Implementation present; **VERIFICATION CLOSURE = BLOCKED** |
| Digital World Priority 001 | `feature/digital-world-reconciliation-priority` @ `68389673…` / PR #4 | FROZEN PRIORITY BASELINE; **UNMERGED** |

ACES → Orca → DSH → Inference execution lineage remains preserved as Axis A. DSH remains a **replaceable substrate**, never ACES authority.

---

## 9. Priority Realization Plan v2.0

### P0 — IMMEDIATE (Priority #1) — Digital Reality axis foundation

**AUTHORIZED NEXT architectural work (contracts only until further authorization):**

1. Freeze / refine DWOM object contracts
2. Connector Contract (capability, identity, event, evidence, authority mapping)
3. Identity Mapping
4. Capability Mapping
5. Event Mapping
6. Evidence Mapping (digital-world observations into Axis C Evidence)
7. Authority Mapping (source precedence vs ASA — strict separation)
8. Reconciliation Contract (conflict preserve; no truth arbitration)
9. Human Interaction Cost metrics definition
10. Reality Layer control principles (architectural; UI deferred)

**Explicitly NOT started by this document:**

- runtime DWOM implementation
- production Connector Fabric
- Reconciliation Engine implementation
- MCP as default connector path
- merge of PR #4

### P1 — First vertical slice

Implement and verify the mandatory slice:

```text
Obsidian + GitHub + Slack + Gmail + Google Drive + Kaiten
```

Entry conditions:

- P0 contracts frozen
- Axis C Evidence → Verification → AcceptedState remains the only promotion path into Knowledge
- ASA remains authorization boundary for any write/action
- G2-R1 verification closure should be resolved if Knowledge promotion is claimed from live verification path

### P2 — Research / discovery surfaces

Notion, Browser, Exa / Browser Exa, NotebookLM

### P3 — Execution / infrastructure surfaces

Terminal, Cloud, Databases, APIs, Applications, Remote machines

### Parallel continuity work (does not displace P0)

| Work | Status | Notes |
|------|--------|-------|
| G2-R1 verification closure | BLOCKED | Environmental exact-SHA regression; must remain truthful |
| Knowledge/Memory/World Model hardening | CONDITIONAL | Downstream of AcceptedState; cannot authorize |
| Controlled Self-Evolution | NOT STARTED | After stability; no self-authorization |
| E4 Canon Promotion | NOT AUTHORIZED | Evidence-gated |
| MuZero-style World Model research | DEFERRED | Not Connector Core |

---

## 10. Dependency / coupling rules

1. **Axis B cannot mint Knowledge.** DWOM / Reconciliation produce observations and candidate Digital World State only.
2. **Axis A cannot mint AcceptedState.** Execution receipts become Evidence; verification is required.
3. **Axis C is the only path to Semantic Reality updates** via AcceptedState → Knowledge (and governed Semantic Reality update rules).
4. **World Model** may update beliefs from legitimate accepted epistemic inputs; it **MUST NOT** directly mutate Semantic Reality.
5. **ASA** authorizes actions; connectors execute authorized operations; external source power never becomes ACES authority.
6. **P0 Digital Reality work must not erase** completed Axis A/C structural gates.
7. **Roadmap v1.0** remains historical record; **v2.0 is the sole active control roadmap**.

---

## 11. Status vocabulary (required)

Only these labels are used for gate control:

| Label | Meaning |
|-------|---------|
| FROZEN | Normative text locked; further change needs explicit amendment |
| PASS | Gate evidence sufficient for claimed scope |
| CONDITIONAL PASS | Positive signal; residual limits prevent full claim |
| BLOCKED | Progress stopped by external/environment/authorization barrier |
| NOT STARTED | Authorized only after prior gates; not begun |
| AUTHORIZED NEXT | Explicit next engineering/architecture work |
| DEFERRED | Intentionally postponed; not blocking P0 contracts |
| NOT AUTHORIZED | Explicitly forbidden until conditions change |

---

## 12. Non-claims

This roadmap fixation does **not**:

- implement DWOM, Connector Fabric, or Reconciliation Engine
- merge PR #4
- modify `main`
- convert G2-R1 BLOCKED into PASS
- claim Canon Promotion
- claim universal Connector Generality
- claim production readiness
- claim that Digital World State is Semantic Reality
- claim that Reconciliation arbitrates truth
- authorize MCP as default connector architecture
- authorize Controlled Self-Evolution

---

## 13. Canonical artifact control

| Artifact | Role |
|----------|------|
| `docs/architecture/ACES-OS-PRIORITY-REALIZATION-ROADMAP-v2.0.md` | **Canonical active realization roadmap** |
| `docs/architecture/ACES-OS-MASTER-ROADMAP-v1.0.md` | Historical sequential gate list (superseded as control) |
| `spec/ACES-DIGITAL-WORLD-PRIORITY-001.md` | Frozen P0 Digital World priority decision (PR #4 head) |
| Knowledge/Memory/WorldModel Contract v0.1 + v0.1a | Frozen epistemic layer contract |
| Execution Adapter / ASA / Evidence contracts | Frozen structural contracts on their branches |

Exactly **one** active realization roadmap: **v2.0**.

---

## 14. Proposed next authorized gate

```text
AUTHORIZED NEXT =
P0 Contract Freeze Pack for Axis B:
  DWOM Object Contract
  + Connector Contract
  + Reconciliation Contract
  + Identity / Capability / Event / Evidence / Authority Mapping
  + Human Interaction Cost metric definition
```

**Not authorized by this document:**

- runtime implementation of DWOM / Fabric / Reconciliation
- PR #4 merge
- G3 / Self-Evolution
- Canon Promotion

Optional parallel (does not displace P0):

```text
G2-R1 VERIFICATION CLOSURE retry when authenticated exact-SHA Git worktree is available
```

---

## 15. Final status line

```text
ROADMAP RECONCILIATION = PASS (document fixation)
CANONICAL ROADMAP = v2.0
P0 = Digital World Model + Connector Fabric + Reconciliation Engine
PR #4 = UNMERGED
G2-R1 VERIFICATION CLOSURE = BLOCKED (preserved)
main = UNTOUCHED
IMPLEMENTATION OF DWOM/FABRIC/RECONCILIATION = NOT STARTED
NEXT = P0 Axis B contract freeze pack
```
