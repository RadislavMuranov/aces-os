# ACES OS EVOLUTION MASTER PROTOCOL

**Status:** CANONICAL PROPOSAL — governed by Master Control Protocol

## 1. Purpose

This protocol governs the evolution of ACES OS under rapidly changing LLM capabilities. Its purpose is to prevent historical agent scaffolding from becoming permanent architecture without current evidence.

## 2. Fundamental Law

> No agent scaffolding is permanent merely because it once worked.

Every non-protected control must remain justified by current evidence.

## 3. Agent Scaffolding Ablation Principle

```text
OLD MODEL
   ↓
old corrections / prompts / skills / hooks / assumptions
   ↓
MODEL CHANGES
   ↓
ABLATION
   ↓
REMOVE OPTIONAL SCAFFOLDING
   ↓
OBSERVE ACTUAL BEHAVIOR
   ↓
IDENTIFY REAL FAILURES
   ↓
REINTRODUCE ONLY NECESSARY CONTROL
```

The canonical lifecycle is:

```text
REMOVE → OBSERVE → MEASURE → CLASSIFY → REINTRODUCE → VERIFY → RETAIN/RETIRE
```

## 4. No Scaffolding Without Evidence

A single anomalous result does not automatically create a permanent rule. Repeated or material failures may produce a candidate control. Candidate controls become active only after controlled testing and verification.

## 5. Project and Session Context

Each project or independently meaningful working environment shall maintain minimal current context. The default `CLAUDE.md` structure is:

- Project Facts
- Architecture Facts
- Permanent Conventions
- Build/Test Commands
- Non-Negotiable Project Rules
- Critical Safety Constraints

`CLAUDE.md` is advisory context, not an authorization boundary or deterministic enforcement mechanism.

## 6. Separation of Concerns

```text
FACT
   ↓
CLAUDE.md / Rules

WORKFLOW
   ↓
SKILL

ENFORCEMENT
   ↓
HOOK

CAPABILITY
   ↓
TOOL / MCP

SPECIALIZED COGNITION
   ↓
AGENT

ACCEPTANCE
   ↓
VERIFICATION
```

## 7. Skills

Skills encode reusable workflows and capabilities that are not required as permanent global context.

Canonical structure:

```text
.claude/skills/<skill>/
├── SKILL.md
├── references/
├── scripts/
└── examples/
```

A Skill should minimize permanent context and use progressive disclosure. `SKILL.md` should contain, at minimum, routing-oriented `name` and `description`, followed by Goal, Invariants, Evidence, Required Output, and Gotchas where applicable.

Example:

```yaml
---
name: security-review
description: >
  Use when reviewing changes that affect authorization,
  capabilities, permissions, provenance, protected artifacts,
  or security boundaries.
---
```

```markdown
# Goal

Determine whether the change preserves the security invariants.

# Invariants

...

# Evidence

...

# Required output

...

# Gotchas

...
```

## 8. Hooks

```text
HOOK = RUNTIME CONTROL
```

Hooks are used where correctness or safety must not depend exclusively on model compliance, including protected artifacts, authorization, secrets, destructive operations, provenance, audit, and mandatory verification.

## 9. Protected Canonical Artifacts

Canonical artifacts may only be modified through the Master Control Protocol workflow.

Protected canonical artifact:

```text
ACES_OS_MASTER_CONTROL_PROTOCOL.md
```

Evolution tooling shall not silently rewrite canonical governance artifacts.

## 10. Security / Authority Exception

Ablation never authorizes removal of security, authority, safety, provenance, or governance invariants merely because a newer model appears more capable. If an invariant can be violated by model error or compromise, independent enforcement is required.

```text
MODEL CAPABILITY ≠ SECURITY GUARANTEE
```

## 11. Control Lifecycle

Controls are classified as:

```text
ACTIVE
CANDIDATE
STALE
PROTECTED
RETIRED
```

A control becomes `STALE` when its current necessity is no longer demonstrated. A `PROTECTED` control cannot be retired solely because model capability improved.

## 12. Ablation Triggers

Ablation may be triggered by:

- a new frontier model;
- approximately six months of evolution;
- major architecture changes;
- repeated unexpected behavior;
- material changes in tool, context, reasoning, or agentic behavior.

The six-month interval is a review trigger, not an unconditional deletion command.

## 13. Self-Evolving Scaffolding

ACES OS shall evolve toward a governed mechanism capable of observing failures, generating candidate controls, testing them, measuring utility, and promoting, modifying, or retiring them.

```text
OBSERVE
   ↓
DETECT FAILURE
   ↓
CLASSIFY
   ↓
GENERATE CANDIDATE CONTROL
   ↓
TEST
   ↓
MEASURE
   ↓
PROMOTE / MODIFY / RETIRE
```

## 14. LLM Evolution

ACES OS shall distinguish native model capability, project requirements, historical workarounds, and deterministic invariants.

Emerging trends are hypotheses, not facts:

```text
OBSERVATION → HYPOTHESIS → EXPERIMENT → EVIDENCE → DECISION → CANON
```

ACES OS shall seek early detection and validation of emerging LLM capabilities and failure modes rather than pretending to predict the future with certainty.

## 15. Tomorrow-Ready Principle

> ACES OS must evolve faster than its scaffolding fossilizes, while changing slower than its evidence warrants.

## 16. Final Principle

> Reality precedes canon.
>
> No historical agent scaffolding is permanent without current evidence.
>
> Security, authority, safety, provenance, and governance invariants must remain independently enforceable.
