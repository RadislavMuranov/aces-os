# DSH-RESEARCH-001 Decision

## Pinned
- **DSH commit:** `0a53fb55bea101816fa226bb964ae2bed71c343b`
- **Version:** dsh@0.1.2-alpha.2 (pre-release)
- **Status:** Developer preview, MIT, public

## PRIMARY CANDIDATE STATUS
**CONDITIONAL**

## Summary answers
| Topic | Finding |
|-------|--------|
| Cordis kernel | Plugin runtime (services/events/effects/lifecycle) — not agent semantics |
| Agent loop | Documented turn/step driver; plugin-replaceable |
| Plugin architecture | Everything-is-plugin; profiles/bundles |
| Context | Session log + systemPrompt assembly; model-visible⇒logged |
| Skills | Optional capability packs |
| Hooks | Event waterfalls + Claude/Codex bridges |
| MCP/tools | Guarded tool pipeline; MCP-capable ecosystem |
| Sessions/replay | Append-only SessionEvent; fork/project |
| Security | Sandbox seam + approval; **not** ACES Authority; PI risk measured externally |
| Observability | Strong session log/trace; weak as governance evidence |

## Confidence
**Medium–High** on architecture from official docs; **Medium** on unreviewed source paths; external security **High concern**.

## Unresolved
Full native sandbox code audit; exact MCP host source; verification of secondary RCE claims; production hardness under plugin marketplace.

## ACES controls
No ACES implementation performed: **YES**  
No Canon mutation: **YES**  
No E1 execution: **YES**

**STOP.**
