"""ACES Execution Adapter — runtime-neutral boundary.

ACES owns semantic intent and authority evaluation.
The adapter hands authorized requests to a replaceable runtime substrate.
The runtime never grants authority. Execution success never implies AcceptedState.
"""

from .models import (
    AuthorizationRecord,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
    VerificationStatus,
    AcceptedStateStatus,
)
from .runtimes import ExecutionRuntime, LocalSyntheticRuntime
from .adapter import ExecutionAdapter

__all__ = [
    "AuthorizationRecord",
    "ExecutionRequest",
    "ExecutionResult",
    "ExecutionStatus",
    "VerificationStatus",
    "AcceptedStateStatus",
    "ExecutionRuntime",
    "LocalSyntheticRuntime",
    "ExecutionAdapter",
]

__version__ = "0.1.0"
