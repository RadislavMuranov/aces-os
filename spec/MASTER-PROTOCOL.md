# ACES OS — MASTER PROTOCOL

**Status:** CANONICAL / ACTIVE
**Version:** 1.1
**Date:** 2026-09-07
**Repository:** `RadislavMuranov/aces-os`
**Mode:** Architectural / experimental governance record

---

## 0. Purpose

This document is the master protocol for the current ACES OS architectural investigation. It records the governing premise, experimental method, falsification history, boundary conditions, and the current research question.

The protocol exists to prevent the project from turning an unproven architectural hypothesis into unnecessary software, storage, UI, or process.

**Rule:** evidence precedes architecture.

**Mandatory iteration controls:** `spec/governance/CHATGPT-FAILURE-FILTER.md` and `spec/governance/CHATGPT-ITERATION-REFACTOR-AND-BUG-LEARNING-GATE.md` are mandatory process controls for every future iteration. They do not establish ACES necessity.

---

## 1. Canonical definition

> **ACES OS — a layer of continuity between the spaces in which a human lives and acts in the Digital World.**

Equivalent architectural formulation:

> **ACES OS does not replace the Digital World. It makes the Digital World usable by a human without requiring the human to become its integration layer.**

ACES is therefore not defined as another Notion, Obsidian, CRM, task manager, or workspace.

The target is the cross-environment coordination burden that remains after existing platforms, MCP, LLMs, and agent platforms are available.

---

## 2. Foundational human principle

> **The inevitability of interaction with the Digital World is not a justification for expending human psychic energy.**

Operational consequence:

> **ACES does not remove necessary friction. It removes parasitic friction.**

A system that introduces its own coordination burden, mandatory data entry, duplicate task management, duplicate knowledge management, or architectural ceremony fails this principle.

---

## 3. Zero-friction coordinator hypothesis

Current research question:

> **Does a human become objectively more effective when existing mechanisms work automatically through one zero-friction connective agent?**

Related question:

> **Is a zero-friction coordinator required that uses existing layers without becoming a new layer?**

This is an open research question, not a settled architectural requirement.

The coordinator hypothesis must be tested against the strongest 2026 baseline available: native platform capabilities + MCP + LLMs + agent platforms + existing protocols/metadata.

---

## 4. Market / architecture baseline

The 2026 Digital World already contains mature specialized environments that increasingly provide their own orchestration:

- Google Workspace — communication, time, storage, documents, collaboration, AI
- GitHub — software creation, engineering execution, agents, MCP
- Obsidian — personal thinking / knowledge work
- Notion — collaborative knowledge / workspace / agents
- Kaiten — execution / workflows / project work
- CRM systems — relationships / relationship records
- Communication platforms — social and team connectivity
- Research and publishing tools — discovery, synthesis, publication
- Banking / accounting / tax systems — administration and economy
- AI assistants / agents — cognitive augmentation and execution

**Architectural implication:** ACES must not assume that missing capability equals missing application.

The primary unit of analysis is the **transition between environments**, not the environment itself.

---

## 5. Human-space ownership boundaries

The current working ecology recognizes these human activities and external owners:

| Human activity | Current owner / baseline |
|---|---|
| Communication / Time / Storage | Google ecosystem |
| Research / Discovery | Composite ecosystem; no canonical single owner yet |
| Thinking | Obsidian |
| Creation | Split across specialized creation tools; do not collapse prematurely |
| Publishing | Candidate ecosystem; not yet canonical |
| Relationships | Google by default; dedicated CRM only after demonstrated need |
| Execution | Kaiten + GitHub |
| Administration / Economy | Country-specific banking + accounting + tax |

These are **human activities**, not ACES product modules.

ACES must not create a competing owner for any of these activities unless evidence proves that an external owner cannot satisfy the required function.

---

## 6. Transition unit of analysis

The research unit is the continuity chain:

`Owner → Artifacts → Events → Relationships → Intent → Authority → Memory → Actions`

The chain describes what must survive movement across environments.

It must **not** become a form, dashboard, mandatory schema, or user-maintained object model.

The moat, if one exists, is in transitions — not in a card, database, or new workspace.

---

## 7. Strongest 2026 baseline

All future gap claims must first be tested against:

`Existing platform capabilities + MCP + LLM + native agents + existing permissions/policies + existing automation`

A gap is not architectural merely because an individual application does not implement it.

A gap qualifies for ACES consideration only when it survives the strongest reasonable cross-platform baseline.

---

## 8. Experimental protocol

For every proposed ACES capability:

1. Select a real or controlled human situation.
2. Run it through the strongest existing stack without ACES.
3. Permit MCP, LLMs, native agents, metadata, and minimal protocol markers.
4. Preserve uncertainty rather than inventing relationships.
5. Measure the actual human integration work remaining.
6. Locate the first broken transition.
7. Test the smallest possible mechanism in existing systems.
8. Only if the gap survives minimality testing may a new ACES layer/component be proposed.

**Default outcome is rejection of new architecture.**

---

## 9. Mandatory Per-Iteration Verification, Refactoring & Bug-Learning Gate

This section is **mandatory for every iteration**. It is not optional guidance and cannot be bypassed because the change is small, documentation-only, urgent, previously validated, or apparently obvious.

Before an iteration may be marked complete, ChatGPT MUST execute the following loop:

```text
REPOSITORY BEFORE
→ CLAIMS / ASSUMPTIONS
→ MINIMAL CHANGE / EXECUTION
→ REPOSITORY AFTER
→ BEHAVIOR / EVIDENCE VERIFICATION
→ FULL CHATGPT BUG AUDIT
→ ADVERSARIAL NEW-BUG SEARCH
→ REFACTOR / DELETE / SIMPLIFY
→ RE-VERIFY
→ FAILURE-FILTER + REGRESSION CHECK
→ BUG-BASE UPDATE
→ ITERATION VERDICT
```

### 9.1 Repository verification

The relevant repository state MUST be inspected before repository-dependent work and independently inspected after the change.

Intended state, committed state, and verified behavior MUST NOT be conflated.

When ChatGPT's assertion conflicts with directly observed repository state, repository observation takes precedence unless independently disproven.

### 9.2 Full ChatGPT bug audit

Every iteration MUST actively audit the complete failure catalogue in `spec/governance/CHATGPT-FAILURE-FILTER.md`, including epistemic, architectural, validation, minimality, runtime/environment, evidence, product/human-value, process, sunk-cost, complexity, reset, and research-recursion failure classes.

The audit MUST also search for bugs not already present in the catalogue.

### 9.3 Refactoring and deletion

After verification, ChatGPT MUST perform an explicit refactoring pass:

`DELETE > SIMPLIFY > REUSE > EXISTING SYSTEM > GENERIC MECHANISM > NEW ACES MECHANISM`

The pass MUST consider what can be deleted, simplified, replaced by an existing capability, weakened to match evidence, or eliminated entirely.

### 9.4 Bug learning

Every discovered bug MUST be classified and recorded. At minimum:

`NEW / RECURRING / AMPLIFIED / ESCAPED / EXPOSED / RESOLVED / UNRESOLVED / UNKNOWN`

A generalizable new failure MUST update the failure-filter knowledge base. Existing bugs that recur or escape detection MUST also update the filter when the prevention rule needs strengthening.

ChatGPT MUST NOT silently correct its own prior error. The record must preserve:

`PREVIOUS CLAIM → CONTRADICTION → BUG → IMPACT → CORRECTION → PREVENTION`

### 9.5 Fail-closed completion

An iteration may be marked:

**PASS — VERIFIED + REFACTORED + BUG AUDITED + LEARNED**

only when the applicable repository, evidence, bug-audit, refactoring, and regression checks are complete.

If required verification cannot be performed, the result is:

**BLOCKED / INCOMPLETE — DO NOT CLAIM PASS.**

### 9.6 Mandatory stop conditions

The iteration MUST stop if:

- repository state cannot be inspected;
- relevant evidence cannot be accessed;
- a claimed fix cannot be verified;
- a contradiction remains unresolved;
- a material bug is discovered without verified containment;
- a required regression check cannot be performed;
- the self-audit is incomplete;
- a confirmed generalizable bug cannot be recorded in the failure base;
- the proposed change depends on an unverified ACES architectural premise.

### 9.7 Iteration record

Each completed iteration MUST preserve, at minimum:

`ITERATION_ID / OBJECTIVE / REPOSITORY_BEFORE / ACTION / REPOSITORY_AFTER / VERIFICATION / KNOWN_BUGS / NEW_BUGS / RECURRING_BUGS / REFACTORING / DELETIONS_CONSIDERED / REMAINING_UNKNOWN / FILTER_UPDATED / REGRESSION_CHECK / FINAL_VERDICT`

If a field is not applicable, record `N/A`; if it cannot be established, record `UNKNOWN` or `NOT VERIFIED`.

---

## 10. Canonical R-series record

The following results are accepted as the current experimental record:

| Test | Result |
|---|---|
| R2 — Residual Gap Analysis | Positive signal |
| R5.1 — Minimality Test: Next-Step Gap | Gap confirmed |
| R5.2 — Minimal Field Test | PASS |
| R5.3 — Field Automation Test | Difficulty signal |
| R5.4 — Commodity Automation Test | PASS |
| R6 — Scan for Remaining Gaps | INTENT → AUTHORITY |
| R6.1 — Authority Gap Minimality Test | FAIL |
| R6.2 — Enforcement Boundary Test | PASS |
| R7 — Residual Gap Hunt | PASS |
| R8 — Life / Creative Continuity Hunt | SIGNAL |
| R8.1 — Continuity Externalization Test | FAIL |
| R8.2 — Provenance Protocol Test | PASS |
| R9 — Human Agency Preservation Test | FAIL |
| R9.1 — Agency Protocol Minimality Test | PASS |
| R10 — Necessity Test | INVALID |
| R11 — Native Baseline Sufficiency Test | FAIL |
| R12 — Minimal Mechanism Design | PASS |
| R13 — Boundary Failure Hunt | PARTIAL / boundary nearly reached |
| R13.1 — Intuition Preservation Minimality Test | PASS |

These results do **not** establish that ACES is architecturally necessary.

Current conclusion:

> **ACES architectural necessity remains unconfirmed.**

The experiments demonstrate that multiple apparent gaps can be addressed by mechanisms placed in existing systems. This strengthens, rather than weakens, the requirement for further minimality testing.

---

## 11. R13.1 — Intuition Preservation Minimality Test

### Objective

Test whether intuitive and otherwise difficult-to-formalize human knowledge can be preserved with minimal structures in existing systems, without a new ACES layer or storage system.

### Tested mechanism

Minimal marker structures were proposed for:

- intuitive perception / rationale;
- trigger of intuition;
- confidence and uncertainty;
- cognitive-process phases;
- temporal cognitive-state changes;
- relationship to decisions and directions.

Candidate placement:

- Obsidian properties / daily notes / notes;
- Google Docs comments / existing document context.

### Result

**PASS.**

The test demonstrated that the information required for continuity can, in principle, be represented by minimal structures in existing systems.

### Boundary

The structures preserve a report or trace of cognition, not the underlying subjective experience itself. That limitation is accepted as evidence of representational boundary, not evidence for a new storage layer.

### Architectural consequence

No new ACES object, storage, or UI is justified by R13.1.

---

## 12. The Minimal Mechanism Principle

Canonical postulate:

> **Minimal mechanisms work only on condition that someone creates them, maintains them, places them correctly, and keeps them coherent across the Digital World.**

This is a critical distinction.

A mechanism may be technically sufficient while still imposing recurring human coordination work.

Therefore:

`Technical sufficiency ≠ Human sufficiency`

and:

`Automation available ≠ Coordination eliminated`

The research must measure not only whether a protocol can work, but **who bears the cost of creating, maintaining, placing, repairing, and interpreting it.**

---

## 13. The residual question after minimality

The next level of inquiry is no longer:

> "Can existing tools store this?"

It is:

> **"Can existing mechanisms operate automatically, continuously, and correctly across the Digital World without requiring the human to create and maintain the integration itself?"**

This is the current residual gap hypothesis.

The proposed zero-friction coordinator is therefore not yet an ACES architectural layer. It is a **test hypothesis**.

---

## 14. Zero-friction coordinator test

The minimum falsifiable question is:

> **Given the same existing tools and protocols, does adding one connective agent materially reduce human coordination effort while preserving owner boundaries, authority, provenance, uncertainty, and continuity?**

The agent may:

- observe existing environments;
- interpret cross-system state;
- create or maintain minimal markers automatically;
- route actions to the existing owner tool;
- preserve provenance and uncertainty;
- avoid creating a competing workspace.

The agent may not:

- become the owner of knowledge, tasks, relationships, documents, or code;
- require a new user-maintained database;
- require duplicate task entry;
- replace Obsidian, Google, Kaiten, GitHub, Notion, CRM, or other domain owners;
- hide uncertainty by fabricating cross-system links.

---

## 15. Success criterion

The coordinator hypothesis passes only if a controlled comparison demonstrates a measurable reduction in **human integration work**.

At minimum compare:

`Baseline: human + existing tools + MCP/LLM/agents`

against:

`Treatment: human + same tools + one zero-friction connective agent`

Measure:

- number of manual cross-system joins;
- number of context re-constructions;
- number of duplicate entries;
- time spent locating state;
- time spent deciding what changed / matters / happens next;
- errors caused by lost context;
- unnecessary actions;
- recovery effort after interruption;
- preservation of uncertainty;
- owner-boundary violations.

The treatment fails if it merely moves complexity from applications into an ACES-like control surface.

---

## 16. Reality Layer rule

The canonical human-facing output remains:

`NOW / IMPORTANT / NEXT`

The Reality Layer is not a dashboard of all connected systems.

Its purpose is to expose only the minimum cross-world state needed for the human to act without becoming the integration layer.

Internal coordination must remain invisible unless the human explicitly needs to inspect it.

---

## 17. No-new-workspace invariant

The following invariant is active:

> **ACES must not create a new workspace merely to connect existing workspaces.**

No new ACES task manager, knowledge base, CRM, vault, project board, publishing system, or duplicate document repository is justified by connectivity alone.

---

## 18. Owner-boundary invariant

Actions remain in the system that owns the action.

Examples:

- email → Gmail;
- time commitment → Calendar;
- document → Docs / Drive;
- code → GitHub / coding environment;
- execution work → Kaiten;
- thinking → Obsidian;
- relationship record → appropriate relationship owner;
- accounting / financial record → appropriate financial system.

ACES, if eventually required, coordinates rather than becomes the owner.

---

## 19. Uncertainty invariant

The system must preserve uncertainty.

A missing artifact is not a found artifact.

An ambiguous request is not a task.

A probable relationship is not an established relationship.

A technical success is not automatically a semantic success.

A summary is not evidence of continuity unless its provenance can be reconstructed.

---

## 20. Human-agency invariant

Human judgment remains authoritative wherever the decision is genuinely human.

Automation may prepare, connect, recommend, route, execute authorized actions, and verify results.

Automation must not silently convert recommendation into intention, technical permission into decision authority, or inferred context into human commitment.

---

## 21. Current architecture status

**ACES architectural hypothesis:** NOT CONFIRMED.

**ACES as product hypothesis:** OPEN.

**Zero-friction connective agent hypothesis:** OPEN / next research target.

**New ACES storage:** NOT JUSTIFIED.

**New ACES objects:** NOT JUSTIFIED by the current evidence.

**New ACES UI:** NOT JUSTIFIED beyond the existing Reality Layer experiment.

**Primary research direction:** determine whether a connective agent can eliminate the human maintenance burden that remains after minimal mechanisms are available.

---

## 22. Immediate next experiment

Do not build an ACES layer.

Run one controlled comparison on the same synthetic cross-system scenario:

### Baseline
Existing Google/GitHub/communication environments + MCP + LLM/agent capabilities + minimal markers.

### Treatment
The same environment + **one zero-friction connective agent** that automatically creates, updates, and maintains the minimal cross-system markers and presents only the resulting human-relevant continuity.

### Question

> **Does the connective agent reduce human coordination work enough to constitute a real residual capability gap?**

### Hard stop

If the agent adds no material reduction, or if existing platform agents can provide the same result without a distinct connective role, the coordinator hypothesis is rejected.

If the agent materially reduces cross-system maintenance while preserving all invariants, the residual gap becomes concrete and can be specified precisely.

---

## 23. Governance rule

No new architecture is admitted because it is elegant, desirable, or theoretically cleaner.

It is admitted only when:

`Observed residual human burden`

survives:

`strongest existing baseline`

and:

`minimal mechanism test`

and:

`automation / commodity test`

and:

`owner-boundary / agency / provenance tests`.

Only then may an ACES architectural component be considered necessary.

---

## 24. Canonical closing statement

> **ACES OS does not exist to add another place where the human must work. It exists, if it is necessary at all, to make the existing Digital World continuously usable without making the human responsible for maintaining its connections.**

And the current research question is therefore:

> **Can one zero-friction connective agent make the existing Digital World behave as a coherent environment for a human, without becoming another environment itself?**

**Status: OPEN — FALSIFIABLE.**


---

## 25. Scope-Anchor Integrity Requirement

A 100% synchronization operation MUST reconstruct the **entire chat state**, not merely repository or implementation state.

The minimum reconstruction order is:

`ENTIRE CHAT PURPOSE`
→ `ORIGINAL RESEARCH OBJECTIVE`
→ `OBJECTIVE LINEAGE`
→ `OPEN / CLOSED OBJECTIVES`
→ `AUTHORIZATIONS`
→ `EVIDENCE / DEFECTS / CORRECTIONS`
→ `CURRENT VERIFIED STATE`
→ `NEXT LEGITIMATE SCOPE`

The following substitutions are prohibited:

- `RepositoryState ≠ CompleteChatState`
- `ClosedImplementationIteration ⇏ ClosedResearchObjective`
- `RepositoryState ⇏ NextLegitimateScope`

### Scope-Derivation Invariant

> **No original research objective → no valid scope derivation.**

If the original research objective cannot be established from available evidence, the result MUST be:

**UNKNOWN / NOT VERIFIED**

and MUST NOT be:

**NO NEW SCOPE JUSTIFIED**.

### Scope-Anchor Preservation

The original research objective remains open until evidence explicitly establishes its closure, rejection, supersession, or authorization-controlled termination.

Closing an implementation iteration MUST NOT implicitly close the research objective that initiated the branch.

### Required Scope-Derivation Input

Before deriving a next legitimate scope, ChatGPT MUST have:

`ENTIRE_CHAT_PURPOSE / ORIGINAL_RESEARCH_OBJECTIVE / OBJECTIVE_LINEAGE / OPEN_OBJECTIVES / CLOSED_OBJECTIVES / AUTHORIZATIONS / EVIDENCE / DEFECTS / CORRECTIONS / CURRENT_VERIFIED_STATE`

If any material scope anchor is missing, derivation is incomplete and the process MUST stop rather than infer a new scope or terminate the objective.

This requirement is a process-control rule. It does not establish ACES architectural necessity.
