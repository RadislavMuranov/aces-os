"""Typed transition contract and deterministic fail-closed structural validator.

This module implements only the bounded P4/P6-authorized structural boundary.
It intentionally does not infer truth, authorization validity, verification success,
replay semantics, or production effectiveness.
"""

from dataclasses import dataclass, fields
from typing import Tuple


@dataclass(frozen=True)
class TransitionContract:
    """The six required fields of a transition candidate."""

    PredecessorState: str
    CandidateAction: str
    ExpectedResultingState: str
    Evidence: str
    VerificationRequirement: str
    AuthorizationRequirement: str


@dataclass(frozen=True)
class ValidationResult:
    """Deterministic validation outcome."""

    accepted: bool
    errors: Tuple[str, ...]


_REQUIRED_FIELDS = tuple(field.name for field in fields(TransitionContract))


def validate_transition_contract(value: object) -> ValidationResult:
    """Validate contract structure and fail closed on any invalid field.

    No coercion, defaulting, inference, or semantic truth assessment is performed.
    """

    if not isinstance(value, TransitionContract):
        return ValidationResult(
            accepted=False,
            errors=("contract must be a TransitionContract",),
        )

    errors = []
    for field_name in _REQUIRED_FIELDS:
        field_value = getattr(value, field_name)
        if not isinstance(field_value, str):
            errors.append(f"{field_name}: expected string")
        elif not field_value.strip():
            errors.append(f"{field_name}: must be non-empty")

    return ValidationResult(
        accepted=not errors,
        errors=tuple(errors),
    )
