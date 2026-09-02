# P1 Conflict Taxonomy

| Code | Meaning | Detection | Allowed resolution | Default | Provenance |
|------|---------|-----------|-------------------|---------|------------|
| IDENTITY_CONFLICT | Same assumed entity, incompatible bindings | Divergent Level 0–2 keys | Explicit correlation policy only | UNRESOLVED | Full identity + observations |
| VALUE_CONFLICT | Same identity, different field values | Comparison_rule fail | Field-scoped precedence policy | UNRESOLVED | Field-level |
| VERSION_CONFLICT | Incompatible revisions | Revision ids/hashes disagree | Revision policy | UNRESOLVED | Revision refs |
| TEMPORAL_CONFLICT | Incompatible times | Conflicting source times | Temporal policy | UNRESOLVED / ORDERING_UNKNOWN | Timestamps |
| PERMISSION_CONFLICT | Capability/visibility disagree | Scope mismatch | Never elevates ACES authz | UNRESOLVED | Scopes |
| DELETION_CONFLICT | Deleted vs live/trash disagree | Lifecycle states clash | Deletion policy | UNRESOLVED | Lifecycle |
| EXISTENCE_CONFLICT | Exists vs not | Presence disagree | Must not treat NOT_OBSERVED as ABSENT | UNRESOLVED | |
| PARTIAL_OBSERVATION_CONFLICT | Partial vs full clash | Partial flags | Prefer preserve unknown | PARTIAL / UNRESOLVED | |
| SOURCE_SCOPE_CONFLICT | Assertions outside scope | Scope check | Reject out-of-scope claim | UNRESOLVED | Scope |
| ORDERING_CONFLICT | Sequence disagree | Order rules fail | Temporal policy | ORDERING_UNKNOWN | |
| REPRESENTATION_CONFLICT | Same facts, incompatible shapes | Normalization residual | Versioned normalize | UNRESOLVED if residual | Norm version |
| POLICY_CONFLICT | Overlapping policies | Composition check | Human/governance | POLICY_CONFLICT | Policy ids |

**No class defaults to silent winner.**
