"""Resource references — never collapse path/name/id into one identity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ResourceScope:
    namespace: str
    account_or_workspace: Optional[str] = None
    configuration_id: Optional[str] = None


@dataclass(frozen=True)
class ResourceRef:
    """Provider-neutral resource reference.

    provider-native ID, path, display name remain distinct fields.
    """

    provider: str
    resource_kind: str
    resource_id: str
    scope: ResourceScope
    parent_ref: Optional[str] = None
    revision: Optional[str] = None
    path: Optional[str] = None
    display_name: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.provider or not self.resource_kind or not self.resource_id:
            raise ValueError("provider, resource_kind, resource_id required")
