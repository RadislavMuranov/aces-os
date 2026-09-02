# P1 Domain Policy Instance Authorization v1.0

**Status:** AUTHORIZATION CONTRACT (runtime use NOT authorized by this pack alone)  
**Date:** 2026-09-03  
**Upstream:** P1-DOMAIN-RECONCILIATION-POLICY-v1.0 @ `b8fc7c8e…`

---

## 1. DomainReconciliationPolicyInstance (canonical)

Every instance **MUST** include all fields below. Unstated defaults are **forbidden**.

| Field | Requirement |
|-------|-------------|
| `policy_id` | Stable id (e.g. `aces.p1.obsidian.path_identity.v1`) |
| `policy_version` | Exact version string |
| `status` | DRAFT\|REVIEW\|APPROVED\|ACTIVE\|SUPERSEDED\|RETIRED |
| `policy_class` | P0\|P1\|P2\|P3\|P4\|P5 |
| `scope` | Textual + structured bounds |
| `applicable_provider` | One of six or `cross` |
| `applicable_resource_kind` | e.g. file, message, commit |
| `applicable_resource_scope` | Namespace pattern |
| `applicable_fields` | Explicit field list or `representation_identity` |
| `identity_matching_level` | 0–4 (Level 4 never auto-identity) |
| `comparison_rule` | Deterministic |
| `precedence_rule` | Explicit or `NONE` (→ no auto-resolve) |
| `temporal_basis` | Allowed clocks + missing-clock behavior |
| `staleness_rule` | Explicit |
| `conflict_types` | Taxonomy codes |
| `partial_observation_rule` | UNKNOWN≠FALSE etc. |
| `deletion_semantics` | PRESENT/DELETED/TRASHED/… |
| `version_semantics` | Mutable vs immutable |
| `resolution_rule` | Or `NO_AUTO_RESOLVE` |
| `resolution_authority` | Approval path; **not** ASA action mint |
| `required_participants` | Min observations |
| `required_provenance` | Mandatory refs |
| `effective_interval` | from/until |
| `supersedes` | Prior id@version or null |
| `approval_reference` | Required for ACTIVE |
| `approved_by` | Principal for ACTIVE |
| `created_by` | Principal |
| `content_digest` | Hash of canonical instance body |
| `evidence_basis` | VERIFIED\|PARTIAL\|PVR\|UNSUPPORTED\|DEFERRED |

```text
ACTIVE is an authorization state for a policy instance,
NOT evidence that resolution output is true.
```

---

## 2. Lifecycle

```text
DRAFT → REVIEW → APPROVED → ACTIVE → SUPERSEDED | RETIRED
```

| Action | Rule |
|--------|------|
| Create | Any design principal → DRAFT |
| Review | Distinct reviewer recommended; may equal creator only if approval_reference records dual-control waiver |
| Approve | Requires PolicyInstanceApprovalRecord |
| Activate | Only from APPROVED; effective_from ≤ now ≤ effective_until |
| Supersede | New ACTIVE points supersedes; old → SUPERSEDED |
| Revoke | → RETIRED; future use REJECTED |
| Overlap | Incomparable ACTIVE pair → **POLICY_CONFLICT** |

Creator and approver **may** be the same only with explicit dual-control waiver in approval_reason (governance risk accepted by Human/Canonical Authority).

---

## 3. Composition (deterministic)

When multiple ACTIVE instances apply:

1. scope match  
2. policy_class (P0 > P1 > … > P5)  
3. version (explicit supersession)  
4. specificity (narrower resource/field wins if declared)  
5. explicit precedence_rule  
6. effective_interval  
7. approval requirements  

If still incomparable → **POLICY_CONFLICT**. No invented precedence.

Lower class **MUST NOT** override P0 Safety/Authority.

---

## 4. Cross-provider instances (mandatory)

| ID | Level | Rule |
|----|-------|------|
| CP-001 | 0 | Provider-local exact id only; no cross inference |
| CP-002 | 2 | Explicit mapping record + authority + provenance + interval |
| CP-003 | 3 | Correlation **candidate** only; not identity |
| CP-004 | 4 | Similarity **never** establishes identity |
| CP-005 | — | Cross-provider value conflict → CONFLICT/UNRESOLVED unless approved resolve instance |

**Forbidden:** global `Provider A > Provider B`.

---

## 5. Temporal / staleness / partial / deletion / version

- Arrival **MUST NOT** be sole authoritative order (temporal_basis must say so).
- Missing source time → ORDERING_UNKNOWN / TEMPORAL_CONFLICT when order required.
- Stale ≠ deleted ≠ false.
- UNKNOWN ≠ FALSE ≠ ABSENT; NOT_OBSERVED ≠ DELETED; INACCESSIBLE ≠ DELETED; PARTIAL ≠ COMPLETE.
- Mutable ref ≠ immutable revision (GitHub branch ≠ commit SHA).
- “Latest observed” ≠ truth.

---

## 6. Authority boundaries

```text
Policy Instance ≠ ACES Authority ≠ ASA ≠ Capability ≠ AuthorizationRecord
≠ Verification ≠ Evidence ≠ AcceptedState ≠ Knowledge ≠ Semantic Reality
Source Authority ≠ ACES Authorization Authority
Reconciliation Resolution ≠ Truth
```

Policy constrains **future** reconciliation comparison only; **no** side-effect authorization.

---

## 7. Resolution binding

Every resolution under ACTIVE instance **MUST** bind ResolutionRecord fields (P1-RESOLUTION-RECORD-SPEC) including `policy_id`, `policy_version`, `content_digest` match, approval_reference.

If binding impossible → instance **NOT AUTHORIZABLE**.

**END**
