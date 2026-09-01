# DSH-RE2 — R2 Runtime / Agent State Machine

Status: COMPLETE
Baseline: deepseek-ai/deepseek-harness @ dd6322d604e00eec1ba5e0c8541159906a21094a

## State machine

Agent phase is explicitly typed:
- idle { lastTurn }
- maintenance { abort, lastTurn, wakeRequested }
- running { abort, turn, step, wakeRequested }

`status` maps idle/maintenance -> idle and running -> running.

## Driver

`wakeDriver()` transitions idle -> running and starts `kick()` under `ctx.agents.withInitiator(this, ...)`.
`kick()` repeatedly executes `turn()` until no next turn remains, then transitions running -> idle.

## Turn

Each turn:
1. validates running phase;
2. increments turn;
3. appends `turn/start`;
4. runs `preStep`;
5. appends `step/start`;
6. appends claimed user messages;
7. executes `step`;
8. appends `step/end`;
9. invokes `agent/turn-stopping` when terminal and no next-step input exists;
10. appends `turn/end`.

A pending next-turn inbox causes another turn. Step counter resets between turns.

## Pre-step

`preStep`:
- claims inbox input;
- assembles system prompt;
- renders context sections;
- projects runtime context;
- runs `agent/pre-step` waterfall;
- can reject the step;
- otherwise returns messages plus prompt assembly.

## Step

`step`:
- derives messages from session;
- builds/freeze request configuration;
- resolves LLM adapter through `prepareCall`;
- appends request header when initial/resume/config-change/series boundary requires it;
- streams LLM output;
- appends assistant chunks;
- assembles assistant message;
- appends assistant message with source chunk sequence references;
- handles request errors and optional retry;
- detects tool calls;
- executes tools;
- queues continuation as next-step when tools do not conclude the turn.

## Cancellation / maintenance

Cancellation aborts the current phase. Wakeups arriving during maintenance or after abort are latched through `wakeRequested` subject to disposal rules. Maintenance is mutually exclusive with active driver work.

## Ownership / causality

`AgentRegistry.withInitiator()` uses process-local AsyncLocalStorage for causal attribution. Source comments explicitly state that initiator presence is not liveness proof and not authorization. Agent creation has an owner context and an owned `AgentHandle` with disposal semantics.

## R2 state transition model

IDLE
 -> RUNNING on wake
 -> TURN
 -> PRE-STEP
 -> STEP
 -> [TOOL CONTINUATION -> NEXT STEP]
 -> TURN END
 -> [PENDING INPUT -> NEXT TURN]
 -> IDLE

Maintenance is a separate exclusive phase and does not execute model turns.

## Findings

CONFIRMED:
- explicit finite runtime phase model;
- explicit turn/step counters;
- abort-controlled execution;
- queued input with next-turn/next-step targets;
- prompt/context assembly before each step;
- model request construction from session-derived messages;
- durable event append at execution boundaries;
- tool calls can create continuation steps;
- retry is an explicit request-error policy;
- initiator attribution is separated from authorization.

R2 verdict: PASS.

Next: R3 — Capability Graph & Cordis.
