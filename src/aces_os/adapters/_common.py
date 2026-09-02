"""Shared helpers for fixture-backed adapters."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

from aces_os.connector.identity import ConnectorIdentity
from aces_os.connector.observation import (
    Observation,
    ObservationState,
    PartialState,
    Provenance,
)
from aces_os.connector.replay import ReplayBinding
from aces_os.connector.resource import ResourceRef, ResourceScope


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_observation(
    *,
    identity: ConnectorIdentity,
    ref: ResourceRef,
    request_id: str,
    payload: Dict[str, Any],
    observed_state: ObservationState = ObservationState.KNOWN,
    partial_state: PartialState = PartialState.COMPLETE,
    source_timestamp: Optional[str] = None,
    pvr_flags: Tuple[str, ...] = (),
) -> Observation:
    binding = ReplayBinding.from_payload(request_id, payload)
    prov = Provenance(
        provider=identity.provider,
        connector_id=identity.connector_id,
        resource_ref_id=ref.resource_id,
        observed_at=utc_now(),
        request_id=request_id,
        configuration_scope=identity.configuration_scope,
        authenticity_crypto="DEFERRED",
    )
    return Observation(
        observation_id=f"obs:{identity.provider}:{ref.resource_id}:{binding.payload_digest[:12]}",
        provider=identity.provider,
        resource_ref=ref,
        observed_at=prov.observed_at,
        observed_state=observed_state,
        partial_state=partial_state,
        provenance=prov,
        request_id=request_id,
        payload_digest=binding.payload_digest,
        source_timestamp=source_timestamp,
        observed_payload=dict(payload),
        pvr_flags=pvr_flags,
    )


def default_scope(namespace: str = "fixture") -> ResourceScope:
    return ResourceScope(namespace=namespace, account_or_workspace="fixture", configuration_id="local-fixture")
