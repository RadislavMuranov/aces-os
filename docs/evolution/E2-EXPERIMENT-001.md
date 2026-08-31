# E2 — EXPERIMENT 001

**Status:** READY TO RUN
**Purpose:** first falsifiable test of the ACES Connector hypothesis

## Design

### Task

Choose one real workflow where information/state in System A must cause a bounded action or preparation in System B.

The task must already occur in the user's real work and must contain genuine cross-system friction.

### Conditions

**Baseline B:** user uses the strongest currently available combination of native tooling, APIs/MCP and agents, but no ACES connector.

**Treatment T:** the same workflow with the smallest ACES connector capable of preserving context and coordinating the handoff.

### Required instrumentation

For each run record:

- start/end timestamps;
- human integration actions;
- agent turns/actions;
- context supplied;
- tool calls;
- decision point;
- authority check;
- execution result;
- verification result;
- accepted state;
- failures;
- recovery actions;
- provenance gaps;
- uncertainty changes.

### Primary comparison

`HIW_B vs HIW_T`

where HIW = Human Integration Work attributable to maintaining the connection between systems.

### Secondary comparison

`time_B vs time_T`

`recovery_B vs recovery_T`

`verification_B vs verification_T`

`failure_B vs failure_T`

### Safety veto

Treatment cannot be accepted if it introduces a critical unauthorized action, owner-boundary violation, provenance forgery/loss, unrecoverable state change, or verification bypass.

## Required evidence record

The experiment is not complete until the raw observations can be reconstructed from an audit/evidence record.

## Outcome

**NOT YET EXECUTED.**

No numerical improvement claim may be made before actual runs are recorded.

## Next action

Execute repeated B/T trials on one genuine cross-system workflow and record the complete trajectory.
