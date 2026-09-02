# P1 Provider Semantic Matrix

**Legend:** S = VERIFIED-BY-OFFICIAL-SPEC · P = PARTIAL · PVR = PROVIDER-VERIFICATION-REQUIRED · N = native preferred

| Dimension | Obsidian | GitHub | Slack | Gmail | Drive | Kaiten |
|-----------|----------|--------|-------|-------|-------|--------|
| Stable identity | P (path mutable) | S (SHA/ids) | S (ch+ts) | S (msg id) | S (fileId) | S (int id) |
| Namespace | vault | owner/repo | workspace | mailbox | drive | space |
| Rename | S (path changes) | S | S | n/a labels | S (name≠id) | S |
| Move | S | S | n/a | n/a | S | S / PVR |
| Delete | S (delete/trash) | S | S | S trash/perm | S trash/perm | S condition |
| Recreate | PVR (epoch needed) | S new id/SHA | S new ts | S new id | S new fileId | S new id |
| Revision/version | P (hash) | S (SHA) | P (edit) | P | S (revisionId) | P |
| Event ID | P | P (webhook) | S (event_id) | P (historyId) | P (changes) | P / PVR |
| Change feed | P (FS watch) | P | S Events API | S history.list | P changes | P webhooks |
| Source timestamp | P (mtime) | S | S (ts) | S internalDate | S modifiedTime | S created/updated |
| Ordering | P | S graph | S ts | S internalDate | P | P |
| Partial observability | S | S | S | S | S | S |
| Permissions | local FS | S scopes | S scopes | S scopes | S | S / PVR |
| Side effects | S | S | S | S | S | S |
| Idempotency primitives | P | P | P | P | P | P |
| Native/CLA path | N FS | N API/git | N Web API | N Gmail API | N Drive API | N REST |
| MCP necessity | only if no local | only if no native | only if no native | only if no native | only if no native | only if no native |
| Evidence readiness | S w/ adapter | S | S | S | S | S w/ residual PVR |
| Confidence | HIGH core / PVR sync | HIGH | HIGH core / PVR Grid | HIGH | HIGH / PVR shared | MED–HIGH |
| Contract fit | FIT+NORM | FIT | FIT+NORM | FIT | FIT | FIT+NORM |
