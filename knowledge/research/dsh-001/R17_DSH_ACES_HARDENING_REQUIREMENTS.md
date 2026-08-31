# R17 — DSH → ACES Hardening Requirements

**Research only.** Target: hardened DSH as physical execution engine under ACES control plane.

| Subsystem | Current capability | Trust level | Attack surface | Failure mode | ACES requirement | Hardening | Adapter | Verification |
|-----------|-------------------|-------------|----------------|--------------|------------------|-----------|---------|--------------|
| Cordis | Plugin mount/DI/events | High for composition; plugins in-process | Malicious/buggy plugin = process trust | Cascade unload/fail | Stable engine kernel | Pin version; restrict load sources | Thin host only | Boot tree dump / allowlist |
| Plugin loading | Dynamic composition | Low for untrusted | Code exec | RCE/supply chain | Only signed/allowlisted plugins in ACES profiles | Allowlist; no market default | Profile gate | Audit log of mounts |
| Plugin trust | In-process peers | **Low** | Confused deputy | Privilege bleed | Treat install as root-equivalent | Deny-by-default | N/A | Inventory |
| Agent loop | Turn/step driver | Med | Prompt/tool chain | Stuck/unsafe loops | Mediated by ACES Decision for protected steps | pre-step policy hooks | Contract: enter only if authorized | Trace step IDs |
| Tool execution | Guarded pipeline | Med | Tool args/results | Side effects | No protected side effect without ACES Decision | post-policy wrapper | Adapter intercept | Result attestation |
| MCP | External tools | Low-Med | Untrusted results | IPI | Taint + gate privileged follow-ons | Result quarantine | Connector Fabric map | Origin tags |
| Skills | Content packs | Low | Skill channel IPI (external study) | Instruction injection | No auto-load; ablation | Disable until evidence | Optional later | Necessity test |
| Hooks | Bridges + waterfalls | Med | Bypass paths | Policy skip | ACES-owned enforcement hooks only | Strip foreign bridges by default | Map to ACES policy | Hook audit |
| Context | Prompt assembly | Med | Injection in sections | Contaminated model input | Untrusted content labeled | Sanitize/assemble rules | Inject only authorized context | Context hash |
| Session state | Append-only events | High as log | Tamper if storage weak | Incomplete replay | Integrity of engine log | Signed/append-only store | Export to ACES evidence | Replay tests |
| Filesystem | fs policy | Med | Path escape | Data loss/leak | Workspace bounds | Fail-closed paths | Policy from ACES | Path audit |
| Shell | subprocess | Low-Med | Command injection | Host compromise | Sandbox + approval | Always sandboxed for ACES | Argv policy | Command log |
| Sandbox | Multi-backend seam | Med | Escape (claims unverified) | Breakout | Defense in depth | Prefer strongest backend; monitor | N/A | Confinement tests |
| Approval | Product UX | Med | User fatigue | Rubber-stamp | ACES Decision supersedes | Map approval → DecisionObject | **Required** | Decision ID on exec |
| Secrets | Env scrub patterns (reported) | Med | Leak via tools | Credential theft | No secret in model/tool args outbound | Redact sinks | Vault outside DSH | Secret scan |
| Events | Cordis + session | High observability | Log injection | Misleading audit | Separate live vs durable | Schema validation | Forward selected events | Schema tests |
| Persistence | Session plugins | Med | Corruption | Lost continuity | Durable engine state | Backup/integrity | Export API | Resume tests |
| Replay | From SessionEvent | High design | Incomplete events | Non-reproducible | Reconstructability | Enforce model-visible⇒logged | ACES may re-verify | Golden replays |
| Observability | Telemetry/UI | Med | PII in traces | Leak | Redaction policy | Filter | Export | Access control |

**Scaffolding:** CLAUDE.md / Skills / Hooks do **not** auto-inherit; only via observed failure → experiment → ablation → necessity.
