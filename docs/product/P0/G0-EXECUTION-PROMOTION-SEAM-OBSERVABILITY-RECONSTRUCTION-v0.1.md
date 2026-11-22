# G0 — Execution/Promotion Seam: Observability Reconstruction v0.1

**Record status:** WORKING-TREE RECONSTRUCTION RECORD / NOT CANON / NOT ACCEPTED  
**Mission:** Establish the factual upstream execution/promotion seam for the observed Desktop Commander `start_process` call.  
**Mode:** Read-only evidence reconstruction. No runtime, source, configuration, or authority changes.  
**Repository:** `C:\\Users\\Радислав Муранов\\aces-os`  
**Observed HEAD (historical/currently last verified):** `686bf75f91789ca9055fa6d07a957453093cb339`  
**Disposition:** `PARTIALLY ESTABLISHED / UPSTREAM BLOCKED — EVIDENCE ACCESS LIMITATION`

## 1. Question and decision boundary

Question: which upstream component makes or enforces the decision that permits a particular MCP `start_process` request, and how is that decision bound to the exact request?

The local Desktop Commander execution path is established in the previously inspected package source:

```text
incoming MCP CallToolRequest
→ server dispatcher
→ handleStartProcess
→ command validation / blockedCommands
→ terminal manager
→ spawn(shell, command)
→ process result
→ MCP response
```

This proves the inspected local dispatch path only. It does not establish who decided upstream to issue the request, whether an upstream ACES mission/scope gate ran, or whether a decision was bound to this request.

## 2. Evidence observed in this iteration

1. A bounded `get_recent_tool_calls` query returned recent `start_process` calls with timestamps, tool name, arguments, output and duration. The exposed records did not include an upstream policy decision, a caller decision trace, or a correlation identifier linking a decision to a specific call.
2. `get_config` returned Desktop Commander version `0.2.52`, server PID `14872`, client name `desktop-commander-client`, client version `1.0.0`, and client ID `bd9c978b-aa88-4617-ae6e-75fb25bfcdef`.
3. These configuration fields identify the connected client as reported by the server. They do not identify which component decided to issue a particular `start_process` call.
4. The available history/configuration interfaces do not expose the upstream decision event or a per-call causal link. This is a limitation of the inspected interfaces, not proof that such a decision or record does not exist elsewhere.
5. No source code, configuration, runtime settings, process state, or authority settings were changed. This reconstruction record itself was created in the working tree and read back for verification.

## 3. Finite working hypotheses and distinguishing observations

| ID | Hypothesis (not fact) | Observation that would distinguish it | Result with currently exposed interfaces |
|---|---|---|---|
| H1 | The client runtime decides to issue the tool call | Client-side decision event bound to the exact call/request | Not observable |
| H2 | An intermediate dispatcher makes or enforces the decision | Dispatcher trace showing input request, gate/policy evaluation and decision output | Not observable |
| H3 | Another component initiates the call | Caller-component identity bound to the exact request, with a causal trace to the tool call | Not observable |

This is a finite working set for the current test, not a claim that no other architecture is possible. None of H1–H3 is established or rejected by the evidence available here.

## 4. Observability boundary

**Observable at the exposed Desktop Commander interface:** tool name, arguments, result/output, timestamps/duration, aggregate usage information, current-client identity as reported by the server, and server process metadata.

**Not exposed by the inspected interface:** a per-call upstream decision record; the identity of the component that made that decision; a decision result/reason; a shared correlation ID connecting that decision to the exact MCP request; evidence that an ACES mission/scope authorization was evaluated.

**Important distinction:** “not exposed by the inspected interface” does not mean “absent from the system.” The local server's request metadata/telemetry handling is not, by itself, evidence of an upstream authorization decision.

## 5. Minimal discriminating evidence required

One trace/export from the client runtime or intermediate dispatcher for a single identified `start_process` call, containing:

- a unique request/call correlation ID, shared with or deterministically bound to the Desktop Commander call;
- immediate caller/component identity;
- the decision event that authorized or initiated the call;
- policy/gate name and decision result/reason, including an explicit “no gate evaluated” only if the trace can reliably establish that fact;
- exact request/tool identity and relevant arguments or a stable request hash;
- timestamp and trace provenance.

A general configuration dump, another directory listing, an uncorrelated client identity, or another tool-call history export without decision/correlation data does not satisfy this requirement.

## 6. Repair of the two methodological defects

### Defect A — Observability was mistaken for search volume

**Failure:** repeated artifact searches were used in place of testing whether available interfaces could distinguish the upstream hypotheses.

**Repair rule:** before any evidence-acquisition action, state (1) the hypothesis pair it can distinguish, (2) the exact observable field/event required, and (3) the possible outcomes and how each changes the verdict. Do not execute an acquisition step that cannot change the hypothesis classification.

### Defect B — Iteration cyclicity without progress

**Failure:** repeated iterations could return the same “not found” result without changing uncertainty, the evidence boundary, or the decision.

**Repair rule:** every iteration must produce at least one of:
- a new discriminating observation;
- a falsified/strengthened hypothesis with cited evidence;
- a narrower, evidenced observability boundary;
- a terminal bounded disposition with the exact missing evidence.

If none occurs, the iteration is **NON-PROGRESS** and must stop. The same search/source/action may not be repeated unless the source, query target, available access, hypothesis, or relevant system state has materially changed and that change is stated in advance.

**Stop condition:** once all currently accessible interfaces have been tested for the required decision/correlation fields and do not expose them, stop acquisition. Record `BLOCKED / EVIDENCE ACCESS LIMITATION`; do not infer global absence and do not wait indefinitely for an unspecified log.

## 7. Reconciliation and verdict

- Local Desktop Commander dispatch path: **ESTABLISHED within the previously inspected source scope**.
- Upstream execution/promotion decision seam: **UNKNOWN / NOT ESTABLISHED**.
- H1/H2/H3: **NOT DISTINGUISHED** by currently exposed history/configuration interfaces.
- Method defect A (no observability-boundary test): **REPAIRED AT METHOD/RECORD LEVEL** by defining exposed vs unexposed fields and a minimal discriminating trace.
- Method defect B (cyclic acquisition without progress): **REPAIRED AT METHOD/RECORD LEVEL** by imposing a progress invariant and a terminal stop condition.
- Runtime enforcement of these method rules: **NOT IMPLEMENTED OR VERIFIED**.
- Global absence of an upstream gate: **NOT CLAIMED**.
- G0 seam: **PARTIALLY ESTABLISHED; UPSTREAM EDGE BLOCKED**.
- Next execution node: **NOT AUTHORIZED**. `NoReconciliation ⇒ NoNextNode` remains in force.

This record is a bounded reconstruction result, not Canon promotion, AcceptedState, or proof of production readiness.
