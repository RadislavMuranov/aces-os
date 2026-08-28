"""ACES Security Adapter (ASA) v0 — authorization core (ASA-004).

Normative source: spec/asa/v0/data-model.md (ASA-003.2).
GitHub/Grok administrative privilege is never an input to authorization (I8).
"""

from .authorize import authorize
from .types import DecisionOutcome

__all__ = ["authorize", "DecisionOutcome"]
