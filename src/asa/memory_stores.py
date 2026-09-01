"""In-memory ASA stores for local/synthetic testing. Not production IAM."""

from __future__ import annotations

from typing import Dict, Optional, Tuple

from .types import AuthorizationEvent, Capability, Policy, RevocationRecord


class InMemoryCapabilityStore:
    def __init__(self) -> None:
        self._caps: Dict[str, Capability] = {}

    def put(self, capability: Capability) -> None:
        self._caps[capability.capability_id] = capability

    def get(self, capability_id: str) -> Optional[Capability]:
        return self._caps.get(capability_id)


class InMemoryPolicyStore:
    def __init__(self) -> None:
        self._policies: Dict[Tuple[str, str], Policy] = {}

    def put(self, policy: Policy) -> None:
        self._policies[(policy.policy_id, policy.version)] = policy

    def get(self, policy_id: str, version: str) -> Optional[Policy]:
        return self._policies.get((policy_id, version))


class InMemoryRevocationStore:
    def __init__(self, available: bool = True) -> None:
        self._revoked: Dict[str, RevocationRecord] = {}
        self._available = available

    def set_available(self, available: bool) -> None:
        self._available = available

    def revoke(self, record: RevocationRecord) -> None:
        self._revoked[record.capability_id] = record

    def get_revocation(self, capability_id: str) -> Optional[RevocationRecord]:
        return self._revoked.get(capability_id)

    def is_available(self) -> bool:
        return self._available


class InMemoryAuthorityRegistry:
    def __init__(self, known: Optional[set[str]] = None) -> None:
        self._known = set(known or ())

    def register(self, authority_id: str) -> None:
        self._known.add(authority_id)

    def is_known(self, authority_id: str) -> bool:
        return authority_id in self._known


class InMemoryAuditSink:
    def __init__(self, available: bool = True) -> None:
        self.events: list[AuthorizationEvent] = []
        self._available = available

    def set_available(self, available: bool) -> None:
        self._available = available

    def append(self, event: AuthorizationEvent) -> bool:
        if not self._available:
            return False
        self.events.append(event)
        return True
