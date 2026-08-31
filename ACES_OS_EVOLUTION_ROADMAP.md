# ACES OS EVOLUTION ROADMAP

**Program:** ACES OS Evolution Control System  
**Status:** CANONICAL PROPOSAL — pending Master Control Protocol / Canon Gate approval

## Objective

Build a governed Evolution Engine that keeps ACES OS aligned with rapidly changing LLM capabilities while preventing agent scaffolding from fossilizing.

## Governing Loop

```text
MODEL CHANGE
   ↓
ABLATION
   ↓
REMOVE OPTIONAL SCAFFOLDING
   ↓
OBSERVE
   ↓
IDENTIFY REAL FAILURE
   ↓
CLASSIFY
   ↓
REINTRODUCE ONLY NECESSARY CONTROL
   ↓
VERIFY
   ↓
MEASURE
   ↓
PROMOTE / MODIFY / RETIRE
```

## Phase E0 — Canonical Foundation

Create and govern:

- `ACES_OS_EVOLUTION_ROADMAP.md`
- `ACES_OS_EVOLUTION_MASTER_PROTOCOL.md`
- `ACES_OS_EVOLUTION_MASTER_SPECIFICATION.md`
- `ACES_OS_EVOLUTION_MASTER_CHECKLIST.md`
- `ACES_OS_EVOLUTION_MANIFEST.md`

Gate: authority, lifecycle, evidence model, ablation model, promotion/retirement criteria, protected invariants, and relationship to the Master Control Protocol are defined.

## Phase E1 — Scaffolding Inventory

Inventory project/session agent scaffolding:

```text
CLAUDE.md
.claude/rules/
.claude/skills/
.claude/hooks/
agents/
tools/
MCP configuration
verification tooling
```

Record purpose, provenance, expected benefit, observed benefit, cost, risk, dependencies, status, last verification and last ablation.

## Phase E2 — Minimal Baseline

Provide a reproducible environment with optional scaffolding removed, while preserving protected security and governance invariants. Establish baseline behavior for representative tasks.

## Phase E3 — Project Context Compiler

Generate minimal project/session `CLAUDE.md` from:

- Project Facts
- Architecture Facts
- Permanent Conventions
- Build/Test Commands
- Non-Negotiable Project Rules
- Critical Safety Constraints

Do not convert historical prompt debt into permanent context.

## Phase E4 — Skill Compiler

Generate evidence-driven Skills using progressive disclosure:

```text
.claude/skills/<skill>/
├── SKILL.md
├── references/
├── scripts/
└── examples/
```

`SKILL.md` uses routing-oriented `name` and `description`, plus Goal, Invariants, Evidence, Required Output and Gotchas where applicable.

## Phase E5 — Hook Compiler

Generate runtime controls only when requirements require deterministic enforcement. Prioritize protected artifacts, authorization, secrets, destructive actions, provenance, audit and mandatory verification.

## Phase E6 — Observed Failure Engine

Capture and classify actual failures:

```text
MODEL
CONTEXT
WORKFLOW
TOOL
MCP
VERIFICATION
GOVERNANCE
SECURITY
```

A failure becomes a control candidate only through defined evidence criteria.

## Phase E7 — Control Synthesis

Map observed needs to the semantically correct mechanism:

```text
FACT        → CLAUDE.md / Rule
WORKFLOW    → Skill
ENFORCEMENT → Hook
CAPABILITY  → Tool / MCP
SPECIALIZED COGNITION → Agent
ACCEPTANCE  → Verification
```

## Phase E8 — Ablation Engine

Run controlled removal experiments and compare identical task sets against baseline. Measure reliability, verification, cost, latency, context usage, safety impact and relevant error rates.

## Phase E9 — LLM Change Detection

Track model-generation changes in capabilities, instruction following, tool use, context behavior, reasoning, multimodality, agency and failure modes.

## Phase E10 — Emerging Trend Engine

Treat trend detection as hypothesis generation, not prophecy:

```text
OBSERVATION
   ↓
HYPOTHESIS
   ↓
EXPERIMENT
   ↓
EVIDENCE
   ↓
DECISION
   ↓
CANON
```

## Phase E11 — Self-Evolving Toolchain

Allow the system to propose and construct project/session/task-specific:

```text
CLAUDE.md
Rules
Skills
Hooks
Agents
Verification
Scripts
References
MCP integrations
```

Promotion remains governed; autonomous systems may observe, analyze, propose, experiment and measure, but may not silently canonicalize.

## Phase E12 — Evolution Gate

Every material evolution passes the applicable:

```text
ABLATION
REGRESSION
SECURITY
VERIFICATION
CANON
```

gates before acceptance.

## Long-Term End State

ACES OS becomes capable of constructing the minimum effective agent environment for each project, session, task and model generation, while continuously detecting and retiring obsolete scaffolding.

> Minimum sufficient control for maximum reliable capability.

> Reality precedes canon.
