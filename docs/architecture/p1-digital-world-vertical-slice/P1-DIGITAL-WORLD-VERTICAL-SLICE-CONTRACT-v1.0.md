# P1 Digital World Vertical Slice Contract v1.0

**Status:** FROZEN for contract preparation (implementation NOT authorized)  
**Date:** 2026-09-03  
**Repository:** `RadislavMuranov/aces-os`  
**Upstream:** P0 Axis-B Contract Freeze Pack v1.0 (remediated; Adversarial Closure PASS)  
**Slice:** Obsidian · GitHub · Slack · Gmail · Google Drive · Kaiten

---

## 0. Purpose and architectural question

**Question:** What is the minimum **provider-neutral** contract that allows ACES OS to observe, represent, reconcile, authorize interaction with, and produce evidence about heterogeneous digital-world systems **without** allowing any provider to become ACES authority?

**Answer structure:**

```text
ONE provider-neutral Digital World contract
  + SIX provider mappings
  + explicit uncertainty where provider semantics are not verified
```

### Canonical path (binding — inherits P0)

```text
DIGITAL WORLD
  → CONNECTOR FABRIC
  → OBSERVATION
  → DWOM
  → RECONCILIATION → DIGITAL WORLD STATE
  → EVIDENCE CANDIDATE
  → EVIDENCE ADMISSION
  → EVIDENCE
  → AXIS-C VERIFICATION
  → ACCEPTED STATE
  → KNOWLEDGE / MEMORY / WORLD MODEL
  → SEMANTIC REALITY
```

### Frozen inequalities (P0 — not reinterpreted)

```text
Observation ≠ EvidenceCandidate ≠ Evidence ≠ Verification ≠ AcceptedState
Verification ≠ Authorization
Execution success ≠ AcceptedState
Capability ≠ Authority
Connector Capability ≠ ACES Authority
Source Authority ≠ ACES Authorization Authority
DWOM ≠ Knowledge ≠ Semantic Reality
Digital World State ≠ Semantic Reality ≠ World Model
Reconciliation Result ≠ Truth
MCP ≠ Authority ≠ Authorization
DSH ≠ Authority
Orca ≠ Authority
```

---

## 1. Provider-neutral Connector Adapter Contract

### 1.1 Identity

| Field | Requirement |
|-------|-------------|
| `connector_id` | Mandatory — ACES connector instance |
| `provider_id` | Mandatory — e.g. `obsidian`, `github`, `slack`, `gmail`, `google_drive`, `kaiten` |
| `provider_account` / tenant / workspace | Mandatory namespace at source |
| `external_identity` | Provider principal / account identity as observed |
| `identity_epoch` | Mandatory on DWOM resource identities (P0 §2.6) |

**Stable identity semantics:** Provider-local durable IDs bind as (`provider_id`, `namespace`, `external_native_id`, `identity_epoch`). Names, paths, titles, and URLs are **labels**, not identity proof.

**Rename / move:** Must not erase prior provenance; must not invent Knowledge identity; successor linkage only via explicit correlation/lifecycle record.

**Delete / recreate:** New `identity_epoch` (or tombstone + successor). Native id match after delete ≠ same identity.

**Cross-provider correlation:** Requires correlation policy, correlation authority, provenance, inspectable record, status/confidence. **MUST NOT** silently become truth or ACES authorization.

### 1.2 Capability

| Dimension | Meaning |
|-----------|---------|
| Existence | Provider exposes the operation class |
| Scope | Workspace/repo/mailbox/drive/board bounds |
| Subject / principal | Mapped ACES principal |
| Resource | Target resource binding |
| Operation | READ / CREATE / UPDATE / DELETE / EXECUTE / EXPORT / IMPORT |
| Expiration / revocation | Time-bound or revoked grants |
| `authorization_ref` | **Mandatory** for side-effecting ops — Axis-A ASA |

```text
Capability existence ≠ ACES Authority
```

A connector **MUST NOT** manufacture ACES authority, capabilities, policy, Verification, or AcceptedState.

### 1.3 Resource (provider-neutral)

| Field | Requirement |
|-------|-------------|
| `resource_id` | ACES-side or provider-native id in binding |
| `provider_id` | Mandatory |
| `resource_kind` | Typed kind (file, message, issue, card, …) |
| `namespace` | Tenant/workspace/vault/repo scope |
| `parent_refs` | Optional hierarchy |
| `external_uri` | Optional |
| `observation_timestamp` | Mandatory when observed |
| `source_timestamp` | Optional |
| `source_metadata` | Provider metadata bag |
| `representation` | Schema-bound projection |
| `version` / revision | Optional — **do not assume** all providers expose equivalent semantics |

### 1.4 Operations

| Class | Side-effecting | Notes |
|-------|----------------|-------|
| READ / observe / discover | No | Capability-gated; no `authorization_ref` for pure read **unless** policy requires it |
| CREATE / UPDATE / DELETE / EXECUTE / EXPORT / IMPORT | **Yes** | Require valid `authorization_ref` |

Absence of a capability is **not** license to invent it via MCP or ad hoc paths.

### 1.5 CLA / MCP rule

```text
MCP only when CLA / Connector / Local / Native alternative is unavailable
under the governing rule.
```

MCP-mediated side effects: **same** ASA path, **same** `authorization_ref`, **same** provenance and evidence requirements. MCP **MUST NOT** create an alternate authorization path.

---

## 2. Observation Contract

Observation is a provenance-bearing record of external intake. **It is not Evidence.**

| Field | Requirement |
|-------|-------------|
| `observation_id` | Mandatory durable id |
| `connector_id` | Mandatory |
| `provider_id` | Mandatory |
| Resource identity binding | Mandatory |
| `observation_timestamp` | Mandatory (ACES observe/ingest time) |
| `source_timestamp` | Optional |
| `arrival_timestamp` | Optional diagnostic; **not** authoritative ordering alone |
| `event_id` | Source durable id **or** ACES-assigned |
| `request_id` | Mandatory when request-scoped |
| `payload_digest` | Mandatory for side-effect and Evidence-relevant ops |
| Observed state / representation | As available |
| Source metadata | As available |
| Provenance | Mandatory |
| `identity_epoch` | When identity-bound |
| Correlation ids | As applicable |
| Partial-observation flags | Mandatory when incomplete |

**If `source_timestamp` is absent:** implementation **MUST NOT** invent authoritative temporal ordering from arrival time alone (P0 F8).

---

## 3. EvidenceCandidate / Admission / Evidence / Verification / AcceptedState

| Stage | Meaning |
|-------|---------|
| **EvidenceCandidate** | Non-admitted package from Observation(s); not Evidence |
| **Evidence Admission** | Controlled transition Candidate → Evidence under Evidence Admission policy; **≠** Verification; **≠** AcceptedState; **≠** action authorization |
| **Evidence** | Admitted package eligible for Axis-C Verification |
| **Verification** | Axis-C trusted verifier policy |
| **AcceptedState** | **Only** Evidence → Axis-C Verification → AcceptedState |

**Forbidden mint paths:** connector success, HTTP 200, tool success, agent assertion, source claim, inference, reconciliation result, status-field self-attestation.

Mandatory Candidate fields inherit P0 §7.2 (observation refs, source binding, request/payload binding, event correlation, structural provenance, freshness/validity/uncertainty).

---

## 4. Replay / idempotency

Canonical binding: (`request_id`, `payload_digest`) with operation, resource, scope, principal, source identity in provenance.

| Case | Handling |
|------|----------|
| same `request_id` + same `payload_digest` | Deterministic replay / idempotent handling; no new semantic mutation solely from replay |
| same `request_id` + different `payload_digest` (or different op/resource/scope/source) | **REJECT / CONFLICT** |
| Duplicate event (`event_id`) | Detect; no silent double-admission |
| Missing event id | ACES assigns durable observation event id; still subject to request binding |
| Stale / reordered | Policy-scoped freshness; preserve uncertainty |

Providers **need not** provide exactly-once delivery. ACES detects duplicates/conflicts at Observation / Candidate / Admission boundaries.

---

## 5. Partial observability

| Class | Rule |
|-------|------|
| Full observation | All contracted fields present and valid |
| Partial | Missing fields marked unknown/unavailable |
| Permission-limited | Explicit limitation; not silent empty |
| Deleted / inaccessible | Typed lifecycle or error; not fabricated content |
| Stale | Freshness class/bound |
| Unknown state | Remains unknown |

```text
unknown ≠ false
not observed ≠ domain absence
```

without explicit policy.

---

## 6. Reconciliation Contract

Reconciliation = comparison under **explicit policy**, not truth arbitration.

**Inputs:** Observations / DWOM representations with provenance.  
**Matching:** Identity rules (§1.1 / P0 §2.6); field-level comparison under schema.  
**Conflict:** First-class; default **CONFLICT / UNRESOLVED** if no applicable policy.  
**Resolution record (when policy applies):** `policy_id`, `policy_version`, `resolution_rule`, participants, provenance, residual uncertainty.

**Forbidden unless named policy:** latest-wins, first-wins, provider-wins, local-wins, majority-wins, arrival-order-wins, lexical-wins.

```text
Reconciliation Result ≠ Truth
```

---

## 7. Digital World State Contract

```text
Provider representations → DWOM → Reconciliation → Digital World State
```

DWS is reconciled/projected external state: provenance-bearing, policy-scoped, possibly incomplete or conflicted.

**MUST NOT** directly mutate Knowledge, Semantic Reality, or World Model. Convergence remains Observation → … → Evidence → Verification → AcceptedState → Knowledge.

---

## 8. Provider authority boundary (all six)

**Provider may assert:** externally scoped facts it controls or observes (within its API/FS semantics).

**Provider may NOT assert:** ACES authorization, ACES capability issuance, Semantic Reality truth, AcceptedState, Verification, ACES policy, ACES governance.

```text
Source Authority ≠ ACES Authorization Authority
```

---

## 9. Failure semantics (provider-neutral)

Fail-closed for: unknown/ambiguous identity; invalid/expired/revoked capability; missing policy; ASA unavailable; audit/provenance unavailable; connector/provider unavailable; partial response (mark partial); malformed observation/candidate; replay/payload mismatch; conflicting identity; unresolved reconciliation; unsupported operation; stale beyond policy.

```text
Provider API success ≠ AcceptedState
```

---

## 10. Six provider mappings

Uncertainty marked **PROVIDER-VERIFICATION-REQUIRED** where live API/FS behavior is not contractually verified in this gate.

### 10.A Obsidian

| Concern | Mapping |
|---------|---------|
| Namespace | Vault root / vault id |
| Primary resources | Note (markdown file), folder, attachment |
| Identity | Prefer durable file identity (inode/path+vault epoch **with care**); path/title = label only |
| Revision | mtime / content hash; **not** git-commit equivalent |
| Links / frontmatter | Observed as representation fields; not automatic Semantic Reality |
| Plugins | Plugin metadata = source_metadata; not ACES authority |
| CLA/native | **Local filesystem / vault API** preferred |
| MCP | Only if no adequate local/CLA path |
| Side effects | Write/create/delete require `authorization_ref` |
| Uncertainty | Plugin-generated side channels; multi-device sync races — **PROVIDER-VERIFICATION-REQUIRED** |

### 10.B GitHub

| Concern | Mapping |
|---------|---------|
| Namespace | `owner/repo`, org, installation |
| Resources | repository, branch (mutable ref), commit (immutable SHA), issue, pull_request, file (path@ref), release, workflow_run |
| Identity | Numeric/node ids + repo namespace; commit SHA immutable; branch name ≠ identity of tip content |
| Permissions | Map to capability; never to ACES Authority |
| CLA/native | **GitHub REST/GraphQL / git** preferred |
| MCP | Only if native unavailable |
| Authority | GitHub permissions ≠ ACES authorization |
| Uncertainty | Installation vs user token scopes; eventual consistency of search — **PROVIDER-VERIFICATION-REQUIRED** |

### 10.C Slack

| Concern | Mapping |
|---------|---------|
| Namespace | Workspace / team |
| Resources | channel, message, thread, user, file, reaction |
| Identity | channel_id, message `ts`, thread_ts; edits/deletes are lifecycle events |
| Timestamps | Slack `ts` as source_timestamp when present |
| CLA/native | **Slack Web API** preferred |
| MCP | Only if native unavailable |
| Uncertainty | Enterprise Grid, retention, edit history completeness — **PROVIDER-VERIFICATION-REQUIRED** |

### 10.D Gmail

| Concern | Mapping |
|---------|---------|
| Namespace | Account / mailbox |
| Resources | message, thread, label, attachment |
| Identity | RFC Message-ID ≠ Gmail message id ≠ thread id — **distinct kinds** |
| Dates | internalDate / Date header as source_timestamp when available |
| Archive/trash | Lifecycle; not silent non-existence |
| CLA/native | **Gmail API** preferred |
| MCP | Only if native unavailable |
| Uncertainty | Label semantics, delegated mailboxes, historyId gaps — **PROVIDER-VERIFICATION-REQUIRED** |

### 10.E Google Drive

| Concern | Mapping |
|---------|---------|
| Namespace | My Drive / shared drive id |
| Resources | file, folder, shortcut, revision, permission |
| Identity | Drive `fileId` stable; **path/name ≠ identity** |
| Trash | Trashed state explicit |
| Revisions | When API exposes revisions — optional field |
| CLA/native | **Drive API** preferred |
| MCP | Only if native unavailable |
| Uncertainty | Shortcut resolution, shared-drive permission models — **PROVIDER-VERIFICATION-REQUIRED** |

### 10.F Kaiten

| Concern | Mapping |
|---------|---------|
| Namespace | Space / workspace |
| Resources | board, column, card, comment, user, tag, attachment, relation |
| Identity | Provider numeric/string ids in space namespace |
| Ordering | Column/board order is representation; not Semantic Reality |
| State | Card column/status as observed_state |
| CLA/native | **Kaiten API** preferred when available |
| MCP | Only if native/CLA unavailable |
| Uncertainty | Full resource model, webhooks, id stability under board moves — **PROVIDER-VERIFICATION-REQUIRED** |

---

## 11. Cross-provider identity

Conceptual sameness across providers (e.g. “same task” in Kaiten + GitHub issue) is **only** via explicit correlation records (policy, authority, provenance, status). String equality of titles/paths/URLs is **not** identity proof.

---

## 12. Self-consistency (contract-level)

1. Two implementers share one authority model (ASA + `authorization_ref`).  
2. Provider details may differ under mappings without violating neutral contract.  
3. Observation traces to provider + connector + identity + time + provenance.  
4. Replay/conflict detectable via request/payload/event binding.  
5. Partial observability explicit.  
6. Reconciliation policy-governed.  
7–9. No provider/connector/MCP becomes ACES authority.  
10. Observation cannot mint AcceptedState.  
11. DWS cannot mint Knowledge/Semantic Reality.  
12. Future adapters remain provider-neutral at the Fabric boundary.

---

## 13. Deferred / unresolved

| Item | Status |
|------|--------|
| Runtime connectors / SDKs | NOT AUTHORIZED |
| Live provider API verification | PROVIDER-VERIFICATION-REQUIRED |
| Crypto provenance authenticity | DEFERRED (P0 F5) |
| Concrete domain reconciliation policies | Must be versioned when written |
| PR #4 merge | UNMERGED |
| G2-R1 | BLOCKED |
| Canon Promotion | NOT AUTHORIZED |

**END OF P1 VERTICAL SLICE CONTRACT v1.0**
