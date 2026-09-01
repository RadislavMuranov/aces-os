# DSH-RE2 — R6 Sandbox / Approval / Security Boundaries

Status: COMPLETE
Baseline: deepseek-ai/deepseek-harness @ dd6322d604e00eec1ba5e0c8541159906a21094a
Date: 2026-09-01

## Findings

1. Sandbox is a capability seam. `ctx.sandbox.confine(argv, policy)` returns enforcing argv plus an enforcement report, or fails closed with `SANDBOX_UNAVAILABLE`.
2. SandboxMode is limited to file effects: `read-only`, `workspace-write`, `danger-full-access`. Network and process visibility are outside this policy vocabulary.
3. `danger-full-access` bypasses `ctx.sandbox`; it is an explicit unconfined execution path.
4. `SandboxEnforcement` reports `full` or `partial`. Partial enforcement is explicitly not equivalent to a full boundary.
5. Sandbox policy is resolved per capability call. Session mode and immutable session cwd participate in resolution; an approved explicit mode can override the session mode.
6. The sandbox consumer, not the backend, owns process spawn and failure/denial attribution.
7. Approval is a separate capability: `ctx.approval.request()` returns a closed outcome: `allowed-once`, `rejected`, `cancelled`, or `unavailable`.
8. Only `allowed-once` is a grant. Missing, throwing, or non-conforming answerers become `unavailable`; callers fail closed.
9. `ApprovalPolicy` has `ask` and `never`. `never` deterministically rejects before answerer dispatch.
10. Approval requests are auditable: `approval/asked` and `approval/decided` are paired durable session events. An unlogged decision is rejected.
11. Approval request requires an open turn. Audit events are log-only and are excluded from the model transcript.
12. Permission presets combine sandbox mode and approval policy but own no enforcement. They write through the canonical sandbox and approval setters.
13. Child-agent approval can be narrowed to `never`; sandbox inheritance forms part of the delegation model.
14. The repository itself warns that DSH is a developer preview and is not a security-audited production security boundary.

## Security boundary model

```text
Agent
  |
  +--> Tool Consumer
          |
          +--> Approval Policy / Answerer
          |
          +--> Sandbox Policy
                    |
                    +--> Sandbox Provider
                              |
                              +--> OS Backend
```

## R6 conclusions

PASS for explicit sandbox/approval composition and fail-closed semantics.

NOT PROVEN as a complete security boundary because:
- sandbox vocabulary covers file effects only;
- `danger-full-access` is an explicit bypass mode;
- enforcement can be `partial`;
- network/process/credential isolation is outside sandbox mode;
- DSH is not security audited;
- approval is an interaction/authorization gate, not a complete capability-security model.

## ACES implication

DSH sandbox and approval can be reused as enforcement primitives, but ACES must place them below its own Authorization/Policy/Provenance boundary. `allowed-once` is not equivalent to ACES Authority. Sandbox `full` is not equivalent to ACES Security PASS.

Next: R7 — Forkability & Adaptability Analysis.
