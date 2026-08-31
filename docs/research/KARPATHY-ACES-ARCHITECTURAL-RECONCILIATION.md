# Karpathy → ACES Architectural Reconciliation

**Status:** ACCEPTED RESEARCH INPUT / STRATEGIC PRIORITY
**Date:** 2026-08-31
**Source:** Andrej Karpathy, *Software Is Changing (Again)*, YC AI Startup School, San Francisco, 2025-06-17

## 1. External signal

Karpathy's talk describes a transition from Software 1.0/2.0 toward Software 3.0, where natural language and prompts become a programming interface; LLMs become a new computational substrate; agents become a new class of software actor; autonomy becomes partial and bounded; generation must be coupled to verification; and digital infrastructure must increasingly be built for agents.

Primary source trail:

- Y Combinator AI Startup School announcement and event context.
- YC presentation: *Andrej Karpathy: Software Is Changing (Again)*.
- Synchronized transcript and slide reconstruction: Latent Space, 2025-06-17.

## 2. Architectural reconciliation

| Karpathy thesis | ACES response | Priority |
|---|---|---|
| Software 3.0 | Treat prompts, context, skills and agent policies as governed executable artifacts | P0 |
| LLM as computer / substrate | Keep models replaceable and subordinate to ACES authority | P0 |
| Jagged intelligence | Separate capability, reliability and authority | P0 |
| Anterograde amnesia | Separate context, memory, knowledge, evidence and strategy | P0 |
| System prompt learning | Introduce candidate learned-strategy lifecycle with evidence and controlled promotion | P0 |
| Partial autonomy | Formalize autonomy levels as capability/policy/authority contracts | P0 |
| Generation ↔ verification | Make verification a first-class execution boundary | P0 |
| Small changes / tight loops | Preserve AcceptedState and atomic verified transitions | P0 |
| Demo → product gap | Measure repeated successful state transitions, not isolated demos | P0 |
| Vibe coding / agent execution | Treat generated actions and artifacts as untrusted until verified | P0 |
| Build for Agents | Make ACES connector contracts agent-readable and machine-verifiable | P0 |
| Context builders | Build a provenance-preserving Context Compiler | P0 |
| Agent-native interfaces | Define capability/context/permission/state contracts across owners | P0 |

## 3. New ACES formulation

The reconciliation establishes the following working architectural formula:

`HUMAN ↔ ACES ↔ AGENTS ↔ DIGITAL WORLD`

The core execution unit is:

`Intent → Context → Evidence/Knowledge → Decision → Authority → Execution → Verification → AcceptedState`

The core trust distinction is:

`Capability ≠ Reliability ≠ Authority`

The core learning loop is:

`Experience → Reflection → Candidate Strategy → Evidence → Evaluation → Approved Strategy`

## 4. Strategic conclusion

The Karpathy signal does not prove that an ACES architectural layer is necessary. It does, however, sharpen the residual problem: as the Digital World becomes increasingly agent-native, the human's cross-system coordination burden can increase rather than disappear unless a connective layer safely carries context, authority, provenance, verification and continuity.

Therefore the **Human–Agent–Digital World Connector** becomes the highest-priority ACES research and realization target.

This is a priority decision, not an exemption from the Evidence-Before-Architecture rule.

## 5. Required falsification

The connector must still be rejected if:

- existing native agents provide equivalent cross-world continuity;
- the connector merely moves complexity into a new ACES workspace;
- human coordination effort does not materially decrease;
- authority or owner boundaries become ambiguous;
- provenance or uncertainty is degraded;
- autonomous execution cannot be reliably verified.

## 6. Success condition

A controlled treatment must demonstrate measurable reduction in human integration work against the strongest available baseline while preserving:

`agency + owner boundaries + authority + provenance + uncertainty + security + recoverability`.

Only then is the connector not merely desirable but an empirically supported architectural capability.
