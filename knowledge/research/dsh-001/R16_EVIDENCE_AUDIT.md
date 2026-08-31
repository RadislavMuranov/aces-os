# R16 — DSH Research Evidence Audit

**Prior research:** `research/dsh-001-system-archaeology` @ `54432fbd566b557fec4c472558a31e256608094e`  
**Pinned DSH:** `0a53fb55bea101816fa226bb964ae2bed71c343b` (dsh@0.1.2-alpha.2)  
**Method:** Re-check material claims against official DSH docs at pin (architecture.md, agent-lifecycle.md, AGENTS.md, Cordis primer) + prior research texts. **Not** a full TypeScript AST audit of every package.

---

## Claim audit table (major)

| CLAIM | SOURCE PATH | COMMIT | TYPE | EVIDENCE | CONF | VERDICT |
|-------|-------------|--------|------|----------|------|--------|
| Cordis = plugin runtime (services, inject, reversible effects) | docs/architecture.md, cordis-primer | 0a53fb55 | DIRECT (doc) | Explicit: no privileged core; plugins contribute services/events/effects | High | **SUPPORTED** |
| Fiber lifecycle PENDING→…→DISPOSED | docs site plugins/lifecycle | 0a53fb55 era | DIRECT (doc) | Documented state machine | High | **SUPPORTED** |
| Agent-loop is a plugin (`core/agent-loop`) | architecture.md core packages | 0a53fb55 | DIRECT | ctx.agentLoop listed | High | **SUPPORTED** |
| Turn/step flow pre-step→llm→tools | architecture.md turn flow; agent-lifecycle.md | 0a53fb55 | DIRECT | Sequence documented | High | **SUPPORTED** |
| Model-visible means logged | architecture.md Session log | 0a53fb55 | DIRECT | Stated invariant | High | **SUPPORTED** (doc); code path not line-audited |
| SessionEvent append-only + deriveMessages | architecture.md | 0a53fb55 | DIRECT | Documented | High | **SUPPORTED** |
| Fork/projection/resume from session stream | architecture.md | 0a53fb55 | DIRECT | Documented capabilities | Med-High | **SUPPORTED** (doc) |
| Everything is a plugin / profiles/bundles | architecture.md, product pages | 0a53fb55 | DIRECT | Documented | High | **SUPPORTED** |
| Skills package exists | AGENTS.md packages/skill | 0a53fb55 | DIRECT | Topology lists skill/ | High | **SUPPORTED** |
| Hooks package + Claude/Codex bridges | AGENTS.md packages/hooks | 0a53fb55 | DIRECT | Listed | High | **SUPPORTED** |
| Tool guarded pipeline pre/execute/post | architecture.md, agent-lifecycle | 0a53fb55 | DIRECT | Documented waterfalls | High | **SUPPORTED** |
| MCP integration | guides (mcp-memory etc.) | pin era | DERIVED | Ecosystem/docs imply MCP; full host source not audited | Med | **PARTIALLY SUPPORTED** |
| Sandbox multi-backend (Landlock/bwrap/Seatbelt) | secondary blogs + package e2b/sandbox mentions | mixed | EXTERNAL + topology | Native path not fully verified this pass | Med | **PARTIALLY SUPPORTED** |
| Approval policy in dsh-base | architecture.md dsh-base description | 0a53fb55 | DIRECT | Listed in base layer | High | **SUPPORTED** (existence) |
| In-process plugins = trust boundary | design + external audits | mixed | DERIVED | Follows from plugin-in-process model | Med-High | **SUPPORTED** as architectural implication |
| Session log = ACES governance Evidence | prior research mapping | N/A | DERIVED | Category error risk | High | **SUPPORTED** as *distinction* (log ≠ Canon evidence) |
| DSH security = ACES Authority | prior research | N/A | DERIVED | Correctly denied | High | **SUPPORTED** (denial) |
| IPI rates 17–25.5% etc. | arXiv 2608.16393 | EXTERNAL | EXTERNAL ONLY | Paper claims controlled study | Med (paper not re-run) | **EXTERNAL ONLY** — not SOURCE-VERIFIED DSH fact |
| Sandbox escape RCE (secondary posts) | zone.ci etc. | EXTERNAL | UNVERIFIED | Not confirmed against pin source | Low | **UNVERIFIED** |
| PRIMARY CONDITIONAL | prior DECISION.md | 54432fbd | DERIVED | Judgment call | Med | **PARTIALLY SUPPORTED** (reasonable; not forced by single metric) |

---

## Discrepancies / honesty gaps in prior research

1. Prior pack claimed comprehensive R1–R20 coverage while **evidence basis was documentation-primary** — correctly noted in README, but some tables read as stronger than line-level source proof → record as **confidence overstatement risk**, not false architecture claims.
2. MCP: treated as available; exact MCP host implementation lines **not** cited → **PARTIALLY SUPPORTED**.
3. Sandbox backends: partly from secondary sources → **PARTIALLY SUPPORTED**.
4. External IPI numbers must not be restated as DSH source facts → prior research mostly separated them; R16 hardens separation.
5. No claim found that DSH *is* ACES or that Canon should change — **no unsupported promotion**.

---

## Security evidence status

| Class | Status |
|-------|--------|
| SOURCE-VERIFIED DSH FACT | Sandbox/approval as product features (docs); tool pipeline hooks; developer-preview warnings |
| EXTERNAL SECURITY EVIDENCE | arXiv 2608.16393 IPI study; community defense plugins; secondary RCE claims **UNVERIFIED** |

---

## Contamination
Production **NONE** · Canon **NONE** · SCE **NONE** (this branch only adds research audit files).
