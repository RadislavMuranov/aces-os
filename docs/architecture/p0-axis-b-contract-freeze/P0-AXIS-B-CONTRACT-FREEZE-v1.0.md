# P0 Axis-B Contract Freeze Pack v1.0

**Status:** FROZEN (with targeted remediation amendments)  
**Date:** 2026-09-03  
**Repository:** `RadislavMuranov/aces-os`  
**Gate origin:** P0 Axis-B Contract Freeze Pack  
**Remediation:** P0 Axis-B Contract Targeted Remediation (F1–F8)  
**Kind:** Architecture / specification contracts only  
**Implementation authorized by this document alone:** **NO**

---

## 0. Purpose and non-claims

This pack freezes the **Axis-B Digital Reality Plane** as an explicit contractual architecture so subsequent implementation (when separately authorized) cannot invent identity, authority, evidence, or truth semantics ad hoc.

### Axis-B operational chain (frozen)

```text
DIGITAL WORLD
  → CONNECTOR FABRIC
  → OBSERVATION
  → DWOM (representation; parallel, not Evidence)
  → RECONCILIATION ENGINE
  → DIGITAL WORLD STATE (projection; not Truth)
```

### Epistemic admission chain (frozen — ordered, non-collapsible)

```text
OBSERVATION
  → EVIDENCE CANDIDATE
  → EVIDENCE ADMISSION
  → EVIDENCE
  → AXIS-C VERIFICATION
  → ACCEPTED STATE
  → KNOWLEDGE
  → MEMORY / WORLD MODEL
  → SEMANTIC REALITY
  → REALITY LAYER
```

**Mandatory inequalities on this chain:**

```text
Observation ≠ EvidenceCandidate
EvidenceCandidate ≠ Evidence
Evidence ≠ Verification
Evidence ≠ AcceptedState
Verification ≠ AcceptedState
```

Axis-B may produce Observations, DWOM objects, Digital World State projections, and **EvidenceCandidates**. Axis-B **MUST NOT** mint AcceptedState, Knowledge, or Semantic Reality. Convergence with Axis-A/C occurs **only** through Evidence → Axis-C Verification → AcceptedState.

### Explicit non-claims

- Not runtime implementation of DWOM / Connector Fabric / Reconciliation Engine
- Not adapters, databases, UI, or production code
- Not PR #4 merge
- Not `main` mutation
- Not G2-R1 status change
- Not Canon Promotion
- Not Self-Evolution authorization
- Not a second realization roadmap
- Not cryptographic authenticity of provenance (see §7.5 — **DEFERRED**)

---

## 1. Canonical architectural position (frozen)

```text
ACES CONSTITUTION
        │
        ▼
AUTHORITY / POLICY (ASA)
        │
   ┌────┴────┐
   │         │
   ▼         ▼
EXECUTION   DIGITAL WORLD
PLANE       PLANE
   │         │
Execution   Connector Fabric
Contract    │
   │       Observation
Orca        │
   │       DWOM
DSH         │
   │       Reconciliation → Digital World State
   │         │
   │       EvidenceCandidate → Evidence Admission → Evidence
   │         │
   └────┬────┘
        ▼
  AXIS-C VERIFICATION
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
| Orca | Fleet / execution orchestration — **not** authority |
| DSH | Per-agent Harness / Execution Kernel substrate — **not** authority |
| Connector Fabric | Digital World access boundary |
| Observation | Provenance-bearing record of what was seen/done externally — **not** Evidence |
| DWOM | Canonical representation of observed/projected digital-world objects — **not** Knowledge/Evidence |
| Reconciliation | Organization of observations — **not** truth authority |
| Digital World State | Reconciled **projection** — **not** Semantic Reality |
| EvidenceCandidate | Pre-admission epistemic package — **not** Evidence |
| Evidence Admission | Controlled transition EvidenceCandidate → Evidence — **not** Verification |
| Evidence | Admitted observation package eligible for Axis-C Verification — **not** AcceptedState |
| Verification | Axis-C epistemic acceptance gate |
| Knowledge | Canonical semantic layer (post-AcceptedState) |
| World Model | Epistemic belief/projection — **not** Semantic Reality authority |
| Reality Layer | Human-facing projection (architectural from P0; UI deferred) |

---

## 2. CONTRACT A — DWOM Object Contract

**Status:** FROZEN

### 2.1 Purpose

DWOM is the **canonical ACES representation** of externally observed or projected digital-world entities. It preserves identity, source, provenance, and state **without** becoming Knowledge, Evidence, EvidenceCandidate, AcceptedState, World Model, or Semantic Reality.

### 2.2 Explicit inequalities

```text
DWOM != Knowledge
DWOM != Evidence
DWOM != EvidenceCandidate
DWOM != AcceptedState
DWOM != Semantic Reality
DWOM != World Model
DWOM != Authorization
```

DWOM **MUST NOT** establish epistemic truth or ACES authorization.

### 2.3 Field model

| Field | Requirement | Notes |
|-------|-------------|-------|
| `dwom_id` | **Mandatory** | Stable ACES-side identity for this DWOM object |
| `object_kind` / type | **Mandatory** | Class of external entity |
| `namespace` | **Mandatory** | Logical domain / tenancy scope |
| `source_system_id` | **Mandatory** | Provider / system identity |
| `source_identity` | **Mandatory** | Account/org/workspace at source where applicable |
| `external_native_id` | **Mandatory** | Native identifier in source system |
| `representation` | **Mandatory** | Structured projection (schema-bound) |
| `observed_state` | **Mandatory** | State as observed at observation time |
| `observation_timestamp` | **Mandatory** | When ACES observed / ingested |
| `source_timestamp` | Optional | When source claims validity/change time |
| `version` / revision | Optional | Source version if available |
| `provenance` | **Mandatory** | Connector, request, raw refs, transforms |
| `correlation_id` / request / task id | Optional | Link to ACES request/task |
| `capability_refs` | Optional | Capabilities exercised |
| `freshness` | **Mandatory** | Policy-relevant freshness class or bound |
| `validity` | **Mandatory** | Whether treated as valid input |
| `uncertainty` | **Mandatory** | Uncertainty / partial-observability flags |
| `lifecycle` | **Mandatory** | observed, stale, superseded, tombstoned, … |
| `relationship_refs` | Optional | Related DWOM objects |
| `reconciliation_status` | **Mandatory** | unreconciled, candidate, conflicted, projected, … |
| `identity_epoch` | **Mandatory** | Distinguishes create vs post-delete recreate epochs (see §2.6) |

### 2.4 Invariants

1. Binding key is (`source_system_id`, `external_native_id`, `namespace`, `identity_epoch`) **or** an explicit multi-identity correlation record (§2.6) — **no silent identity collapse**.
2. Provenance is never stripped on copy or projection.
3. Creating/updating DWOM does **not** create EvidenceCandidate, Evidence, Knowledge, or AcceptedState.
4. Incompleteness must be visible via `uncertainty` / `validity`.
5. Malformed or provenance-missing candidates **MUST NOT** be admitted as valid DWOM objects.

### 2.5 Lifecycle (contractual)

```text
observed → (optional reconcile) → projected | conflicted | superseded | tombstoned
```

### 2.6 Identity lifecycle (F3 remediation)

#### 2.6.1 Initial creation

First valid observation of (`source_system_id`, `external_native_id`, `namespace`) creates a DWOM object with a new `identity_epoch` and full provenance.

#### 2.6.2 Same native ID, different providers

Different `source_system_id` ⇒ **distinct** identities. No automatic merge across providers.

#### 2.6.3 Namespace collision

Same native id in different `namespace` ⇒ **distinct** identities.

#### 2.6.4 Delete → recreate

```text
old identity ≠ recreated identity
```

merely because `external_native_id` matches after delete. Recreate **MUST** use a **new** `identity_epoch` (or equivalent tombstone+successor linkage). Prior provenance remains on the tombstoned object; it is **not** overwritten as if continuous.

#### 2.6.5 Rename / move / migration

- Rename/move **MUST NOT** erase prior identity provenance.
- Rename/move **MUST NOT** silently invent a new semantic Knowledge identity.
- Successor linkage, if any, is an **explicit** correlation or lifecycle transition with provenance — not field-match alone.

#### 2.6.6 Alias / multi-identity correlation

Correlation between identities **MUST** have:

- explicit **policy identifier** and policy version;
- **correlation authority** (ACES policy/decision path — **not** source authority alone, **not** connector preference, **not** inference alone, **not** latest-wins);
- inspectable **correlation record** with provenance;
- participating identity refs.

**Forbidden as sole basis for correlation:**

- automatic field coincidence;
- model inference alone;
- connector preference;
- source authority claim alone;
- latest-wins.

#### 2.6.7 Authority note

Identity correlation does **not** mint ACES action authorization. It is a representation/linkage decision under declared policy, subject to fail-closed rules when policy or authority is missing.

---

## 3. CONTRACT B — Connector Contract

**Status:** FROZEN

### 3.1 Purpose

**Connector Fabric** is the boundary between ACES and heterogeneous digital systems — access and observation, **not** authorization authority, **not** architectural center.

### 3.2 Conceptual operations (capability-gated)

```text
discover | read | observe | write | execute | subscribe/watch
```

Availability is connector-specific. Absence of a capability is not a license to invent it via MCP or ad hoc paths.

### 3.3 Field / interface model

| Element | Requirement | Notes |
|---------|-------------|-------|
| `connector_id` | **Mandatory** | ACES connector instance id |
| `provider_id` | **Mandatory** | External system |
| `resource_id` | **Mandatory** for resource ops | |
| `operation` | **Mandatory** | |
| `scope` | **Mandatory** | |
| `principal` | **Mandatory** | Mapped ACES principal |
| `capability` | **Mandatory** | Connector capability invoked |
| `authorization_ref` | **Mandatory** for side-effecting ops | Axis-A ASA/policy decision ref |
| `request_id` | **Mandatory** | Request identity (see §3.7) |
| `payload_digest` | **Mandatory** for side-effecting and Evidence-relevant ops | Binding of semantic payload to request_id |
| `event_id` | **Mandatory** when source supplies a durable event id; otherwise ACES **MUST** assign a durable observation event id in provenance | Correlation / replay detection |
| `idempotency_key` | Optional | Provider-supported |
| `input` / `output` / `observation` | Operation-dependent | |
| `provenance` | **Mandatory** | |
| `errors` | **Mandatory** on failure | Typed |
| `retry_semantics` | **Mandatory** (declared) | |
| `rate_limits` | Declared where known | |
| `freshness` | When returning state | |
| `consistency_characteristics` | Declared | |
| `native_transaction_semantics` | Optional | Only if truly offered |

### 3.4 Critical distinction

```text
Connector Capability != ACES Authorization Authority
```

- Connector **MUST NEVER** mint ACES authority.
- Connector **MUST NOT** bypass ASA / policy.
- Side-effecting operations **require** valid `authorization_ref` from Axis-A.
- Successful connector I/O is **not** Observation-as-Evidence, **not** Evidence, **not** AcceptedState.

### 3.5 CLA / MCP rule (frozen) + F7

```text
MCP is used ONLY when a CLA / Connector / Local / Native alternative
cannot provide the required capability under established rule.
```

```text
MCP != Connector Fabric
MCP != Authority
MCP != Authorization
```

MCP is an optional **protocol/mechanism** that may appear **inside** Connector Fabric. It is **not** mandatory and **not** the architectural center.

**F7 rule (explicit):**

> MCP-mediated side effects **MUST** use the **same ASA authorization path** and the **same `authorization_ref` semantics** as any other Connector Fabric side effect. MCP **MUST NOT** create an alternative authorization path.

### 3.6 Fail-closed (connector)

Unknown connector, invalid/expired/revoked capability, missing `authorization_ref` for side effects, unavailable authorization evaluator, or unavailable audit/provenance path → **deny / no side effect / no fabricated success observation**.

### 3.7 Replay / request payload binding (F4)

**Canonical request binding** is (`request_id`, `payload_digest`) together with operation, scope, resource, principal, and source identity as recorded in provenance.

| Case | Required behavior |
|------|-------------------|
| same `request_id` + same `payload_digest` | Deterministic replay / idempotent handling — **no** new semantic mutation solely from replay |
| same `request_id` + **different** `payload_digest` (or different operation/resource/scope/source identity) | **REJECT** or **CONFLICT** — **not** a valid new operation under the reused request identity |

**Invariant:**

```text
same request identity + different semantic payload ≠ valid replay
```

Reuse of a request identity **MUST NOT** enable:

- repeat Evidence admission as if new;
- payload substitution;
- resource / operation / scope / source-identity substitution;
- provenance rebinding to a different semantic act.

Silent double-admission of the same event is **forbidden**. Durable `event_id` (source or ACES-assigned) **MUST** participate in duplicate detection where events are ingested.

---

## 4. CONTRACT C — Identity / Capability / Event / Evidence / Authority Mappings

**Status:** FROZEN

### 4.1 Identity mapping

| External | ACES |
|----------|------|
| Provider account / user / service | ACES principal (mapped, never assumed equal) |
| Resource native id | DWOM binding per §2.6 |

Unknown identity → **fail-closed** (no silent principal elevation).

### 4.2 Capability mapping

```text
Capability != Authority
Connector Capability != ACES Authority
```

Provider grants map to distinct ACES capability objects evaluated by ASA/policy.

### 4.3 Event mapping

Webhook / poll / watch → **Observation** (not Evidence). May later feed EvidenceCandidate path under Contract F.

Duplicates/replays: §3.7.

### 4.4 Evidence mapping

Connector/DWOM-derived material becomes at most an **EvidenceCandidate** under Contract F — never Evidence by connector success alone.

### 4.5 Authority mapping

```text
Source Authority != ACES Authorization Authority
```

A source may be authoritative for a **narrowly scoped external fact**. A source **MUST NOT**: authorize ACES actions; issue ACES capabilities; override ASA; redefine Semantic Reality; bypass Verification; establish AcceptedState.

---

## 5. CONTRACT D — Reconciliation Engine

**Status:** FROZEN

### 5.1 Purpose

Organize multiple observations of related digital-world entities **without** becoming a truth oracle.

```text
Reconciliation Result != Truth
```

### 5.2 Required behaviors

| Concern | Requirement |
|---------|-------------|
| Observation intake | Provenance-bearing only |
| Identity matching | Explicit rules; no silent merge of distinct natives (§2.6) |
| Correlation | Inspectable rationale; correlation authority per §2.6.6 |
| Temporal ordering | `source_timestamp` and `observation_timestamp` distinct (§5.5) |
| Version comparison | When present; else mark unknown |
| Conflict detection | Mandatory on disagreement |
| Precedence | **Only** via explicit policy id + version |
| Source reliability metadata | Optional policy inputs — never silent trust |
| Freshness | Stale must not silently dominate |
| Partial observability | Preserve unknown |
| Competing observations | **Preserved** unless resolved under §5.3 |
| Result | Candidate Digital World State projection + status |
| Unresolved conflict | First-class status |

### 5.3 Conflict resolution (F6 — replaces vague “legitimately resolved”)

**Default:** if representations disagree and **no** applicable explicit policy is identified → status **CONFLICT / UNRESOLVED**. Competing observations **MUST** remain preserved with provenance.

**If and only if** an explicit policy applies, a resolution record **MUST** include:

- `policy_id`
- `policy_version`
- `resolution_rule`
- participating observation refs
- provenance of the resolution decision
- result / residual uncertainty

**Forbidden unless explicitly defined by named policy for that resource/domain:**

- latest-wins
- source-order-wins
- connector-order-wins
- lexical-wins
- first-wins
- local-preference-wins
- hidden global source hierarchy

No silent discard of competing observations.

### 5.4 Fail-closed

Malformed observation, unverifiable-as-structurally-required provenance, ambiguous resource identity → **not** a clean reconciled truth; emit conflicted / rejected / unresolved with provenance intact.

### 5.5 Temporal semantics (F8)

| Field | Role |
|-------|------|
| `observation_timestamp` | When ACES observed/ingested — **mandatory** on Observation/DWOM |
| `source_timestamp` | When source claims change/validity — **optional** |

If `source_timestamp` is **absent**, implementation **MUST NOT** invent an **authoritative** temporal ordering merely from local arrival time. Any temporal precedence beyond recording observation time **MUST** be **explicit domain/policy-scoped**. Freshness remains mandatory as a policy-relevant class/bound; stale observations must not silently dominate valid ones under policy.

---

## 6. CONTRACT E — Digital World State

**Status:** FROZEN

### 6.1 Layer separation

| Layer | Meaning |
|-------|---------|
| Raw external representation | What source exposes |
| Observation | Provenance-bearing ACES record of intake |
| DWOM | Canonical object representation |
| Reconciled Digital World State | Projection of observed external state |
| EvidenceCandidate | Pre-admission package |
| Evidence | Post-admission package for Verification |
| Knowledge | Post-AcceptedState semantic knowledge |

### 6.2 Required path (no collapse)

```text
Digital World
  → Connector Fabric
  → Observation
  → DWOM / Reconciliation / Digital World State
  → EvidenceCandidate
  → Evidence Admission
  → Evidence
  → Axis-C Verification
  → AcceptedState
  → Knowledge
```

```text
Digital World State != Semantic Reality
Digital World State != Knowledge
Digital World State != World Model State
Digital World State != Authorization
```

**Forbidden direct links:** Digital World→Knowledge; DWOM→Knowledge; Observation→AcceptedState; Evidence→AcceptedState; Reconciliation→Truth; World Model→Semantic Reality.

---

## 7. CONTRACT F — Observation → EvidenceCandidate → Evidence Admission → Evidence

**Status:** FROZEN (F1/F2 remediation)

### 7.1 Observation

Provenance-bearing record of external intake or connector result. **MUST** preserve: source/source object, operation, scope, timestamps, request/correlation identity, `payload_digest` where applicable, event id (source or ACES-assigned), connector identity, provenance, observed payload/state, freshness/validity.

```text
Observation ≠ EvidenceCandidate
Observation ≠ Evidence
Execution Success ≠ Observation-as-Evidence
Execution Success ≠ Evidence
```

### 7.2 EvidenceCandidate

A **non-admitted** package of provenance-bearing data derived from Observation(s) (and optional DWOM refs), proposed for Evidence Admission. Creating an EvidenceCandidate does **not** create Evidence, Verification, or AcceptedState.

**Minimum fields (mandatory):** candidate id; observation ref(s); source_system_id; source object binding; connector_id; request_id + payload_digest binding; event_id (or equivalent durable correlation id); provenance chain; observed payload/state digest; freshness/validity/uncertainty; creation timestamp.

### 7.3 Evidence Admission

Controlled transition:

```text
EvidenceCandidate → Evidence
```

| Element | Rule |
|---------|------|
| **Meaning** | Administrative/epistemic **eligibility** of a candidate package to be treated as Evidence for Axis-C Verification |
| **Not Verification** | Admission **≠** Verification |
| **Not AcceptedState** | Admission **≠** AcceptedState |
| **Authority** | ACES **Evidence Admission policy** evaluated under governing policy/ASA boundaries for **admission decisions** — **not** a connector, **not** source authority, **not** DWOM, **not** Reconciliation, **not** MCP. Does **not** mint general action authorization and **must not** bypass ASA for side effects |
| **Required inputs** | Valid EvidenceCandidate; complete mandatory fields; identity binding; source binding; observation binding; request/event correlation; structural provenance present |
| **Decision record** | Admit or reject with reason, policy_id/version, actor/ref, timestamp, provenance |
| **Rejection** | Fail-closed on missing fields, ambiguous identity, replay violation (§3.7), structural provenance failure |
| **Replay** | Same request binding cannot re-admit under substituted payload (§3.7) |

**Only** Evidence (post-admission) may enter Axis-C Verification. Axis-B does **not** own Verification.

### 7.4 Evidence

Post-admission object eligible for Verification.

```text
Evidence ≠ AcceptedState
Evidence ≠ Verification
```

AcceptedState is established **only** by:

```text
Evidence → Axis-C Verification → AcceptedState
```

### 7.5 Provenance authenticity (F5 — deferred crypto)

```text
structurally valid provenance ≠ cryptographically authentic provenance
```

Until a future **security gate** defines binding mechanisms, **self-asserted provenance is untrusted for authenticity purposes**. Structural presence remains mandatory for admission pathways; lack of structural provenance → reject. This pack **does not** invent cryptography. Residual forgery risk is **explicitly deferred**, not denied.

### 7.6 Fail-closed (epistemic intake)

Missing structural provenance, malformed payload, stale beyond policy without explicit override, ambiguous identity, replay binding violation → **no EvidenceCandidate success path / no Evidence admission**.

---

## 8. CONTRACT G — Authority Boundary

**Status:** FROZEN

### 8.1 Planes

**Axis-A:** Constitution → Authority / Policy (ASA) → Execution Contract → authorized execution  
**Axis-B:** Digital World → Connector Fabric → observation / external operation **under ACES authz for side effects**

### 8.2 Rules

- Axis-B observes freely only within declared read/observe capabilities; **side effects** require Axis-A `authorization_ref`.
- Axis-B **cannot** create ACES authority.
- Connector / MCP **MUST NOT** become hidden authorization layers (§3.5).
- ASA remains the authority evaluator for actions.
- Unavailable authorization evaluator → **fail-closed** (no side effect).
- **No Axis-B operation may mint AcceptedState.**
- **No Axis-B operation may directly mutate Semantic Reality.**

```text
Context != Authority
Capability != Authority
Verification != Authorization
Runtime != Authority
DSH != Authority
Orca != Authority
MCP != Authority
MCP != Authorization
```

---

## 9. HIC / ASPE integration

**Status:** FROZEN (criteria — not overrides)

HIC reduces **parasitic** human middleware work. ASPE limits **unnecessary** psychic-energy expenditure.

**MUST NOT** override: safety, authorization, verification, necessary human approval, epistemic integrity, fail-closed behavior.

```text
ACES removes parasitic friction, not necessary friction.
```

---

## 10. Consolidated invariants

**Status:** FROZEN

```text
Observation ≠ EvidenceCandidate
EvidenceCandidate ≠ Evidence
Evidence ≠ AcceptedState
Evidence ≠ Verification
Verification ≠ Authorization
Execution ≠ Evidence
Execution Success ≠ AcceptedState
Capability ≠ Authority
Connector Capability ≠ ACES Authority
Source Authority ≠ ACES Authorization Authority
DWOM ≠ Knowledge
DWOM ≠ Semantic Reality
DWOM ≠ Authorization
Digital World State ≠ Semantic Reality
Digital World State ≠ Authorization
World Model ≠ Semantic Reality
World Model ≠ Evidence
World Model ≠ Authority
Reconciliation Result ≠ Truth
Memory ≠ Truth
Inference ≠ Evidence
MCP ≠ Connector Fabric
MCP ≠ Authority
MCP ≠ Authorization
Runtime ≠ Authority
DSH ≠ Authority
Orca ≠ Authority
Self-improvement ≠ Self-authorization
Context ≠ Authority
```

**Operational freezes:**

```text
No Axis-B operation may mint AcceptedState.
No Axis-B operation may directly mutate Semantic Reality.
No Connector may bypass ASA for side effects.
No Evidence admission may bypass Verification.
No reconciliation result may silently become Truth.
No identity correlation without explicit authority/policy.
No replay may mutate semantic state under a reused request identity with a different payload.
```

---

## 11. Security / failure semantics (cross-cutting)

**Status:** FROZEN for policy posture; crypto mechanisms **DEFERRED**

| Case | Posture |
|------|---------|
| Unknown identity | Fail-closed |
| Invalid / expired / revoked capability | Fail-closed |
| Missing policy | Fail-closed |
| Unavailable authorization evaluator | Fail-closed |
| Unavailable audit / structural provenance | Fail-closed for side effects / admission |
| Malformed observation | Reject |
| Structurally missing provenance | Reject |
| Self-asserted “authentic” provenance without binding mechanism | Untrusted for authenticity (F5) |
| Conflicting observations | Preserve; CONFLICT/UNRESOLVED unless policy record |
| Stale observation | Policy-bound; no silent dominance |
| Connector failure | Typed error; no fabricated success |
| Partial response | Mark partial |
| Duplicate / replay | §3.7 |
| same request_id + different payload | REJECT/CONFLICT |
| Ambiguous resource identity | Fail-closed |

**Deferred:** concrete cryptography, key management, transport profiles, storage encryption — future security gate; must not weaken postures above.

---

## 12. Traceability

| This pack | Maps to |
|-----------|---------|
| Axis-B plane | Canonical Roadmap v2.0 |
| P0 priority | PR #4 / `ACES-DIGITAL-WORLD-PRIORITY-001` (unmerged) |
| Four PR #4 boundaries | Preserved |
| Authority | ASA / Axis-A |
| Evidence / Verification / AcceptedState | Axis-C; G2-R1 remains **BLOCKED** |
| Remediation F1–F8 | `docs/architecture/p0-axis-b-contract-targeted-remediation/` |

---

## 13. Deferred items

| Item | Status |
|------|--------|
| Runtime DWOM / Fabric / Reconciliation | NOT STARTED |
| Per-provider schemas | P1 |
| Cryptographic provenance binding | DEFERRED (security gate) |
| Reality Layer UI | DEFERRED |
| G2-R1 verification closure | BLOCKED |
| Canon Promotion | NOT AUTHORIZED |
| Self-Evolution | NOT STARTED |

---

## 14. Contract status summary

| Contract | Status |
|----------|--------|
| A DWOM (+ identity lifecycle) | **FROZEN** |
| B Connector (+ MCP ASA path + replay binding) | **FROZEN** |
| C Mappings | **FROZEN** |
| D Reconciliation (+ policy resolution + temporal) | **FROZEN** |
| E Digital World State | **FROZEN** |
| F Observation → Candidate → Admission → Evidence | **FROZEN** |
| G Authority Boundary | **FROZEN** |
| HIC / ASPE | **FROZEN** |
| Invariants | **FROZEN** |
| Crypto authenticity | **DEFERRED** |
| Runtime | **NOT STARTED** |

**END OF P0 AXIS-B CONTRACT FREEZE PACK v1.0 (remediated)**
