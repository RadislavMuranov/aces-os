"""Replay binding: request_id + payload_digest."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict


class ReplayConflictError(ValueError):
    """same request_id + different payload_digest → REJECT/CONFLICT."""


@dataclass(frozen=True)
class ReplayBinding:
    request_id: str
    payload_digest: str

    @staticmethod
    def digest_payload(payload: Dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @classmethod
    def from_payload(cls, request_id: str, payload: Dict[str, Any]) -> "ReplayBinding":
        if not request_id:
            raise ValueError("request_id required")
        return cls(request_id=request_id, payload_digest=cls.digest_payload(payload))


class ReplayRegistry:
    """In-memory binding registry for conflict detection (fixture/tests)."""

    def __init__(self) -> None:
        self._bindings: Dict[str, str] = {}

    def register(self, binding: ReplayBinding) -> None:
        existing = self._bindings.get(binding.request_id)
        if existing is not None and existing != binding.payload_digest:
            raise ReplayConflictError(
                f"request_id={binding.request_id} payload_digest mismatch"
            )
        self._bindings[binding.request_id] = binding.payload_digest

    def get(self, request_id: str) -> str | None:
        return self._bindings.get(request_id)
