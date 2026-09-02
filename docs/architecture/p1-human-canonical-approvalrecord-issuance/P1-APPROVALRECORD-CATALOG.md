# P1 ApprovalRecord Catalog — Eligibility

**Source instances:** P1-POLICY-INSTANCE-CATALOG (~41). No new instances invented.  
**approval status column:** eligibility for Human/Canonical issuance — **not** issued ACTIVE records in-repo (issuance is Human act; this pack freezes rules + eligibility).

### Universal / safety / cross

| Instance ID | Class | PVR | Eligibility | Approver authority | Reason |
|-------------|-------|-----|-------------|-------------------|--------|
| DEF-001 | P2 | no | **APPROVABLE** | Human/Canonical | Default CONFLICT/UNRESOLVED |
| CP-001 | P1 | no | **APPROVABLE** | Human/Canonical | Level 0 local only |
| CP-002 | P1 | no | **APPROVABLE** | Human/Canonical | Explicit mapping schema; mapping *data* separate |
| CP-003 | P1 | no | **APPROVABLE** | Human/Canonical | Candidate only |
| CP-004 | P1 | no | **APPROVABLE** | Human/Canonical | Similarity ≠ identity |
| CP-005 | P2 | no | **APPROVABLE** | Human/Canonical | Cross conflict default |
| TMP-001 | P3 | no | **APPROVABLE** | Human/Canonical | No arrival authority |
| TMP-002 | P3 | no | **APPROVABLE** | Human/Canonical | Missing source → ORDERING_UNKNOWN |
| PART-001 | P2 | no | **APPROVABLE** | Human/Canonical | UNKNOWN≠FALSE |
| REPLAY-001 | P0 | no | **APPROVABLE** | Human/Canonical | Request/payload binding |
| AUTH-001 | P0 | no | **APPROVABLE** | Human/Canonical | No AcceptedState from reconcile |

### Obsidian

| ID | Eligibility | PVR | Reason |
|----|-------------|-----|--------|
| OBS-ID-001, OBS-RN-001, OBS-DEL-001, OBS-CNT-001 | **APPROVABLE** | no | Spec-verified path/epoch/delete/content conflict |
| OBS-SYNC-001 | **APPROVABLE_WITH_PVR_GUARD** or **NOT_ELIGIBLE_PENDING_LIVE_VERIFICATION** | yes | Sync races PVR |

### GitHub

| ID | Eligibility |
|----|-------------|
| GH-ID-001, GH-REF-001, GH-ISS-001, GH-FILE-001, GH-DEL-001 | **APPROVABLE** |

### Slack

| ID | Eligibility |
|----|-------------|
| SL-MSG-001, SL-THR-001, SL-ED-001, SL-DEL-001 | **APPROVABLE** |
| SL-RET-001 | **APPROVABLE_WITH_PVR_GUARD** / **NOT_ELIGIBLE_PENDING_LIVE_VERIFICATION** |

### Gmail

| ID | Eligibility |
|----|-------------|
| GM-MSG-001, GM-THR-001, GM-HIST-001, GM-DEL-001, GM-TIME-001 | **APPROVABLE** |

### Google Drive

| ID | Eligibility |
|----|-------------|
| GD-ID-001, GD-MV-001, GD-REV-001, GD-DEL-001 | **APPROVABLE** |
| GD-SD-001 | **APPROVABLE_WITH_PVR_GUARD** / **NOT_ELIGIBLE_PENDING_LIVE_VERIFICATION** |

### Kaiten

| ID | Eligibility |
|----|-------------|
| KT-ID-001, KT-ST-001, KT-ST-002, KT-DEL-001 | **APPROVABLE** |
| KT-WH-001 | **APPROVABLE_WITH_PVR_GUARD** / **NOT_ELIGIBLE_PENDING_LIVE_VERIFICATION** |

**Counts (approx):** APPROVABLE ≥ 30 · APPROVABLE_WITH_PVR_GUARD / PENDING_LIVE = 4 (OBS-SYNC, SL-RET, GD-SD, KT-WH) · DEFERRED = 0 mandatory.
