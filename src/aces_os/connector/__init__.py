"""Provider-neutral Connector Fabric (Phase I)."""

from .identity import ConnectorIdentity
from .capability import Capability, READ_ONLY_CAPABILITIES
from .resource import ResourceRef, ResourceScope
from .observation import (
    Observation,
    ObservationState,
    PartialState,
    Provenance,
)
from .replay import ReplayBinding, ReplayConflictError
from .base import ReadOnlyConnector, ConnectorError

__all__ = [
    "ConnectorIdentity",
    "Capability",
    "READ_ONLY_CAPABILITIES",
    "ResourceRef",
    "ResourceScope",
    "Observation",
    "ObservationState",
    "PartialState",
    "Provenance",
    "ReplayBinding",
    "ReplayConflictError",
    "ReadOnlyConnector",
    "ConnectorError",
]
