# Plugin / Capability Graph (summary)

| Capability | Class | ctx / note |
|------------|-------|------------|
| Cordis | CORE runtime | vendor |
| agent-loop | CORE EXECUTION | ctx.agentLoop |
| agent registry | CORE | ctx.agents |
| session log | CORE DATA | ctx.sessions |
| system-prompt | CORE CONTEXT | ctx.systemPrompt |
| tools | CORE EXECUTION | ctx.tools |
| llm adapters | PLUGIN/SERVICE | ctx.llm |
| fs / shell / subprocess / sandbox | EXECUTION seams | multi-provider |
| skill | PLUGIN | skill registry |
| MCP | INTERFACE (via tools/MCP) | docs/guides |
| web search/fetch | PLUGIN | |
| subagent / workflow | PLUGIN | |
| hooks bridge | PLUGIN | Claude Code/Codex |
| UI web | INTERFACE | dsh-web-app |
| session projection | DATA | ctx.sessionProjections |

Seam pattern: Service Definition + Provider + Consumer.
