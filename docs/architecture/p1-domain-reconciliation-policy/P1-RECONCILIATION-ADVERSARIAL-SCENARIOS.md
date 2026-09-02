# P1 Reconciliation Adversarial Scenarios (documentation-level)

| ID | Scenario | Expected under this pack |
|----|----------|--------------------------|
| **T1** | GitHub branch moves A→B | Branch projection updates; commits A and B remain distinct immutable identities |
| **T2** | Obsidian file renamed | Rename ≠ new entity if continuity policy+evidence; else IDENTITY handling with epoch; path is label |
| **T3** | Gmail thread multi-message | threadId ≠ message id; both preserved |
| **T4** | Slack message edited | Edit recorded; do not fabricate pre-edit text if provider no longer exposes it (PARTIAL) |
| **T5** | Drive file moved | fileId stable; parent change is representation; no new identity |
| **T6** | Kaiten conflicting card status | CONFLICT/UNRESOLVED unless ACTIVE domain policy resolves; no silent latest-wins |
| **T7** | Two providers conflicting state | CONFLICT/UNRESOLVED without Level-2 mapping + policy |
| **T8** | Missing source_timestamp | ORDERING_UNKNOWN where order required; no arrival-as-truth |
| **T9** | same request_id + different payload_digest | REJECT/CONFLICT (P0/P1 replay) — not a reconciliation “winner” |
| **T10** | Provider write success | Observation only; **no** AcceptedState without Evidence→Verification |

All scenarios: implementers claiming compliance must match these outcomes; residual PVR must surface as PARTIAL/UNKNOWN not invented truth.
