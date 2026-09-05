"""Minimal semantic objects for R6 contract."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import hashlib
import json
import uuid

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"

def content_hash(payload: Any) -> str:
    raw = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

@dataclass
class Evidence:
    evidence_id: str
    target_ref: str
    source_system: str
    connector_instance_id: str
    actor_workload_ref: str
    observation_payload_ref: str
    content_hash: str
    observed_at: str
    status: str
    integrity_marker: str
    received_at: Optional[str] = None
    provenance_parent_ids: List[str] = field(default_factory=list)
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AdmissibilityEvaluation:
    admissibility_id: str
    evidence_id: str
    evaluator_ref: str
    evaluator_authority_id: str
    policy_id: str
    policy_version: str
    policy_integrity_marker: str
    target_ref: str
    evaluated_at: str
    result: str
    residual_unknowns: List[str] = field(default_factory=list)
    integrity_marker: str = ""
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if not d["integrity_marker"]:
            d["integrity_marker"] = content_hash({k: v for k, v in d.items() if k != "integrity_marker"})
        return d

@dataclass
class VerificationRecord:
    verification_id: str
    evidence_ids: List[str]
    target_ref: str
    procedure_ref: str
    verifier_ref: str
    verification_authority_id: str
    policy_id: str
    policy_version: str
    policy_integrity_marker: str
    scope: str
    verified_at: str
    result: str
    residual_unknowns: List[str] = field(default_factory=list)
    integrity_marker: str = ""
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if not d["integrity_marker"]:
            d["integrity_marker"] = content_hash({k: v for k, v in d.items() if k != "integrity_marker"})
        return d

@dataclass
class AcceptanceDecision:
    acceptance_id: str
    verification_ids: List[str]
    target_ref: str
    proposed_state: str
    acceptance_authority_id: str
    policy_id: str
    policy_version: str
    policy_integrity_marker: str
    scope: str
    decided_at: str
    decision: str
    reason_code: str
    evidence_ids: List[str] = field(default_factory=list)
    integrity_marker: str = ""
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if not d["integrity_marker"]:
            d["integrity_marker"] = content_hash({k: v for k, v in d.items() if k != "integrity_marker"})
        return d

@dataclass
class AcceptedDigitalWorldState:
    accepted_state_id: str
    target_ref: str
    state_payload: Dict[str, Any]
    acceptance_id: str
    verification_ids: List[str]
    accepted_at: str
    scope: str
    status: str
    version: str = "1"
    supersedes: Optional[str] = None
    evidence_ids: List[str] = field(default_factory=list)
    integrity_marker: str = ""
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if not d["integrity_marker"]:
            d["integrity_marker"] = content_hash({k: v for k, v in d.items() if k != "integrity_marker"})
        return d

@dataclass
class AuthorityEntry:
    authority_id: str
    role: str
    scope: str
    policy_id: str
    current_status: str
    status_as_of: str
    status_history: List[Dict[str, str]] = field(default_factory=list)
    trust_root_ref: str = "architectural_authority_root"
    integrity_marker: str = ""
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if not d["integrity_marker"]:
            d["integrity_marker"] = content_hash({k: v for k, v in d.items() if k != "integrity_marker"})
        return d
