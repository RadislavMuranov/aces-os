# Agent Loop Reconstruction

**Owner:** `core/agent-loop` implements `Agent` via `ctx.agentLoop`.

Documented turn flow (architecture.md):

```
turn/start
  claim next-step input + queued message
  assemble prompt sections + tool schemas
  agent/pre-step (waterfall) → reject | enter
  step/start
  user/message logged
  agent/request → llm/stream → assistant/chunk* → assistant/message
  tool/call* → tools/pre-execute → tools/execute → tools/post-execute → tool/result*
  step/end
  (repeat if tools owe request or next-step input)
  agent/turn-stopping (serial)
turn/end
```

**Decisions:** pre-step waterfall; model tool calls; tool pipeline waterfalls.  
**Termination:** natural stop + empty inbox + turn-stopping.  
**Persistence:** durable session events; model history derived from log (`deriveMessages`).  
**Invariant:** model-visible ⇒ logged.

Confidence: High for documented sequence; medium for every error/retry edge without code walk.
