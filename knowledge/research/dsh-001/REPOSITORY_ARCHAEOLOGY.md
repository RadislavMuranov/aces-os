# Repository Archaeology

**Commit:** 0a53fb55…  
**Topology (from AGENTS.md + tree listings):**

```
vendor/          Vendored Cordis
packages/
  core/          session, system-prompt, tools, agent, agent-loop, scope
  api/           BFF / Typert RPC
  llm/           LLM service + deepseek + pi-ai adapters
  e2b/           sandbox POC adapters
  shell/         bash capability
  subprocess/    process tree
  terminal/      persistent sessions
  fs/            filesystem + policy
  lsp/
  skill/         skill registry + loader tool
  web/           search/fetch
  compaction/
  context/
  subagent/
  bundle/        profile bundles (base, web-app, headless, sdk, acp…)
  workflow/
  webhook/
  todo/, plan/, preset/
  guard/
  self-modification/
  hooks/         Claude Code/Codex hook bridges
  session/       durable projection, titles, telemetry
  identity/
apps/            CLI / launchers
docs/, website/, python/, native/, scripts/, snapshots/, patches/
.claude/, .agents/
```

**Profiles:** web, headless, sdk, sdk-minimal, acp  
**Composition:** profile → ordered bundles → cordis.patch.yml → home patch → CLI --patch

Confidence: High (layout documented + observed).
