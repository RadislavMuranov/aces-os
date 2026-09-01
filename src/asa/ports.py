"""Store ports for ASA-004 orchestration.

Implementations are injected by the host. Unavailable stores MUST cause DENY
for protected operations (fail-closed). Ports do not consult GitHub privileges.
"""

from __future__ import annotations

from typing import Optional, Protocol

from .types import AuthorizationEvent, Capability, Policy, RevocationRecord


class CapabilityStore(Protocol):
    def get(self, capability_id: str) -> Optional[Capability]:
        """Return capability record or None if unknown."""


class PolicyStore(Protocol):
    def get(self, policy_id: str, version: str) -> Optional[Policy]:
        """Return policy or None if missing."""


class RevocationStore(Protocol):
    def get_revocation(self, capability_id: str) -> Optional[RevocationRecord]:
        """Return revocation record if capability is revoked; None if not revoked."""

    def is_available(self) -> bool:
        """False → DENY for protected ops (revocation store unavailable)."""


class AuthorityRegistry(Protocol):
    def is_known(self, authority_id: str) -> bool:
        """Whether authority_id is known to ASA (not a GitHub role)."""


class AuditSink(Protocol):
    def append(self, event: AuthorizationEvent) -> bool:
        """Append AuthorizationEvent. Return False if audit unavailable."""
