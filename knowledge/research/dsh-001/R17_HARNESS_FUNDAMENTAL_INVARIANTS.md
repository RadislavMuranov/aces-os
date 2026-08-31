# R17 — Harness Fundamental Invariants v0.1 — RESEARCH CANDIDATE

**Not Canon.** Technology-neutral. Based on R16 + DSH pin evidence + cross-harness patterns.

Question: What must survive if DSH is replaced?

---

## Classification table

| # | DSH property | Evidence | Fundamental? | Class | Rationale (A–G compressed) |
|---|--------------|----------|--------------|-------|----------------------------|
| 1 | Model/runtime separation (LLM adapter plugin) | architecture.md | **Yes** | **REUSABLE** | Any modern harness needs model-neutral execution |
| 2 | Context assembly (prompt + tools + history) | systemPrompt + log | **Yes** | **REUSABLE** | Required for capability |
| 3 | Tool abstraction | ctx.tools | **Yes** | **REUSABLE** | Industry-convergent |
| 4 | Tool execution boundary (pre/exec/post) | tool pipeline | **Yes** (policy hooks) | **ADAPTABLE** | Safety requires *some* boundary; shape varies |
| 5 | Agent loop | agent-loop plugin | **Yes** | **ADAPTABLE** | Loop required; implementation replaceable |
| 6 | Plugin composition (Cordis) | Cordis | **No** as Cordis-specific | **REPLACEABLE** | Extensibility yes; Cordis is one implementation |
| 7 | Capability discovery | registry/schemas | **Yes** | **REUSABLE** | Model needs tool schemas |
| 8 | Session state | SessionEvent log | **Yes** (durable work) | **ADAPTABLE** | Persist/reconstruct; schema may differ |
| 9 | Replay/resume/fork | session APIs | **Strong candidate** | **ADAPTABLE** | Reconstructability; not always full fork |
| 10 | Typed event model | Cordis events | **No** as typed Cordis | **REPLACEABLE** | Coordination needed; bus shape varies |
| 11 | Sandbox | sandbox seam | **Safety-critical when side effects** | **ADAPTABLE** | Required for safety with shell/fs; backend varies |
| 12 | Approval / human gate | approval in base | **Yes for high-risk** | **REUSABLE** | Human intervention |
| 13 | MCP integration | docs/ecosystem | **Useful not universal** | **ADAPTABLE** | Protocol optional; tool boundary is fundamental |
| 14 | Skills packs | skill/ | **No** | **REPLACEABLE / optional** | Convenience content; ablatable |
| 15 | Hooks (product bridges) | hooks/ | **No** as Claude-bridge | **REPLACEABLE** | Interception points yes; product hooks no |
| 16 | Scheduling/jobs | jobs | **Optional** | **REPLACEABLE** | Capability-dependent |
| 17 | Observability (logs/traces) | session/telemetry | **Yes** | **REUSABLE** | Debug + audit |
| 18 | Provenance (governance-grade) | weak in DSH | **Yes for ACES** | **ACES-owned** | Not satisfied by session log alone |
| 19 | Failure recovery | request-error/compaction | **Yes** | **ADAPTABLE** | Recovery required; policy varies |
| 20 | Cancellation | documented agent handle | **Yes** | **REUSABLE** | Safety/control |
| 21 | Human intervention | approval/inbox | **Yes** | **REUSABLE** | Authority path |
| 22 | Runtime extensibility | plugins | **Yes** | **ADAPTABLE** | Mechanism varies |
| 23 | Runtime isolation | sandbox + process limits | **Yes when effects** | **ADAPTABLE** | In-process plugins weaken isolation |
| 24 | Policy enforcement | tool/fs policy | **Yes** | **ADAPTABLE** | ACES Decision above |
| 25 | Reconstructability | model-visible⇒logged | **Yes** | **REUSABLE** | Strong candidate invariant |

---

## Harness Fundamental Invariants v0.1 (candidate set)

1. **Model/runtime separation**  
2. **Explicit context assembly**  
3. **Tool abstraction + mediated execution boundary**  
4. **Agent control loop** (shape free)  
5. **Durable session record for model-visible inputs/outputs**  
6. **Reconstructability of model-visible history**  
7. **Observable execution (log/trace)**  
8. **Cancellation**  
9. **Human intervention path for high-risk actions**  
10. **Policy enforcement before side effects**  
11. **Isolation proportional to side-effect power**  
12. **Extensibility without forking the loop binary** (mechanism free)

**Not fundamental:** Cordis specifically, Skills packs, CLAUDE.md, product UI, marketplace plugins, self-modification, danger-full-access.

ACES remains independent of DSH implementation of any row marked ADAPTABLE/REPLACEABLE.
