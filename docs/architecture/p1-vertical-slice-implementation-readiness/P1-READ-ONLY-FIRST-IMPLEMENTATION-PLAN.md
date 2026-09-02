# P1 Read-Only First Implementation Plan

**Status:** PLAN ONLY — phases **not** executed  
**Principle:** smallest safe vertical demonstration without external side effects

---

## Recommended first mode

```text
READ / OBSERVE only
→ Connector → DWOM → Observation → EvidenceCandidate
→ (Admission under approved policy or structural admit rules)
→ Reconciliation (default CONFLICT/UNRESOLVED)
→ Digital World State projection
```

No CREATE/UPDATE/DELETE/EXECUTE until Phase X + write gate.

---

## Phases (not authorized by this document)

| Phase | Content |
|-------|---------|
| **I** | Provider-neutral interfaces (identity, capability, resource, op, observation, provenance, replay) |
| **II** | Read-only connector adapters (six providers; avoid PVR surfaces) |
| **III** | DWOM ingestion |
| **IV** | Observation → EvidenceCandidate → Admission |
| **V** | Reconciliation (default UNRESOLVED; resolve only with ACTIVE ApprovalRecord-bound instances) |
| **VI** | Verification integration (Axis-C) |
| **VII** | AcceptedState integration |
| **VIII** | Knowledge integration |
| **IX** | Memory / World Model integration |
| **X** | Controlled writes (separate authorization) |

---

## Provider order (recommendation only — not authorization)

| Order | Provider | Rationale |
|-------|----------|-----------|
| 1 | **GitHub** | Identity-rich (SHA/ids); official-spec FIT; native API; low PVR on core read |
| 2 | **Gmail** | Clear message≠thread; history constraints known |
| 3 | **Google Drive** | fileId≠path; avoid shared-drive PVR initially |
| 4 | **Slack** | channel+ts; avoid retention-complete claims |
| 5 | **Kaiten** | Native REST; avoid webhook-complete claims; poll-first |
| 6 | **Obsidian** | Local FS first; avoid Sync PVR entirely in first slice |

Categories: foundational (GitHub) · identity-rich · conflict-rich (cross-provider later) · PVR-dependent (last or guarded) · write-sensitive (Phase X only).

---

## PVR handling per provider

| PVR | Strategy |
|-----|----------|
| OBS-SYNC | **Avoid** — local single-vault only; no Sync claims |
| SL-RET | **Avoid** — do not claim complete history; mark PARTIAL |
| GD-SD | **Avoid** — My Drive only first; shared-drive deferred |
| KT-WH | **Avoid** — poll/API read; no webhook delivery guarantees |
