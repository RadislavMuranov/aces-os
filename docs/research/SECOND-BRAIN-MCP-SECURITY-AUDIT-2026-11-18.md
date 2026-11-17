# second-brain-mcp — Dependency Security Audit

Date: 2026-11-18  
Repository: vladilenm/second-brain-mcp  
Pinned source commit: 53c45847d178f50b45e7620c0e701380f76cc4f6

## Baseline

The existing local checkout audit initially reported 10 production-tree vulnerabilities: 3 moderate, 6 high, 1 critical.

Affected packages included @modelcontextprotocol/sdk, proxy-addr, fast-uri, ip-address, js-yaml, body-parser, qs, hono, @hono/node-server and zod. The critical advisory was proxy-addr (IPv4-mapped IPv6 trust-subnet / IP spoofing issue).

## Safe remediation

Applied npm audit fix --ignore-scripts to the existing local checkout. No --force was used and no install scripts ran. package.json was not changed by this operation; its pre-existing local edit was preserved. package-lock.json changed by 66 insertions / 41 deletions.

After safe remediation:
- 2 production-tree findings remain: 1 moderate in @hono/node-server and 1 high in zod.
- Critical count: 0.
- npm test: 9/9 PASS; TypeScript build PASS; git diff --check PASS.
- The Zod fix offered by npm audit requires zod@4.6.7 and is marked as a breaking major change. It was not applied pending compatibility validation.
- The remaining @hono/node-server issue is transitive through the MCP Node package and needs a compatibility-safe dependency/override decision.

## Control

| Item | Status |
|---|---|
| Baseline dependency audit | CONFIRMED — 10 findings |
| Non-forced remediation | CONFIRMED — critical removed |
| Tests after remediation | CONFIRMED — 9/9 |
| Remaining vulnerabilities | REVIEW — 1 moderate, 1 high |
| Zod major upgrade | NOT APPLIED — breaking compatibility risk |
| Production readiness | NOT ESTABLISHED |

No upstream commit, push or PR. No service deployment or restart. The local checkout remains uncommitted.
