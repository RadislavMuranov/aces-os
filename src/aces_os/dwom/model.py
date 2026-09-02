"""Minimal DWOM data model."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional, Tuple

from aces_os.connector.observation import ObservationState, PartialState
from aces_os.connector.resource import ResourceRef


class ExistenceState(str, Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    UNKNOWN = "UNKNOWN"
    NOT_OBSERVABLE = "NOT_OBSERVABLE"


class DeletionState(str, Enum):
    NOT_DELETED = "NOT_DELETED"
    DELETED = "DELETED"
    TRASHED = "TRASHED"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class DWOMStatus(str, Enum):
    KNOWN = "KNOWN"
    UNKNOWN = "UNKNOWN"
    PARTIAL = "PARTIAL"
    NOT_OBSERVABLE = "NOT_OBSERVABLE"
    ABSENT = "ABSENT"
    CONFLICT = "CONFLICT"
    UNRESOLVED = "UNRESOLVED"
    STALE = "STALE"


@dataclass(frozen=True)
class DWOMObject:
    """Observed/projected external digital-world state — not ACES truth."""

    dwom_object_id: str
    provider: str
    resource_ref: ResourceRef
    resource_kind: str
    scope_namespace: str
    observed_state: ObservationState
    existence_state: ExistenceState
    deletion_state: DeletionState
    partial_state: PartialState
    version_or_revision: Optional[str]
    observed_at: str
    source_timestamp: Optional[str]
    provider_event_time: Optional[str]
    observation_id: str
    request_id: str
    payload_digest: str
    connector_id: str
    configuration_scope: str
    status: DWOMStatus
    payload: Dict[str, Any] = field(default_factory=dict)
    pvr_flags: Tuple[str, ...] = ()
    correlation_key: str = ""
    authenticity_crypto: str = "DEFERRED"

    def is_evidence(self) -> bool:
        return False

    def is_accepted_state(self) -> bool:
        return False

    def is_knowledge(self) -> bool:
        return False

    def is_semantic_reality(self) -> bool:
        return False


@dataclass
class DigitalWorldState:
    """Collection of DWOM objects for a scope — not Semantic Reality."""

    objects: Dict[str, DWOMObject] = field(default_factory=dict)

    def get(self, dwom_object_id: str) -> Optional[DWOMObject]:
        return self.objects.get(dwom_object_id)

    def by_correlation(self, key: str) -> Tuple[DWOMObject, ...]:
        return tuple(o for o in self.objects.values() if o.correlation_key == key)
