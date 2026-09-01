"""ACES Security Adapter (ASA) — authorization core + hardening gate.

Normative lineage: ASA-004 authorization core (asa-004-authorization-core).
Hardening: store-backed capability authenticity + explicit handoff to ExecutionAdapter.

GitHub/Grok administrative privilege is never an input to authorization (I8).
"""

from .authorize import authorize
from .types import DecisionOutcome, Decision
from .gate import AuthorityGate, GateDecision
from .handoff import AdapterHandoff, build_adapter_authorization

__all__ = [
    "authorize",
    "DecisionOutcome",
    "Decision",
    "AuthorityGate",
    "GateDecision",
    "AdapterHandoff",
    "build_adapter_authorization",
]

__version__ = "0.2.0-hardening"
