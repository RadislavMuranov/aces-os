"""Logical types aligned with spec/asa/v0/data-model.md (ASA-003.2).

No GitHub role fields. Authentication does not imply Authority (I8).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Mapping, Optional, Union


class DecisionOutcome(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class Operation(str, Enum):
    """Closed Operation enum — DELEGATE excluded (OPEN-7)."""

    READ = "READ"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    EXECUTE = "EXECUTE"
    EXPORT = "EXPORT"
    IMPORT = "IMPORT"
    AUTHORIZE = "AUTHORIZE"
    REVOKE = "REVOKE"


class ResourceKind(str, Enum):
    KnowledgeObject = "KnowledgeObject"
    EvidenceObject = "EvidenceObject"
    MemoryObject = "MemoryObject"
    DecisionObject = "DecisionObject"
    SecretObject = "SecretObject"
    PolicyObject = "PolicyObject"
    ProtectedArtifact = "ProtectedArtifact"


ACCEPTED_AUTHENTICATORS = frozenset(
    {
        "architectural_authority_human",
        "implementation_agent",
    }
)

AUTHORITY_KIND_ARCHITECTURAL = "architectural_authority"


@dataclass(frozen=True)
class Identity:
    identity_id: str
    authenticator_id: str
    subject_ref: str
    verified_at: datetime
    claims: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class Principal:
    principal_id: str
    identity_id: str
    display_label: Optional[str] = None


@dataclass(frozen=True)
class ResourceRef:
    resource_id: str
    resource_kind: ResourceKind
    namespace: Optional[str] = None


@dataclass(frozen=True)
class ResourceSelectorExact:
    """Selector form A: exact resource_id list."""

    resource_ids: tuple[str, ...]


@dataclass(frozen=True)
class ResourceSelectorStructured:
    """Selector form B: kinds + optional namespace."""

    kinds: tuple[ResourceKind, ...]
    namespace: Optional[str] = None


ResourceSelector = Union[ResourceSelectorExact, ResourceSelectorStructured]


@dataclass(frozen=True)
class Capability:
    """Opaque server-side capability record (MULTI-USE within window)."""

    capability_id: str
    principal_id: str
    resource_selector: ResourceSelector
    operations: tuple[Operation, ...]
    not_before: datetime
    not_after: datetime
    issued_under_authority: str
    policy_id: str
    policy_version: str
    purpose: Optional[str] = None


@dataclass(frozen=True)
class Policy:
    policy_id: str
    version: str
    authority_id: str
    body: Mapping[str, Any]
    status: str
    not_after: Optional[datetime] = None


@dataclass(frozen=True)
class Authority:
    authority_id: str
    kind: str
    label: Optional[str] = None


@dataclass(frozen=True)
class RevocationRecord:
    capability_id: str
    revoked_at: datetime
    revoked_under_authority: str
    state: str


@dataclass(frozen=True)
class AuthorizationRequest:
    """Client-supplied request; non-authoritative until validated."""

    correlation_id: str
    identity: Identity
    principal: Principal
    capability_id: str
    resource: ResourceRef
    operation: Operation
    context: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class Decision:
    decision_id: str
    principal_id: str
    resource_id: str
    operation: Operation
    outcome: DecisionOutcome
    reason_code: str
    policy_id: str
    policy_version: str
    timestamp: datetime
    correlation_id: str
    capability_id: Optional[str] = None
    authority_id: Optional[str] = None


@dataclass(frozen=True)
class AuthorizationEvent:
    """Audit + Provenance record. Never an input that produces ALLOW (I7)."""

    event_id: str
    principal_id: str
    operation: Operation
    resource_id: str
    timestamp: datetime
    authority_id: str
    policy_id: str
    policy_version: str
    decision: DecisionOutcome
    result_or_error_class: str
    correlation_id: str
    capability_id: Optional[str] = None
