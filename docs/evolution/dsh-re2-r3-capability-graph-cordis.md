# DSH-RE2 — R3 Capability Graph & Cordis

Status: COMPLETE
Baseline: deepseek-ai/deepseek-harness @ dd6322d604e00eec1ba5e0c8541159906a21094a
Date: 2026-09-01

## 1. Scope primitive

`dsh-scope` creates a Cordis-derived scoped Context with an opaque ScopeKey. The scope owns registrations made through the scoped context and can be disposed as a unit.

## 2. Scope hierarchy

Scope parents form an explicit tree/chain. Parent links are cycle-checked. Registration visibility inherits from ancestors, while scoped event admission flows from a dispatch key upward to matching ancestors.

## 3. Scoped registry model

`ScopedLayers` maintains a global layer plus per-scope layers. Reads can merge the global layer and ancestor layers, with the nearest scope winning name collisions. Registration is attached to the registering Cordis context through `ctx.effect()` and receives an exact undo/disposer.

## 4. Agent capability ownership

`dsh-agent` exposes an AgentHandle whose disposer is the capability to tear down the live agent. Agent creation is delegated to an AgentFactory supplied by `dsh-agent-loop`. Creation occurs in an unpublished scoped world; setup registrations are committed before publication. Failure rolls back the unpublished world.

## 5. Agent-loop capability dependencies

The concrete agent-loop imports/depends on agent, LLM, session, system-prompt, tools, session-projection and persistence interfaces. It injects these through the Cordis context rather than hard-coding a monolithic implementation.

## 6. Tool capability graph

`dsh-tools` is a scoped registry. Tool execution is intercepted by ordered capability events: `tools/pre-execute`, `tools/execute`, `tools/post-execute`. Approval is an optional seam. Scope filtering is applied to agent-scoped listeners.

## 7. Session capability graph

`dsh-session` exposes the session store through `ctx.sessions`. Session events are scope-filtered using the same scope routing mechanism. Persistence subscribes to session events/flush rather than being embedded in the session store.

## 8. Cordis role

Cordis is the substrate for:
- Context and service registration;
- plugin/fiber ownership;
- effect/disposer lifecycle;
- event dispatch;
- scoped contexts;
- dependency access.

`dsh-scope` extends Cordis with scope-aware registration and event routing.

## 9. Capability graph reconstruction

```text
Cordis Context
  |
  +-- global services/events
  |
  +-- ScopeKey
       |
       +-- scoped Context
            |
            +-- Agent
            |    +-- Agent Loop
            |    +-- LLM
            |    +-- Session
            |    +-- System Prompt
            |    +-- Tools
            |    +-- Projections
            |
            +-- scoped registrations
            +-- scoped event listeners
            +-- scoped disposers
```

## 10. Critical findings

1. Scope is an architectural primitive, not merely metadata.
2. Capability visibility and lifecycle ownership are coupled to Cordis Context.
3. Scope inheritance is explicit and cycle-checked.
4. Registry mutations have reversible ownership through Cordis effects.
5. Agent creation is transaction-like: compose -> validate/commit -> publish -> run.
6. Agent ownership is separate from durable session lineage.
7. Tool execution is an interception pipeline rather than a single hard-coded call path.
8. Session persistence is decoupled from the session core.

## 11. Privileged-core test

R3 does NOT prove that DSH has no privileged substrate. It proves that major runtime capabilities are exposed through Cordis Context/plugin/seam mechanisms. Cordis itself remains a foundational dependency and must be analyzed as the substrate in R7.

## 12. ACES relevance

The directly reusable primitives are:
- scoped capability ownership;
- hierarchical capability visibility;
- reversible registration;
- transactional publication boundaries;
- separation of provider interfaces from consumers;
- event interception at capability seams.

ACES-specific authority, policy, epistemic trust and verification are not present in this R3 evidence and remain separate concerns.

## R3 verdict

PASS — capability graph and Cordis integration are reconstructed sufficiently to proceed to R4.

Next: R4 — Context Compiler / Profiles / Bundles / Patches.
