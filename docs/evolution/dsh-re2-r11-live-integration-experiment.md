# DSH-RE2 — R11 Live Integration Experiment / Instrumented DSH Adapter

Status: BLOCKED — LIVE EXECUTION NOT VERIFIED
Baseline: deepseek-ai/deepseek-harness @ dd6322d604e00eec1ba5e0c8541159906a21094a
Date: 2026-09-01

## Objective

Execute the R10 vertical slice against the real DSH runtime and prove the runtime boundary with observable evidence.

## Source verification

The baseline exposes independent core packages for scope, agent, agent-loop, tools, system-prompt and session. The repository also contains runtime-closure verification and agent lifecycle documentation. Tool execution is represented by tool/call and tool/result events; lifecycle documentation describes driver/tool classification and execution. These establish the integration points but are not themselves a live run.

## Required live experiment

```text
Test Intent
  -> ACES authorization PASS
  -> construct authorized runtime
  -> start DSH agent
  -> deterministic test capability
  -> capture DSH session events
  -> convert selected events through Evidence Adapter
  -> provenance check
  -> verification PASS
  -> AcceptedState
```

## Negative tests required

A. Authorization DENY -> no DSH execution.
B. Unauthorized capability -> BLOCK.
C. Tool execution failure -> no AcceptedState.
D. Missing evidence/provenance -> no AcceptedState.
E. Verification failure -> no AcceptedState.
F. Model output attempting direct acceptance -> BLOCK.
G. DSH approval without ACES authorization -> BLOCK.

## Instrumentation requirements

Capture at minimum:
- ACES request ID;
- authorization decision;
- effective capability set;
- compiled runtime/profile/patch identity;
- DSH session ID;
- ordered event sequence;
- tool call/result;
- execution result;
- evidence IDs;
- provenance links;
- verification result;
- final AcceptedState transition or BLOCK reason.

## Current result

The available GitHub connector permits source inspection and repository mutation, but it does not provide a command-execution/runtime-test action for executing the DSH TypeScript workspace from this session. Therefore a real runtime execution cannot be honestly marked PASS from the available evidence.

No fabricated execution result is recorded.

## R11 verdict

BLOCKED — source/integration boundary is sufficiently identified, but live execution evidence is absent.

This is an explicit evidence gap, not an architectural failure.

Next action: execute the instrumented adapter in an environment capable of installing/building/running the DSH workspace, then attach raw run evidence and update this record to PASS or FAIL.
