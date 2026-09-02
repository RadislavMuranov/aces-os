"""Read-only connector base — no write surface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable, Sequence

from .capability import Capability, FORBIDDEN_CAPABILITIES, READ_ONLY_CAPABILITIES
from .identity import ConnectorIdentity
from .observation import Observation
from .resource import ResourceRef


class ConnectorError(Exception):
    pass


class WriteNotAuthorizedError(ConnectorError):
    """Phase I/II forbids all write operations."""


class ReadOnlyConnector(ABC):
    """Provider-neutral read-only connector.

    Connector ≠ Authority. Runtime ≠ Authority.
    """

    def __init__(self, identity: ConnectorIdentity) -> None:
        self._identity = identity
        self._assert_no_forbidden_capabilities()

    @property
    def identity(self) -> ConnectorIdentity:
        return self._identity

    @abstractmethod
    def supported_capabilities(self) -> Sequence[Capability]:
        ...

    def _assert_no_forbidden_capabilities(self) -> None:
        for cap in self.supported_capabilities():
            name = cap.value if isinstance(cap, Capability) else str(cap)
            if name in FORBIDDEN_CAPABILITIES:
                raise WriteNotAuthorizedError(f"forbidden capability: {name}")
            if name not in READ_ONLY_CAPABILITIES:
                raise WriteNotAuthorizedError(f"non-read-only capability: {name}")

    def write(self, *args, **kwargs) -> None:
        raise WriteNotAuthorizedError("WRITE not authorized in Phase I/II")

    def create(self, *args, **kwargs) -> None:
        raise WriteNotAuthorizedError("CREATE not authorized in Phase I/II")

    def update(self, *args, **kwargs) -> None:
        raise WriteNotAuthorizedError("UPDATE not authorized in Phase I/II")

    def delete(self, *args, **kwargs) -> None:
        raise WriteNotAuthorizedError("DELETE not authorized in Phase I/II")

    def execute(self, *args, **kwargs) -> None:
        raise WriteNotAuthorizedError("EXECUTE not authorized in Phase I/II")

    def authorize(self, *args, **kwargs) -> None:
        raise WriteNotAuthorizedError("AUTHORIZE not authorized — Connector ≠ Authority")

    def mint_evidence(self, *args, **kwargs) -> None:
        raise WriteNotAuthorizedError("Observation ≠ Evidence")

    def mint_accepted_state(self, *args, **kwargs) -> None:
        raise WriteNotAuthorizedError("Observation ≠ AcceptedState")

    @abstractmethod
    def read_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        ...

    @abstractmethod
    def list_resources(self, kind: str, request_id: str) -> Iterable[Observation]:
        ...

    @abstractmethod
    def observe_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        ...
