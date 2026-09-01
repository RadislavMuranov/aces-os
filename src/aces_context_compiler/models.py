"""Domain objects for the E3.1 Context Compiler."""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class EpistemicStatus(str, Enum):
    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    PROPOSED = "PROPOSED"
    VERIFIED = "VERIFIED"
    ACCEPTED = "ACCEPTED"
    UNKNOWN = "UNKNOWN"


class CompilationError(ValueError):
    """Fail-closed compilation error (missing provenance, malformed source)."""


def _iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


@dataclass(frozen=True)
class SourceContribution:
    owner_system: str
    source_object_id: str
    retrieval_timestamp: datetime
    source_type: str
    observed_state: str
    access_authority: str
    provenance_reference: str
    epistemic_status: EpistemicStatus = EpistemicStatus.OBSERVED
    source_timestamp: Optional[datetime] = None
    claim_key: Optional[str] = None
    confidence: Optional[float] = None
    permissions: tuple[str, ...] = ()
    uncertainty_reason: Optional[str] = None

    def validate(self) -> None:
        missing = []
        if not self.owner_system:
            missing.append("owner_system")
        if not self.source_object_id:
            missing.append("source_object_id")
        if not self.source_type:
            missing.append("source_type")
        if self.observed_state is None:
            missing.append("observed_state")
        if not self.access_authority:
            missing.append("access_authority")
        if not self.provenance_reference:
            missing.append("provenance_reference")
        if self.retrieval_timestamp is None:
            missing.append("retrieval_timestamp")
        if missing:
            raise CompilationError(
                f"SourceContribution missing mandatory fields: {', '.join(missing)}"
            )


@dataclass(frozen=True)
class ProvenanceRecord:
    owner_system: str
    source_ref: str
    provenance_reference: str
    access_authority: str
    retrieved_at: str
    source_time: Optional[str] = None


@dataclass(frozen=True)
class ContextItem:
    id: str
    owner_system: str
    source_ref: str
    observed_state: str
    retrieved_at: str
    epistemic_status: EpistemicStatus
    provenance: ProvenanceRecord
    source_time: Optional[str] = None
    confidence: Optional[float] = None
    claim_key: Optional[str] = None
    conflicts: tuple[str, ...] = ()
    permissions: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["epistemic_status"] = self.epistemic_status.value
        return d


@dataclass(frozen=True)
class Conflict:
    conflict_id: str
    claim_key: str
    item_ids: tuple[str, ...]
    observations: tuple[str, ...]
    resolved: bool = False
    resolution: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Unknown:
    unknown_id: str
    reason: str
    source_scope: str
    checked_at: str
    claim_key: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ContextPackage:
    task: str
    context_items: tuple[ContextItem, ...]
    provenance: tuple[ProvenanceRecord, ...]
    unknowns: tuple[Unknown, ...]
    conflicts: tuple[Conflict, ...]
    permissions: tuple[str, ...]
    compiled_at: str
    compiler_version: str
    package_id: str
    suggested_next_action: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id,
            "task": self.task,
            "context_items": [i.to_dict() for i in self.context_items],
            "provenance": [asdict(p) for p in self.provenance],
            "unknowns": [u.to_dict() for u in self.unknowns],
            "conflicts": [c.to_dict() for c in self.conflicts],
            "permissions": list(self.permissions),
            "suggested_next_action": self.suggested_next_action,
            "compiled_at": self.compiled_at,
            "compiler_version": self.compiler_version,
        }

    def material_fingerprint(self) -> str:
        import hashlib
        import json

        payload = {
            "task": self.task,
            "context_items": [
                {
                    "id": i.id,
                    "owner_system": i.owner_system,
                    "source_ref": i.source_ref,
                    "observed_state": i.observed_state,
                    "epistemic_status": i.epistemic_status.value,
                    "claim_key": i.claim_key,
                    "permissions": list(i.permissions),
                    "conflicts": list(i.conflicts),
                    "provenance_reference": i.provenance.provenance_reference,
                }
                for i in sorted(self.context_items, key=lambda x: x.id)
            ],
            "unknowns": [
                {"reason": u.reason, "source_scope": u.source_scope, "claim_key": u.claim_key}
                for u in sorted(self.unknowns, key=lambda x: x.unknown_id)
            ],
            "conflicts": [
                {
                    "claim_key": c.claim_key,
                    "item_ids": list(c.item_ids),
                    "observations": list(c.observations),
                    "resolved": c.resolved,
                }
                for c in sorted(self.conflicts, key=lambda x: x.conflict_id)
            ],
            "permissions": sorted(self.permissions),
            "suggested_next_action": self.suggested_next_action,
            "compiler_version": self.compiler_version,
        }
        raw = json.dumps(payload, sort_keys=True, ensure_ascii=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


@dataclass
class CompilationEvidence:
    run_id: str
    task_id: str
    compiler_version: str
    source_systems: list[str] = field(default_factory=list)
    source_objects: list[str] = field(default_factory=list)
    context_item_ids: list[str] = field(default_factory=list)
    unknowns: list[dict[str, Any]] = field(default_factory=list)
    conflicts: list[dict[str, Any]] = field(default_factory=list)
    human_interventions: list[str] = field(default_factory=list)
    agent_actions: list[str] = field(default_factory=list)
    decision_point: Optional[str] = None
    authority_evaluation_reference: Optional[str] = None
    execution_reference: Optional[str] = None
    verification_result: Optional[str] = None
    accepted_state_reference: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    elapsed_ms: Optional[float] = None
    package_id: Optional[str] = None
    material_fingerprint: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CompilationResult:
    package: ContextPackage
    evidence: CompilationEvidence
    intermediate_items: tuple[ContextItem, ...]
