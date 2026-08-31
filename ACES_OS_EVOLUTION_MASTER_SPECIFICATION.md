# ACES OS EVOLUTION MASTER SPECIFICATION

**Status:** CANONICAL PROPOSAL — governed by Master Control Protocol

## 1. System Objective

Build an Evolution Engine that continuously determines which agent controls remain necessary for the current generation of LLMs.

## 2. Core Objects

```text
Model
Project
Session
Task
Fact
Failure
Hypothesis
Control
Skill
Hook
Experiment
Evidence
Decision
Canon
Manifest
```

## 3. Control Object

Every control should have:

```text
control_id
 type
 purpose
 origin
 provenance
 trigger
 expected_effect
 observed_effect
 risk
 cost
 dependencies
 status
 last_verified
 last_ablated
```

## 4. Control Types

```text
CLAUDE_CONTEXT
RULE
SKILL
HOOK
AGENT
TOOL
MCP
VERIFIER
```

## 5. Evidence Model

Evidence shall distinguish:

```text
EXPECTED
OBSERVED
REPRODUCED
VERIFIED
CANONICAL
```

A control is not canonical merely because its author expects it to work.

## 6. Failure Model

Every observed failure should record:

```text
task
model
environment
action
expected_result
actual_result
failure_class
severity
reproducibility
evidence
```

## 7. Ablation Experiment

Each ablation experiment should define:

```text
baseline
control_removed
task_set
model
environment
metrics
observations
comparison
decision
```

## 8. Metrics

Minimum metrics:

```text
success_rate
failure_rate
verification_rate
context_cost
execution_cost
latency
false_positive_rate
false_negative_rate
security_impact
```

## 9. Skill Specification

Minimum form:

```yaml
---
name: <name>
description: >
  Use when <trigger conditions>.
---
```

Body:

```text
Goal
Invariants
Evidence
Required Output
Gotchas
```

Additional material:

```text
references/
scripts/
examples/
```

## 10. Hook Specification

Every Hook should define:

```text
trigger
scope
condition
action
allow/block semantics
failure semantics
audit behavior
```

Security-sensitive hooks shall fail closed where required by the relevant invariant.

## 11. Project Context Compiler

The compiler shall derive:

```text
Project Facts
Architecture Facts
Permanent Conventions
Build/Test Commands
Non-Negotiable Rules
Critical Safety Constraints
```

and produce the minimum sufficient project context.

## 12. Skill Compiler

Input:

```text
task
workflow
repeated failure
reference material
verification criteria
```

Output:

```text
SKILL.md
references/
scripts/
examples/
```

## 13. Control Selection Engine

The engine shall determine whether a requirement belongs in:

```text
CLAUDE.md
RULE
SKILL
HOOK
AGENT
TOOL
MCP
VERIFIER
```

based on semantic role rather than convenience.

## 14. Evolution Engine

The Evolution Engine shall support:

```text
inventory
baseline
ablation
observation
failure detection
classification
candidate generation
testing
measurement
promotion
retirement
regression
```

## 15. Trend Engine

The Trend Engine shall compare:

```text
model generations
capabilities
failure distributions
scaffolding utility
tool usage
workflow changes
```

and generate hypotheses concerning emerging LLM behavior. No hypothesis becomes canonical without validation.

## 16. Governance Boundary

The Evolution Engine may propose changes autonomously. It shall not silently promote changes to canonical architecture.

```text
AUTONOMOUS
OBSERVE
ANALYZE
PROPOSE
EXPERIMENT
MEASURE

GOVERNED
DECIDE
PROMOTE
CANONICALIZE
```

## 17. Required End State

ACES OS shall be able to construct the minimum effective agent environment for:

```text
PROJECT
SESSION
TASK
MODEL GENERATION
```

while continuously removing obsolete scaffolding.

## 18. Target

> Minimum sufficient control for maximum reliable capability.
