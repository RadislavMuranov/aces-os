# Authority–Evidence–Reality Frontier Research — 2026

**Status:** RESEARCH FIXED / INPUT TO HDE-002 STEP 7  
**Date:** 2026-09-03  
**Branch:** `architecture/priority-realization-roadmap-v2`

## 1. Research question

How strongly is the proposition represented in contemporary software/agent engineering that after an agent performs an action, a separate authority function must determine whether the resulting effect is permissible, correct, accepted, and part of canonical system reality?

## 2. Finding

The problem is real and rapidly emerging, but the terminology is fragmented.

Contemporary engineering already treats the following as serious, distinct concerns:

- agent identity and authorization;
- delegation of authority;
- policy enforcement and runtime control planes;
- execution-time authorization;
- approval and permission boundaries;
- verification and assurance;
- evidence and provenance;
- accountability and auditability;
- system of record / source of truth;
- epistemic authority in AI-mediated decision making.

However, no surveyed mainstream architecture establishes a universally adopted single layer that closes the entire chain:

`ACTION → OBSERVATION → EVIDENCE → VERIFICATION → ACCEPTANCE → CANONICAL STATE`

with explicit separation of epistemic, decision, and execution authority.

## 3. Important external convergence

### NIST / agent identity and authorization

NIST's 2026 work on software and AI agent identity and authorization treats identity, authorization, auditing, non-repudiation and agent actions as a distinct engineering problem. NIST's AI Agent Standards Initiative further establishes agent security/interoperability as an emerging standards domain.

Implication: authority for autonomous agents is not merely an ACES invention; it is an established emerging engineering concern.

### Agentic control planes

Current enterprise architecture work increasingly describes an agent control plane responsible for identity, context, policy, tools and authorized actions while agent runtimes perform reasoning and execution.

Implication: the industry is converging on separation of intelligence/execution from governance/control.

### Action authorization boundaries

Recent research introduces explicit action authorization boundaries, canonical action representations and decision artifacts that must be checked before execution.

Implication: `can act` is increasingly separated from the agent's ability to propose an action.

### Execution-time authorization

Recent work explores signed mandates, intent-governed authorization and runtime enforcement immediately before consequential execution.

Implication: authorization must bind to concrete proposed actions, not merely to an agent identity in the abstract.

### Canonical action verification / attestation

Recent research explores canonical runtime action objects and evidence/attestation linking approval, execution, receipts and verification.

Implication: an execution event is not sufficient by itself; its semantic identity and evidence chain matter.

### AI-native SDLC / agentic CI-CD

Current work on AI-native software delivery emphasizes explicit specifications, verification gates, provenance and human sign-off, and identifies authority transfer from human-controlled pipelines to agents as a central governance problem.

Implication: agent autonomy increases the importance of independent verification and explicit authority boundaries.

### Epistemic authority

AI governance/philosophy research increasingly treats AI systems as potential epistemic authorities: systems whose outputs influence what humans or institutions accept as knowledge, evidence, expertise or justified decisions.

Implication: epistemic authority is a real interdisciplinary concept, although it is less standardized in software architecture than authorization.

### Source of truth / state control

Agentic workflow research increasingly distinguishes authoritative state from memory, generated assumptions, stale context and inferred state.

Implication: `system of record` / `source of truth` is a close established analogue of ACES canonical reality, but ordinary systems of record usually govern one domain rather than a cross-system digital reality layer.

## 4. Critical distinction

The following are not equivalent:

`CAPABILITY ≠ PERMISSION ≠ APPROVAL ≠ EXECUTION ≠ VERIFICATION ≠ ACCEPTANCE ≠ CANONICALITY`

A successful execution proves only that an effect occurred or was reported by the execution substrate.

A permission proves that a policy mechanism allowed an action.

An approval proves that an authorized approver permitted a particular proposed action.

Verification provides evidence that an observed outcome satisfies specified criteria.

None of these alone proves that the resulting state is entitled to become canonical ACES reality.

## 5. ACES-specific synthesis

The strongest defensible ACES hypothesis is not:

`ACES owns truth.`

It is:

> ACES owns the authority and procedure for determining what state is accepted as canonical within ACES operational reality, subject to declared policy, evidence and verification requirements.

This explicitly avoids claiming authority over objective reality.

The proposed ACES boundary is therefore better described as an **Authority–Evidence–Reality Layer** rather than merely an Authority Layer.

Candidate flow:

`INTENT → PROPOSAL → AUTHORIZATION → EXECUTION → OBSERVATION → EVIDENCE → VERIFICATION → ACCEPTANCE → CANONICAL STATE`

## 6. Three authority dimensions

### Execution Authority

Whether an actor/runtime is authorized to cause a specified side effect.

### Decision Authority

Whether an actor/person/system is authorized to make a binding choice about what should be done.

### Epistemic Authority

Whether an actor/process has sufficient grounds, evidence and standing to cause a proposition/state to be accepted as knowledge within the governed system.

### Acceptance / canonicalization function

A distinct ACES function may be required to determine whether a verified state becomes part of canonical ACES reality. This should not be conflated with objective truth or with execution permission.

## 7. Architectural hypothesis

Modern agentic systems increasingly solve:

`MODEL → AGENT → HARNESS → TOOLS → EXECUTION`

and are adding:

`POLICY → PERMISSION → APPROVAL → EXECUTION BOUNDARY`

The comparatively under-standardized frontier is:

`RESULT → EVIDENCE → VERIFICATION → ACCEPTANCE → CANONICAL REALITY`

Therefore ACES should not duplicate model, agent or harness functionality merely to obtain autonomy. Its defensible differentiation is the governed transition from external execution to accepted, evidence-backed canonical state.

## 8. What the research does NOT establish

This research does not establish that ACES's proposed Authority–Evidence–Reality Layer is already a recognized industry standard.

It does not establish that ACES invented epistemic authority, agent authorization, control planes, provenance, verification or systems of record.

It establishes convergence of adjacent disciplines and identifies a still-fragmented architectural gap at their intersection.

## 9. Research conclusion

**FOUNDATIONAL HYPOTHESIS: SUPPORTED.**

The question "do we have the right to regard this effect as permissible, correct and part of our system's reality?" is a legitimate and increasingly important software/AI engineering problem.

The novel ACES opportunity is the explicit integration of:

`AUTHORITY + EVIDENCE + VERIFICATION + ACCEPTANCE + CANONICAL STATE`

above model/agent/harness execution runtimes and across heterogeneous digital systems.

## 10. Relationship to HDE-002

This research strengthens Step 6 — ACES GAP ANALYSIS.

It is an external research input, not itself an architectural specification.

It must be used as evidence for Step 7 — ACES BOUNDARY SPEC, where the minimum ACES-owned boundary is to be defined precisely.

## 11. Principal external references

- NIST — software/AI agent identity and authorization work, 2026.
- NIST — AI Agent Standards Initiative, 2026.
- Enterprise agent control-plane architecture literature, 2026.
- Recent research on Action Authorization Boundaries, execution-time authorization and canonical action verification/attestation, 2026.
- Recent research on AI-native SDLC and agentic CI/CD governance, 2026.
- Research on epistemic authority and AI-mediated governance, 2025–2026.
- Research on state/source-of-truth control surfaces for agentic workflows, 2026.
