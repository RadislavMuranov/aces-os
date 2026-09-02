# P1 Layer Implementation Readiness Matrix

| Layer | Status | Notes |
|-------|--------|-------|
| ConnectorIdentity | READY | P0/P1 |
| ConnectorCapability | READY | ≠ Authority |
| ResourceRef | READY | provider+namespace+native id+epoch |
| Operation | READY | READ vs side-effect classes |
| Scope | READY | |
| AuthorizationRef | READY | Mandatory for side effects; ASA |
| Observation | READY | ≠ Evidence |
| EvidenceCandidate | READY | |
| EvidenceAdmission | READY-WITH-CONSTRAINT | Needs ApprovalRecord for ACTIVE admission policy |
| Evidence | READY | ≠ AcceptedState |
| Provenance (structural) | READY | Crypto DEFERRED |
| ReplayBinding | READY | request_id+payload_digest |
| PartialObservation | READY | UNKNOWN≠FALSE |
| DWOM | READY | ≠ Knowledge/Semantic Reality |
| Reconciliation | READY-WITH-CONSTRAINT | Default CONFLICT; resolve needs ACTIVE instances |
| Digital World State | READY | ≠ Semantic Reality |
| Verification (Axis-C) | READY-WITH-CONSTRAINT | G2-R1 env BLOCKED |
| AcceptedState | READY (boundary) | Connector must not mint |
| Knowledge / Memory / WM | DEFERRED for first slice after AcceptedState | Downstream |
| Semantic Reality | DEFERRED | Not connector path |
| ASA | READY (boundary) | Writes blocked until write gate |
| MCP/CLA | READY (rule) | Native preferred |
| Fail-closed | READY | Catalogued cases |
