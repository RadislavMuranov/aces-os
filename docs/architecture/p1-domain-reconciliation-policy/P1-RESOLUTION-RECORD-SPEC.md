# P1 ResolutionRecord Spec

A **ResolutionRecord** explains a policy-governed outcome. **It is not Truth.**

## Mandatory fields

| Field | Requirement |
|-------|-------------|
| `resolution_id` | Durable id |
| `policy_id` | |
| `policy_version` | |
| `conflict_id` | Or equivalent conflict key |
| `participants` | Observation / DWOM refs |
| `observations` | Full set preserved |
| `identity_mapping` | Level + keys used |
| `rule_applied` | From policy |
| `temporal_basis` | Which clocks; ORDERING_UNKNOWN if any |
| `source_scope` | |
| `provenance` | Chain |
| `resolution_timestamp` | ACES time |
| `authority_or_approval_reference` | Policy activation/approval |
| `resulting_dws_representation` | Projection + status |
| `unresolved_residuals` | Explicit |
| `outcome_status` | RESOLVED_UNDER_POLICY \| … |

## Forbidden

- ResolutionRecord as AcceptedState
- ResolutionRecord as Knowledge
- ResolutionRecord as ACES authorization
- Dropping losing observations when “resolved”
