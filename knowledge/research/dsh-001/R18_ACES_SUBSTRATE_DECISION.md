# R18 — ACES Substrate Decision (Research Only)

**Prior:** R16 PASS WITH DOC LIMIT · R17 invariants v0.1 candidate · DSH pin `0a53fb55`  
**Allowed outcomes:** STRONG | CONDITIONAL | REFERENCE ONLY | UNSUITABLE

---

## Decision matrix (summary)

| DIMENSION | DSH EVIDENCE | ACES REQUIREMENT | FIT | GAP | RISK | MITIGATION | CONF |
|-----------|--------------|------------------|-----|-----|------|------------|------|
| Capability coverage | Full agent loop, tools, session | Execution substrate | High | Governance layers | Preview churn | Pin commit; adapter | Med-H |
| Model neutrality | Adapter seam | Required | High | DeepSeek bias in defaults | Low | Multi-adapter | High |
| Composability | Cordis plugins | Desired | High | Cordis lock-in | Med | Contract above Cordis | Med |
| Plugin architecture | Strong | Extensibility | High | In-process trust | High | Authority gate on plugins | Med |
| Context control | systemPrompt + log | Required | High | Skills coupling | Med | Ablate skills | Med |
| Session/replay | Append-only log | Reconstructability | High | ≠ AcceptedState | Med | ACES evidence layer | High |
| MCP/tools | Pipeline | Connector path | Med-H | Host depth partial | Med | Fabric above tools | Med |
| Sandbox/security | Seam + approval | Side-effect safety | Med | PI; plugin trust | **High** | ACES Decision; harden | Med |
| Authority separation | Weak (product policy) | **Must own** | Low | Delegating authority | **Critical** | Never delegate | High |
| Observability | Strong logs | Required | High | Not governance evidence | Med | Map log→evidence carefully | High |
| Evidence compatibility | Session log | Canon evidence | Low-Med | Category mismatch | High | Separate systems | High |
| Verification | Limited | Required | Low | H10 gap | High | ACES owns | High |
| Durable execution | Session persistence | Optional Temporal-class | Med | Multi-runtime | Med | Later | Med |
| Evolutionary compatibility | Self-mod exists | Controlled evolution | Conflict risk | Self-mod | High | Reject self-mod | High |
| Replaceability | Loop is plugin | Required | High | Ecosystem gravity | Med | Explicit adapter | High |
| Ecosystem risk | Marketplace plugins | Trust | Low | Supply chain | High | Deny by default | Med |
| Developer-preview risk | Explicit | Stability | Low | Breakage | High | Pin; freeze tests | High |
| Security risk | External IPI study | Fail-closed authority | Med | Measured IPI | High | Controls above DSH | Med |
| Maturity | Alpha preview | Production ACES | Low | Immature | High | Experimental only | High |
| Architectural fit | Strong execution | UH substrate | Med-H | H0/H3/H10–12 | High | Boundary below | Med-H |

---

## PRIMARY SUBSTRATE STATUS

**B. PRIMARY EXPERIMENTAL SUBSTRATE — CONDITIONAL**

(Unchanged from prior research; R16/R17 **reinforce** rather than upgrade to STRONG or downgrade to REFERENCE ONLY.)

**Conditions (non-binding research):**
1. ACES owns authority, decision, verification, evidence, evolution — never DSH.
2. DSH is behind a replaceable **Harness Contract / adapter**.
3. Pin exact DSH commit; treat preview breakage as expected.
4. Ablate skills/CLAUDE.md/hooks; no auto-import as doctrine.
5. No self-modification plugins in ACES-controlled profiles.
6. Session log is input to evidence, not substitute for Canon evidence.

**Reversible:** Yes.

---

## Research boundary (NOT implemented)

```text
ACES
 |
 +-- Semantic Reality
 +-- Intent
 +-- Decision
 +-- Authority
 +-- Verification
 +-- Evidence
 +-- Evolution Control
 |
 v
ACES HARNESS CONTRACT
 |
 v
DSH ADAPTER
 |
 v
DSH / CORDIS
 |
 +-- Agent / Tools / Plugins / Sessions / MCP
 |
 v
DIGITAL WORLD
```

---

## ACES responsibilities that must NEVER be delegated to DSH

- Canonical authority / Human-Canonical Gate  
- Authorization Decision (ALLOW/DENY) for protected resources  
- Final policy decision  
- AcceptedState / verified state transition as ACES governance  
- Canonical provenance (AuthorizationEvent-class)  
- Verification authority  
- Evolution authority / Canon promotion  

---

## Major gaps
Authority/Decision/Evidence/Verification · AcceptedState · evolution control · preview maturity · plugin trust.

## Major risks
IPI (external) · in-process plugins · marketplace · breaking changes · confusing session log with evidence.
