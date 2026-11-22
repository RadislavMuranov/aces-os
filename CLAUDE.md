# Claude Code — ACES OS repository entrypoint

This is harness-specific guidance, not Canon or an authorization source.

1. Read AGENTS.md and SCHEMA.md before repository-dependent work.
2. Apply the authoritative Notion rule RULE-METHOD-SELECTION-001 before material action: https://app.notion.com/p/3d60e90e16c681c4a964f8006517ce2e
3. Keep governance, method selection, execution, evidence, verification, and acceptance separate.
4. Do not edit AGENTS.md, SCHEMA.md, spec/MASTER-PROTOCOL.md, or active governance artifacts without the applicable explicit authorization and Master Control Protocol procedure.
5. PreToolUse hooks apply only to Claude Code tool calls. They do not govern other harnesses, external processes, or file mentions inserted without a tool call.
6. Never claim that a hook proves semantic truth. The Stop hook validates defect-specific evidence fields for 23 registered defects and rule-specific evidence fields for 155 policy sections; these are machine-checked evidence gates, not independent semantic proof.
7. Never read .env or .env.*; .env.example is allowed. Do not use @ file mentions for sensitive files.
8. Do not disable, bypass, or weaken hooks. Ambiguous commands require user confirmation.
9. The journal records timestamp, rule ID, and decision only. Never log command text or secret values.
10. /code-review reviews code; --fix authorizes minimal corrections to confirmed findings only. /security-review is a separate security pass.
11. Report findings with exact file and line. Separate pre-existing findings from regressions. Maximum three style notes per review.
12. Do not create branches, commits, PRs, or push without explicit authorization.
13. Shell enforcement is conservative, not a complete Bash/PowerShell interpreter. Tested command-local Git aliases, Bash aliases to Git, and PowerShell Set-Alias/New-Alias mappings are resolved before applying Git controls. Unknown Git subcommands and unresolved shell aliases with protected Git argument signatures return ASK. Dynamic PowerShell Invoke-Expression and variable-based call operators return ASK. Start-Process/start launching Git with parseable arguments is passed through the existing Git controls (DENY/ASK/ALLOW); ambiguous launch arguments return ASK. Do not claim universal interception of persistent shell functions/aliases or arbitrary scripts.
14. A direct invocation of aces-hook-engine.mjs verifies engine behavior, not that Claude Code loaded the hook. Runtime integration requires an observed Claude Code tool event and correlated journal record.
15. Current review entrypoints are .claude/commands/code-review.md and .claude/commands/security-review.md. No root review.md exists; do not create one until its intended path and authority are resolved.

A PASS in this repository requires an ACES_ITERATION_RECORD with exact verification command, raw output, exit code, all 23 defect classifications, one CONTROL <DEFECT-ID> record with the defect-specific fields and test reference per defect, and POLICY RULES CHECKED entries in the form <POLICY-ID>=PASS@<source-evidence>#<test-path> for all 155 policy sections. Each policy section also requires its mapped rule-specific evidence fields. Missing evidence or test references means BLOCKED. These attestations do not prove semantic truth; semantic review remains evidence-bound and must not be self-certified as independently verified.
