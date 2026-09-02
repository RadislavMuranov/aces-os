# P1 Policy Instance Catalog

**Convention:** status below is **catalog candidate status**. Promotion to ACTIVE requires PolicyInstanceApprovalRecord.  
**evidence_basis:** from P1 Provider Semantic Verification — PVR never listed as VERIFIED.

---

## Universal / cross-provider

### DEF-001 `aces.p1.default.conflict_unresolved.v1`
- **class:** P2 · **provider:** `*` · **fields:** * · **level:** n/a  
- **resolution_rule:** NO_AUTO_RESOLVE → CONFLICT/UNRESOLVED; preserve all observations  
- **precedence_rule:** NONE  
- **evidence_basis:** VERIFIED (architecture)  
- **catalog_status:** APPROVED-CANDIDATE (default always applicable when no domain resolve)

### CP-001 `aces.p1.cross.identity_level0.v1`
- Exact provider-local immutable/stable id only; no cross inference  
- **class:** P1 · **evidence_basis:** VERIFIED

### CP-002 `aces.p1.cross.explicit_mapping.v1`
- Requires mapping record, authority, provenance, interval  
- **class:** P1 · **evidence_basis:** VERIFIED (schema); instances of mappings PARTIAL until issued

### CP-003 `aces.p1.cross.derived_correlation_candidate.v1`
- Candidate only; **MUST NOT** establish identity  
- **class:** P1 · **evidence_basis:** VERIFIED

### CP-004 `aces.p1.cross.similarity_no_identity.v1`
- Name/path/content similarity → never identity  
- **class:** P1 · **evidence_basis:** VERIFIED

### CP-005 `aces.p1.cross.conflict_default.v1`
- Cross-provider value conflict → CONFLICT/UNRESOLVED  
- **class:** P2 · **evidence_basis:** VERIFIED

### TMP-001 `aces.p1.temporal.no_arrival_authority.v1`
- Arrival not authoritative source order  
- **class:** P3 · **evidence_basis:** VERIFIED

### TMP-002 `aces.p1.temporal.missing_source_ordering_unknown.v1`
- Missing source_timestamp when order required → ORDERING_UNKNOWN  
- **class:** P3 · **evidence_basis:** VERIFIED

### PART-001 `aces.p1.partial.unknown_not_false.v1`
- UNKNOWN≠FALSE≠ABSENT; NOT_OBSERVED≠DELETED; INACCESSIBLE≠DELETED  
- **class:** P2 · **evidence_basis:** VERIFIED

### REPLAY-001 `aces.p1.replay.request_payload_binding.v1`
- same request_id + different payload_digest → REJECT/CONFLICT  
- **class:** P0 · **evidence_basis:** VERIFIED (P0)

### AUTH-001 `aces.p1.safety.no_acceptedstate_from_reconcile.v1`
- Resolution MUST NOT mint AcceptedState/Knowledge/ASA  
- **class:** P0 · **evidence_basis:** VERIFIED

---

## Obsidian

| ID | Resource/fields | Rule summary | evidence_basis |
|----|-----------------|--------------|----------------|
| OBS-ID-001 | file identity | Path is label; binding path+vault+identity_epoch; path≠immutable content id | VERIFIED |
| OBS-RN-001 | rename/move | Continuity only with explicit lifecycle/epoch evidence; else new epoch | VERIFIED |
| OBS-DEL-001 | delete/trash | delete≠trash; do not map inaccessible→deleted | VERIFIED |
| OBS-CNT-001 | content | Conflicting content → VALUE_CONFLICT unless approved resolve | VERIFIED |
| OBS-SYNC-001 | Sync multi-device | PVR → default CONFLICT; no silent merge | **PVR** |

## GitHub

| ID | Resource/fields | Rule summary | evidence_basis |
|----|-----------------|--------------|----------------|
| GH-ID-001 | commit | SHA immutable identity Level 0 | VERIFIED |
| GH-REF-001 | branch/tag | Mutable ref ≠ commit; tip rewrite updates projection only | VERIFIED |
| GH-ISS-001 | issue/PR | Numeric id / node_id stable in repo scope | VERIFIED |
| GH-FILE-001 | path@ref | Path at ref is representation; content identity via blob SHA when available | VERIFIED |
| GH-DEL-001 | deletion | API delete states; not_observed≠deleted | VERIFIED |

## Slack

| ID | Resource/fields | Rule summary | evidence_basis |
|----|-----------------|--------------|----------------|
| SL-MSG-001 | message | Identity = channel_id + ts | VERIFIED |
| SL-THR-001 | thread | thread_ts links; thread≠message | VERIFIED |
| SL-ED-001 | edit | Preserve edit event; no fabricate prior text if unavailable | VERIFIED |
| SL-DEL-001 | delete | message_deleted / deleted_ts tombstone | VERIFIED |
| SL-RET-001 | retention/Grid | PVR → PARTIAL history allowed | **PVR** |

## Gmail

| ID | Resource/fields | Rule summary | evidence_basis |
|----|-----------------|--------------|----------------|
| GM-MSG-001 | message | API id immutable; ≠ RFC Message-ID | VERIFIED |
| GM-THR-001 | thread | threadId distinct from message id | VERIFIED |
| GM-HIST-001 | history | Stale historyId → fail-closed re-bootstrap; not invent | VERIFIED |
| GM-DEL-001 | trash/delete | trash≠permanent delete | VERIFIED |
| GM-TIME-001 | internalDate | Use as source_timestamp when present | VERIFIED |

## Google Drive

| ID | Resource/fields | Rule summary | evidence_basis |
|----|-----------------|--------------|----------------|
| GD-ID-001 | file | fileId identity; path/name≠id | VERIFIED |
| GD-MV-001 | move | Parent change; same fileId | VERIFIED |
| GD-REV-001 | revision | revisionId; incomplete history → PARTIAL | VERIFIED |
| GD-DEL-001 | trash | trashed flag; ≠ permanent delete | VERIFIED |
| GD-SD-001 | shared drive | PVR permission edges → fail-closed unknown capability | **PVR** |

## Kaiten

| ID | Resource/fields | Rule summary | evidence_basis |
|----|-----------------|--------------|----------------|
| KT-ID-001 | card/board/space | Integer ids (+ space uid) Level 0/1 | VERIFIED |
| KT-ST-001 | state/condition | condition live/archived/deleted; state queued/inProgress/done — provider-local | VERIFIED |
| KT-ST-002 | conflicting status | VALUE_CONFLICT → UNRESOLVED unless ACTIVE domain resolve | VERIFIED |
| KT-DEL-001 | archive/delete | condition-based; not_observed≠deleted | VERIFIED |
| KT-WH-001 | webhooks | PVR completeness → poll/partial; no silent event truth | **PARTIAL/PVR** |

**Catalog count:** 11 universal/cross + 5×6 provider-themed = **41** candidate instances (provider rows 5 each × 6 + universals).
