---
description: Independent security review of the current change set and affected execution paths.
argument-hint: [scope or --fix]
disable-model-invocation: true
context: fork
---

Perform a separate security review. Do not modify files unless $ARGUMENTS contains --fix.

Inspect the current diff and trace affected code paths. Prioritize authentication, authorization, identity/capability/policy checks, secrets and credentials, command/shell/SQL/template/path injection, path traversal and symlinks, subprocess execution, network boundaries and SSRF, logging and data leakage, cross-user isolation, replay, provenance, state transitions, and dependency/supply-chain risks where evidence exists.

For every finding provide severity, exact file and line, preconditions, impact, and evidence. Search the full class across analogous paths. Mark pre-existing findings separately. Do not claim exploitability without a demonstrated path; label unverified exploit hypotheses. Do not repeat prior findings. Style notes are not security findings.

Output: Critical/High/Medium/Low findings, pre-existing findings, attack paths inspected, exact tests/raw output/exit code, unverified hypotheses, remaining unknowns.

If --fix is present, minimally correct confirmed findings, add regression tests for each corrected failure mode, run relevant tests, and re-review. Do not commit or push.
