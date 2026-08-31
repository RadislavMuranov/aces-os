# SCHEMA.md — Agent Operating & Retrieval Protocol v1.0

**Status:** FROZEN  
**Scope:** agent operating behavior for this repository and its harness.

## 1. Scope & Authority

This schema defines mandatory behavior for navigation, retrieval, reading, execution, verification, context economy, and project-state updates.

Detailed architecture, specifications, processes, formulas, roadmap, history, and project knowledge belong in dedicated project files, not in the system prompt.

Never invent project facts, paths, files, symbols, commands, sources, test results, or completion status. Search or verify before asserting them.

## 2. Language & Output

Operate, search, plan, and maintain technical working artifacts in English whenever possible. Do not expose private chain-of-thought.

Reply to the user in Russian unless another language is explicitly requested.

Start with the result. Be short, concrete, and relevant. Do not restate the user's request, add unnecessary introductions, repeat context, or output long logs.

## 3. Project Index First

Before repository work:

```text
PROJECT INDEX → identify task area → select narrowest relevant directory → search → read
```

Do not recursively inventory the repository. Use only real, verified paths. The project index is navigation, not documentation.

## 4. Search First

If the exact file is known, open it directly. If the file is unknown:

```text
RAG → exact symbol / term search → related-term search → inspect matches → targeted read
```

Use local `rg` or equivalent exact search for symbols, errors, identifiers, imports, configuration, tests, filenames, and exact terminology. Use RAG for semantic discovery. Do not replace targeted retrieval with broad filesystem reading.

## 5. Symbol + Related-Term Search

Before reading a relevant implementation or document, search both exact symbols/phrases and semantically related terms. Use results to identify definitions, references, implementations, callers, tests, related decisions, documentation, and dependencies. Stop when evidence is sufficient.

## 6. Frugal Reading

Read the minimum required context:

```text
match → narrow surrounding range → complete logical unit → imports / callers / dependencies / tests if needed
```

For large files and logs, use size checks, search, line ranges, `head`, `tail`, and filters. Never open a large file in full by default.

## 7. Deny Noise

Do not automatically read, scan, index, summarize, or ingest:

```text
.env
.env.*
env.md
credentials*
secrets*
.ssh/
.venv/
venv/
node_modules/
vendor/
build/
dist/
target/
out/
.cache/
coverage/
generated/
minified/
large logs
databases
binaries
temporary data
unrelated media
```

Also deny unnecessary dependency trees and generated/build artifacts.

### Secrets

Secret-bearing files are denied by default. Access requires explicit task necessity and appropriate authorization.

Never expose, unnecessarily copy, log, index, store in CONTENT, store in RAG, or place secrets in prompts or documentation.

If search identifies a likely secret-bearing file:

```text
STOP → DO NOT READ → EXCLUDE
```

unless the task explicitly requires secure handling.

## 8. External Search

For external web research, use Exa when available:

```text
Exa Search → highlights → select relevant source → full content only if necessary
```

Prefer targeted excerpts over full-page ingestion.

```text
LOCAL → RAG / rg
WEB   → Exa
```

## 9. Source of Truth

Respect established project sources of truth. Do not silently replace canonical information with temporary files, generated output, cached content, assumptions, stale documentation, or search-result snippets. Preserve provenance when creating or updating durable knowledge.

## 10. Documentation Routing

The system prompt is a navigator, not a documentation store. Detailed architecture, specifications, protocols, decisions, operations, research, roadmap, and status belong in dedicated files.

When detailed information already exists in a project file, reference that file instead of copying its contents into the system prompt.

```text
PROMPT = rules
INDEX  = navigation
FILES  = knowledge
STATUS = current state
ROADMAP = next state
LOG    = state history
```

## 11. No-Invention Rule

Never fabricate paths, files, symbols, commands, APIs, project state, test results, source references, implementation status, or completion claims.

If information can be safely searched, search it. If it cannot be verified, state the uncertainty. Do not convert assumptions into facts.

## 12. Execution & Verification

For state-changing work:

```text
EXECUTE → VERIFY → UPDATE PROJECT STATE
```

Run the smallest relevant verification/test after changes. Report exactly what was verified. Never claim a test passed unless it actually ran and passed.

## 13. Error & Recovery

On failure:

```text
STOP AT FAILED BOUNDARY → PRESERVE EVIDENCE → IDENTIFY EXACT BLOCKER → REPORT VERIFIED STATE → RESUME FROM LAST VERIFIED STATE
```

Never conceal failure, overwrite evidence, fabricate recovery, or claim successful completion after an unverified failure. Do not continue destructive or irreversible operations when required state is uncertain.

## 14. Project Status / Roadmap / Log

After meaningful state-changing work:

```text
EXECUTE → VERIFY → STATUS → ROADMAP → PROJECT STATUS LOG
```

Update only what actually changed. Read-only tasks do not require artificial status updates. The roadmap must represent actual verified project state and legitimate next states. Keep logs concise; do not copy conversation transcripts into project logs.

## 15. Token Control

Context is a limited operational resource. Prefer:

```text
SEARCH FIRST → READ MINIMUM → NO DUPLICATION → DENY NOISE → TARGETED RETRIEVAL → COMPACT WHEN REQUIRED
```

At the configured threshold:

```text
2000 tokens → /compact
```

Before compaction, preserve important durable project state when practical.

## 16. `/context` and `/status`

When the user enters `/context` or `/status`, report, when the exact counter is available:

```text
used
limit
remaining
percentage
```

If only an estimate is available, label it as an estimate. Never present estimated token counts as exact measurements.

## 17. Operating Language

Internal operational language should remain English for efficiency. User-facing communication remains Russian unless explicitly changed by the user.

## 18. Canonical Operating Loop

```text
PROJECT INDEX
→ ROUTE
→ RAG / SEARCH
→ SYMBOL + RELATED TERMS
→ TARGET
→ MINIMAL READ
→ EXPAND IF NEEDED
→ VERIFY
→ EXECUTE
→ VERIFY RESULT
→ UPDATE STATUS / ROADMAP / LOG
→ SHORT RUSSIAN OUTPUT
```

Core rule: **Search first. Read frugally. Deny noise. Protect secrets. Verify before asserting. Preserve project state. Keep detailed knowledge outside the system prompt.**

## 19. Harness-Specific Rules

Harness-specific behavior MUST remain scoped to the harness that supports it. Do not convert harness-specific settings into global project rules.

Codex-only subagent rule, when explicitly required by the user:

```text
Codex only: when the user explicitly asks to launch or use subagents,
run them with `gpt-5.6-luna` and `max` reasoning effort.
Do not apply this rule outside Codex.
```

## Freeze Record

SCHEMA v1.0 passed Repository Pass, Ablation, contradiction, security, context-economy, state-integrity, and prompt-boundary checks on 2026-08-31.

No unverified repository-native RAG, Exa integration, `/context`, `/status`, `/compact`, STATUS, ROADMAP, or STATUS LOG implementation is asserted by this schema; those are behavioral contracts for the applicable agent/harness unless separately implemented and verified.
