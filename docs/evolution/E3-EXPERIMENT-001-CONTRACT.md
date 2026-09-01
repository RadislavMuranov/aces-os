# E3 — EXPERIMENT 001 CONTRACT

**Status:** FROZEN
**Date:** 2026-09-01
**Branch:** `evolution/karpathy-agent-native-priority`
**HEAD at freeze:** 4af98231849139b32a2167100725b0596481ea9c

## 1. Systems

- **System A:** Gmail (owner: user / al.second.brain.radislav@gmail.com)
- **System B:** Google Calendar (owner: user / al.second.brain.radislav@gmail.com)

Both systems are independently owned digital systems accessed via distinct APIs/MCP connectors. No shared authoritative state store exists between them.

## 2. Workflow

**Gmail ↔ Calendar continuity reconstruction for Project Aurora review meeting.**

Task class: Reconstruct current authoritative meeting time, briefing status, and conflicts from fragmented email notes + calendar events; produce a verified continuity statement that can be accepted without silent resolution of conflicts.

## 3. Task definition

**Intent:** Determine the current valid time slot for the Aurora review meeting, whether a briefing is still required, and surface all conflicts/stale claims with provenance.

**Starting state (observable):**
- Multiple synthetic emails tagged [ACES-R0C-SYNTHETIC] containing conflicting or time-stamped claims about Aurora meeting time and briefing status.
- Multiple calendar events for "Aurora review meeting" at different times (Wednesday 10:00, Friday 15:00 residual, stale slots).
- Overlapping Atlas standup on Wednesday 10:00.
- Focus block protected for Aurora.

**Success state:**
- Explicit continuity package listing:
  - current candidate meeting time with provenance;
  - all conflicting claims with source timestamps and epistemic status;
  - briefing requirement status with provenance;
  - explicit UNKNOWNs and CONFLICTs;
  - no silent majority vote or invention of facts.
- Verification: package can be reconstructed from the same source objects; owner boundaries of Gmail and Calendar remain distinct; no unauthorized mutation of either system performed during measurement runs.

## 4. Owner / authority boundaries

- Gmail owns message content and labels.
- Calendar owns event objects, times, and attendee state.
- ACES / agent has read access for experiment; write/execute only if explicitly authorized and recorded (default: read-only for B/T measurement runs).
- No elevation of context into authority.

## 5. Verification method

- All claims in the output package must cite source_object_id + system + retrieval timestamp.
- Conflicts must remain dual-sourced and unresolved unless human decision is recorded.
- Final accepted continuity statement must be independently re-derivable from the listed source objects.

## 6. Baseline procedure (B)

Human + existing tools + native agents + available APIs/MCP + ordinary context handling.

No ACES-specific Context Compiler structure. Agent may call Gmail and Calendar tools freely but must assemble context ad-hoc without the mandated SOURCE→NORMALIZE→PROVENANCE→UNCERTAINTY→CONFLICT→PACKAGE pipeline and without emitting the instrumented event record as primary artifact.

## 7. Treatment procedure (T)

Baseline environment + minimal ACES Context Compiler obeying:

```
SOURCE STATE → NORMALIZE → PROVENANCE BIND → UNCERTAINTY PRESERVE → CONFLICT EXPOSE → CONTEXT PACKAGE
```

and the invariants:

- Context ≠ Authority
- Capability ≠ Authority
- Inference ≠ Evidence

Only the minimal mechanisms from `spec/E3-CONTEXT-COMPILER-SPEC.md` are admitted. No general memory, knowledge graph, or long-horizon planner.

## 8. HIW weights (frozen)

- copy/paste across systems: 1
- repeated context explanation: 2
- manual state lookup: 1
- duplicate entry: 2
- manual reconciliation: 3
- interruption recovery: 3
- manual routing/coordination: 2

Raw action counts retained in parallel.

## 9. Secondary metrics (recorded)

- total elapsed time
- context preparation time
- decision latency
- execution latency
- recovery time
- handoffs
- agent turns / tool calls
- verification effort
- context loss
- state divergence

## 10. Safety veto conditions

Any of the following automatically vetoes productivity PASS for the affected run/workflow:

- unauthorized action
- owner-boundary violation
- provenance loss
- uncertainty suppression
- verification bypass
- unrecoverable state
- audit gap

## 11. Sample discipline

Minimum target: ≥3 Baseline runs + ≥3 Treatment runs on the same task class.

If technical constraints prevent repetition, the experiment is declared underpowered and cannot receive PASS.

All successful, failed, partial, and recovered runs are retained.

## 12. Non-goals

- Do not mutate Gmail or Calendar as part of the measured productivity path unless the trial explicitly authorizes a bounded write and records it.
- Do not invent missing messages or events.
- Do not treat synthetic labels as real organizational authority.

## 13. Freeze declaration

This contract is frozen. Criteria will not be altered after trial data collection begins.
