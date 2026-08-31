# Context Architecture

**Assembly:** `ctx.systemPrompt` waterfall + tool schemas + history projected from session log.  
**Sources:** system sections, tools, skills content, user/assistant/tool events, inject(), external tool results.  
**Persistent vs ephemeral:** durable SessionEvent stream vs live agent/* events.  
**Scaffolding:** skills, prompts, presets, AGENTS.md for repo agents, `.claude` present in tree — treat as DSH product conventions, not ACES necessity.

Confidence: High for log-as-source-of-truth claim (documented invariant).
