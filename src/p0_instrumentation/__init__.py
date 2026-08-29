"""P0.3.2-I instrumentation: provenance-aware event recording for HCC measurement.

This package records experimental events with mandatory actor provenance.
It does NOT capture real desktop focus, clipboard, or OS switches automatically.
Callers (test drivers, future adapters, or consented local agents) must supply
events with explicit actor attribution.

HCC composite is computed only from primary-analysis-eligible HUMAN events.
Coordinator and system events are retained for provenance separation and
supervision-cost accounting; they never enter the HCC numerator.
"""

from .events import (
    Actor,
    ProvenanceConfidence,
    EventType,
    InstrumentationEvent,
)
from .recorder import EventRecorder
from .hcc import compute_hcc_components, HCCComponents

__all__ = [
    "Actor",
    "ProvenanceConfidence",
    "EventType",
    "InstrumentationEvent",
    "EventRecorder",
    "compute_hcc_components",
    "HCCComponents",
]
