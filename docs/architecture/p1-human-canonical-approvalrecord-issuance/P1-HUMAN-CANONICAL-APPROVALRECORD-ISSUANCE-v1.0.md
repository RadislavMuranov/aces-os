# P1 Human/Canonical ApprovalRecord Issuance v1.0

**Status:** AUTHORIZATION CONTRACT  
**Date:** 2026-09-03  
**Upstream:** Domain Policy Instance Authorization @ `5f213329…`

---

## 1. Object distinctions (frozen)

| Object | Meaning |
|--------|---------|
| **A. Candidate Policy Instance** | Catalog entry; not approved |
| **B. Approved Policy Instance** | Instance has valid ApprovalRecord in APPROVED state |
| **C. Active Policy Instance** | Approved + within effective interval + not superseded/revoked |
| **D. PolicyInstanceApprovalRecord** | Human/Canonical metadata authorizing **policy use** |
| **E. Runtime authorization** | Future engine may *consume* active instance for reconciliation only |
| **F. Execution AuthorizationRecord** | ASA path for side effects — **separate**; never this record |

---

## 2. PolicyInstanceApprovalRecord (canonical)

| Field | Mandatory |
|-------|-----------|
| `approval_id` | Yes |
| `policy_id` | Yes |
| `policy_version` | Yes |
| `policy_instance_id` | Yes |
| `policy_instance_version` | Yes |
| `policy_class` | Yes (P0–P5) |
| `scope` | Yes |
| `provider_scope` | Yes |
| `resource_scope` | Yes |
| `field_scope` | Yes (or explicit `*`) |
| `policy_digest` | Yes |
| `instance_digest` | Yes |
| `approver` | Yes |
| `approval_authority` | Yes (Human/Canonical path) |
| `approval_timestamp` | Yes |
| `effective_from` / `effective_until` | Yes / Yes (no implicit indefinite) |
| `approval_reason` | Yes |
| `evidence_refs` | Yes |
| `supersedes` | Optional |
| `status` | Yes: DRAFT\|REVIEW\|APPROVED\|ACTIVE\|SUPERSEDED\|RETIRED\|REVOKED |
| `created_by` / `created_at` | Yes |
| `pvr_guard` | Yes: NONE\|EXPLICIT_PVR\|PENDING_LIVE |
| `dual_control_waiver` | Optional; if present must be auditable |

Additional required for verification: digests must match current policy/instance bodies at activation time.

---

## 3. Lifecycle

```text
DRAFT → REVIEW → APPROVED → ACTIVE → SUPERSEDED | RETIRED | REVOKED
```

| Transition | Who | Rule |
|------------|-----|------|
| Create DRAFT | Design principal | |
| REVIEW | Reviewer (Human/Canonical) | |
| APPROVED | Approver under `approval_authority` | Eligibility § Issuance Rules |
| ACTIVE | Activation after APPROVED when `now ∈ [effective_from, effective_until]` | Digest match |
| SUPERSEDED | New approval supersedes | Old inactive |
| REVOKED | Canonical authority | Immediate inactive |
| RETIRED | End of life | |
| Expiry | Automatic | status not ACTIVE after effective_until |
| Digest change | Automatic invalidation | Re-approval required |
| Scope change | Invalidates | Re-approval |
| Provider semantics change / PVR invalidated | May force REVOKED or re-approval | Explicit |

**Forbidden:** approval by runtime success, model confidence, or provider authority alone.

**Dual control:** optional; if used, both approvers recorded; waiver of dual control must be explicit in `dual_control_waiver` + reason.

---

## 4. Human/Canonical boundary

Approval authorizes **use of a specific policy instance** under scope + interval for **reconciliation comparison only**.

**Does NOT authorize:** execution, connector side effects, capability issuance, ASA bypass, Execution AuthorizationRecord, Evidence admission, Verification, AcceptedState, Knowledge promotion, Semantic Reality mutation.

```text
Policy Approval ≠ Execution Authorization
Policy Activation ≠ AcceptedState
ApprovalRecord ≠ Evidence
ApprovalRecord cannot mint Evidence or AcceptedState
```

Write to GitHub/Slack/Gmail/Drive/Kaiten/Obsidian still requires **ASA + authorization_ref**.

---

## 5. Boundaries preserved

```text
Policy Instance ≠ Authority ≠ Capability ≠ AuthorizationRecord
ApprovalRecord ≠ Execution Authorization
Source Authority ≠ ACES Authorization Authority
Reconciliation Resolution ≠ Truth
Evidence ≠ Authorization · Verification ≠ Authorization
AcceptedState ≠ Policy Activation
PVR ≠ VERIFIED
Digital World State ≠ Semantic Reality
```

**END**
