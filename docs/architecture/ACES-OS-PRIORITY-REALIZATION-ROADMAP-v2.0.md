# ACES OS — Priority Realization Roadmap v2.0

**Status:** FROZEN / CANONICAL REALIZATION ROADMAP  
**Gate:** ROADMAP RECONCILIATION GATE  
**Date:** 2026-09-03  
**Repository:** `RadislavMuranov/aces-os`  
**Canonical branch (this fixation):** `architecture/roadmap-reconciliation-gate`  
**Base (main):** `b2f8b4265e13793b89a3fa718d0c707fb2cc816b`  
**Related P0 decision:** `spec/ACES-DIGITAL-WORLD-PRIORITY-001.md` (PR #4 head `68389673a7459d674440c7a362645c70bc645526`)  
**Scope:** Architecture / prioritization only. **No implementation.**  
**main mutation:** FORBIDDEN  
**PR #4 merge:** NOT performed by this gate

### Canonical control

This file is the **sole active realization roadmap**.  
Prior draft copies on `architecture/priority-realization-roadmap-v2` and `docs/priority-realization-roadmap-v2` are **superseded as living plan** by this fixation (historical commits retained; not deleted).

---

## 0. Purpose and non-claims

This document reconciles:

1. Priority Realization Roadmap v1.0 lineage (sequential gates / phase thinking)
2. Frozen P0 decision: **Digital World Model + Connector Fabric + Reconciliation Engine = P0 / IMMEDIATE / PRIORITY #1**
3. Completed execution / authority / epistemic gates
4. G2-R1 verification-closure (**BLOCKED** — must not be converted to PASS)
5. PR #4 architectural PASS boundaries (**unmerged**)

Architecture ≠ implementation ≠ verification ≠ Canon promotion.

### Explicit non-claims

- Does **not** implement DWOM, Connector Fabric, or Reconciliation Engine
- Does **not** merge PR #4
- Does **not** alter `main`
- Does **not** convert G2-R1 BLOCKED → PASS
- Does **not** authorize Canon Promotion or Controlled Self-Evolution
- Does **not** claim production readiness

---

## 1. Frozen P0 decision (priority baseline)

```text
Digital World Model + Connector Fabric + Reconciliation Engine
= P0 / IMMEDIATE / PRIORITY #1
```

This is a **fundamental architectural axis**, not Phase-6 integration work.

Source: `spec/ACES-DIGITAL-WORLD-PRIORITY-001.md` on branch `feature/digital-world-reconciliation-priority` @ `68389673…` / **PR #4 open, unmerged**.

### Four PR #4 boundaries (canonical, non-negotiable)

```text
DWOM != Knowledge
Source Authority != ACES Authorization Authority
Reconciliation != Truth Arbitration
Digital World State != World Model State != Semantic Reality
```

### Standing rules retained

- **MCP:** only when CLA / Connector / Local / Native alternative is unavailable
- **Human Interaction Cost / ASPE:** explicit realization criteria
- **First mandatory P1 vertical slice:** Obsidian + GitHub + Slack + Gmail + Google Drive + Kaiten

---

## 2. Three foundational axes (not a flat sequence)

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

**Lineage:** ACES → Orca → DSH → Inference **preserved**. DSH is substrate, never ACES authority.

### Axis B — Digital Reality

```text
Digital World
  → Connector Fabric
  → DWOM (Digital World Object Model)
  → Reconciliation Engine
  → Digital World State
  → Observation / Evidence (digital-world observations)
```

**Priority:** P0 / IMMEDIATE. Runtime implementation **NOT STARTED** under this gate.

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

Knowledge / Memory / World Model = **downstream governed epistemic layers**, not authorities.

### Canonical architecture summary

```text
ACES CONSTITUTION
        │
        ▼
AUTHORITY / POLICY
        │
   ┌────┴────┐
   │         │
   ▼         ▼
EXECUTION   DIGITAL WORLD
PLANE       PLANE
   │         │
Execution   DWOM
Contract    │
   │       Connector Fabric
Orca        │
   │       Reconciliation
DSH         │
   │       Observations
Inference   │
   └────┬────┘
        ▼
     EVIDENCE
        │
   VERIFICATION
        │
   ACCEPTEDSTATE
        │
 Knowledge / Memory / World Model
        │
   SEMANTIC REALITY
        │
   REALITY LAYER  (architectural from P0; UI may be later)
        │
      HUMAN
```

### Convergence boundary (mandatory)

```text
Evidence → Verification → AcceptedState
```

is the **only** legitimizing convergence of Axis A receipts and Axis B observations. No axis may short-circuit this boundary.

### Binding non-equalities

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

**Architectural human-facing control principle from P0.**  
Obligation: present/control interaction with the Digital World so the human is not permanent middleware.

| Aspect | Status |
|--------|--------|
| Architectural principle | **FROZEN from P0** |
| UI / product surface | **DEFERRED** |

Not postponed to “Phase 6 integration.”

---

## 4. Mapping: Roadmap v1.0 lineage → v2.0

Historical gates are **preserved as lineage**, not deleted. No single in-repo file titled “Priority Realization Roadmap v1.0” was present on `main` at fixation; v1 is reconstructed from Master Protocol, E3.x sequences, and PR #4 §13.

| v1.0 Gate | Historical meaning | v2.0 placement | Current status |
|-----------|--------------------|----------------|----------------|
| G0 Canon integrity | Canon reconciliation without retroactive mutation | Continuity / governance hygiene | PASS (historical lineage) |
| G1 E3.1 Durable Context Compiler | Minimal compiler + instrumentation | Axis A support | PASS (implementation lineage) |
| G2 E3.2 Replication | Workflow replication | Limited connector-value signal | CONDITIONAL PASS |
| G3 E3.3 Interruption / Recovery | Reconstruct after interruption | Axis A + C recoverability | CONDITIONAL PASS |
| G4 E3.4 Bounded Authorized Write | Human-approved bounded write | Axis A authority path | CONDITIONAL PASS (scope-closed) |
| G5 Execution Adapter / DSH | Runtime-neutral adapter | Axis A Execution Contract → substrate | CONDITIONAL PASS |
| G6 ASA | Authorization authenticity | Axis A Authority / Policy | CONDITIONAL PASS |
| G7 Evidence / Verification | Evidence → Verifier → AcceptedState | **Axis C convergence kernel** | CONDITIONAL PASS |
| G8 Knowledge / Memory / World Model | Downstream epistemic layers | Axis C after AcceptedState | Contract FROZEN; **G2-R1 VERIFICATION CLOSURE = BLOCKED** |
| G9 Controlled Self-Evolution | Learning under immutable gates | Deferred post-stability | NOT STARTED |
| G10 MuZero-style research | Learned planning research | Deferred research | DEFERRED |
| G11 E4 Canon Promotion | Promotion only on sufficient evidence | Terminal governance gate | NOT AUTHORIZED |
| Late “integration / Phase 6 connectors” | Peripheral connectors | **Elevated to Axis B = P0** | Primary reconciliation change |

### Critical truthful blockers (must not be rewritten)

```text
G2-R1 VERIFICATION CLOSURE = BLOCKED
Reason: authenticated exact-SHA local Git worktree unavailable in prior execution environments
NOT converted to PASS
```

```text
PR #4 = architecturally PASS at boundary level; UNMERGED
main = untouched by this roadmap fixation
Canon Promotion = NOT AUTHORIZED
```

---

## 5. Completed / frozen stack (execution lineage preserved)

| Component | Representative branch / HEAD | Status |
|-----------|------------------------------|--------|
| Execution Adapter | `feature/execution-adapter` @ `5fc7b102…` | CONDITIONAL PASS |
| ASA Hardening | `feature/asa-hardening` @ `55b788ea…` | CONDITIONAL PASS |
| Evidence / Verification Hardening | `feature/evidence-verification-hardening` @ `e70ce9b5…` | CONDITIONAL PASS |
| Knowledge/Memory/WorldModel Contract | `feature/knowledge-memory-worldmodel-contract` @ `f0362a21…` | FROZEN |
| Knowledge/Memory/WorldModel minimal | `feature/knowledge-memory-worldmodel-minimal` @ `70ae38ef…` | CONDITIONAL PASS |
| G2-R1 live Verification→Knowledge | `feature/g2r1-live-verification-knowledge` @ `62853bcf…` | **VERIFICATION CLOSURE = BLOCKED** |
| Digital World Priority 001 | `feature/digital-world-reconciliation-priority` @ `68389673…` / PR #4 | FROZEN PRIORITY BASELINE; **UNMERGED** |

---

## 6. Priority Realization Plan v2.0

### P0 — IMMEDIATE (Priority #1) — Axis B foundation

**AUTHORIZED NEXT (contracts only until further authorization):**

1. DWOM object contracts  
2. Connector Contract  
3. Identity Mapping  
4. Capability Mapping  
5. Event Mapping  
6. Evidence Mapping (digital observations → Axis C Evidence)  
7. Authority Mapping (source precedence vs ASA — strict separation)  
8. Reconciliation Contract (conflict preserve; no truth arbitration)  
9. Human Interaction Cost metrics  
10. Reality Layer control principles (architectural; UI deferred)

**NOT started by this document:** runtime DWOM / Fabric / Reconciliation; MCP-as-default; PR #4 merge.

### P1 — First vertical slice

```text
Obsidian + GitHub + Slack + Gmail + Google Drive + Kaiten
```

Path class:

```text
External Representation → DWOM Object → Observation / Evidence
  → Reconciliation / Candidate State → Decision / Verification where required
  → AcceptedState → Knowledge only via existing epistemic path
```

### P2 — Research / discovery surfaces

Notion, Browser, Exa / Browser Exa, NotebookLM

### P3 — Execution / infrastructure surfaces

Terminal, Cloud, Databases, APIs, Applications, Remote machines

### Parallel continuity (does not displace P0)

| Work | Status |
|------|--------|
| G2-R1 verification closure | **BLOCKED** |
| Knowledge/Memory/World Model hardening | CONDITIONAL |
| Controlled Self-Evolution | NOT STARTED |
| E4 Canon Promotion | NOT AUTHORIZED |
| MuZero-style research | DEFERRED |

---

## 7. Dependency / coupling rules

1. Axis B cannot mint Knowledge.  
2. Axis A cannot mint AcceptedState.  
3. Axis C is the only path to Semantic Reality updates via AcceptedState → Knowledge.  
4. World Model must not directly mutate Semantic Reality.  
5. ASA authorizes actions; connectors execute; external source power ≠ ACES authority.  
6. P0 Digital Reality work must not erase completed Axis A/C structural gates.  
7. **v2.0 is the sole active control roadmap**; v1 remains historical record.

---

## 8. Status vocabulary

| Label | Meaning |
|-------|---------|
| FROZEN | Normative text locked |
| PASS | Evidence sufficient for claimed scope |
| CONDITIONAL PASS | Positive signal; residual limits |
| BLOCKED | Stopped by external/environment/authorization barrier |
| NOT STARTED | Not begun |
| AUTHORIZED NEXT | Explicit next work |
| DEFERRED | Intentionally postponed |
| NOT AUTHORIZED | Forbidden until conditions change |

---

## 9. Status matrix (this gate)

| Item | Status |
|------|--------|
| Priority Realization Roadmap v2.0 | **FROZEN / CANONICAL** |
| Digital World Priority Decision | **FROZEN** |
| PR #4 | Architecturally **PASS**, **UNMERGED** |
| Four PR #4 boundaries | **FROZEN** |
| Axis A execution lineage | **PRESERVED** |
| Axis B runtime (DWOM/Fabric/Reconciliation) | **NOT STARTED** |
| Axis C Evidence/Verification contracts | **FROZEN** (lineage) |
| G2-R1 verification closure | **BLOCKED** |
| Reality Layer principle | **FROZEN from P0** |
| Reality Layer UI | **DEFERRED** |
| P1 vertical slice | **NOT STARTED** |
| Controlled Self-Evolution | **NOT STARTED** / DEFERRED |
| Canon Promotion | **NOT AUTHORIZED** |
| `main` | **UNTOUCHED** |

---

## 10. Acceptance of ROADMAP RECONCILIATION GATE

| Criterion | Result |
|-----------|--------|
| Exactly one canonical realization roadmap | **YES** — this file |
| No competing v1/v2 living-plan ambiguity | **YES** — v2.0 sole control; drafts superseded |
| Execution Plane first-class | **YES** |
| Digital World Plane first-class | **YES** |
| Evidence / Verification / AcceptedState = convergence | **YES** |
| Reality Layer architectural from P0 | **YES** |
| Historical gates preserved | **YES** |
| G2-R1 remains BLOCKED | **YES** |
| PR #4 not merged | **YES** |
| No DWOM/Fabric/Reconciliation implementation | **YES** |
| main not mutated | **YES** |

**Gate result: PASS**

---

## 11. Remaining architectural ambiguity

1. Many FROZEN/PASS artifacts live on feature branches; `main` remains minimal — promotion requires separate gates.  
2. G2-R1 / Knowledge runtime: experimental material on feature branches; verification-closure **BLOCKED**.  
3. Orca naming vs Execution Adapter module naming — documentation alignment, not structural blocker.  
4. Connector generality unproven until P1 slice.  
5. Reality Layer UI design open.

---

## 12. Proposed next authorized gate

```text
AUTHORIZED NEXT =
P0 Axis-B Contract Freeze Pack:
  DWOM Object Contract
  + Connector Contract
  + Reconciliation Contract
  + Identity / Capability / Event / Evidence / Authority Mapping
  + Human Interaction Cost metric definition
```

**Not authorized:** runtime implementation; PR #4 merge; Self-Evolution; Canon Promotion.

Optional parallel: G2-R1 VERIFICATION CLOSURE retry when authenticated exact-SHA Git worktree is available.

---

## 13. Final status line

```text
ROADMAP RECONCILIATION = PASS
CANONICAL ROADMAP = v2.0
P0 = Digital World Model + Connector Fabric + Reconciliation Engine
PR #4 = UNMERGED
G2-R1 VERIFICATION CLOSURE = BLOCKED (preserved)
main = UNTOUCHED
IMPLEMENTATION OF DWOM/FABRIC/RECONCILIATION = NOT STARTED
NEXT = P0 Axis B contract freeze pack
```

**END OF PRIORITY REALIZATION ROADMAP v2.0**
