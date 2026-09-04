# ACES OS — Distributed Digital Reality Reconciliation Protocol Pack v1.0

**Status:** FROZEN RESEARCH PROTOCOL / NOT CANON
**Date:** 2026-09-04
**Roadmap:** `docs/research/distributed-digital-reality-reconciliation-roadmap-v1.0.md`
**Scope:** read-only research and controlled verification first; implementation only after explicit gate authorization.

## 0. Protocol doctrine

The protocol pack defines the executable research procedure for resolving the problem:

```text
multiple agents
+ multiple contexts
+ multiple connector instances
+ multiple external representations
        ↓
       ACES
```

Core rule:

> Observation is admissible only together with enough identity, target, provenance and temporal context to determine what was observed, by whom, where, and when.

Second rule:

> Reconciliation may identify consistency, conflict, precedence or uncertainty; it must not silently arbitrate truth.

Third rule:

> No unresolved observation may be promoted to AcceptedState.

---

# Protocol RDR-P00 — Baseline Freeze

### Objective
Freeze the research question, scope and vocabulary before collecting new evidence.

### Inputs
- RDR roadmap v1.0.
- Existing ACES P0 boundaries.
- Existing connector inventory.

### Procedure
1. Record repository, branch, commit and protocol version.
2. Record the exact research hypothesis.
3. Record all non-equalities listed in the roadmap.
4. Declare excluded systems and actions.
5. Mark current knowledge as `BASELINE`, never `CANON`.

### Required evidence
- Baseline record.
- Git commit SHA.
- Research hypothesis identifier.

### Gate
`G-RDR-0 PASS` iff the baseline is reproducible and no implementation claim is mixed into the research baseline.

---

# Protocol RDR-P01 — Connector Reality Inventory

### Objective
Determine what each connector actually exposes, rather than what its tool description implies.

### Record
For each connector/channel:

```text
connector_id
connector_instance_id
execution_channel
host/context identifier
read capability observed?
write capability observed?
authentication observed?
actor identity observed?
scope observed?
reachable target observed?
source timestamp
provenance
status
```

### Procedure
1. Enumerate connector instances.
2. Perform the smallest safe read operation.
3. Record successful identity/authentication evidence separately from tool availability.
4. Record write capability only if directly observed; otherwise `UNKNOWN`.
5. Record execution channel separately for API, local shell, browser, remote runner, etc.
6. Never infer common identity from common human ownership.

### Failure rule
`tool exists` without successful authentication/identity observation = `UNKNOWN`, not `AUTHENTICATED`.

### Gate
`G-RDR-1 PASS` iff every connector claim has direct evidence or explicit `UNKNOWN`.

---

# Protocol RDR-P02 — Actor / Workload Identity Binding

### Objective
Bind an observation or action to a verifiable actor/workload identity.

### Minimum identity tuple

```text
human_actor (when available)
agent_id
agent_instance_id
workload/execution identity
connector_instance_id
identity_scope
credential/auth method
identity evidence
validity interval
```

### Procedure
1. Obtain connector-native identity evidence.
2. Obtain workload identity where available.
3. Bind identity evidence to the observation envelope.
4. Distinguish human identity from workload identity.
5. Mark unverifiable identity as `UNKNOWN`.

### External alignment
SPIFFE is a candidate identity substrate because its Workload API provides cryptographically verifiable workload identities; its references are explicitly scoped to an applicable execution/control-plane boundary. citeturn0search1turn0search6

### Gate
`G-RDR-1` cannot PASS for an observation class if the claimed actor cannot be independently identified.

---

# Protocol RDR-P03 — External Object / Target Binding

### Objective
Prove what external object a connector observation or action refers to.

### Target tuple

```text
system_id
connector_instance_id
native_object_type
native_object_id
native_scope
canonical locator if available
object version / revision if available
retrieval timestamp
identity confidence
```

### Procedure
1. Capture the source-native identifier.
2. Capture its scope (workspace, repository, account, tenant, branch, path, etc.).
3. Resolve the identifier using the source system, not agent text alone.
4. Compare candidate objects across connectors.
5. If equivalence cannot be proven, retain separate objects or mark `AMBIGUOUS`.

### Prohibition
Name similarity, URL similarity or semantic similarity alone cannot mint `SAME_OBJECT`.

### Gate
`G-RDR-2 PASS` iff same-object mappings are independently reproducible.

---

# Protocol RDR-P04 — Provenance Chain

### Objective
Make every observation/action reconstructible.

### Minimum provenance envelope

```text
observation_id
evidence_id
actor/workload identity
connector instance
source system
source object
operation
input/reference
output/observation
timestamp
causal parent(s)
retrieval/execution context
content hash or equivalent integrity marker
```

### Procedure
1. Capture provenance at ingestion/execution time.
2. Preserve source-native identifiers.
3. Link derived observations to their parent evidence.
4. Never replace source provenance with an agent-generated summary.
5. Store raw evidence where policy permits.

### External alignment
W3C PROV provides a standard vocabulary for entities, activities, agents and derivation/provenance relationships and is therefore a candidate interchange layer, not an ACES authority layer. citeturn0search8

### Gate
`G-RDR-3 PASS` iff an independent reviewer can reconstruct the observation path without trusting an agent's narrative.

---

# Protocol RDR-P05 — Temporal / Causal Ordering

### Objective
Prevent arrival order from being mistaken for world-state order.

### Required fields

```text
observed_at
received_at
executed_at (if applicable)
source_version
causal_parent_ids
sequence / revision if source provides one
clock quality
freshness / expiry policy
```

### Procedure
1. Record source time and ACES receipt time separately.
2. Preserve source revisions/version identifiers.
3. Detect stale observations.
4. Mark concurrent observations as concurrent unless causality is proven.
5. Never choose the latest-arriving observation solely because it arrived last.

### Gate
`G-RDR-4 PASS` iff stale/concurrent/superseding observations are distinguishable.

---

# Protocol RDR-P06 — Cross-Connector Reconciliation

### Objective
Reconcile observations that may describe the same external reality.

### Input
Two or more target-bound observations.

### Procedure
1. Resolve target identity.
2. Normalize only semantics required for comparison; preserve source representation.
3. Compare state fields.
4. Classify relation:

```text
CONSISTENT
SUPERSEDES
CONCURRENT
CONFLICT
DUPLICATE
INCOMPARABLE
UNKNOWN
```

5. Preserve every source observation.
6. Produce a reconciliation record.
7. Do not delete or overwrite evidence because a source appears more authoritative.

### Output

```text
reconciliation_id
subject_target
input_observation_ids
relation
conflict_fields
resolution_status
policy_reference (if any)
proposed state
unresolved fields
```

### Gate
`G-RDR-5 PASS` iff reconciliation preserves source evidence and makes conflict explicit.

---

# Protocol RDR-P07 — Authority / Policy Separation

### Objective
Prevent source-system authority from becoming ACES authorization authority.

### Decision tuple

```text
actor
requested action
resource/target
capability
policy_id
rule_id
scope
source authority
ACES authorization decision
reason
```

### Procedure
1. Identify who owns/controls the external system.
2. Identify what the source permits.
3. Separately evaluate what ACES permits the actor to request.
4. Reject any implicit authority escalation.
5. Record policy decision before execution.

### Rule

```text
Source Authority != ACES Authorization Authority
Capability != Permission
Permission != Approval
```

### Gate
`G-RDR-6 PASS` iff authorization remains ACES-governed and source permissions are treated as external constraints, not ACES policy.

---

# Protocol RDR-P08 — Evidence → Verification → Acceptance

### Objective
Establish the only state-promotion path.

### Pipeline

```text
Observation / Execution Receipt
        ↓
Evidence
        ↓
Verification
        ↓
Acceptance Decision
        ↓
AcceptedState
```

### Verification minimum
- Expected condition.
- Observed condition.
- Evidence references.
- Verification method/version.
- Result.
- Uncertainty/conflict status.

### Acceptance rule
Acceptance is prohibited when verification is missing, contradictory or out of scope.

### Gate
`G-RDR-7 PASS` iff no direct connector/agent/model path can mint AcceptedState.

---

# Protocol RDR-P09 — Accepted Digital World State

### Objective
Define the smallest state ACES is willing to rely upon operationally.

### AcceptedState tuple

```text
accepted_state_id
target_id
state payload
source observation ids
evidence ids
verification id
acceptance id
accepted_at
valid_until / freshness policy
scope
status
```

### Rules
1. Every accepted field must be evidence-backed.
2. Every accepted target must be identity-bound.
3. Acceptance is scoped and temporal.
4. Unknown fields remain unknown.
5. AcceptedState is not a claim of omniscient external truth.

### Gate
`G-RDR-8 PASS` iff accepted state is reconstructible from evidence and verification.

---

# Protocol RDR-P10 — Mutation Gate

### Objective
Block dangerous writes when Digital Reality is unresolved.

### Pre-mutation sequence

```text
Mutation Intent
 → Actor Identity
 → Connector Identity
 → Target Identity
 → Current State
 → Lineage
 → Provenance
 → Conflict Check
 → Capability
 → ACES Authorization
 → Execution Target
 → Execute
 → Observe
 → Verify
 → Accept
```

### Mandatory BLOCK conditions
- actor unknown where identity is required;
- connector instance unknown;
- target ambiguous;
- authorization absent/expired;
- conflicting state unresolved where conflict matters;
- stale state beyond policy;
- execution target differs from authorized target;
- verification impossible;
- evidence persistence unavailable where evidence is mandatory.

### Gate
`G-RDR-9 PASS` iff every unresolved mandatory condition fails closed.

---

# Protocol RDR-P11 — Adversarial / Chaos Verification

### Objective
Reproduce the multi-agent/multi-connector failure class before implementation claims are made.

### Mandatory scenarios

1. Same human, different connector instances.
2. Same external service, different authenticated accounts.
3. Same object name, different object IDs.
4. Same object ID, different scopes.
5. Same target, stale observation.
6. Two concurrent conflicting observations.
7. API authenticated, shell unauthenticated.
8. Agent claims an action succeeded without independent observation.
9. Connector reports success but target state cannot be verified.
10. Evidence arrives after an attempted mutation.
11. Replay of an old valid observation.
12. Connector disappears between authorization and execution.
13. Target changes between authorization and execution.
14. Agent/model consensus conflicts with source evidence.
15. Cross-session host continuity is assumed but unproven.

### Required result
Each scenario must yield a deterministic status and preserved evidence.

### Gate
`G-RDR-10 PASS` iff the system fails closed on unresolved reality and does not silently collapse contexts.

---

# Protocol RDR-P12 — Minimality / Necessity Test

### Objective
Test whether existing standards and infrastructure already satisfy the complete contract.

### Candidate stack

```text
Identity: SPIFFE / platform identity
Auth: OAuth/OIDC / source authorization
Connectivity: native / direct / MCP
Agent interoperability: A2A
Provenance: W3C PROV
Telemetry: OpenTelemetry
State reconstruction: event sourcing / append-only records
Distributed convergence: CRDT/causal mechanisms where applicable
Policy: existing policy/IAM engine
```

MCP itself defines transport-level authorization mechanisms, while A2A defines interoperability between independent agents; neither should be treated as the reconciliation or acceptance authority. citeturn0search9turn0search3

### Procedure
1. Implement the smallest complete experimental composition.
2. Run RDR-P01 through P11 against it.
3. Record every unresolved requirement.
4. Attempt to close each gap without introducing an ACES-specific authority layer.
5. Only then assess whether a new ACES boundary is necessary.

### Outcomes

```text
SUFFICIENT
SUFFICIENT_WITH_THIN_COORDINATION
INSUFFICIENT_NEW_BOUNDARY_REQUIRED
INCONCLUSIVE
```

### Gate
`G-RDR-11 PASS` only when the comparison is executable and evidence-backed.

---

# Protocol RDR-P13 — Architecture Decision

### Objective
Turn the research result into a bounded architectural decision without overclaiming.

### Decision record

```text
question
alternatives
evidence references
failed/satisfied contracts
residual gaps
operational consequences
security consequences
human interaction consequences
decision
scope
non-claims
reversal conditions
```

### Gate
`G-RDR-12 PASS` iff the decision is traceable to experimental evidence and includes explicit reversal conditions.

---

# Protocol RDR-P14 — Implementation Contract

### Objective
Translate only proven residual requirements into executable contracts.

### Preconditions
- RDR-P12 complete.
- RDR-P13 decision accepted.
- No unresolved blocker hidden by terminology.

### Procedure
1. Extract only failed/minimal contracts.
2. Define executable interfaces.
3. Define evidence schema.
4. Define deterministic failure states.
5. Define automated tests.
6. Define adversarial tests.
7. Define reproducible verification procedure.
8. Integrate with the existing ACES P0 roadmap without creating a competing roadmap.

### Gate
Implementation is `AUTHORIZED NEXT` only after explicit approval of the resulting contract.

---

## 15. Global evidence bundle

Every RDR experiment must produce, at minimum:

```text
experiment_id
protocol_version
roadmap_version
repo
branch
commit
executor/agent identity
connector instance(s)
execution context(s)
input references
observations
raw outputs where permitted
provenance
timestamps
target bindings
reconciliation records
policy decisions
verification records
acceptance records
failures
unknowns
final gate status
```

## 16. Evidence integrity rules

- No manually reconstructed result may be represented as observed execution.
- No successful tool call proves the whole chain.
- No failed local environment proves remote repository non-existence.
- No connector's tool availability proves authentication.
- No agent narrative substitutes for source evidence.
- No missing evidence may be silently inferred.
- Every blocked execution remains `BLOCKED / NOT EXECUTED`, not `FAIL` or `PASS`.

## 17. Relationship to existing ACES runtime

The current ACES minimum runtime already uses the conceptual sequence:

```text
Intent → Context → Authority/Policy → Connector Resolution → Execution
→ Observation → Evidence → Verification → Acceptance → Accepted State
```

The RDR protocol pack extends the research surface across **multiple independent connector instances and execution contexts**. It does not replace the existing runtime contract and does not authorize BASTION integration.

## 18. Final research invariant

```text
Many observations
    ↓
not automatically one reality

Many identities
    ↓
not automatically one actor

Many representations
    ↓
not automatically one object

Many successful actions
    ↓
not automatically one accepted state

ACES AcceptedState
    ↓
only through explicit evidence + verification + acceptance
```
