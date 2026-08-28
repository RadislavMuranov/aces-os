"""In-memory port fakes for ASA-008. Not production stores."""
from __future__ import annotations
from typing import Dict, Optional, Tuple
from asa.types import AuthorizationEvent, Capability, Policy, RevocationRecord


class InMemoryCapabilityStore:
    def __init__(self, items: Optional[Dict[str, Capability]] = None, raise_on_get: bool = False):
        self._items = dict(items or {})
        self.raise_on_get = raise_on_get
        self.get_calls = 0

    def get(self, capability_id: str) -> Optional[Capability]:
        self.get_calls += 1
        if self.raise_on_get:
            raise RuntimeError("capability store failure")
        return self._items.get(capability_id)


class InMemoryPolicyStore:
    def __init__(self, items: Optional[Dict[Tuple[str, str], Policy]] = None, raise_on_get: bool = False):
        self._items = dict(items or {})
        self.raise_on_get = raise_on_get

    def get(self, policy_id: str, version: str) -> Optional[Policy]:
        if self.raise_on_get:
            raise RuntimeError("policy store failure")
        return self._items.get((policy_id, version))


class InMemoryRevocationStore:
    def __init__(
        self,
        revocations: Optional[Dict[str, RevocationRecord]] = None,
        available: bool = True,
        raise_on_get: bool = False,
    ):
        self._rev = dict(revocations or {})
        self._available = available
        self.raise_on_get = raise_on_get
        self.get_calls = 0

    def is_available(self) -> bool:
        return self._available

    def get_revocation(self, capability_id: str) -> Optional[RevocationRecord]:
        self.get_calls += 1
        if self.raise_on_get:
            raise RuntimeError("revocation lookup failure")
        return self._rev.get(capability_id)


class InMemoryAuthorityRegistry:
    def __init__(self, known: Optional[set] = None):
        self._known = set(known or set())

    def is_known(self, authority_id: str) -> bool:
        return authority_id in self._known


class InMemoryAuditSink:
    def __init__(self, succeed: bool = True):
        self.succeed = succeed
        self.events = []

    def append(self, event: AuthorizationEvent) -> bool:
        if not self.succeed:
            return False
        self.events.append(event)
        return True
