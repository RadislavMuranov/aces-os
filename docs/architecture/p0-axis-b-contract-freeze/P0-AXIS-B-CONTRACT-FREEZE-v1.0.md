# P0 Axis-B Contract Freeze Pack v1.0

**Status:** FROZEN  
**Date:** 2026-09-03  
**Repository:** `RadislavMuranov/aces-os`  
**Gate:** P0 Axis-B Contract Freeze Pack  
**Kind:** Architecture / specification contracts only  
**Implementation authorized by this document alone:** **NO**

---

## 0. Purpose and non-claims

This pack freezes the **Axis-B Digital Reality Plane** as an explicit contractual architecture so subsequent implementation (when separately authorized) cannot invent identity, authority, evidence, or truth semantics ad hoc.

### Axis-B chain (frozen)

```text
DIGITAL WORLD
  → CONNECTOR FABRIC
  → DWOM
  → RECONCILIATION ENGINE
  → DIGITAL WORLD STATE
  → OBSERVATION / EVIDENCE
```

### Convergence with Axis-A (frozen)

```text
Execution observation + Digital observation
  → Evidence
  → Verification
  → AcceptedState
  → Knowledge
  → Memory / World Model
  → Semantic Reality
```

Axis-B converges with Axis-A **only** through Evidence → Verification → AcceptedState. No other path may mint Knowledge, Semantic Reality, or ACES authority.

### Explicit non-claims

- Not runtime implementation of DWOM / Connector Fabric / Reconciliation Engine
- Not adapters, databases, UI, or production code
- Not PR #4 merge
- Not `main` mutation
- Not G2-R1 status change
- Not Canon Promotion
- Not Self-Evolution authorization
- Not a second realization roadmap

---

## 1. Canonical architectural position (frozen)

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
   │         │
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
   REALITY LAYER
        │
      HUMAN
```

### Role interpretation (frozen)

| Element | Role |
|---------|------|
| Orca | Fleet / execution orchestration layer — **not** authority |
| DSH | Per-agent Harness / Execution Kernel substrate — **not** authority |
| Connector Fabric | Digital World access boundary |
| DWOM | Canonical representation of observed/projected digital-world objects |
| Reconciliation | Organization of observations — **not** truth authority |
| Verification | Epistemic acceptance gate |
| Knowledge | Canonical semantic layer (post-AcceptedState) |
| World Model | Epistemic belief/projection — **not** Semantic Reality authority |
| Reality Layer | Human-facing projection of Semantic Reality (architectural from P0; UI deferred) |

---

## 2. CONTRACT A — DWOM Object Contract

**Status:** FROZEN

### 2.1 Purpose

DWOM (Digital World Object Model) is the **canonical ACES representation** of externally observed or projected digital-world entities, events, and observations. It preserves identity, source, provenance, and state **without** becoming Knowledge, Evidence, AcceptedState, World Model, or Semantic Reality.

### 2.2 Explicit inequalities

```text
DWOM != Knowledge
DWOM != Evidence
DWOM != AcceptedState
DWOM != Semantic Reality
DWOM != World Model
```

DWOM **MUST NOT** establish epistemic truth or ACES authorization.

### 2.3 Field model

| Field | Requirement | Notes |
|-------|-------------|-------|
| `dwom_id` | **Mandatory** | Stable ACES-side identity for this DWOM object |
| `object_kind` / type | **Mandatory** | Class of external entity (issue, message, file, event, …) |
| `namespace` | **Mandatory** | Logical domain / tenancy scope within ACES mapping |
| `source_system_id` | **Mandatory** | Provider / system identity (e.g. github, slack) |
| `source_identity` | **Mandatory** | Account/org/workspace identity at source where applicable |
| `external_native_id` | **Mandatory** | Native identifier in source system |
| `representation` | **Mandatory** | Structured projection of what was observed (schema-bound) |
| `observed_state` | **Mandatory** | State as observed at observation time |
| `observation_timestamp` | **Mandatory** | When ACES observed / ingested |
| `source_timestamp` | Optional | When source claims the state changed / was valid |
| `version` / revision | Optional | Source version if available |
| `provenance` | **Mandatory** | Chain: connector, request, raw refs, transformation notes |
| `correlation_id` / request / task id | Optional | Link to ACES request/task when applicable |
| `capability_refs` | Optional | Capabilities exercised to obtain this object |
| `freshness` | **Mandatory** | Policy-relevant freshness class or absolute bound |
| `validity` | **Mandatory** | Whether projection is currently treated as valid input |
| `uncertainty` | **Mandatory** | Explicit uncertainty / confidence / partial-observability flags |
| `lifecycle` | **Mandatory** | e.g. observed, stale, superseded, tombstoned |
| `relationship_refs` | Optional | Links to related DWOM objects |
| `reconciliation_status` | **Mandatory** | e.g. unreconciled, candidate, conflicted, projected |

### 2.4 Invariants

1. Every DWOM object has unique (`source_system_id`, `external_native_id`, `namespace`) binding **or** an explicit multi-identity correlation set — no silent identity collapse.
2. Provenance is never stripped on copy or projection.
3. Creating or updating a DWOM object does **not** create Evidence, Knowledge, or AcceptedState.
4. DWOM may be incomplete; incompleteness must be visible via `uncertainty` / `validity`.
5. Fail-closed: malformed or provenance-missing candidates **MUST NOT** be admitted as valid DWOM objects.

### 2.5 Lifecycle (contractual)

```text
observed → (optional reconcile) → projected | conflicted | superseded | tombstoned
```

---

## 3. CONTRACT B — Connector Contract

**Status:** FROZEN

### 3.1 Purpose

**Connector Fabric** is the boundary between ACES and heterogeneous digital systems. It is an **access and observation boundary**, not an authorization authority and not the architectural center of ACES.

### 3.2 Conceptual operations (capability-gated)

Connectors **may** support, where the provider allows:

```text
discover | read | observe | write | execute | subscribe/watch
```

Availability is **connector-specific**. Absence of a capability is not a license to invent it via MCP or ad hoc paths.

### 3.3 Field / interface model (contractual)

| Element | Requirement | Notes |
|---------|-------------|-------|
| `connector_id` | **Mandatory** | ACES identity of connector instance |
| `provider_id` / source system | **Mandatory** | External system identity |
| `resource_id` | **Mandatory** for resource ops | Target resource in provider terms |
| `operation` | **Mandatory** | discover/read/observe/write/execute/subscribe… |
| `scope` | **Mandatory** | What the operation is allowed to touch |
| `principal` | **Mandatory** | Acting identity (mapped; see Contract C) |
| `capability` | **Mandatory** | Connector capability being invoked |
| `authorization_ref` | **Mandatory** for side-effecting ops | Reference to ACES ASA/policy decision — **not** connector-local authority |
| `request_id` | **Mandatory** | Correlation / idempotency key |
| `idempotency_key` | Optional | When provider supports |
| `input` | Operation-dependent | |
| `output` | Operation-dependent | |
| `observation` | When applicable | Structured observation payload |
| `provenance` | **Mandatory** | |
| `errors` | **Mandatory** on failure | Typed, non-silent |
| `retry_semantics` | **Mandatory** (declared) | Policy-level; not silent infinite retry |
| `rate_limits` | Declared where known | |
| `freshness` | When returning state | |
| `consistency_characteristics` | Declared | e.g. eventual, snapshot, unknown |
| `native_transaction_semantics` | Optional | Only if provider truly offers them |

### 3.4 Critical distinction

```text
Connector Capability != ACES Authorization Authority
```

- A connector **MUST NEVER** mint ACES authority.
- A connector **MUST NOT** bypass ASA / policy authorization.
- Side-effecting operations **require** a valid `authorization_ref` from Axis-A authority evaluation.
- Successful connector I/O is **not** Evidence and **not** AcceptedState.

### 3.5 CLA / MCP rule (frozen)

```text
MCP is used ONLY when a CLA / Connector / Local / Native alternative
cannot provide the required capability.
```

```text
MCP != Connector Fabric
```

MCP is an optional **protocol/mechanism** that may appear **inside** Connector Fabric. It is **not** mandatory and **not** the architectural center.

### 3.6 Fail-closed (connector)

Unknown connector, invalid/expired/revoked capability, missing `authorization_ref` for side effects, unavailable authorization evaluator, or unavailable audit/provenance path → **deny / no side effect / no fabricated success observation**.

---

## 4. CONTRACT C — Identity / Capability / Event / Evidence / Authority Mappings

**Status:** FROZEN

### 4.1 Identity mapping

| External | ACES |
|----------|------|
| Provider account / user / service identity | ACES principal (mapped, never assumed equal) |
| Resource native id | Bound via DWOM `external_native_id` + `source_system_id` |

Unknown identity → **fail-closed** (no silent principal elevation).

### 4.2 Capability mapping

| Connector capability | ACES capability |
|---------------------|-----------------|
| Provider-specific operation grant | Distinct ACES capability object evaluated by ASA/policy |

```text
Capability != Authority
Connector Capability != ACES Authority
```

### 4.3 Event mapping

| External event / change notification | ACES |
|-------------------------------------|------|
| Webhook / poll delta / watch event | Observation candidate → may feed DWOM / Evidence path |

Duplicate/replayed events must be detectable via `request_id` / event ids / provenance; silent double-admission is forbidden.

### 4.4 Evidence mapping

| External observation | ACES Evidence |
|----------------------|---------------|
| Connector/DWOM observation | **Candidate** EvidenceObject only after Contract F rules |

Observation alone does **not** equal Evidence.

### 4.5 Authority mapping (mandatory distinction)

```text
Source Authority != ACES Authorization Authority
```

A source may be authoritative for a **narrowly scoped external fact/state/operation** (e.g. GitHub for the state of a GitHub issue). A source **MUST NOT**:

- authorize an ACES action;
- issue ACES capabilities;
- override ASA;
- redefine Semantic Reality;
- bypass Verification;
- establish AcceptedState by itself.

---

## 5. CONTRACT D — Reconciliation Engine

**Status:** FROZEN

### 5.1 Purpose

Organize multiple observations of the same or related digital-world entities **without** becoming an omniscient truth oracle.

```text
Reconciliation Result != Truth
```

### 5.2 Required behaviors (contractual)

| Concern | Requirement |
|---------|-------------|
| Observation intake | Accept only provenance-bearing observations |
| Identity matching | Explicit rules; no silent merge of distinct natives |
| Correlation | Link related objects/events with inspectable rationale |
| Temporal ordering | Use `source_timestamp` and `observation_timestamp` distinctly |
| Version comparison | When versions exist; otherwise mark unknown |
| Conflict detection | Mandatory when representations disagree |
| Precedence policies | **Explicit, policy-scoped, inspectable**; not hidden globals |
| Source reliability metadata | Optional inputs to policy — never silent trust |
| Freshness | Stale observations must not silently dominate |
| Partial observability | Preserve “unknown” rather than invent completeness |
| Uncertainty | Carried into result |
| Competing observations | **Preserved** when conflict cannot be legitimately resolved |
| Reconciliation result | Candidate Digital World State projection + status |
| Provenance | Full |
| Confidence / uncertainty | Explicit |
| Unresolved conflict state | First-class status |

### 5.3 Precedence rules

- No hidden source hierarchy.
- No arbitrary “latest wins” **unless** explicitly defined by policy for that resource/domain.
- Precedence must be **reversible/auditable** where possible.

### 5.4 Fail-closed

Malformed observation, unverifiable provenance, ambiguous resource identity → do **not** emit a clean reconciled truth; emit conflicted / rejected / unresolved with provenance intact.

---

## 6. CONTRACT E — Digital World State

**Status:** FROZEN

### 6.1 Layer separation (mandatory)

| Layer | Meaning |
|-------|---------|
| Raw external representation | What a connector/source exposes |
| DWOM | Canonical ACES representation of external digital objects |
| Reconciled Digital World State | ACES’ current reconciled **projection** of observed external state |
| Evidence | Epistemically bound observation candidate / object under Verification |
| Knowledge | Canonical semantic knowledge (post-AcceptedState path only) |

### 6.2 Required path (no collapse)

```text
Digital World
  → Observation
  → DWOM
  → Reconciliation
  → Digital World State
  → Observation / Evidence
  → Verification
  → AcceptedState
  → Knowledge
```

```text
Digital World State != Semantic Reality
Digital World State != Knowledge
Digital World State != World Model State
```

Digital World State **MUST NOT** become Semantic Reality by fiat.

---

## 7. CONTRACT F — Observation → Evidence Boundary

**Status:** FROZEN

### 7.1 Observation must preserve

- source / source object
- operation / scope
- timestamp(s)
- request / correlation identity
- raw/native reference where available
- connector identity
- provenance
- observed payload/state
- freshness / validity

### 7.2 Invariants

```text
Execution Success != Evidence
Observation != Evidence
Evidence != AcceptedState
```

Evidence **MUST NOT** be fabricated merely because a connector returned successfully.

AcceptedState is established **only** through the existing trusted **Verification** path (Axis-C). Axis-B does not own Verification.

### 7.3 Fail-closed

Missing provenance, malformed payload, stale beyond policy without explicit override, or ambiguous identity → **no Evidence admission**.

---

## 8. CONTRACT G — Authority Boundary

**Status:** FROZEN

### 8.1 Planes

**Axis-A**

```text
Constitution → Authority / Policy → Execution Contract → authorized execution
```

**Axis-B**

```text
Digital World → Connector Fabric → observation / external operation under ACES authz
```

### 8.2 Rules

- Axis-B may **observe** and may perform **externally directed operations** only when Axis-A authorization is present for side effects.
- Axis-B **cannot** create ACES authority.
- Connector layer **MUST NOT** become a hidden authorization layer.
- **ASA** remains the authority evaluator.
- Unavailable authorization evaluator → **fail-closed** (no side effect).

```text
Context != Authority
Capability != Authority
Verification != Authorization
DSH != Authority
Orca != Authority
```

---

## 9. HIC / ASPE integration

**Status:** FROZEN (realization criteria — not overrides)

### 9.1 Definitions

- **HIC (Human Intervention Cost):** Axis-B should reduce **parasitic** human middleware work (duplicate entry, manual sync, re-search, context switching, cross-system reconciliation noise).
- **ASPE (Axiom of Preservation of Psychic Energy):** Interaction with the digital world must not force **unnecessary** expenditure of human psychic energy.

### 9.2 Non-override rule

HIC/ASPE **MUST NOT** override:

- safety
- authorization
- verification
- necessary human approval
- epistemic integrity
- fail-closed behavior

```text
ACES removes parasitic friction, not necessary friction.
```

---

## 10. Consolidated invariants

**Status:** FROZEN

```text
Context ≠ Authority
Capability ≠ Authority
Connector Capability ≠ ACES Authority
Source Authority ≠ ACES Authorization Authority
Execution Success ≠ Evidence
Execution Success ≠ AcceptedState
Observation ≠ Evidence
Evidence ≠ AcceptedState
DWOM ≠ Knowledge
DWOM ≠ Semantic Reality
Digital World State ≠ Semantic Reality
Reconciliation Result ≠ Truth
World Model ≠ Reality
World Model ≠ Evidence
World Model ≠ Authority
Inference ≠ Evidence
Verification ≠ Authorization
Memory ≠ Truth
DSH ≠ Authority
Orca ≠ Authority
Self-improvement ≠ Self-authorization
MCP ≠ Connector Fabric
```

---

## 11. Security / failure semantics (cross-cutting)

**Status:** FROZEN for policy posture; **mechanism details DEFERRED** where not already canonical

| Case | Posture |
|------|---------|
| Unknown identity | Fail-closed |
| Invalid / expired / revoked capability | Fail-closed |
| Missing policy | Fail-closed |
| Unavailable authorization evaluator | Fail-closed |
| Unavailable audit / provenance | Fail-closed for admission of side effects / Evidence |
| Malformed observation | Reject; no clean DWOM/Evidence |
| Unverifiable provenance | Reject |
| Conflicting observations | Preserve competitors; mark conflicted |
| Stale observation | Policy-bound; no silent dominance |
| Connector failure | Typed error; no fabricated success |
| Partial response | Mark partial; no invented completeness |
| Duplicate / replayed event | Detect; no double-admission |
| Ambiguous resource identity | Fail-closed |

**Deferred (explicit):** concrete cryptography, key management, transport security profiles, and storage encryption — **not invented** by this pack; must be supplied by existing or future security gates without weakening the above postures.

---

## 12. Traceability

**Status:** FROZEN (reference map)

| This pack | Maps to |
|-----------|---------|
| Axis-B plane | Canonical Roadmap v2.0 three-axis model |
| P0 priority | `spec/ACES-DIGITAL-WORLD-PRIORITY-001.md` / PR #4 decision (unmerged) |
| Four boundaries | DWOM≠Knowledge; Source Authority≠ACES Authz; Reconciliation≠Truth Arbitration; Digital World State≠World Model≠Semantic Reality |
| Authority | ASA / Authority-Policy plane (Axis-A) |
| Evidence / Verification / AcceptedState | Existing Axis-C convergence kernel |
| Knowledge / Memory / World Model | Downstream epistemic contracts (G2-R1 verification-closure remains **BLOCKED**) |
| Constitution | ACES Constitution / governing protocols (unchanged by this pack) |
| MCP rule | Roadmap v2.0 + this Contract B |
| HIC / ASPE | Roadmap v2.0 realization criteria |

This pack **does not rewrite** those historical documents; it **contracts** Axis-B against them.

---

## 13. Deferred items (explicit)

| Item | Why deferred |
|------|----------------|
| Runtime DWOM / Fabric / Reconciliation implementation | Implementation not authorized |
| Per-provider connector schemas (GitHub, Slack, …) | Belong to P1 vertical slice after validation |
| Cryptographic mechanism suite | Not already fully canonical here; avoid invention |
| Reality Layer UI | Architectural principle frozen in roadmap; UI deferred |
| G2-R1 verification closure | Remains **BLOCKED** (environment) |
| Canon Promotion | **NOT AUTHORIZED** |
| Controlled Self-Evolution | **NOT STARTED** |

---

## 14. Contract status summary

| Contract | Status |
|----------|--------|
| A DWOM Object | **FROZEN** |
| B Connector (+ CLA/MCP rule) | **FROZEN** |
| C Identity/Capability/Event/Evidence/Authority mappings | **FROZEN** |
| D Reconciliation Engine | **FROZEN** |
| E Digital World State separation | **FROZEN** |
| F Observation → Evidence boundary | **FROZEN** |
| G Authority Boundary | **FROZEN** |
| HIC / ASPE integration | **FROZEN** (criteria, non-override) |
| Consolidated invariants | **FROZEN** |
| Crypto / transport mechanisms | **DEFERRED** |
| Runtime implementation | **NOT STARTED** |

**END OF P0 AXIS-B CONTRACT FREEZE PACK v1.0**
