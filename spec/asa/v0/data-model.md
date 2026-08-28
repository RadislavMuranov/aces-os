# ASA v0 Data Model (Frozen — ASA-003)

**Status:** SPECIFICATION ONLY — schema freeze for ASA v0  
**Authority sources:** ASA-001, ASA-002  
**HSD-001:** OPTION B active  
**Normative rule:** GitHub/Grok administrative privilege does **not** imply ACES Authority (I8).

This document freezes the minimal v0 logical data model. It does not implement code, connect DSH, or claim Source/Deployment integrity.

---

## 0. Layer Separation (Non-Negotiable)

| Layer | Owned by ASA v0? | Claim
|-------|------------------|-------
| **ACES Runtime Security** | YES | Protected-resource operations require Decision
| **Repository Source Integrity** | NO | Deferred; GitHub admin can mutate source
| **Deployment Integrity** | NO | Deferred; not part of ASA runtime boundary

---

## 1. Design Decisions Retained from ASA-002

| Decision | Rationale
|----------|----------
| Scope is an **evaluation concept** embedded in Capability | No separate Scope entity
| Audit + Provenance = single **AuthorizationEvent** | One append-only record type in v0
| No first-class Role | Roles would be policy sugar later
| No full ABAC engine | Minimal policy body only
| No signed capabilities | Opaque server-side capability ids
| No macaroon model | Premature complexity
| No DSH adapter in v0 schema | Explicit non-goal
| Expiration fields live on Capability | No separate Expiration entity
| Revocation is a separate record keyed by capability_id | Supports kill-list / emergency revoke

---

## 2. Invariants (Normative)

| ID | Invariant
|----|----------
| I1 | No protected-resource operation without Decision
| I2 | No Decision without authenticated Identity/Principal
| I3 | No capability use outside granted Scope (resource selector + operations + temporal window)
| I4 | Revoked capability cannot authorize
| I5 | Expired capability cannot authorize
| I6 | Policy failure cannot silently grant
| I7 | Audit (AuthorizationEvent) cannot grant authority
| I8 | GitHub administrative privilege does not imply ACES authority

Any evaluation path that would violate these is a specification defect.

---

## 3. Entity Catalog

### 3.1 Identity

Verified authentication result for a subject. Non-authoritative claims must not grant rights.

| Field | Req | Mutable | Authoritative | Validation | Failure
|-------|-----|---------|---------------|------------|--------
| `identity_id` | YES | NO (immutable after creation) | YES | Non-empty unique id | DENY
| `authenticator_id` | YES | NO | YES | Must reference an authenticator accepted by Architectural Authority | DENY if unknown
| `subject_ref` | YES | NO | YES | Non-empty subject reference as defined by authenticator | DENY if empty/invalid
| `verified_at` | YES | NO | YES | Valid timestamp; verification must have succeeded | DENY if missing/failed
| `claims` | NO | NO after verify record fixed | NO (unless policy explicitly elevates a named claim) | Opaque map; must not alone produce ALLOW | Ignore for grant unless policy says otherwise

**Failure behavior:** Unknown or failed Identity → DENY (I2).

**OPEN — REQUIRES AUTHORITY DECISION:** Which `authenticator_id` values are accepted in v0 (human vs agent).

---

### 3.2 Principal

Subject of authorization, resolved from Identity.

| Field | Req | Mutable | Authoritative | Validation | Failure
|-------|-----|---------|---------------|------------|--------
| `principal_id` | YES | NO | YES | Non-empty unique id | DENY
| `identity_id` | YES | NO | YES | Must reference a verified Identity | DENY if unresolved
| `display_label` | NO | YES | NO | Optional human label | N/A

**Failure behavior:** Cannot resolve Principal from Identity → DENY (I2).

---

### 3.3 Operation

Closed vocabulary for v0. Not a stored entity; value on Request and Capability.

**Allowed values (normative enum):**

`READ` | `CREATE` | `UPDATE` | `DELETE` | `EXECUTE` | `EXPORT` | `IMPORT` | `AUTHORIZE` | `REVOKE`

| Aspect | Rule
|--------|------
| Required on Request | YES
| Mutable on Request after acceptance | NO
| Authoritative source of allowed set for a grant | Capability.operations + Policy
| Unknown enum value | DENY (malformed)
| `DELEGATE` | **Not in v0 enum** unless Authority enables it in a later gate

---

### 3.4 Resource

Protected object identity. GitHub paths are **not** ACES resource ids by default.

| Field | Req | Mutable | Authoritative | Validation | Failure
|-------|-----|---------|---------------|------------|--------
| `resource_id` | YES | NO | YES | Non-empty stable id | DENY if missing
| `resource_kind` | YES | NO | YES | Must be a known v0 kind (below) | DENY if unknown for protected path
| `namespace` | NO | NO after create | YES if used | If present, must match capability resource selector | DENY on mismatch

**v0 resource_kind values:**

`KnowledgeObject` | `EvidenceObject` | `MemoryObject` | `DecisionObject` | `SecretObject` | `PolicyObject` | `ProtectedArtifact`

**Failure behavior:** Unknown protected target → DENY.

---

### 3.5 Capability (opaque server-side)

Issued grant. Client holds `capability_id` only; server record is authoritative.

**Scope (evaluation concept, embedded):** resource selector + operations[] + temporal window (`not_before` / `not_after`).

| Field | Req | Mutable | Authoritative | Validation | Failure
|-------|-----|---------|---------------|------------|--------
| `capability_id` | YES | NO | YES | Non-empty unique id | DENY if unknown
| `principal_id` | YES | NO | YES | Must equal request Principal | DENY if mismatch
| `resource_selector` | YES | NO | YES | Must cover request resource (id and/or kind/namespace rules as defined at issuance) | DENY if outside (I3)
| `operations` | YES | NO | YES | Non-empty subset of Operation enum; request op must be member | DENY if not (I3)
| `not_before` | YES | NO | YES | Valid timestamp; now >= not_before | DENY if early (I5)
| `not_after` | YES | NO | YES | Valid timestamp; now <= not_after; not_after > not_before | DENY if expired (I5)
| `issued_under_authority` | YES | NO | YES | Must be known Authority id | DENY if unknown
| `policy_id` | YES | NO | YES | Must reference Policy used at issuance | DENY if missing binding
| `policy_version` | YES | NO | YES | Must match issued policy version | DENY if unbound
| `purpose` | NO | NO | NO unless policy requires | Optional label | Policy-dependent
| `delegation_parent_id` | NO | NO | YES if present | **Deferred:** ignore in v0 unless DELEGATE enabled | OPEN if used

**Issuance:** Only via AUTHORIZE path under Authority; not by self-assertion; not by GitHub role (I8).

**Failure behavior:** Invalid / unbound / wrong principal / out of scope / expired → DENY.

**OPEN — REQUIRES AUTHORITY DECISION:** Single-use vs multi-use within window; whether `resource_selector` is exact id list, kind+namespace, or pattern language.

---

### 3.6 Policy

Authority-accepted rules. Not inferred from GitHub.

| Field | Req | Mutable | Authoritative | Validation | Failure
|-------|-----|---------|---------------|------------|--------
| `policy_id` | YES | NO | YES | Non-empty id | DENY if missing policy
| `version` | YES | NO for a published version | YES | Monotonic non-empty version id | DENY if unknown version
| `authority_id` | YES | NO | YES | Must be known Authority | DENY if unknown
| `body` | YES | NO after publish | YES | Well-formed minimal rule set (issuance + optional use-time checks) | DENY if invalid (I6)
| `status` | YES | YES (active ↔ retired only via Authority) | YES | Must be `active` for use in ALLOW path | DENY if not active
| `not_after` | NO | NO if set | YES | If set, policy itself not usable after | DENY if expired

**Missing / invalid / conflicting policy → DENY (I6).** No silent union-allow.

**OPEN — REQUIRES AUTHORITY DECISION:** Concrete `body` syntax/format (JSON/YAML/code); conflict detection rules beyond “DENY on conflict”.

---

### 3.7 Authority

Root of issuance. Distinct from Identity and from GitHub accounts.

| Field | Req | Mutable | Authoritative | Validation | Failure
|-------|-----|---------|---------------|------------|--------
| `authority_id` | YES | NO | YES | Non-empty; known to ASA | DENY path if unknown authority on grant
| `kind` | YES | NO | YES | v0: at least `architectural_authority` | DENY if unsupported kind
| `label` | NO | YES | NO | Optional | N/A

**Normative:** Architectural Authority is the sole root Authority for v0 issuance. Mapping humans to Authority is operational configuration, **not** ambient GitHub admin (I8).

---

### 3.8 Decision

Explicit evaluation outcome. Produced only by ASA evaluation.

| Field | Req | Mutable | Authoritative | Validation | Failure
|-------|-----|---------|---------------|------------|--------
| `decision_id` | YES | NO | YES | Unique id | N/A (internal)
| `principal_id` | YES | NO | YES | Must match resolved Principal | DENY if mismatch
| `resource_id` | YES | NO | YES | Request resource | —
| `operation` | YES | NO | YES | Request operation | —
| `outcome` | YES | NO | YES | `ALLOW` \| `DENY` only | —
| `reason_code` | YES | NO | YES | Stable machine-readable reason | —
| `capability_id` | NO | NO | YES if present | Required for ALLOW on capability-mediated ops | DENY if ALLOW without valid capability where required
| `policy_id` | YES | NO | YES | Policy used | —
| `policy_version` | YES | NO | YES | Version used | —
| `timestamp` | YES | NO | YES | Evaluation time | —
| `correlation_id` | YES | NO | YES | Request correlation | —

**ALLOW only if** Identity/Principal, Capability (when required), Scope, Expiration, Revocation, and Policy all pass. Otherwise **DENY**.

**I1:** Protected-resource side effects must not occur without an ALLOW Decision.

---

### 3.9 AuthorizationEvent (Audit + Provenance)

Single append-only event type for v0. **Never** an input that produces ALLOW (I7).

| Field | Req | Mutable | Authoritative | Validation | Failure
|-------|-----|---------|---------------|------------|--------
| `event_id` | YES | NO | YES | Unique | —
| `principal_id` | YES | NO | YES | From Decision | —
| `operation` | YES | NO | YES | From Decision | —
| `resource_id` | YES | NO | YES | From Decision | —
| `timestamp` | YES | NO | YES | Event time | —
| `authority_id` | YES | NO | YES | From evaluation | —
| `policy_id` | YES | NO | YES | From Decision | —
| `policy_version` | YES | NO | YES | From Decision | —
| `capability_id` | NO | NO | YES if present | From Decision | —
| `decision` | YES | NO | YES | `ALLOW` \| `DENY` | —
| `result_or_error_class` | YES | NO | YES | Outcome summary / error class | —
| `correlation_id` | YES | NO | YES | Links request | —

**Audit unavailable / cannot append for protected ops → DENY** (fail-closed).

**Provenance** in v0 = reconstructability from AuthorizationEvent records. No mandatory cryptographic signature in v0.

---

### 3.10 Revocation

Kill-list entry for a capability.

| Field | Req | Mutable | Authoritative | Validation | Failure
|-------|-----|---------|---------------|------------|--------
| `capability_id` | YES | NO | YES | Must reference existing capability | —
| `revoked_at` | YES | NO | YES | Valid timestamp | —
| `revoked_under_authority` | YES | NO | YES | Known Authority | —
| `state` | YES | NO after revoke | YES | `REVOKED` | If REVOKED → DENY on use (I4)

**Revocation store unavailable → DENY for protected ops.**

**OPEN — REQUIRES AUTHORITY DECISION:** Global epoch bump vs per-capability flags only.

---

### 3.11 Expiration

Not a separate entity. Represented exclusively by Capability.`not_before` / Capability.`not_after`.

| Check | Rule | Failure
|-------|------|--------
| Early use | now < not_before | DENY (I5)
| Late use | now > not_after | DENY (I5)
| Window inverted | not_after <= not_before at issuance | Reject issuance (invalid capability)

---

## 4. Request (Evaluation Input, Not a Stored Grant)

Logical request presented to ASA:

| Field | Req | Authoritative | Notes
|-------|-----|---------------|------
| `correlation_id` | YES | NO (client-supplied; server may reject duplicates per policy) | Replay handling OPEN
| `identity` / proof | YES | Via authenticator | —
| `capability_id` | YES for capability-mediated ops | Id only; record is authoritative | —
| `resource_id` | YES | NO until validated against registry/selector | —
| `operation` | YES | NO until validated against enum + capability | —
| `context` | NO | NO | Purpose etc.; optional

Client-supplied fields are **non-authoritative** until validated against authoritative stores.

**OPEN — REQUIRES AUTHORITY DECISION:** Whether correlation_id uniqueness is enforced; nonce/jti requirements.

---

## 5. Normative Evaluation Order (Schema Consistency)

1. Authenticate → Identity  
2. Resolve Principal  
3. Validate Request shape  
4. Load Capability by id  
5. Validate Scope (resource + operation ⊆ grant)  
6. Validate Expiration  
7. Validate Revocation  
8. Evaluate Policy  
9. Produce Decision  
10. Append AuthorizationEvent  
11. Perform resource side effect **only if** outcome = ALLOW and audit append succeeded (protected ops)

No step may treat GitHub permissions as Capability or Authority.

---

## 6. Failure Matrix (Schema-Aligned)

| Failure | Result
|---------|--------
| Unknown identity | DENY
| Invalid capability | DENY
| Expired capability | DENY
| Revoked capability | DENY
| Missing policy | DENY
| Policy conflict / invalid | DENY
| Policy engine unavailable | DENY
| Audit unavailable (protected ops) | DENY
| Malformed request | DENY
| Timeout / incomplete evaluation | DENY
| Partial multi-resource failure | DENY

No v0 fail-open exception without a separate Authority decision.

---

## 7. Razor Review (ASA-003)

| Removed / not introduced | Reason
|--------------------------|--------
| Separate Scope entity | Embedded in Capability
| Separate Expiration entity | Fields on Capability
| Separate Audit vs Provenance types | Single AuthorizationEvent
| Role entity | Not necessary for v0
| Signed capability fields | Opaque server-side only
| Macaroon caveats | Deferred
| DSH-specific types | Out of scope
| `claims`-driven ambient allow | Forbidden; claims non-authoritative by default
| GitHub role fields on Principal/Capability | Would violate I8

All retained fields map to invariants I1–I8 or issuance/audit necessity.

---

## 8. Consistency Check vs ASA-002

| Check | Result
|-------|--------
| Contradiction with ASA-001/002 primitives | None identified
| Hidden authority path (GitHub → ALLOW) | None; I8 explicit
| Implicit fail-open | None; matrix is DENY-only
| Ambient privilege | None; capability-bound
| Scope escalation path | Blocked by immutable operations + resource_selector checks
| Audit-as-authority | Blocked by I7 and evaluation input list

---

## 9. OPEN — REQUIRES AUTHORITY DECISION

1. Accepted `authenticator_id` set for v0 (human / agent).
2. Capability single-use vs multi-use within temporal window.
3. `resource_selector` exact language (ids vs kind/namespace vs patterns).
4. Policy `body` concrete syntax and conflict rules.
5. Replay controls beyond correlation_id (nonce/jti).
6. Global revocation epoch vs per-capability only.
7. Whether `DELEGATE` enters the Operation enum in a later gate.

These must **not** be defaulted by implementers without Authority decision.

---

## 10. Document Control

| Item | Value
|------|------
| Gate | ASA-003
| Artifact | `spec/asa/v0/data-model.md`
| Implementation | NOT authorized by this freeze alone
| Next gate | ASA-004 Authorization Core (separate authorization)

**End of ASA v0 Data Model Freeze.**
