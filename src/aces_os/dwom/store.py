"""In-memory deterministic DWOM store — no external DB."""

from __future__ import annotations

from typing import Dict, Optional

from .model import DWOMObject, DigitalWorldState


class InMemoryDWOMStore:
    def __init__(self) -> None:
        self._by_id: Dict[str, DWOMObject] = {}
        self._by_observation: Dict[str, str] = {}  # observation_id -> dwom_object_id
        self._digest_by_observation: Dict[str, str] = {}

    def put(self, obj: DWOMObject) -> None:
        self._by_id[obj.dwom_object_id] = obj
        self._by_observation[obj.observation_id] = obj.dwom_object_id
        self._digest_by_observation[obj.observation_id] = obj.payload_digest

    def get(self, dwom_object_id: str) -> Optional[DWOMObject]:
        return self._by_id.get(dwom_object_id)

    def get_by_observation(self, observation_id: str) -> Optional[DWOMObject]:
        did = self._by_observation.get(observation_id)
        return self._by_id.get(did) if did else None

    def observation_digest(self, observation_id: str) -> Optional[str]:
        return self._digest_by_observation.get(observation_id)

    def snapshot(self) -> DigitalWorldState:
        return DigitalWorldState(objects=dict(self._by_id))

    def __len__(self) -> int:
        return len(self._by_id)
