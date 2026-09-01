"""E3.1 Durable Minimal Context Compiler.

Transforms fragmented state from independently owned systems into a
provenance-preserving, uncertainty-preserving, reconstructable ContextPackage.

Invariants enforced:
  Context ≠ Authority
  Capability ≠ Authority
  Inference ≠ Evidence
  Execution success ≠ AcceptedState
"""

from .models import (
    EpistemicStatus,
    SourceContribution,
    ContextItem,
    Conflict,
    Unknown,
    ProvenanceRecord,
    ContextPackage,
    CompilationEvidence,
    CompilationResult,
    CompilationError,
)
from .compiler import ContextCompiler, COMPILER_VERSION

__all__ = [
    "EpistemicStatus",
    "SourceContribution",
    "ContextItem",
    "Conflict",
    "Unknown",
    "ProvenanceRecord",
    "ContextPackage",
    "CompilationEvidence",
    "CompilationResult",
    "CompilationError",
    "ContextCompiler",
    "COMPILER_VERSION",
]
