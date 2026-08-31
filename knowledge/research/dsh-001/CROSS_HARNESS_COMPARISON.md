# Cross-Harness Comparison (primitives)

| Primitive | DSH | Claude Agent SDK / Code | OpenAI Agents | LangGraph | MCP |
|-----------|-----|-------------------------|---------------|-----------|-----|
| Loop | Plugin agent-loop | Product loop | SDK loop | Graph nodes | N/A protocol |
| Context | Session log + systemPrompt | CLAUDE.md/skills | Instructions | State | Tool schemas |
| Tools | Guarded registry | Tools | Tools | Tools | Tools protocol |
| Sessions/replay | First-class append-only log | Session | Varies | Checkpoints | N/A |
| Plugins | Cordis everything-is-plugin | Limited | Limited | Custom | Servers |
| Sandbox | Multi-backend seam | sandbox-exec etc. | Varies | External | N/A |
| Policy | Approval + tool hooks | Permissions | Guardrails | Custom | Auth at server |

**Distinctive DSH:** Cordis spatiotemporal plugin composition; agent-loop itself a plugin; session-log invariant model-visible⇒logged; profile/bundle patch composition.

**Convergent:** tool loops, MCP, skills-like packs, sandbox attempts.
