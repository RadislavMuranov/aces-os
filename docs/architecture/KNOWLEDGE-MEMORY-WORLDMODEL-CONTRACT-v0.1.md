# Knowledge / Memory / World Model — Contract v0.1

**Version:** v0.1  
**Status:** FROZEN  
**Gate:** CONTRACT ONLY  
**Date:** 2026-09-01  
**Repository:** `RadislavMuranov/aces-os`  
**Branch:** `feature/knowledge-memory-worldmodel-contract`  
**Base HEAD:** `e70ce9b59964254f216d2f55619846ba1a7b2cf0`  
**main (must remain untouched):** `58a5e596d9fc469561b32d457cf80658667055c2`

---

## A. Scope and status

### A.1 Purpose

This document freezes the **canonical epistemic boundary** for Knowledge, Memory, and World Model in ACES OS.

It defines objects, transitions, authority limits, failure semantics, and invariants.

It does **not** authorize implementation.

### A.2 Gate classification

| Item | Value |
|------|--------|
| Gate type | Contract freeze only |
| Implementation | **DEFERRED** to a subsequent authorized gate |
| Runtime modules | **FORBIDDEN** in this gate |
| Tests of new layers | **FORBIDDEN** in this gate |
| Database / vector / API | **FORBIDDEN** in this gate |
| ASA / Adapter / Evidence code changes | **FORBIDDEN** |
| `main` mutation | **FORBIDDEN** |

### A.3 Dependencies (must remain intact)

| Dependency | Artifact / status |
|------------|-------------------|
| ASA (authorization) | `docs/architecture/ASA-HARDENING-CONTRACT-v0.1.md` + `src/asa/` |
| Execution Adapter | `docs/architecture/EXECUTION-ADAPTER-CONTRACT-v0.1.md` + `src/aces_execution_adapter/` |
| Evidence / Verification | `docs/architecture/EVIDENCE-VERIFICATION-HARDENING-CONTRACT-v0.1.md` + `src/aces_evidence/` |
| AcceptedState | Post-verification gate only (Execution Adapter + VerificationService) |
| Context Compiler | `src/aces_context_compiler/` (EpistemicStatus, ProvenanceRecord) |
| Master Control Protocol | `docs/architecture/ACES-MASTER-CONTROL-PROTOCOL-2026-09-01.md` |
| Master Protocol | `spec/MASTER-PROTOCOL.md` |
| ASA resource kinds | `ResourceKind` includes `KnowledgeObject`, `EvidenceObject`, `MemoryObject` as **labels only** |

### A.4 Relationship to ACE Knowledge Standard

**Repository finding at base HEAD:** no file named or titled “ACE Knowledge Standard v1.2-RC3” is present under `e70ce9b59964254f216d2f55619846ba1a7b2cf0`.

Therefore this contract treats the following vocabulary as **CONTRACT TARGETS** aligned with the stated ACE Knowledge Standard lineage (Fact / Decision / Artifact / Hypothesis / Policy; truth levels Working / Operational / Canonical), without asserting that the standard document itself is an in-repo artifact at this SHA.

If a future gate imports the full ACE Knowledge Standard text, it MUST NOT silently redefine the frozen boundaries of this contract. Conflicts require an explicit amendment gate.

### A.5 Governing directional chain

```text
Semantic Reality
  → Intent
  → Decision
  → Authorized Execution (ASA → Execution Adapter → Runtime)
  → Observed Result
  → Evidence
  → Verification
  → AcceptedState
  → Knowledge / Memory / World Model
  → Updated Semantic Reality
```

No reverse path may grant authority, manufacture evidence, or bypass verification.

---

## B. Canonical epistemic objects

Objects below are **semantic definitions**. Implementation is deferred.

### B.1 RealityState

| Aspect | Definition |
|--------|------------|
| Meaning | The ACES-maintained claim about the state of Semantic Reality after acceptance |
| Owns | Coordinated semantic state representation |
| Does not own | Authorization; execution; raw observations |
| Source of updates | Only through the epistemic chain ending in AcceptedState → Knowledge/Memory/WM → projection |
| Status | **CONTRACT TARGET** (no dedicated type in `src/` at base HEAD) |

### B.2 EvidenceObject

| Aspect | Definition |
|--------|------------|
| Meaning | Bound observation of an execution/result context |
| Runtime at HEAD | Implemented as `Evidence` in `src/aces_evidence/` (class name `Evidence`; ASA `ResourceKind.EvidenceObject` is a label) |
| Owns | Observation payload + fingerprint + provenance binding fields |
| Does not own | Authority; Knowledge promotion; AcceptedState alone |
| Rule | Evidence ≠ Knowledge |

### B.3 AcceptedState

| Aspect | Definition |
|--------|------------|
| Meaning | Epistemic acceptance gate after trusted verification of bound Evidence |
| Runtime at HEAD | `AcceptedStateStatus` on `ExecutionResult`; established only via VerificationService path |
| Owns | Signal that verification criteria for a specific execution binding were satisfied |
| Does not own | Capability issuance; automatic Fact creation; authorization |
| Rules | AcceptedState ≠ Authorization; AcceptedState ≠ automatically-created Fact; Execution success ≠ AcceptedState |

### B.4 KnowledgeObject

| Aspect | Definition |
|--------|------------|
| Meaning | Durable epistemic claim ACES is permitted to maintain |
| Runtime at HEAD | **Absent** as domain module; only `ResourceKind.KnowledgeObject` enum |
| Owns | Claim identity, type, truth level, verification state, evidence refs, provenance |
| Does not own | Authority; capability; execution permission |
| Rule | Knowledge ≠ Authority; Knowledge ≠ Evidence |

**Object types (CONTRACT TARGET, ACE-aligned):**

| Type | Role |
|------|------|
| Fact | Claim treated as established under its truth level |
| Decision | Record of a decision (human or system); not automatic Fact |
| Artifact | Reference to a durable work product / object |
| Hypothesis | Proposed or provisional claim; must not be treated as Fact |
| Policy | Normative rule under Authority; not a Fact |

**Truth levels (CONTRACT TARGET):**

| Level | Meaning |
|-------|---------|
| Working | Provisional / local / experimental claim |
| Operational | Stable enough for operational use under stated scope |
| Canonical | Highest in-scope epistemic status; still not authority |

Promotion between truth levels is a governance concern. Quantitative thresholds are **deferred** unless already frozen elsewhere.

### B.5 MemoryObject

| Aspect | Definition |
|--------|------------|
| Meaning | Durable recall/consolidation record |
| Runtime at HEAD | **Absent** as ACES Memory layer; `src/asa/memory_stores.py` is **authorization store**, not Memory |
| Owns | Historical/record material with provenance |
| Does not own | Truth; verification; authority |
| Rules | Memory ≠ Truth; Memory ≠ Evidence; Memory ≠ Authority |

### B.6 WorldModelState

| Aspect | Definition |
|--------|------------|
| Meaning | Aggregate model of believed/probable state |
| Runtime at HEAD | **Absent** |
| Owns | Belief aggregates / estimates |
| Does not own | Reality; Evidence; Authority; Knowledge self-promotion |
| Rules | World Model ≠ Reality; World Model ≠ Evidence; World Model ≠ Authority |

### B.7 BeliefState

| Aspect | Definition |
|--------|------------|
| Meaning | Minimal representation of belief about a claim or parameter |
| Compatible form | Beta(α, β) parameters for binary outcomes (**specification only; not implemented**) |
| Owns | Confidence parameters |
| Does not own | Truth; Evidence; Authority |
| Rules | Confidence ≠ Truth; Belief ≠ Fact |

ERM, KCE, Epistemic Health, and related advanced metrics are **DEFERRED** (see §14).

### B.8 Provenance

| Aspect | Definition |
|--------|------------|
| Meaning | Reconstructable causal trace of origin and transformation |
| Runtime at HEAD | Partial: Context Compiler `ProvenanceRecord`; Evidence provenance dict; ASA `AuthorizationEvent` |
| Requirement | Logical provenance MUST survive Evidence → Verification → AcceptedState → Knowledge → Memory → World Model |
| Cryptographic authenticity | **DEFERRED** (not required by this contract) |

Minimum logical fields for epistemic transitions:

- source / reference
- originating task or execution id (when applicable)
- evidence reference
- verification reference
- AcceptedState reference (when promotion depends on it)
- timestamp / version
- transformation actor or mechanism id

---

## C. Hard epistemic boundaries

The following distinctions are **normative** and non-bypassable:

```text
Evidence ≠ Knowledge
Knowledge ≠ Evidence
Memory ≠ Truth
Memory ≠ Evidence
World Model ≠ Reality
World Model ≠ Evidence
Confidence ≠ Truth
Inference ≠ Evidence
AcceptedState ≠ Authorization
AcceptedState ≠ automatically-created Fact
Knowledge ≠ Authority
Memory ≠ Authority
World Model ≠ Authority
Agent ≠ Authority
Runtime ≠ Authority
Context ≠ Authority
Capability ≠ Authority
Self-improvement ≠ Self-authorization
```

No layer may treat possession of Context, Capability, Memory, Evidence, Confidence, or Inference as authority.

---

## D. Canonical epistemic flow

### D.1 Allowed direction

```text
DIGITAL WORLD
      ↓
Observed Result
      ↓
Evidence
      ↓
Verification
      ↓
AcceptedState
      ↓
Knowledge Update
      ↓
Memory / Consolidation
      ↓
World Model Update
      ↓
Updated Semantic Reality
```

### D.2 Forbidden reverse / shortcut transitions

| Forbidden transition | Rationale |
|----------------------|-----------|
| Memory → Truth | Memory stores records, not truth |
| Memory → Verification | Recall is not verification |
| World Model → Evidence | Belief cannot manufacture evidence |
| World Model → Authorization | Belief is not authority |
| Inference → Evidence | Inference must remain labeled |
| Confidence → Fact | Confidence is not truth |
| Recall → Verification | History is not verification |
| Agent proposal → Knowledge write (without authorized update path) | Silent agent writes forbidden |
| Execution success → Knowledge acceptance (without Evidence + Verification) | Success ≠ AcceptedState ≠ Fact |
| Knowledge → Authorization | Knowledge is not ASA |
| AcceptedState → Capability issuance | AcceptedState is epistemic, not capability |

---

## E. AcceptedState → Knowledge promotion

### E.1 Normative rules

1. Successful execution alone **MUST NOT** create Knowledge.
2. Evidence **MUST** be bound to the relevant execution/task/resource context (existing Evidence/Verification contract).
3. Evidence **MUST** pass the existing trusted-verifier verification boundary.
4. Only an **AcceptedState** (ESTABLISHED for the bound result) may serve as the epistemic **prerequisite** for promotion.
5. AcceptedState **MUST NOT** itself become Knowledge automatically.
6. Promotion **MUST** occur through an explicit **Knowledge Update** transition/service (implementation deferred).
7. Provenance **MUST** survive the transition (evidence ref, verification ref, AcceptedState ref, timestamps).

### E.2 Deferred promotion governance

- Quantitative thresholds for Working → Operational → Canonical
- Human principal requirements for Canonical promotion
- Multi-evidence aggregation policies

These require a future governance/evaluation gate. Absence of thresholds **MUST NOT** be interpreted as free automatic promotion.

---

## F. Knowledge semantics

### F.1 Identity and lifecycle

| Field / concern | Contract requirement |
|-----------------|----------------------|
| Identity | Stable `knowledge_id` (format deferred) |
| Object type | One of: Fact, Decision, Artifact, Hypothesis, Policy |
| Truth level | Working \| Operational \| Canonical |
| Verification state | Compatible with existing verification vocabulary; must not invent a second authority |
| Provenance | Required; reconstructable |
| Evidence references | Required for claims promoted from AcceptedState path |
| Lifecycle | Create / revise / supersede / recover; no silent history erase |
| Supersession | New version references prior; prior remains reconstructable |
| Recovery | Historical versions must be recoverable under policy |

### F.2 Working vs Operational vs Canonical

| Level | Use |
|-------|-----|
| Working | Local/experimental; default for new provisional claims |
| Operational | Scoped operational use; still not authority |
| Canonical | Highest in-scope claim status; still not authority; still not automatic Canon Promotion of ACES itself |

**Knowledge represents claims ACES may maintain epistemically. It is not an authorization source.**

---

## G. Memory semantics

Memory is a **durable recall and consolidation** layer.

### G.1 Normative rules

1. Memory stores **records**, not truth.
2. Memory does **not** independently establish verification.
3. Memory **cannot** authorize actions.
4. Recalled Memory is **not** automatically Evidence.
5. Memory records **require** provenance.
6. Historical records **must** remain reconstructable.
7. Corrections/supersession **must not** silently erase epistemic history.

### G.2 Append / version preference

Preferred minimal model: **append-oriented / versioned** records (logical). Production database design is **deferred**.

### G.3 Naming clarity

`src/asa/memory_stores.py` is **not** the ACES Memory layer. Implementations of MemoryObject MUST NOT overload ASA capability stores as Memory.

---

## H. World Model semantics

World Model is a model of **believed/probable** state, not Reality.

### H.1 Normative rules

1. Belief is distinct from truth.
2. Confidence is distinct from truth.
3. World Model updates require legitimate epistemic input (from AcceptedState / Knowledge / Memory paths as defined by implementation gate — never from raw agent assertion alone).
4. World Model **cannot** manufacture Evidence.
5. World Model **cannot** promote itself to Knowledge.
6. World Model **cannot** authorize execution.
7. World Model **cannot** redefine Semantic Reality by fiat.

### H.2 BeliefState (spec only)

Minimal compatible form: `Beta(α, β)` for binary belief parameters.

**Not implemented by this contract.**

### H.3 Deferred advanced metrics

- ERM
- KCE
- Epistemic Health
- Self-modifying World Model

---

## I. Provenance contract

### I.1 Chain coverage

Provenance requirements apply across:

```text
Evidence → Verification → AcceptedState → Knowledge → Memory → World Model
```

### I.2 Logical vs cryptographic

| Kind | Status |
|------|--------|
| Logical reconstructability | **REQUIRED** by this contract |
| Cryptographic signatures / PKI | **DEFERRED** (Evidence contract already defers crypto authenticity) |

### I.3 Minimum fields (logical)

- source/reference
- originating task/execution (when applicable)
- evidence reference
- verification reference
- AcceptedState reference (for promotion-dependent updates)
- timestamp/version
- transformation actor or mechanism

Missing or invalid provenance → fail-closed (§L).

---

## J. Authority matrix

| Layer | Owns | Does NOT own |
|-------|------|--------------|
| Semantic Reality | Semantic state coordination | Execution authorization |
| Evidence | Observations | Authority |
| Verification | Verification gate | Authorization |
| AcceptedState | Epistemic acceptance gate | Capability issuance |
| Knowledge | Epistemic claims | Authority |
| Memory | Durable recall | Truth / authority |
| World Model | Beliefs / estimates | Reality / evidence / authority |
| ASA | Authorization | Truth / evidence / AcceptedState |
| Execution Adapter | Dispatch | Authority / epistemic acceptance |
| Runtime | Execution | Authority / truth |
| Agent | Proposals / execution work | Self-authorization |

---

## K. Write / mutation boundaries

1. Agents **MUST NOT** silently write Knowledge.
2. Agents **MUST NOT** silently write Memory.
3. Agents **MUST NOT** silently update World Model.
4. Runtime success **MUST NOT** directly mutate epistemic truth.
5. All epistemic mutations **MUST** use an authorized service/path (implementation deferred).
6. ASA remains the **authorization** boundary for protected operations.
7. Epistemic acceptance remains **downstream** of Evidence + Verification.
8. No component may acquire authority merely by possessing Context, Capability, Memory, Evidence, or Confidence.

Protected resource kinds (`KnowledgeObject`, `MemoryObject`, etc.) remain subject to ASA when those resources are operationalized.

---

## L. Failure semantics (fail-closed)

| Condition | Required behavior |
|-----------|-------------------|
| Missing provenance | Reject update / DENY path |
| Invalid provenance | Reject update / DENY path |
| Missing Evidence binding | Reject promotion |
| Mismatched Evidence | Reject verification / promotion |
| Missing AcceptedState | Reject Knowledge promotion |
| Invalid Knowledge truth level | Reject write |
| Unauthorized Knowledge mutation | DENY |
| Unauthorized Memory mutation | DENY |
| Unauthorized World Model mutation | DENY |
| Ambiguous object identity | Reject |
| Unknown epistemic state | Reject; no silent “trusted” |
| Unavailable authority/verification dependency | DENY / fail-closed |

**No silent downgrade to trusted.**

---

## M. Canonical invariants

1. Evidence ≠ Knowledge  
2. Memory ≠ Truth  
3. World Model ≠ Reality  
4. Confidence ≠ Truth  
5. AcceptedState ≠ Authorization  
6. Knowledge ≠ Authority  
7. Memory ≠ Authority  
8. World Model ≠ Authority  
9. Execution success ≠ AcceptedState  
10. Inference ≠ Evidence  
11. Recall ≠ Verification  
12. Agent ≠ Authority  
13. Runtime ≠ Authority  
14. Self-improvement ≠ Self-authorization  

---

## N. Deferred items

Explicitly **out of scope** for Contract v0.1 and for any implementation that claims compliance without a further gate:

- production persistence / databases
- vector retrieval / embeddings
- cryptographic provenance / authenticity
- external verifier trust establishment / PKI
- advanced World Model metrics (ERM, KCE, Epistemic Health)
- self-modifying World Model
- autonomous self-evolution
- UI / product projections
- connector integration for knowledge ingestion
- production scalability
- quantitative promotion thresholds
- full ACE Knowledge Standard document import (if external)

Deferred items **MUST NOT** become implicit authority paths.

---

## O. Compatibility and non-claims

### O.1 Compatibility

This contract is designed to be compatible with:

- Evidence / Verification Hardening Contract v0.1
- ASA Hardening Contract v0.1
- Execution Adapter Contract v0.1
- Master Control Protocol sequencing (Knowledge/Memory/WM after Evidence/Verification)

### O.2 Explicit non-claims

This freeze does **not** claim:

- Knowledge, Memory, or World Model are implemented
- ACE Knowledge Standard v1.2-RC3 is present in-repo at base HEAD
- production readiness
- Canon Promotion
- connector generality
- agent self-authorization

---

## P. Acceptance criteria for this freeze

| Criterion | Required |
|-----------|----------|
| No implementation introduced | YES |
| No contradiction with ASA/Evidence/Verification contracts | YES |
| Evidence / Knowledge / Memory / World Model separated | YES |
| AcceptedState remains post-verification epistemic gate | YES |
| ASA remains authorization authority | YES |
| Knowledge/Memory/WM cannot become hidden authority | YES |
| Critical transitions directional | YES |
| Critical failures fail-closed | YES |
| Deferred work explicit | YES |
| `main` untouched | YES |

---

## Q. Document control

| Item | Value |
|------|--------|
| Artifact | `docs/architecture/KNOWLEDGE-MEMORY-WORLDMODEL-CONTRACT-v0.1.md` |
| Status | **FROZEN** |
| Implementation authorized by this document alone | **NO** |
| Next gate | Separate authorization required for minimal implementation / tests |

**END OF CONTRACT v0.1**
