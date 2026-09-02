# P1 Domain Reconciliation Policy v1.0

**Status:** POLICY CONTRACT (implementation NOT authorized)  
**Date:** 2026-09-03  
**Upstream:** P0 Axis-B · P1 Vertical Slice Contract · P1 Provider Semantic Verification

---

## 0. Architectural answer

> What explicit, versioned, scoped policies are required so conflicting observations can be compared (and where permitted resolved) without turning Reconciliation into a truth oracle?

**Answer:** A **ReconciliationPolicy** object model + **universal default CONFLICT/UNRESOLVED** + **priority classes P0–P5** + **provider-scoped domain policies** that never invent global provider ranking and never mint AcceptedState/Knowledge/Semantic Reality.

```text
Observations → Reconciliation (policy) → Digital World State
  → Evidence path → Axis-C Verification → AcceptedState → Knowledge
```

---

## 1. ReconciliationPolicy object

| Field | Mandatory | Notes |
|-------|-----------|-------|
| `policy_id` | **Yes** | Stable id |
| `policy_version` | **Yes** | Semver or monotonic; **always** in provenance |
| `policy_status` | **Yes** | DRAFT\|REVIEW\|APPROVED\|ACTIVE\|SUPERSEDED\|RETIRED |
| `scope` | **Yes** | Resource/domain/tenant bounds |
| `applicable_providers` | **Yes** | List or `*` with explicit justification |
| `applicable_resource_kinds` | **Yes** | |
| `applicable_fields` | Optional | Empty = whole representation under scope |
| `identity_matching_rule` | **Yes** | Level 0–4 semantics (§6) |
| `comparison_rule` | **Yes** | How values compared |
| `precedence_rule` | Optional | **Only** if resolution allowed; else omit |
| `temporal_rule` | **Yes** | Ordering / missing timestamps |
| `conflict_rule` | **Yes** | Map to taxonomy + default |
| `partial_observation_rule` | **Yes** | UNKNOWN≠FALSE |
| `staleness_rule` | **Yes** | Policy-scoped |
| `resolution_authority` | **Yes** | Who may activate/approve; **not** ACES action authz mint |
| `required_participants` | Optional | Min observation set |
| `provenance_requirements` | **Yes** | |
| `effective_from` / `effective_until` | **Yes** / Optional | |
| `supersedes` | Optional | Prior policy_id@version |
| `created_by` / `approved_by` / `approval_reference` | **Yes** for ACTIVE | |

**Unapproved policy MUST NOT execute.** Ambiguous version → **POLICY_CONFLICT**. Overlapping ACTIVE policies without deterministic precedence → **POLICY_CONFLICT**.

### Lifecycle

```text
DRAFT → REVIEW → APPROVED → ACTIVE → SUPERSEDED | RETIRED
```

No retroactive application without explicit authorization record.

---

## 2. Universal default conflict policy

**policy_id:** `aces.reconciliation.default.v1`  
**Class:** P2 Conflict Safety (always applicable when no domain policy resolves)

```text
IF material disagreement
AND no explicit applicable ACTIVE policy resolves it
THEN
  reconciliation_status = CONFLICT | UNRESOLVED
  preserve all observations + provenance
  do NOT manufacture Digital World Truth
  do NOT create AcceptedState
  do NOT promote to Knowledge
```

Forbidden defaults: latest-wins, first-wins, provider-wins, majority-wins, arrival-order-wins, lexical-wins.

---

## 3. Policy priority classes

| Class | Name | Role |
|-------|------|------|
| **P0** | Safety / Authority | Never overridable; no authz mint; no AcceptedState |
| **P1** | Identity / Provenance | Protect binding and lineage |
| **P2** | Conflict Safety | Prevent silent elimination |
| **P3** | Temporal | Ordering / staleness |
| **P4** | Domain | Provider/resource-specific |
| **P5** | Presentation | Projection/UI only |

Lower class **MUST NOT** override higher. This is **not** a source-authority ranking.

---

## 4. Temporal policy

| Clock | Role |
|-------|------|
| `source_timestamp` | Provider claim of event/state time — optional |
| `observation_timestamp` | ACES observe/ingest — mandatory on Observation |
| `arrival_timestamp` | Diagnostic only |
| `revision_timestamp` | When provider exposes revision time |

**Arrival time is not authoritative source time** unless provider semantics explicitly establish it (P1 verification: none of the six establish that as global rule).

If required order cannot be established: **ORDERING_UNKNOWN** (not invented order).

Clock skew / delayed / reordered events: remain explicit under temporal_rule; default do not invent.

---

## 5. Staleness

Classes: `fresh` | `stale` | `expired` | `unknown_freshness`.

Must be policy-scoped (resource/field). **No universal TTL** unless a named ACTIVE policy defines one with version and provenance.

Stale **MUST NOT** silently dominate under default policy.

---

## 6. Identity matching levels

| Level | Meaning | May establish identity? |
|-------|---------|-------------------------|
| **0** | Exact provider-local immutable id | Yes within provider |
| **1** | Provider-scoped stable id | Yes within provider |
| **2** | Explicit cross-provider mapping record | Yes if policy + correlation authority + provenance |
| **3** | Derived correlation (structured rules) | Only under named policy; status non-authoritative alone |
| **4** | Name/path/content similarity | **MUST NOT** silently establish identity |

Identity conflict default: **UNRESOLVED** unless policy explicitly permits resolution.

---

## 7. Field-level rules

| Category | Rule |
|----------|------|
| Immutable identity | Prefer exact id evidence; no silent merge |
| Mutable descriptive | Only with explicit temporal/source policy |
| Ownership/permission | Source-scoped; **≠** ACES authorization |
| Status | Provider-local ≠ universal semantic status without mapping |
| Content | No silent overwrite of conflicts |
| Metadata | Preserve provider scope + provenance |

---

## 8. Provider authority weight

**Forbidden:** global trusted-provider ranking.

**Allowed form only:**

```text
Provider P may be authoritative for field F
on resource class R under policy_id@version
for interval T within source scope S
```

This **never** implies ACES authorization, capability issuance, or Semantic Reality authority.

```text
Source Authority ≠ ACES Authorization Authority
```

---

## 9. Partial observation / deletion

```text
UNKNOWN ≠ FALSE ≠ ABSENT
NOT_OBSERVED ≠ ABSENT
INACCESSIBLE ≠ DELETED
```

States: DELETED | TRASHED | ARCHIVED | INACCESSIBLE | NOT_OBSERVED | UNKNOWN.

Missing field **MUST NOT** automatically overwrite existing observed field.

Tombstones only where provider evidence supports (e.g. Slack deleted_ts, Drive trashed, Kaiten condition=deleted).

---

## 10. Version / revision

- Mutable reference (e.g. GitHub branch) **≠** immutable object (commit SHA).
- Incomplete revision history → PARTIAL / UNKNOWN, not invented continuity.
- Conflicting revisions → VERSION_CONFLICT unless policy resolves.

---

## 11. Representation normalization

Path vs ID, case, Unicode, timestamps, MIME, status enums, thread vs message — may normalize **only** under versioned rules that **do not** destroy identity or provenance. Normalization affecting results **MUST** be recorded in ResolutionRecord.

---

## 12. Policy composition

Applicability deterministic. Overlap without explicit precedence → **POLICY_CONFLICT**. No best-effort selection.

---

## 13. Outcome states

`CONSISTENT` | `CONFLICT` | `UNRESOLVED` | `PARTIAL` | `STALE` | `UNKNOWN` | `RESOLVED_UNDER_POLICY`

Resolved states **retain** underlying observations.

---

## 14. Safety boundary

Reconciliation **MUST NOT:** mint capability; authorize side effects; verify Evidence; create AcceptedState; create Knowledge; mutate Semantic Reality or World Model directly; override ASA.

---

## 15. Six-provider minimum domain coverage (P4)

Grounded in P1 Provider Semantic Verification only.

| Provider | Required policy themes |
|----------|------------------------|
| Obsidian | Path-as-label; rename/move continuity; delete vs trash; Sync PVR → default CONFLICT; plugin metadata unknown |
| GitHub | Branch≠commit; force-push tip rewrite; issue/PR/blob ids; permissions source-scoped |
| Slack | channel+ts; edit loses original; delete tombstone; retention PVR → partial |
| Gmail | message≠thread≠RFC Message-ID; internalDate; history window fail-closed; trash vs permanent |
| Drive | fileId≠path; trash; revisions; shortcut targetId; shared-drive PVR fail-closed |
| Kaiten | space/board/card ids; condition/state; ordering representation≠truth; webhook PVR → poll/conflict |

Concrete domain policy **bodies** may be authored as separate ACTIVE records; this pack freezes the **schema, defaults, and required themes**.

**END**
