"""P0.3.2-III privacy-safe capture adapter for HCC measurement.

Scoped experiment-surface capture with mandatory actor provenance.
Does NOT perform unrestricted keylogging, screen recording, or global
clipboard harvesting. Automatic OS focus/clipboard capture is environment-
dependent and is NOT claimed as validated in headless CI.

Coordinator actions must use the explicit tagged emission channel.
"""

from .schema import (
    Actor,
    ProvenanceConfidence,
    EventType,
    CaptureEvent,
    MissingEvent,
)
from .allowlist import SurfaceAllowList
from .adapter import CaptureAdapter
from .hcc import compute_hcc_from_capture, HCCSnapshot

__all__ = [
    "Actor",
    "ProvenanceConfidence",
    "EventType",
    "CaptureEvent",
    "MissingEvent",
    "SurfaceAllowList",
    "CaptureAdapter",
    "compute_hcc_from_capture",
    "HCCSnapshot",
]
