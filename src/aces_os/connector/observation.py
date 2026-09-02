"""Observation model — Observation ≠ Evidence ≠ AcceptedState."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional

from .resource import ResourceRef


class ObservationState(str, Enum):
    KNOWN = "KNOWN"
    UNKNOWN = "UNKNOWN"
    PARTIAL = "PARTIAL"
    NOT_OBSERVABLE = "NOT_OBSERVABLE"
    ABSENT = "ABSENT"


class PartialState(str, Enum):
    COMPLETE = "COMPLETE"
    PARTIAL = "PARTIAL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class Provenance:
    """Structural provenance. AUTHENTICITY CRYPTOGRAPHY DEFERRED."""

    provider: str
    connector_id: str
    resource_ref_id: str
    observed_at: str
    request_id: str
    configuration_scope: str
    authenticity_crypto: str = "DEFERRED"


@dataclass(frozen=True)
class Observation:
    """Provider-neutral observation.

    MUST NOT create Evidence or AcceptedState.
    """

    observation_id: str
    provider: str
    resource_ref: ResourceRef
    observed_at: str
    observed_state: ObservationState
    partial_state: PartialState
    provenance: Provenance
    request_id: str
    payload_digest: str
    source_timestamp: Optional[str] = None
    provider_event_time: Optional[str] = None
    observed_payload: Dict[str, Any] = field(default_factory=dict)
    pvr_flags: tuple = ()

    def is_evidence(self) -> bool:
        """Observation is never Evidence."""
        return False

    def is_accepted_state(self) -> bool:
        """Observation is never AcceptedState."""
        return False
