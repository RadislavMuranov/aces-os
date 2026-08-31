# R16 — Engine-Oriented Evidence Audit (Correction)

**Pinned DSH:** `0a53fb55bea101816fa226bb964ae2bed71c343b` (dsh@0.1.2-alpha.2)  
**Prior research:** `54432fbd…` / R16 audit `a901db24…`  
**Clarification:** DSH is **not** Canon and **not** dogma. It **is** the primary **engineering candidate** for the ACES **Harness Engine**. Goal: understand → audit → harden → adapt → secure → verify → **use as engine** — not rebuild a harness from scratch.

Primary question: *Can Cordis/DSH be adapted, hardened, and secured enough to be the execution engine of ACES OS?*

---

## Engine-oriented classification

| Mechanism | Evidence (pin docs) | Classification |
|-----------|---------------------|----------------|
| Cordis runtime | architecture.md, primer | **CORE ENGINE** |
| Plugin lifecycle / reversible effects | lifecycle docs | **CORE ENGINE** |
| Profile/bundle composition | architecture.md | **SAFE TO REUSE** (config surface) |
| Agent loop (`agent-loop`) | architecture.md, agent-lifecycle | **CORE ENGINE** |
| Tool registry + pre/exec/post | architecture.md | **CORE ENGINE** |
| SessionEvent append-only log | architecture.md | **CORE ENGINE** (execution record) |
| deriveMessages / model-visible⇒logged | architecture.md | **SAFE TO REUSE** as engine invariant |
| systemPrompt assembly | core/system-prompt | **SAFE TO REUSE** / **REUSE AFTER HARDENING** (injection filters) |
| LLM adapter seam | llm packages | **SAFE TO REUSE** |
| Sandbox seam | dsh-base, sandbox packages | **REUSE AFTER HARDENING** |
| Approval / tool policy | dsh-base | **REUSE AFTER HARDENING** + **REQUIRES ACES ADAPTER** (final Decision outside) |
| MCP / external tools | guides + tools | **REUSE AFTER HARDENING** |
| fs / shell / subprocess | packages | **REUSE AFTER HARDENING** |
| Skills packs | skill/ | **MUST BE ISOLATED** until ablation proves need |
| Hooks (Claude/Codex bridges) | hooks/ | **MUST BE ISOLATED** / optional adapter |
| Self-modification plugins | self-modification/ | **MUST NOT CROSS ACES AUTHORITY BOUNDARY** |
| Marketplace/untrusted plugins | ecosystem | **MUST BE ISOLATED** / default deny |
| Web UI | web-app | **SAFE TO REUSE** (optional surface) |
| Session log as *Canonical Evidence* | mapping | **MUST NOT CROSS ACES AUTHORITY BOUNDARY** (log ≠ Canon evidence) |
| Final ALLOW/DENY on protected ops | product policy only | **MUST NOT CROSS** — ACES Decision owns |

---

## What DSH already provides (engine)

Execution loop, tool mediation, session durability/replay surface, plugin composition, model adapter seam, sandbox/approval *product* controls, observability stream.

## What prior “replaceable” language meant under correction

“Replaceable” in R17 = *implementation of Cordis could theoretically differ* — **not** a mandate to rebuild. Under this correction: **prefer reuse + harden** unless evidence shows DSH cannot safely provide the capability **and** it is not constitutionally ACES-only.
