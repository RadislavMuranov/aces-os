# H-CENSUS-003 — Harness Architecture Matrix

**Date:** 2026-09-02  
**Status:** CANONICAL RESEARCH RECORD / DECISION SUPPORT  
**Scope:** ACES OS harness ecosystem and substrate selection

## 1. Purpose

H-CENSUS-003 normalizes the observable agent-harness ecosystem by architectural function rather than product name. The objective is not to select one universal harness, but to define the ACES Harness Contract and identify the most suitable open-source execution substrate.

## 2. Preceding census

H-CENSUS-001 established the census method and functional genome. H-CENSUS-002 deduplicated the ecosystem into 17 canonical primitives:

- P01 Loop
- P02 Context
- P03 State
- P04 Planning
- P05 Capability
- P06 Connector
- P07 Execution
- P08 Environment
- P09 Sandbox
- P10 Control
- P11 Lifecycle
- P12 Agents
- P13 Workers
- P14 Evidence
- P15 Verification
- P16 Federation
- P17 Evolution

ACES-specific authority primitives remain outside the harness trust boundary:

- A01 Epistemic Authority
- A02 Decision Authority
- A03 Constitutional Authority
- A04 Proof Authority
- A05 Reality State Transition Authority

## 3. Architectural classification

| Class | Representative systems | ACES role |
|---|---|---|
| Execution Harness | DSH, OpenHands, OpenCode | Runtime / execution providers |
| Coding Harness | Codex, Claude Code, Cursor, Grok Build | Specialized execution workers |
| Orchestration Runtime | LangGraph, CrewAI | State/workflow orchestration |
| Computer / Reality Harness | Perplexity Computer, Antigravity | Reality-layer reference architectures / providers |
| Organizational Harness | QM, OpenWorker | Multi-user worker governance/reference |
| Meta-Harness | Team Harness, AgentGrid and similar systems | Federation / harness coordination |

## 4. Primary substrate decision

**Recommendation:** use DeepSeek Harness (DSH) as the initial reference **open-source Execution Substrate**, but do not make ACES dependent on DSH internals.

The dependency boundary is:

`ACES Harness Contract -> DSH Adapter -> DSH Runtime`

not:

`ACES -> DSH internals`

DSH is a developer-preview substrate and may evolve or introduce breaking changes; therefore the ACES contract must remain independently owned by ACES.

## 5. Complementary reference roles

### OpenHands
Reference for isolated runtime/environment execution and sandbox-oriented agent operation. Candidate federation provider, not the constitutional core.

### OpenCode
Strong open-source, provider-agnostic coding/runtime federation target. Candidate secondary execution provider.

### LangGraph
Reference for durable stateful orchestration, checkpointing, interruption and long-running workflows. It is better modeled as an orchestration/state provider than as ACES's sole execution substrate.

### Perplexity Computer
Important **Reality / Research Harness reference architecture**. Its programmable capabilities, skills, computer interaction and research-oriented composition demonstrate the direction of a programmable reality layer. It is not selected as an open-source substrate.

### Antigravity
Reference for one canonical runtime exposed through multiple surfaces such as UI, CLI and SDK, plus dynamic subagents, asynchronous execution and scheduled work.

### Grok Build
Reference for sandboxing, permission systems, lifecycle hooks and protocol interfaces. Hooks must not be treated as the ACES authority boundary.

### Cursor
Reference for continual harness evolution, experimentation, evaluation and model-specific harness optimization.

### QM / OpenWorker
Reference architectures for organizational and meta-harness concerns: worker isolation, scoped permissions, supervision and governance above individual agent runtimes.

## 6. ACES Harness Contract

The canonical abstraction is:

`Intent -> Capability -> Authority -> Harness -> Connector -> Execution -> Evidence -> Verification -> State Transition`

The harness executes; ACES decides whether execution is authorized and accepted.

## 7. Connector invariant

Connector selection is canonical:

**CLA -> Native/Direct -> MCP only when CLA + Native/Direct cannot correctly solve the task.**

MCP is an implementation option of P06 Connector, not the connector architecture itself.

## 8. Authority boundary

No external harness, connector, model, GitHub integration, or agent runtime is an ACES source of Architectural Authority.

Authorization remains ACES-owned and fail-closed under the established ASA model. Advisory hooks are insufficient as security or authority boundaries.

## 9. Target substrate stack

```text
ACES OS
  Constitutional Authority
  Epistemic Authority
  Decision Authority
  Proof Authority
  Reality State Authority
          |
          v
ACES Harness Contract
          |
   +------+----------------+
   |                       |
Orchestration          Execution
Provider               Substrate
   |                       |
LangGraph-class           DSH
   |                       |
   +-----------+-----------+
               |
       Environment/Sandbox
       OpenHands-class
               |
       Connector / Reality
       CLA -> Native -> MCP-if-needed
               |
        Digital World
```

This is a **contractual architecture**, not a requirement to install all listed systems locally.

## 10. Installation principle

ACES does **not** need all observed harnesses installed simultaneously.

Initial implementation should use one primary substrate and preserve federation through adapters. Other harnesses become reference implementations, benchmark targets, or optional providers.

Minimum first vertical slice:

`ACES -> Harness Contract -> DSH -> sandbox -> connector -> evidence -> verification -> AcceptedState`

## 11. Decision status

- H-CENSUS-001: accepted research basis.
- H-CENSUS-002: accepted functional deduplication basis.
- H-CENSUS-003: accepted as the current harness/substrate selection record.
- DSH: **PRIMARY REFERENCE EXECUTION SUBSTRATE CANDIDATE**.
- ACES Harness Contract: **must be ACES-owned and implementation-independent**.
- Perplexity Computer: **Reality/Research reference**, not selected substrate.
- OpenHands/OpenCode: **federation/reference providers**.
- LangGraph: **orchestration/state reference/provider**.
- MCP: **exception path only** under CLA-first connector invariant.

## 12. Verification boundary

This record captures the synchronized architectural conclusions available from the current ACES conversation branch and the repository state inspected on 2026-09-02. It is a canonical synthesis, not a cryptographic claim that every historical chat token was independently replayed.

The repository itself remains the implementation source of truth for code and committed specifications.
