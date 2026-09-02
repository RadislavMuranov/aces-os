# P1 Provider Gap Register

| ID | Provider | Semantic | Why it matters | Evidence searched | Status | Impact | Adapter workaround | Blocks runtime design? |
|----|----------|----------|----------------|-------------------|--------|--------|--------------------|------------------------|
| G1 | Obsidian | Multi-device Sync races | Conflicting mtime/path | Core official docs | PVR | Reconciliation | identity_epoch + content hash; default CONFLICT | No |
| G2 | Obsidian | Plugin-generated state | Hidden observables | Core API | PVR | Partial observation | Mark plugin fields unknown | No |
| G3 | Obsidian | No native event id | FS event dedup | Vault API | PARTIAL | Replay | ACES event_id + payload_digest | No |
| G4 | GitHub | Webhook delivery guarantees | Exactly-once not assumed | REST; webhooks config-specific | PARTIAL | Replay | ACES request binding | No |
| G5 | GitHub | Force-push tip rewrite | Branch≠commit if mishandled | Official git refs | SPEC OK if modeled | DWOM | Always bind SHA not only branch name | No |
| G6 | Slack | Retention / Grid visibility | Incomplete history | Official events | PVR | Partial | Mark retention-limited | No |
| G7 | Slack | Edit loses original text | Epistemic gap | Official message event | SPEC | Partial | Preserve prior Observation if captured | No |
| G8 | Gmail | historyId validity window | Missed changes | Official history.list | SPEC | Change detection | Fail-closed on stale history; re-bootstrap | No |
| G9 | Drive | Shared-drive permission edges | Capability map | File resource | PVR | Authz | Fail-closed unknown capability | No |
| G10 | Kaiten | Webhook payload completeness | Event correlation | Webhook names documented | PARTIAL/PVR | Events | Poll fallback + ACES event_id | No |
| G11 | Kaiten | Delete constraints (e.g. time logs) | Write failures | Secondary SDK | PVR | Side effects | Typed provider errors | No |
| G12 | All | Crypto provenance authenticity | Trust of traces | P0 F5 | DEFERRED | Security | Structural provenance only | No |

**Blocking gaps: none.**
