# MCP / Tool Boundary

```
LLM → DSH agent-loop → ctx.tools pipeline → tool/MCP/shell/fs → world
```

Guarded pipeline: pre-execute → execute → post-execute waterfalls.  
Can DSH be substrate under ACES Connector Fabric? **Conditionally yes** as execution engine if ACES owns authorization/decision envelope above tool invocation. DSH does not replace ACES Authority Boundary.

Confidence: Medium-High (docs + package map).
