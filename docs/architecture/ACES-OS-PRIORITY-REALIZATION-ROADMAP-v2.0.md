# ACES OS — Priority Realization Roadmap v2.0

**Status:** FROZEN / CANONICAL  
**Gate:** ROADMAP RECONCILIATION GATE  
**Date:** 2026-09-02  
**Repository:** `RadislavMuranov/aces-os`  
**Branch:** `architecture/priority-realization-roadmap-v2`  
**Base (main):** `b2f8b4265e13793b89a3fa718d0c707fb2cc816b`  
**Related decision artifact:** `spec/ACES-DIGITAL-WORLD-PRIORITY-001.md` (PR #4 head `68389673a7459d674440c7a362645c70bc645526`, architecturally PASS, **unmerged**)  
**Scope:** Architecture / prioritization only. **No implementation.**  
**main mutation:** FORBIDDEN by this gate.

---

## 0. Purpose and non-claims

This document is the **single canonical realization roadmap** for ACES OS after reconciliation of:

- prior sequential / phase-oriented realization thinking (v1 lineage),
- the frozen P0 decision: **Digital World Model + Connector Fabric + Reconciliation Engine = P0 / IMMEDIATE / PRIORITY #1**,
- completed and in-progress architectural gates,
- the requirement that Execution Plane and Digital World Plane are **parallel, coupled foundational axes**.

### Explicit non-claims

- This document does **not** implement DWOM, Connector Fabric, or Reconciliation Engine.
- This document does **not** merge PR #4.
- This document does **not** alter `main`.
- This document does **not** convert G2-R1 verification-closure from **BLOCKED** to PASS.
- Presence of architecture language is **not** evidence of implemented capability.

---

## 1. Frozen P0 decision (must remain intact)

From `spec/ACES-DIGITAL-WORLD-PRIORITY-001.md` (PR #4):

> **Digital World Model + Connector Fabric + Reconciliation Engine = P0 / IMMEDIATE / PRIORITY #1**

This is a **fundamental architectural axis**, not Phase-6 integration work.

### Four canonical boundaries (PR #4 — non-negotiable)

| Boundary | Meaning |
|----------|---------|
| **DWOM ≠ Knowledge** | DWOM represents external digital-world entities/events/observations. KnowledgeObjects remain ACES epistemic claims promoted only through the governed path. |
| **Source Authority ≠ ACES Authorization Authority** | A source may be authoritative for a scoped external fact; it does not authorize ACES actions or bypass ASA. |
| **Reconciliation ≠ Truth Arbitration** | Reconciliation discovers, correlates, detects conflict, and applies explicit policy; it does not manufacture epistemic truth. |
| **Digital World State ≠ World Model State ≠ Semantic Reality** | Reconciled external projection ≠ belief/projection layer ≠ canonical semantic state. |

### Standing rules retained

- **MCP rule:** MCP only when CLA / Connector / Local / Native alternative is unavailable.
- **Human Interaction Cost / ASPE:** explicit realization criteria; parasitic human middleware work is a failure mode.
- **First mandatory P1 vertical slice:** Obsidian + GitHub + Slack + Gmail + Google Drive + Kaiten.

---

## 2. Three-axis realization model (v2.0 canonical structure)

ACES realization is **not** a single sequential list. It is three coupled axes with an explicit convergence boundary.

### Axis A — Cognitive / Authority / Execution

```text
Constitution
  → Authority / Policy (ASA)
  → Execution Contract
  → Orca
  → DSH (execution substrate)
  → Inference Fabric
  → Execution Receipt / Observed Result
```

**Role:** decide, authorize, execute, produce observations of execution.

**Lineage status:** frozen execution stack preserved (ACES control → Execution Adapter → Orca/DSH → Inference). DSH is substrate, not trust root.

### Axis B — Digital Reality

```text
Digital World (external systems)
  → Connector Fabric
  → DWOM (Digital World Object Model)
  → Reconciliation Engine
  → Digital World State (reconciled / projected)
  → Observation / Evidence candidates
```

**Role:** represent, connect, reconcile, and observe the fragmented Digital World without making the human the middleware.

**Priority:** P0 / IMMEDIATE / PRIORITY #1 for contracts and first vertical slice. Implementation of DWOM / Connector / Reconciliation remains **NOT STARTED** as runtime capability under this gate.

### Axis C — Epistemic Acceptance

```text
Execution observations + Digital-world observations
  → Evidence
  → Verification
  → AcceptedState
  → Knowledge
  → Memory / World Model
  → Semantic Reality
```

**Role:** bind observations to evidence, verify, accept, then govern epistemic layers downstream.

**Rule:** Knowledge / Memory / World Model remain **downstream governed epistemic layers**. They do not authorize execution and do not become Digital World State by fiat.

### Convergence boundary (mandatory)

```text
Axis A (Execution Receipt / Observed Result)
        ↘
          Evidence → Verification → AcceptedState
        ↗
Axis B (Digital Observation / DWOM-derived Observation)
```

**Evidence → Verification → AcceptedState** is the **only** legitimizing gate between:

- execution success, and
- digital-world retrieval/reconciliation success,

and any path toward Knowledge, Memory, World Model, or Semantic Reality updates.

Execution success ≠ AcceptedState.  
Reconciliation result ≠ Truth.  
Digital World State ≠ Semantic Reality.

---

## 3. Reality Layer (architectural from P0)

**Reality Layer** is redefined as an **architectural human-facing control principle** that exists from P0:

> Expose only the minimum cross-world state needed for the human to act (**NOW / IMPORTANT / NEXT**) without becoming the integration layer.

| Aspect | Status |
|--------|--------|
| Architectural principle | **FROZEN from P0** |
| UI / product surface realization | **DEFERRED** (may occur later) |
| Relationship to axes | Projection of Accepted / policy-filtered state from Axis C; must not become a competing workspace |

Reality Layer is **not** postponed until a late product phase. Its UI may be late; its control principle is not.

---

## 4. Mapping: old v1 lineage → v2.0 axes

There was **no single in-repo file** titled “Priority Realization Roadmap v1.0” at reconciliation time. The v1 lineage is reconstructed from:

- `spec/MASTER-PROTOCOL.md` (research → product transition),
- `docs/architecture/ACES-MASTER-CONTROL-PROTOCOL-2026-09-01.md` (E3.x → harness → Knowledge sequence),
- `spec/ACES-DIGITAL-WORLD-PRIORITY-001.md` §13 priority roadmap (P0–P3 connector surfaces),
- Universal Harness H0–H12 decomposition,
- completed gate results on feature/evolution branches.

| v1-style element | v2.0 placement | Notes |
|------------------|----------------|-------|
| Constitution / Schema / System Prompt | Axis A (Constitution) | Retained |
| ASA / Authority / Policy | Axis A | Hardening contracts FROZEN; runtime present on feature branches |
| Execution Adapter / Execution Contract | Axis A | Contract FROZEN; runtime present on feature branches |
| Orca / DSH / Inference Fabric | Axis A | DSH = substrate; mapping research retained |
| E3.1–E3.4 Context / replication / recovery / bounded write | Axis A + support for continuity | Results recorded; some blockers preserved |
| Evidence / Verification / AcceptedState | **Axis C convergence** | Contracts FROZEN; runtime on feature branches |
| Knowledge / Memory / World Model | Axis C downstream | Contract FROZEN (v0.1 + v0.1a); implementation DEFERRED / G2-R1 BLOCKED |
| Connector / Digital World as late “integration” (old Phase-6 style) | **Elevated to Axis B = P0** | Primary reconciliation change |
| DWOM + Connector Fabric + Reconciliation | Axis B P0 | Decision FROZEN; runtime NOT STARTED |
| P1 vertical slice (Obsidian, GitHub, Slack, Gmail, Drive, Kaiten) | Axis B first verification slice | Unchanged |
| Reality Layer as late UI | **Architectural from P0**; UI DEFERRED | Principle elevated |
| Controlled Self-Evolution | Downstream of gates; governed | Not autonomous authority |
| Universal Harness H0–H12 | Decomposition retained; not 12 independent projects | H6/H7 map to Axis B; H10/H11 to Axis C; H12 to Axis A |

**Historical lineage is preserved.** Completed gate **results** are not rewritten. Proposed architecture is not silently promoted to implemented capability.

---

## 5. Status matrix (truthful at reconciliation)

Canonical status vocabulary:

`FROZEN` · `PASS` · `CONDITIONAL PASS` · `BLOCKED` · `NOT STARTED` · `AUTHORIZED NEXT` · `DEFERRED`

| Item | Status | Evidence / location |
|------|--------|---------------------|
| MASTER PROTOCOL (research governance) | FROZEN / ACTIVE | `spec/MASTER-PROTOCOL.md` |
| Digital World Priority Decision | **FROZEN** (P0 #1) | `spec/ACES-DIGITAL-WORLD-PRIORITY-001.md` on PR #4 branch |
| PR #4 (Digital World priority) | Architecturally **PASS**, **unmerged** | Open PR #4; head `68389673…` |
| Four PR #4 boundaries | **FROZEN** | §1 of this roadmap + PR #4 artifact |
| ASA Hardening Contract | FROZEN | feature branches / docs |
| Execution Adapter Contract | FROZEN | feature branches / docs |
| Evidence / Verification Hardening Contract | FROZEN | feature branches / docs |
| Knowledge / Memory / World Model Contract v0.1 + v0.1a | FROZEN (contract only) | `docs/architecture/KNOWLEDGE-MEMORY-WORLDMODEL-CONTRACT-v0.1.md` |
| Knowledge / Memory / World Model **implementation** | **NOT STARTED** as authorized production path; experimental G2-R1 **BLOCKED** | G2-R1 branch `feature/g2r1-live-verification-knowledge` @ `62853bcf…`; verification-closure **must remain BLOCKED** |
| DWOM runtime | **NOT STARTED** | — |
| Connector Fabric runtime | **NOT STARTED** | — |
| Reconciliation Engine runtime | **NOT STARTED** | — |
| Reality Layer (principle) | **FROZEN from P0** | This roadmap + MASTER PROTOCOL Reality Layer rule |
| Reality Layer (UI) | **DEFERRED** | — |
| P1 vertical slice (6 systems) | **NOT STARTED** (authorized after P0 contracts) | PR #4 §13 |
| Controlled Self-Evolution | **DEFERRED** (governed path only) | Master Control Protocol |
| Canon Promotion | **NOT AUTHORIZED** | Master Control Protocol |
| Production readiness | **BLOCKED** | Multiple gates incomplete |
| `main` | **UNTOUCHED** by this gate | `b2f8b426…` at branch creation |

### G2-R1 preservation rule

**G2-R1 verification-closure remains BLOCKED.**  
This roadmap must **not** be read as converting G2-R1 to PASS. Any Knowledge/Memory/World Model runtime claims remain subject to that blocker.

---

## 6. Dependency and coupling rules

1. **Axis A does not wait for Axis B to exist in full** — execution authority and receipts remain valid for already-authorized substrates.
2. **Axis B does not grant Axis A authority** — connectors are untrusted external systems.
3. **Neither Axis A success nor Axis B reconciliation creates Knowledge** without Axis C (Evidence → Verification → AcceptedState).
4. **Axis C cannot invent Digital World observations** — it consumes bound evidence from A and/or B.
5. **World Model updates** may follow accepted epistemic inputs but **must not** mutate Semantic Reality directly (contract v0.1a).
6. **P0 contract work for Axis B** (DWOM object contracts, Connector Contract, Identity/Capability/Event/Evidence/Authority Mapping, Reconciliation Contract, Human Interaction Cost metrics) is **AUTHORIZED NEXT** relative to pure secondary feature expansion.
7. **P1 vertical slice** is the first mandatory multi-system verification of Axis B coupled through Axis C; it does not authorize Canon Promotion.

---

## 7. Priority realization sequence (non-flat)

### Band 0 — Frozen foundations (preserve)

- Constitution / Schema / System Prompt lineage
- ASA deny-first authority
- Execution Contract + Adapter boundary
- Evidence / Verification / AcceptedState rules
- Knowledge/Memory/WM **contract** boundaries
- Digital World Priority Decision + four boundaries
- Reality Layer principle

### Band 1 — P0 immediate (Axis B contracts + metrics)

Authorized architectural work (still **no** silent runtime promotion):

- DWOM canonical object contracts
- Connector Contract
- Identity / Capability / Event / Evidence / Authority mapping
- Reconciliation Contract
- Human Interaction Cost metrics
- Explicit preservation of competing observations under conflict

### Band 2 — P1 first vertical slice (Axis B × Axis C)

Systems: **Obsidian + GitHub + Slack + Gmail + Google Drive + Kaiten**

Must demonstrate one logical ACES object path:

```text
External Representation
  → DWOM Object
  → Observation / Evidence
  → Reconciliation / Candidate Digital World State
  → explicit Decision / Verification where required
  → AcceptedState
  → Knowledge promotion only via existing epistemic path
```

### Band 3 — Extended surfaces (from PR #4)

- **P2:** Notion, Browser, Exa / Browser Exa, NotebookLM
- **P3:** Terminal, Cloud, Databases, APIs, Applications, Remote machines

### Band 4 — Downstream epistemic runtime (after contracts + blockers cleared)

- Knowledge / Memory / World Model **implementation** only after G2-R1-class blockers are honestly resolved
- Controlled Self-Evolution only under constitutional gates
- Canon Promotion only via explicit E4-class gate

---

## 8. Controlled Self-Evolution (placement)

```text
Experience → Evaluation → Candidate Change → Constitutional Gate → Promotion
```

Self-improvement ≠ self-authorization.  
Learning cannot grant ASA authority or bypass Evidence → Verification → AcceptedState.

Status: **DEFERRED** relative to P0/P1 Digital World realization and unresolved verification blockers.

---

## 9. Reconciliation summary (this gate)

| Required outcome | Satisfied |
|------------------|-----------|
| Exactly one canonical realization roadmap | YES — this document v2.0 |
| No competing v1/v2 ambiguity as living plan | YES — v1 lineage mapped; v2.0 is sole canonical plan |
| Execution Plane first-class (Axis A) | YES |
| Digital World Plane first-class (Axis B) | YES |
| Evidence / Verification / AcceptedState as convergence | YES |
| Reality Layer architectural from P0 | YES |
| Historical gates preserved | YES |
| G2-R1 remains BLOCKED | YES |
| PR #4 not merged | YES |
| No DWOM/Connector/Reconciliation implementation in this gate | YES |
| main not mutated | YES |

---

## 10. Remaining architectural ambiguity (explicit)

1. **Runtime completeness on `main`:** Many PASS/FROZEN contracts and packages live on feature branches; `main` remains minimal. Promotion to `main` requires separate gates.
2. **G2-R1 / Knowledge runtime:** Experimental materialization paths exist on feature branches; verification-closure is **BLOCKED**. Do not treat as available capability.
3. **Orca naming vs Execution Adapter:** Axis A preserves the frozen control → adapter → substrate lineage; exact production naming of “Orca” vs adapter modules remains a documentation alignment item, not a blocker for this roadmap structure.
4. **Connector generality:** Experimental signals (e.g. E-series) do not prove generality; P1 slice is required before broader claims.
5. **UI for Reality Layer:** Principle frozen; concrete surface design is open.

---

## 11. Acceptance of ROADMAP RECONCILIATION GATE

**PASS** if and only if the conditions in §9 hold.  
This document is the acceptance artifact for the gate.

**Authorized next gate (proposed):**  
**P0 Axis-B Contract Freeze Gate** — produce/freeze DWOM object contract, Connector Contract, and Reconciliation Contract as architecture-only artifacts (still no runtime implementation; still no merge of PR #4 unless separately authorized).

---

## 12. Document control

| Field | Value |
|-------|--------|
| Canonical path | `docs/architecture/ACES-OS-PRIORITY-REALIZATION-ROADMAP-v2.0.md` |
| Version | v2.0 |
| Supersedes as living plan | Informal v1 sequential/phase interpretation of realization priority |
| Does not delete | Historical ledger, gate results, PR #4 decision text |
| Implementation authorized by this file alone | **NO** |

**END OF PRIORITY REALIZATION ROADMAP v2.0**
