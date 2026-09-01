# DSH-RE2 — R1 Source Architecture Reconstruction

Status: COMPLETE
Baseline: deepseek-ai/deepseek-harness @ dd6322d604e00eec1ba5e0c8541159906a21094a
Date: 2026-09-01

## 1. Source architecture

DSH is a Cordis plugin runtime. The documented/source package split places model adapters, tools, sessions, agent registry, agent loop, system prompt, projections, filesystem, sandbox, approval and other capabilities in separate packages. The architecture states that the model adapter, tool registry, session log and agent loop are plugins and replaceable through composition.

## 2. Core dependency direction

Agent creation is split from agent driving:
- `dsh-agent` owns the live registry, initiator scope and factory interface.
- `dsh-agent-loop` implements the concrete `AgentFactory` and `ReactLoopAgent` driver.
- The loop injects `agents`, `sessions`, `llm`, `tools`, `systemPrompt`, and `sessionProjections`.

Source evidence: packages/core/agent/src/index.ts; packages/core/agent-loop/src/index.ts; packages/core/agent-loop/src/agent.ts.

## 3. Agent runtime

`ReactLoopAgent` maintains explicit phases: `idle`, `maintenance`, `running`.
It owns an inbox, agent-scoped context/scope, event dispatcher and runtime context projection.
The driver executes turns; each turn claims input, assembles prompt/context, runs `agent/pre-step`, then proceeds through model request and tool execution.

## 4. Session architecture

`dsh-session` implements an event-sourced session service:
- append-only session log;
- in-memory store;
- derived LLM message history.
Persistence is a separate plugin concern subscribing to `session/event` and `session/flush`.
Session events include durable creation/disposal/event/flush boundaries. Session events are validated, snapshotted/frozen and sequence-addressed.

## 5. Prompt architecture

`dsh-system-prompt` is a registry for:
- ordered system sections;
- dynamic context;
- tool schemas;
- prompt variables.
Assembly is scope-aware and passes through `system-prompt/assemble`.

## 6. Tool architecture

`dsh-tools` provides a registry plus execution pipeline:
`tools/pre-execute -> tools/execute -> tools/post-execute`, with additional result handling.
Tool execution is scope-filtered and integrates approval as an optional seam.

## 7. Projection architecture

`dsh-session-projection` defines typed projection units over committed session events. Projection definitions have state schemas and synchronous fold semantics; host consumers access derived state through `stateOf()`, while client-facing carriers can expose snapshots.

## 8. Architecture facts

CONFIRMED:
- pluginized runtime;
- separated agent registry and agent-loop implementation;
- explicit agent-scoped context;
- event-sourced session service;
- persistence separated from session core;
- ordered prompt assembly registry;
- scoped tool registry/execution pipeline;
- typed event projections;
- runtime composition via profiles/bundles/patches.

NOT YET PROVEN at R1:
- complete dependency graph;
- complete capability graph;
- absence of all privileged substrate in actual execution;
- full replacement depth of every component;
- architectural escape velocity;
- security isolation properties.

## R1 verdict

PASS — source architecture reconstructed sufficiently to proceed to R2.

Next: R2 — Runtime / Agent State Machine.
