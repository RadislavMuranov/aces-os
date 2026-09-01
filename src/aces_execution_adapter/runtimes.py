"""Replaceable execution substrates. None of these grant ACES authority."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple

from .models import ExecutionRequest


class ExecutionRuntime(ABC):
    """Runtime-neutral interface. Implementations are substrates only."""

    runtime_id: str

    @abstractmethod
    def execute(self, request: ExecutionRequest) -> Tuple[bool, Dict[str, Any], str | None]:
        """Return (ok, observed, error). Never sets AcceptedState."""


class LocalSyntheticRuntime(ExecutionRuntime):
    """Local, side-effect-free synthetic substrate for boundary tests.

    Not DSH. Not production. Replaceable. No external mutations.
    """

    runtime_id = "local-synthetic-v1"

    def execute(self, request: ExecutionRequest) -> Tuple[bool, Dict[str, Any], str | None]:
        if request.payload.get("force_runtime_failure"):
            return False, {}, "forced_runtime_failure"
        observed = {
            "echo_operation": request.operation,
            "echo_resource": request.resource,
            "echo_scope": request.scope,
            "echo_task_id": request.task_id,
            "echo_intent": request.intent_reference,
            "payload_keys": sorted(request.payload.keys()),
            "substrate": self.runtime_id,
        }
        return True, observed, None


class NullRuntime(ExecutionRuntime):
    """Always fails — used to prove replaceability / failure path."""

    runtime_id = "null-runtime-v1"

    def execute(self, request: ExecutionRequest) -> Tuple[bool, Dict[str, Any], str | None]:
        return False, {}, "null_runtime_always_fails"
