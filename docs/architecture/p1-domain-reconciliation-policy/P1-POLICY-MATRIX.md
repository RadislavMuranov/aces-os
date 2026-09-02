# P1 Policy Matrix — Six-Provider Coverage

| Theme | Obsidian | GitHub | Slack | Gmail | Drive | Kaiten |
|-------|----------|--------|-------|-------|-------|--------|
| Identity Level 0–1 | path+epoch | SHA / issue id | ch+ts | msg id | fileId | card id |
| Cross-provider Level 2+ | explicit only | explicit only | explicit only | explicit only | explicit only | explicit only |
| Rename/move | continuity policy | n/a branch tip | n/a | n/a | fileId stable | board move PVR |
| Delete/trash/archive | delete≠trash | API delete | message_deleted | trash≠perm | trashed | condition |
| Mutable vs immutable | path mutable | branch≠SHA | ts stable | id immutable | id immutable | id |
| Edit history | content hash | commits | original text may be gone | labels | revisions | updated |
| Temporal | mtime PARTIAL | commit time | ts | internalDate | modifiedTime | created/updated |
| Staleness | Sync PVR | ref tip | retention PVR | history window | — | webhook PVR |
| Partial / permissions | FS ACL | scopes | private ch | scopes | shared-drive PVR | access |
| Default on conflict | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED | UNRESOLVED |
| Source≠ACES Authority | Yes | Yes | Yes | Yes | Yes | Yes |

All cells require **ACTIVE** policy_id@version in ResolutionRecord when resolved; otherwise CONFLICT/UNRESOLVED.
