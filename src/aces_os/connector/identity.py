"""Connector identity — NOT authority."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ConnectorIdentity:
    """Deterministic connector identity.

    Connector Identity ≠ ACES Authority.
    """

    connector_id: str
    provider: str
    connector_version: str
    configuration_scope: str

    def __post_init__(self) -> None:
        if not self.connector_id:
            raise ValueError("connector_id required")
        if not self.provider:
            raise ValueError("provider required")
        if not self.connector_version:
            raise ValueError("connector_version required")
