# P1 Provider Contract Matrix

**Status:** CONTRACT PREPARATION  
**Slice:** Obsidian · GitHub · Slack · Gmail · Google Drive · Kaiten  
**Legend:** PASS = contractually specified · PARTIAL = partial/limited · UNSUPPORTED = not assumed · PVR = PROVIDER-VERIFICATION-REQUIRED · DEFERRED = explicitly deferred

---

## Matrix

| Dimension | Obsidian | GitHub | Slack | Gmail | Google Drive | Kaiten |
|-----------|----------|--------|-------|-------|--------------|--------|
| Identity model | PASS (file/vault; path≠id) | PASS (ids + SHA) | PASS (channel/ts) | PASS (msg/thread distinct) | PASS (fileId) | PASS (space ids) |
| Namespace | vault | owner/repo/org | workspace | mailbox | drive/shared | space |
| Resource model | PASS | PASS | PASS | PASS | PASS | PARTIAL / PVR |
| Read / observe | PASS | PASS | PASS | PASS | PASS | PASS / PVR |
| Side effects | PASS (authz_ref) | PASS | PASS | PASS | PASS | PASS / PVR |
| Capability mapping | PASS | PASS | PASS | PASS | PASS | PASS / PVR |
| authorization_ref | PASS | PASS | PASS | PASS | PASS | PASS |
| Timestamps | PARTIAL (mtime) | PASS | PASS (ts) | PASS | PASS | PASS / PVR |
| Event IDs | PARTIAL | PASS | PASS | PASS | PARTIAL | PVR |
| Revisions | PARTIAL (hash/mtime) | PASS (commit) | PARTIAL (edits) | PARTIAL | PARTIAL | PVR |
| Deletion semantics | PASS | PASS | PASS | PASS | PASS (trash) | PVR |
| Partial observability | PASS | PASS | PASS | PASS | PASS | PASS |
| Provenance | PASS | PASS | PASS | PASS | PASS | PASS |
| Reconciliation inputs | PASS | PASS | PASS | PASS | PASS | PASS |
| CLA / native path | Local FS / vault | REST/GraphQL/git | Web API | Gmail API | Drive API | Kaiten API |
| MCP requirement | Only if native N/A | Only if native N/A | Only if native N/A | Only if native N/A | Only if native N/A | Only if native N/A |
| Known uncertainty | Sync/plugins PVR | Token scopes PVR | Grid/retention PVR | historyId PVR | shortcuts PVR | Full model PVR |
| Source ≠ ACES Authority | PASS | PASS | PASS | PASS | PASS | PASS |

---

## Notes

1. **PASS** on a row means the **neutral contract + mapping text** defines the boundary — not that runtime was tested.  
2. **PVR** items must be resolved in a future provider-verification or implementation gate, not by guessing.  
3. MCP is never default; never an alternate ASA path.  
4. No cell implies AcceptedState, Verification success, or Semantic Reality mutation.
