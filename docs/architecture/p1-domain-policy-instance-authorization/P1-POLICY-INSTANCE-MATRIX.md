# P1 Policy Instance Matrix

| Provider | Instance ID | Resource | Field | Conflict | Evidence | Catalog status | Approval for ACTIVE | Live verification |
|----------|-------------|----------|-------|----------|----------|----------------|---------------------|-------------------|
| * | DEF-001 | * | * | any unresolved | VERIFIED | APPROVED-CANDIDATE | required | n/a |
| * | CP-001…005 | cross | identity/value | IDENTITY/VALUE | VERIFIED | APPROVED-CANDIDATE | required | n/a |
| * | TMP-001/002 | * | time | TEMPORAL | VERIFIED | APPROVED-CANDIDATE | required | n/a |
| * | PART-001 | * | partial | PARTIAL | VERIFIED | APPROVED-CANDIDATE | required | n/a |
| * | REPLAY-001 | * | request | REPLAY | VERIFIED | APPROVED-CANDIDATE | required | n/a |
| * | AUTH-001 | * | safety | — | VERIFIED | APPROVED-CANDIDATE | required | n/a |
| Obsidian | OBS-ID/RN/DEL/CNT | file | id/path/content | IDENTITY/VALUE/DELETION | VERIFIED | APPROVED-CANDIDATE | required | no |
| Obsidian | OBS-SYNC-001 | file | multi-device | VALUE | **PVR** | DRAFT-CANDIDATE | required; cannot claim VERIFIED | **required later** |
| GitHub | GH-ID/REF/ISS/FILE/DEL | commit/ref/issue/file | id/ref | VERSION/IDENTITY | VERIFIED | APPROVED-CANDIDATE | required | no |
| Slack | SL-MSG/THR/ED/DEL | message/thread | ts/text | VALUE/DELETION | VERIFIED | APPROVED-CANDIDATE | required | no |
| Slack | SL-RET-001 | history | retention | PARTIAL | **PVR** | DRAFT-CANDIDATE | required | later |
| Gmail | GM-MSG/THR/HIST/DEL/TIME | message/thread | id/time | IDENTITY/TEMPORAL | VERIFIED | APPROVED-CANDIDATE | required | no |
| Drive | GD-ID/MV/REV/DEL | file | id/parent/rev | IDENTITY/VERSION | VERIFIED | APPROVED-CANDIDATE | required | no |
| Drive | GD-SD-001 | shared | permissions | PERMISSION | **PVR** | DRAFT-CANDIDATE | required | later |
| Kaiten | KT-ID/ST/DEL | card | id/state | VALUE/DELETION | VERIFIED | APPROVED-CANDIDATE | required | no |
| Kaiten | KT-WH-001 | events | webhook | PARTIAL | **PARTIAL/PVR** | DRAFT-CANDIDATE | required | later |

**Live verification column:** this gate performed **none**.
