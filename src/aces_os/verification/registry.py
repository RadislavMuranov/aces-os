"""Trusted verifier registry — not caller-controlled."""

from __future__ import annotations

from typing import Dict, Optional, Tuple

from .model import VerificationPolicy, VerifierDescriptor


class RegistryError(ValueError):
    pass


class TrustedVerifierRegistry:
    """Authoritative trust + policy registry.

    Callers cannot mark trusted=True on a request.
    Registration is only via controlled bootstrap, not verification path.
    """

    def __init__(self) -> None:
        self._verifiers: Dict[str, VerifierDescriptor] = {}
        self._policies: Dict[Tuple[str, str], VerificationPolicy] = {}
        self._locked = False

    def register_policy(self, policy: VerificationPolicy) -> None:
        if self._locked:
            raise RegistryError("registry locked; cannot register policy during verification")
        self._policies[(policy.policy_id, policy.policy_version)] = policy

    def register_verifier(self, descriptor: VerifierDescriptor) -> None:
        if self._locked:
            raise RegistryError("registry locked; cannot register verifier during verification")
        if descriptor.trust_status not in ("TRUSTED", "UNTRUSTED"):
            raise RegistryError("invalid trust_status")
        key = f"{descriptor.verifier_id}@{descriptor.verifier_version}"
        self._verifiers[key] = descriptor

    def lock(self) -> None:
        """Prevent further registration after bootstrap."""
        self._locked = True

    def get_policy(self, policy_id: str, policy_version: str) -> VerificationPolicy:
        p = self._policies.get((policy_id, policy_version))
        if p is None:
            raise RegistryError(f"unknown policy {policy_id}@{policy_version}")
        if not p.active:
            raise RegistryError(f"inactive policy {policy_id}@{policy_version}")
        return p

    def get_trusted_verifier(
        self, verifier_id: str, verifier_version: str, policy_id: str
    ) -> VerifierDescriptor:
        key = f"{verifier_id}@{verifier_version}"
        d = self._verifiers.get(key)
        if d is None:
            raise RegistryError(f"unknown verifier {key}")
        if d.trust_status != "TRUSTED":
            raise RegistryError(f"untrusted verifier {key}")
        if policy_id not in d.policy_scope:
            raise RegistryError(f"verifier {key} not trusted for policy {policy_id}")
        return d
