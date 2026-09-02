"""Phase III — Digital World Model ingestion.

Digital World State ≠ Evidence ≠ AcceptedState ≠ Knowledge ≠ Semantic Reality.
"""

from .model import (
    DWOMObject,
    DigitalWorldState,
    ExistenceState,
    DeletionState,
    DWOMStatus,
)
from .ingest import DWOMIngestor, IngestError, IngestConflictError
from .store import InMemoryDWOMStore

__all__ = [
    "DWOMObject",
    "DigitalWorldState",
    "ExistenceState",
    "DeletionState",
    "DWOMStatus",
    "DWOMIngestor",
    "IngestError",
    "IngestConflictError",
    "InMemoryDWOMStore",
]
