# ASA v0 Data Model (Frozen — ASA-003 / ASA-003.2)

**Status:** SPECIFICATION ONLY — schema freeze for ASA v0  
**Authority sources:** ASA-001, ASA-002, ASA-003, **ASA-003.1 Authority Decisions**  
**HSD-001:** OPTION B active  
**Normative rule:** GitHub/Grok administrative privilege does **not** imply ACES Authority (I8).

This document freezes the minimal v0 logical data model. It does not implement code, connect DSH, or claim Source/Deployment integrity.

**ASA-003.2:** Incorporates resolved Authority Decisions OPEN-1…OPEN-7. Those decisions are normative; silent reinterpretation is forbidden. Change requires a new Authority Decision Gate.

**ASA-003.3 (2026-11-27, owner-authorized):** narrow unfreeze for the enforcement-binding profile in §11. §0–§10 remain unchanged: no entity field, enum value, invariant, selector rule, policy rule, evaluation-order step, or failure-matrix row is added, removed, or reinterpreted. Implementation is not asserted by §11.

---

## 0. Layer Separation (Non-Negotiable)

| Layer | Owned by ASA v0? | Claim |
|-------|------------------|-------|
| **ACES Runtime Security** | YES | Protected-resource operations require Decision |
| **Repository Source Integrity** | NO | Deferred; GitHub admin can mutate source |
| **Deployment Integrity** | NO | Deferred; not part of ASA runtime boundary |

---

## 1. Design Decisions Retained from ASA-002 / ASA-003.1

| Decision | Rationale |
|----------|----------|
| Scope is an **evaluation concept** embedded in Capability | No separate Scope entity |
| Audit + Provenance = single **AuthorizationEvent** | One append-only record type in v0 |
| No first-class Role | Roles would be policy sugar later |
| No full ABAC engine | Minimal policy body only |
| No signed capabilities | Opaque server-side capability ids |
| No macaroon model | Premature complexity |
| No DSH adapter in v0 schema | Explicit non-goal |
| Expiration fields live on Capability | No separate Expiration entity |
| Revocation is a separate record keyed by capability_id | Per-capability kill-list only (v0) |
| Capabilities are **MULTI-USE** within temporal window | ASA-003.1 OPEN-2 |
| `DELEGATE` not in Operation enum | ASA-003.1 OPEN-7 |

---

## 2. Invariants (Normative)

| ID | Invariant |
|----|----------|
| I1 | No protected-resource operation without Decision |
| I2 | No Decision without authenticated Identity/Principal |
| I3 | No capability use outside granted Scope (resource selector + operations + temporal window) |
| I4 | Revoked capability cannot authorize |
| I5 | Expired capability cannot authorize |
| I6 | Policy failure cannot silently grant |
| I7 | Audit (AuthorizationEvent) cannot grant authority |
| I8 | GitHub administrative privilege does not imply ACES authority |

Any evaluation path that would violate these is a specification defect.

---

## 2.1 Authenticators (ASA-003.1 OPEN-1) — Normative

Accepted `authenticator_id` values for ASA v0:

| authenticator_id | Meaning |
|------------------|--------|
| `architectural_authority_human` | Human principal under Architectural Authority path |
| `implementation_agent` | External **execution** principal (e.g. Grok as agent) |

**Normative constraints:**

- `implementation_agent` authenticates an **execution principal only**.
- Authentication **MUST NOT** imply: Authority, Capability, policy issuance, or access to any ACES resource.
- Grok is **not** ACES Authority.
- GitHub owner/admin is **not** ACES Authority by virtue of GitHub privilege.
- Any right of an agent is determined **only** by Principal + Capability + Policy + Decision.
- GitHub/Grok administrative privilege **MUST NOT** enter the ACES authority model.

Unknown `authenticator_id` → DENY.

---

## 3. Entity Catalog

### 3.1 Identity

Verified authentication result for a subject. Non-authoritative claims must not grant rights.

| Field | Req | Mutable | Authoritative | Validation | Failure |
|-------|-----|---------|---------------|------------|--------|
| `identity_id` | YES | NO (immutable after creation) | YES | Non-empty unique id | DENY |
| `authenticator_id` | YES | NO | YES | Must be `architectural_authority_human` or `implementation_agent` | DENY if unknown |
| `subject_ref` | YES | NO | YES | Non-empty subject reference as defined by authenticator | DENY if empty/invalid |
| `verified_at` | YES | NO | YES | Valid timestamp; verification must have succeeded | DENY if missing/failed |
| `claims` | NO | NO after verify record fixed | NO (unless policy explicitly elevates a named claim) | Opaque map; must not alone produce ALLOW | Ignore for grant unless policy says otherwise |

**Failure behavior:** Unknown or failed Identity → DENY (I2).

---

### 3.2 Principal

Subject of authorization, resolved from Identity.

| Field | Req | Mutable | Authoritative | Validation | Failure |
|-------|-----|---------|---------------|------------|--------|
| `principal_id` | YES | NO | YES | Non-empty unique id | DENY |
| `identity_id` | YES | NO | YES | Must reference a verified Identity | DENY if unresolved |
| `display_label` | NO | YES | NO | Optional human label | N/A |

**Failure behavior:** Cannot resolve Principal from Identity → DENY (I2).

---

### 3.3 Operation

Closed vocabulary for v0. Not a stored entity; value on Request and Capability.

**Allowed values (normative enum):**

`READ` | `CREATE` | `UPDATE` | `DELETE` | `EXECUTE` | `EXPORT` | `IMPORT` | `AUTHORIZE` | `REVOKE`

| Aspect | Rule |
|--------|------|
| Required on Request | YES |
| Mutable on Request after acceptance | NO |
| Authoritative source of allowed set for a grant | Capability.operations + Policy |
| Unknown enum value | DENY (malformed) |
| `DELEGATE` | **NOT** part of the v0 Operation enum (ASA-003.1 OPEN-7). Multi-agent delegation is deferred to a future Authority gate. |

---

### 3.4 Resource

Protected object identity. GitHub paths are **not** ACES resource ids by default.

| Field | Req | Mutable | Authoritative | Validation | Failure |
|-------|-----|---------|---------------|------------|--------|
| `resource_id` | YES | NO | YES | Non-empty stable id | DENY if missing |
| `resource_kind` | YES | NO | YES | Must be a known v0 kind (below) | DENY if unknown for protected path |
| `namespace` | NO | NO after create | YES if used | If present, must match capability resource selector | DENY on mismatch |

**v0 resource_kind values:**

`KnowledgeObject` | `EvidenceObject` | `MemoryObject` | `DecisionObject` | `SecretObject` | `PolicyObject` | `ProtectedArtifact`

**Failure behavior:** Unknown protected target → DENY.

---

### 3.5 Capability (opaque server-side)

Issued grant. Client holds `capability_id` only; server record is authoritative.

**Semantics (ASA-003.1 OPEN-2):**

- Capabilities are **MULTI-USE** in v0.
- Valid only within `[not_before, not_after]`.
- **Expiration** is checked on **every** authorization request.
- **Revocation** is checked on **every** authorization request.
- **Single-use** capabilities are **out of scope** for v0.

**Scope (evaluation concept, embedded):** resource selector + operations[] + temporal window (`not_before` / `not_after`).

#### Resource selector (ASA-003.1 OPEN-3) — Normative

`resource_selector` MUST be exactly one of:

**A.** Exact id list:

```text
resource_id[]   // non-empty list of exact resource_id values
```

**B.** Structured selector:

```text
{ kinds: [...], namespace?: "..." }
```

- `kinds` is a non-empty list of v0 `resource_kind` values.
- `namespace` is optional.

**Explicitly prohibited:** glob, regex, arbitrary pattern languages, CEL, code-based selectors.

**Scope escalation MUST result in DENY (I3).**

| Field | Req | Mutable | Authoritative | Validation | Failure |
|-------|-----|---------|---------------|------------|--------|
| `capability_id` | YES | NO | YES | Non-empty unique id | DENY if unknown |
| `principal_id` | YES | NO | YES | Must equal request Principal | DENY if mismatch |
| `resource_selector` | YES | NO | YES | Form A or B only; must cover request resource | DENY if outside or illegal form (I3) |
| `operations` | YES | NO | YES | Non-empty subset of Operation enum; request op must be member | DENY if not (I3) |
| `not_before` | YES | NO | YES | Valid timestamp; now >= not_before | DENY if early (I5) |
| `not_after` | YES | NO | YES | Valid timestamp; now <= not_after; not_after > not_before | DENY if expired (I5) |
| `issued_under_authority` | YES | NO | YES | Must be known Authority id | DENY if unknown |
| `policy_id` | YES | NO | YES | Must reference Policy used at issuance | DENY if missing binding |
| `policy_version` | YES | NO | YES | Must match issued policy version | DENY if unbound |
| `purpose` | NO | NO | NO unless policy requires | Optional label | Policy-dependent |

**Not required in v0:** `delegation_parent_id` (ASA-003.1 OPEN-7).

**Issuance:** Only via AUTHORIZE path under Authority; not by self-assertion; not by GitHub role (I8).

**Failure behavior:** Invalid / unbound / wrong principal / out of scope / expired / revoked → DENY.

---

### 3.6 Policy

Authority-accepted rules. Not inferred from GitHub.

**Body form (ASA-003.1 OPEN-4) — Normative:**

- Policy `body` is a **structured JSON object/schema**.
- Conceptual sections only: **`issuance`**, **`use`**.
- **No** general-purpose ABAC language.
- **No** YAML DSL.
- **No** code-as-policy.
- Detailed field grammar beyond these constraints is not invented here; implementers must not expand the language without a new Authority Decision.

| Field | Req | Mutable | Authoritative | Validation | Failure |
|-------|-----|---------|---------------|------------|--------|
| `policy_id` | YES | NO | YES | Non-empty id | DENY if missing policy |
| `version` | YES | NO for a published version | YES | Monotonic non-empty version id | DENY if unknown version |
| `authority_id` | YES | NO | YES | Must be known Authority | DENY if unknown |
| `body` | YES | NO after publish | YES | Structured JSON with conceptual sections `issuance` and/or `use`; well-formed | DENY if invalid (I6) |
| `status` | YES | YES (active ↔ retired only via Authority) | YES | Must be `active` for use in ALLOW path | DENY if not active |
| `not_after` | NO | NO if set | YES | If set, policy itself not usable after | DENY if expired |

**Missing policy → DENY.**  
**Invalid policy → DENY.**  
**Conflicting policy → DENY.**  
No silent union-allow (I6).

---

### 3.7 Authority

Root of issuance. Distinct from Identity and from GitHub accounts.

| Field | Req | Mutable | Authoritative | Validation | Failure |
|-------|-----|---------|---------------|------------|--------|
| `authority_id` | YES | NO | YES | Non-empty; known to ASA | DENY path if unknown authority on grant |
| `kind` | YES | NO | YES | v0: at least `architectural_authority` | DENY if unsupported kind |
| `label` | NO | YES | NO | Optional | N/A |

**Normative:** Architectural Authority is the sole root Authority for v0 issuance. Mapping humans to Authority is operational configuration, **not** ambient GitHub admin (I8).

---

### 3.8 Decision

Explicit evaluation outcome. Produced only by ASA evaluation.

| Field | Req | Mutable | Authoritative | Validation | Failure |
|-------|-----|---------|---------------|------------|--------|
| `decision_id` | YES | NO | YES | Unique id | N/A (internal) |
| `principal_id` | YES | NO | YES | Must match resolved Principal | DENY if mismatch |
| `resource_id` | YES | NO | YES | Request resource | — |
| `operation` | YES | NO | YES | Request operation | — |
| `outcome` | YES | NO | YES | `ALLOW` \| `DENY` only | — |
| `reason_code` | YES | NO | YES | Stable machine-readable reason | — |
| `capability_id` | NO | NO | YES if present | Required for ALLOW on capability-mediated ops | DENY if ALLOW without valid capability where required |
| `policy_id` | YES | NO | YES | Policy used | — |
| `policy_version` | YES | NO | YES | Version used | — |
| `timestamp` | YES | NO | YES | Evaluation time | — |
| `correlation_id` | YES | NO | YES | Request correlation | — |

**ALLOW only if** Identity/Principal, Capability (when required), Scope, Expiration, Revocation, and Policy all pass **on this request**. Otherwise **DENY**.

**I1:** Protected-resource side effects must not occur without an ALLOW Decision for **this** request.

---

### 3.9 AuthorizationEvent (Audit + Provenance)

Single append-only event type for v0. **Never** an input that produces ALLOW (I7).

| Field | Req | Mutable | Authoritative | Validation | Failure |
|-------|-----|---------|---------------|------------|--------|
| `event_id` | YES | NO | YES | Unique | — |
| `principal_id` | YES | NO | YES | From Decision | — |
| `operation` | YES | NO | YES | From Decision | — |
| `resource_id` | YES | NO | YES | From Decision | — |
| `timestamp` | YES | NO | YES | Event time | — |
| `authority_id` | YES | NO | YES | From evaluation | — |
| `policy_id` | YES | NO | YES | From Decision | — |
| `policy_version` | YES | NO | YES | From Decision | — |
| `capability_id` | NO | NO | YES if present | From Decision | — |
| `decision` | YES | NO | YES | `ALLOW` \| `DENY` | — |
| `result_or_error_class` | YES | NO | YES | Outcome summary / error class | — |
| `correlation_id` | YES | NO | YES | Links request | — |

**Audit unavailable / cannot append for protected ops → DENY** (fail-closed).

**Provenance** in v0 = reconstructability from AuthorizationEvent records. No mandatory cryptographic signature in v0.

---

### 3.10 Revocation (ASA-003.1 OPEN-6)

Kill-list entry for a capability.

**Normative:**

- v0 uses **per-capability revocation only**.
- **Global revocation epoch** is **deferred** (not in v0).
- Revocation is checked on **every** authorization request.
- **Revocation store unavailable → DENY** for protected operations.

| Field | Req | Mutable | Authoritative | Validation | Failure |
|-------|-----|---------|---------------|------------|--------|
| `capability_id` | YES | NO | YES | Must reference existing capability | — |
| `revoked_at` | YES | NO | YES | Valid timestamp | — |
| `revoked_under_authority` | YES | NO | YES | Known Authority | — |
| `state` | YES | NO after revoke | YES | `REVOKED` | If REVOKED → DENY on use (I4) |

---

### 3.11 Expiration

Not a separate entity. Represented exclusively by Capability.`not_before` / Capability.`not_after`.

Checked on **every** authorization request (ASA-003.1 OPEN-2).

| Check | Rule | Failure |
|-------|------|--------|
| Early use | now < not_before | DENY (I5) |
| Late use | now > not_after | DENY (I5) |
| Window inverted | not_after <= not_before at issuance | Reject issuance (invalid capability) |

---

## 4. Request (Evaluation Input, Not a Stored Grant)

Logical request presented to ASA:

| Field | Req | Authoritative | Notes |
|-------|-----|---------------|------|
| `correlation_id` | YES | NO (client-supplied) | See §4.1 Replay |
| `identity` / proof | YES | Via authenticator | — |
| `capability_id` | YES for capability-mediated ops | Id only; record is authoritative | — |
| `resource_id` | YES | NO until validated against registry/selector | — |
| `operation` | YES | NO until validated against enum + capability | — |
| `context` | NO | NO | Purpose etc.; optional |

Client-supplied fields are **non-authoritative** until validated against authoritative stores.

### 4.1 Replay / Re-evaluation (ASA-003.1 OPEN-5) — Normative

ASA v0 does **NOT** require:

- uniqueness enforcement for `correlation_id`;
- nonce;
- jti;
- single-use capability.

**Mandatory invariant:**

Every **new** authorization request **MUST** undergo **fresh** authorization evaluation.

A **cached previous ALLOW MUST NOT** authorize a new operation without re-validating:

- Identity/Principal;
- Capability;
- Scope;
- Expiration;
- Revocation;
- Policy.

Repeated use of the same `correlation_id` **alone MUST NOT** imply DENY in v0.

Further replay hardening is deferred.

---

## 5. Normative Evaluation Order (Schema Consistency)

1. Authenticate → Identity (`authenticator_id` ∈ accepted set)  
2. Resolve Principal  
3. Validate Request shape  
4. Load Capability by id  
5. Validate Scope (resource + operation ⊆ grant; selector form A or B only)  
6. Validate Expiration (every request)  
7. Validate Revocation (every request; per-capability)  
8. Evaluate Policy (`issuance`/`use` JSON body; missing/invalid/conflict → DENY)  
9. Produce Decision  
10. Append AuthorizationEvent  
11. Perform resource side effect **only if** outcome = ALLOW and audit append succeeded (protected ops)

**No** step may treat GitHub permissions as Capability or Authority.

**No** step may reuse a prior ALLOW without full re-evaluation.

---

## 6. Failure Matrix (Schema-Aligned)

| Failure | Result |
|---------|--------|
| Unknown identity / unknown authenticator | DENY |
| Invalid capability | DENY |
| Expired capability | DENY |
| Revoked capability | DENY |
| Illegal or escalated resource_selector | DENY |
| Missing policy | DENY |
| Policy conflict / invalid | DENY |
| Policy engine unavailable | DENY |
| Revocation store unavailable (protected ops) | DENY |
| Audit unavailable (protected ops) | DENY |
| Malformed request | DENY |
| Timeout / incomplete evaluation | DENY |
| Partial multi-resource failure | DENY |
| Cached ALLOW without re-evaluation | **Forbidden** (must re-evaluate; failure to re-evaluate is a defect) |

No v0 fail-open exception without a separate Authority decision.

---

## 7. Razor Review

| Removed / not introduced | Reason |
|--------------------------|--------|
| Separate Scope entity | Embedded in Capability |
| Separate Expiration entity | Fields on Capability |
| Separate Audit vs Provenance types | Single AuthorizationEvent |
| Role entity | Not necessary for v0 |
| Signed capability fields | Opaque server-side only |
| Macaroon caveats | Deferred |
| DSH-specific types | Out of scope |
| Pattern/glob/regex/CEL selectors | Prohibited (OPEN-3) |
| Global revocation epoch | Deferred (OPEN-6) |
| DELEGATE / delegation_parent_id | Deferred (OPEN-7) |
| nonce/jti uniqueness as v0-must | Deferred (OPEN-5) |
| `claims`-driven ambient allow | Forbidden |
| GitHub role fields on Principal/Capability | Would violate I8 |

All retained fields map to invariants I1–I8 or issuance/audit necessity.

---

## 8. Consistency Check

| Check | Result |
|-------|--------|
| Contradiction with ASA-001/002/003.1 | None identified |
| Hidden authority path (GitHub → ALLOW) | None; I8 + §2.1 explicit |
| Implicit fail-open | None; matrix is DENY-only |
| Ambient privilege | None; capability-bound; auth ≠ authority |
| Scope escalation path | Blocked; illegal selectors DENY |
| Audit-as-authority | Blocked by I7 |
| Cached ALLOW path | Explicitly forbidden |
| Source/deployment integrity claims | None added |
| New primitives beyond ASA-003 | None |

---

## 9. Authority Decisions Incorporated (ASA-003.1)

| OPEN | Decision | Status in this document |
|------|----------|-------------------------|
| OPEN-1 | Authenticators: `architectural_authority_human`, `implementation_agent`; auth ≠ Authority | §2.1, §3.1 |
| OPEN-2 | MULTI-USE capability; exp+revoke every request; no single-use | §3.5 |
| OPEN-3 | Selector A or B only; no patterns | §3.5 |
| OPEN-4 | JSON body; issuance/use; no ABAC/YAML/code-as-policy; conflict/missing/invalid → DENY | §3.6 |
| OPEN-5 | No mandatory correlation uniqueness/nonce/jti; mandatory fresh evaluation; no cached ALLOW | §4.1 |
| OPEN-6 | Per-capability revocation only; no global epoch; store down → DENY | §3.10 |
| OPEN-7 | No DELEGATE; no delegation_parent_id | §3.3, §3.5 |

Former §9 OPEN list is **closed**. New changes require a new Authority Decision Gate.

---

## 10. Document Control

| Item | Value |
|------|------|
| Gate | ASA-003 + ASA-003.2 |
| Artifact | `spec/asa/v0/data-model.md` |
| Implementation | NOT authorized by this specification alone |
| Next gate | ASA-004 Authorization Core (**separate** authorization; not automatic) |

---

## 11. ASA-003.3 — Enforcement Binding Profile (WA-1)

**Decision ID:** ASA-003.3
**Decision class:** Authority Decision (owner-issued)
**Decision date:** 2026-11-27
**Artifact under decision:** `spec/asa/v0/data-model.md` (ASA-003.2)
**Operational record:** `docs/protection/DATA-LOSS-PROTECTION-METHOD.md` → DLPM-002

### 11.1 Owner authorization (verbatim)

> «Требую разморозить модели ASA v0 (spec/asa/v0/data-model.md) к реальной файловой границе.»

**Recorded interpretation:** ASA v0 is unfrozen for one purpose — binding its existing entities
to the real filesystem / document boundary so that `I1` becomes enforceable for agents that
carry no hooks. The interpretation is recorded, not inferred; a different reading requires a
new owner decision.

### 11.2 Scope of the unfreeze

- **Permitted:** the enforcement-binding profile in §11.3–§11.11.
- **Permitted:** the `resource_kind` values in §11.4, used only by this profile.
- **Forbidden:** modifying, removing, or reinterpreting any field, enum, invariant (I1–I8),
  selector rule, policy rule, evaluation-order step, or failure-matrix row of §0–§10.
- **Forbidden:** treating this profile as implementation, deployment integrity, or AcceptedState.

Any further change still requires a new Authority Decision Gate (ASA-004 or later).

### 11.3 Binding principle

`I1` is unchanged. This profile fixes **where** the Decision is taken: not inside an agent or
harness, but at a single write authority outside it.

> A harness, agent, bot, model, or connector is never the enforcement boundary.
> The boundary is the single point through which a mutation of a durable resource must pass.

This is required because advisory hooks are insufficient as an authority boundary
(H-CENSUS-003 §8) and because the observed loss incident executed 828 ungated calls from a
harness with no hooks (DLPM-001 §1).

### 11.4 Protected resources and resource kinds

| `resource_kind` | Durable boundary |
|---|---|
| `repository_document` | tracked files of an ACES repository tree (excluding `.git` internals) |
| `vault_document` | the Obsidian Vault — durable evidence and records |
| `corpus_artifact` | corpus, provenance, manifest, and audit artifacts |
| `external_document` | documents in an external store reached through a connector |

`Resource.resource_id` is the canonical repo-relative path or a store-qualified document id.
Pattern/gLOB/prefix-range selectors remain prohibited for grants (OPEN-3); a capability
selector is an exact path or an exact document id.

### 11.5 Operation mapping

| ASA operation | Filesystem / document event |
|---|---|
| `CREATE` | new file, directory, document, attachment, import |
| `UPDATE` | overwrite, in-place edit, append, metadata change |
| `DELETE` | unlink, trash, purge, retention expiry, branch or document deletion |
| `EXECUTE` | any command whose durable-resource effect cannot be enumerated in the manifest |
| `RENAME` / `MOVE` | **composite**: `DELETE`(source) + `CREATE`(target) in one `correlation_id` |

A composite mutation is ALLOW only if **both** component Decisions are ALLOW; one ALLOW plus
one DENY is DENY (§6, partial multi-resource failure).

`EXECUTE` is **not** authorized by static command inspection. Static inspection is a policy
input, not a security boundary: aliases, `Start-Process`, `Invoke-Expression`, script
interpreters, and MCP filesystem tools all defeat it. An `EXECUTE` request against a protected
resource is admissible only when the executing identity has no write authority over that
resource (§11.7, class E3); otherwise it resolves to DENY.

### 11.6 Request manifest (mandatory)

| Field | Rule |
|---|---|
| `correlation_id` | non-empty; groups composite operations |
| `operation` | value from §11.5 |
| `resource_id` | exact path or document id |
| `resource_kind` | value from §11.4 |
| `principal_id` | resolved Principal; client assertion is non-authoritative |
| `purpose` | why the mutation is required |
| `extends_component` | CREATE of a new durable document: the existing component it extends. `NONE` is inadmissible |
| `restore_source` | DELETE: path/hash/ref from which the resource is recoverable. Absent → DENY |
| `expected_sha256` | pre-image hash for UPDATE/DELETE |
| `content_sha256` | post-image hash for CREATE/UPDATE |

A request lacking a mandatory field is malformed → DENY (§6).

`extends_component` makes B-134 preventive rule structural rather than advisory: a new durable
document cannot be authorized without naming the existing owner it extends or replaces.

### 11.7 Execution classes and coverage rule

| Class | Where the check happens | Authority |
|---|---|---|
| E1 | harness hook — existing `aces-hook-engine.mjs` | advisory / structural |
| E2 | command or tool proxy in front of the harness | advisory / structural |
| E3 | executing identity has no write authority on the resource (ACL / separate account / container) | **authoritative** |
| E4 | the gate is the sole writer / sole committer of the store | **authoritative** |

**Coverage rule (normative):** an ALLOW is credible for a protected resource only if the
operation is constrained by **E3 or E4**. E1/E2 may block or flag, but MUST NOT be reported as
enforcement. A deployment with only E1/E2 is `ADVISORY`, not `ENFORCED`, and MUST NOT be
described as a prohibition.

### 11.8 Decision point and evidence

- One gate evaluates requests and is the only writer for protected resources (E4).
- Agents hold a **staging lease**: a staging path prefix, operations `CREATE|UPDATE`,
  `not_after`, revocable per capability. A durable-write capability is never issued to an
  agent principal.
- `AuthorizationEvent` appends to the existing ACES journal, extended with `correlation_id`,
  `operation`, `resource_id`, `capability_id`, `decision`. No second ledger is permitted —
  a parallel ledger is a competing enforcement path (B-134).
- Audit append failure → DENY (§6). Audit never grants authority (I7).
- A protected resource present with no matching AuthorizationEvent is an **integrity
  violation**, detected by reconciliation; it is not retroactively authorized.

### 11.9 Failure matrix additions

| Failure | Result |
|---|---|
| CREATE of a new durable document without `extends_component` | DENY |
| DELETE without `restore_source` | DENY |
| Composite mutation with split Decisions | DENY |
| `EXECUTE` on a protected resource by an identity holding write authority | DENY |
| Protected-resource mutation with only E1/E2 coverage | ADVISORY-DENY (not ENFORCED) |
| Reconciliation finds an unrecorded protected file | INTEGRITY-VIOLATION (fail-closed) |

### 11.10 Non-goals

Cryptographic capability signatures; global revocation epoch; delegation; egress/DLP;
protection against a compromised gate identity, an OS administrator, or the owner acting
outside the gate. These remain outside v0.

### 11.11 Implementation status

**NOT IMPLEMENTED.** This section is a specification binding only. Engine, identity boundary,
staging gate, and regression evidence are staged in DLPM-002 (W0–W6). The existing hook engine
is the E1 adapter; it is not, and must not be presented as, the authority boundary.

| Item | Value |
|---|---|
| Gate | ASA-003.3 — owner-authorized narrow unfreeze |
| Supersedes | nothing; §0–§10 unchanged |
| Implementation | NOT authorized by this section alone |
| Next gate | ASA-004 Authorization Core + DLPM-002 W6 ratification |

---

**End of ASA v0 Data Model (ASA-003.2 + ASA-003.3).**
