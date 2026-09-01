"""E3.1 Durable Minimal Context Compiler pipeline."""

from __future__ import annotations

import hashlib
import time
from collections import defaultdict
from datetime import datetime, timezone
from typing import Optional, Sequence
from uuid import uuid4

from .models import (
    CompilationError,
    CompilationEvidence,
    CompilationResult,
    Conflict,
    ContextItem,
    ContextPackage,
    EpistemicStatus,
    ProvenanceRecord,
    SourceContribution,
    Unknown,
    _iso,
)

COMPILER_VERSION = "E3.1-1.0"


def _stable_item_id(owner_system: str, source_object_id: str, claim_key: Optional[str]) -> str:
    key = f"{owner_system}|{source_object_id}|{claim_key or ''}"
    return "ci-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def _stable_unknown_id(reason: str, source_scope: str, claim_key: Optional[str]) -> str:
    key = f"{reason}|{source_scope}|{claim_key or ''}"
    return "unk-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


def _stable_conflict_id(claim_key: str, item_ids: Sequence[str]) -> str:
    key = claim_key + "|" + "|".join(sorted(item_ids))
    return "cnf-" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:12]


class ContextCompiler:
    """Pure, deterministic Context Compiler.

    Does not grant authority, invent state, resolve conflicts, or convert
    inference into observation.
    """

    def __init__(self, version: str = COMPILER_VERSION) -> None:
        self.version = version

    def compile(
        self,
        task: str,
        sources: Sequence[SourceContribution],
        *,
        task_id: Optional[str] = None,
        unknowns: Optional[Sequence[Unknown]] = None,
        suggested_next_action: Optional[str] = None,
        human_interventions: Optional[Sequence[str]] = None,
        agent_actions: Optional[Sequence[str]] = None,
        decision_point: Optional[str] = None,
        authority_evaluation_reference: Optional[str] = None,
        compiled_at: Optional[datetime] = None,
        package_id: Optional[str] = None,
        run_id: Optional[str] = None,
    ) -> CompilationResult:
        started = time.perf_counter()
        started_at = datetime.now(timezone.utc)
        run_id = run_id or str(uuid4())
        task_id = task_id or task

        evidence = CompilationEvidence(
            run_id=run_id,
            task_id=task_id,
            compiler_version=self.version,
            human_interventions=list(human_interventions or []),
            agent_actions=list(agent_actions or []),
            decision_point=decision_point,
            authority_evaluation_reference=authority_evaluation_reference,
            started_at=_iso(started_at),
        )

        try:
            if not task or not str(task).strip():
                raise CompilationError("task/intent is required")

            for src in sources:
                src.validate()

            items = tuple(self._normalize(src) for src in sources)

            unknown_list = list(unknowns or [])
            for item in items:
                if item.epistemic_status is EpistemicStatus.UNKNOWN:
                    unknown_list.append(
                        Unknown(
                            unknown_id=_stable_unknown_id(
                                item.observed_state, item.owner_system, item.claim_key
                            ),
                            reason=item.observed_state,
                            source_scope=item.owner_system,
                            checked_at=item.retrieved_at,
                            claim_key=item.claim_key,
                        )
                    )
            seen_u: set[str] = set()
            deduped_unknowns: list[Unknown] = []
            for u in unknown_list:
                if u.unknown_id not in seen_u:
                    seen_u.add(u.unknown_id)
                    deduped_unknowns.append(u)
            unknowns_t = tuple(sorted(deduped_unknowns, key=lambda x: x.unknown_id))

            conflicts = self._expose_conflicts(items)
            conflict_item_ids: dict[str, list[str]] = defaultdict(list)
            for c in conflicts:
                for iid in c.item_ids:
                    conflict_item_ids[iid].append(c.conflict_id)

            annotated_items = tuple(
                ContextItem(
                    id=i.id,
                    owner_system=i.owner_system,
                    source_ref=i.source_ref,
                    observed_state=i.observed_state,
                    retrieved_at=i.retrieved_at,
                    epistemic_status=i.epistemic_status,
                    provenance=i.provenance,
                    source_time=i.source_time,
                    confidence=i.confidence,
                    claim_key=i.claim_key,
                    conflicts=tuple(conflict_item_ids.get(i.id, ())),
                    permissions=i.permissions,
                )
                for i in items
            )
            annotated_items = tuple(sorted(annotated_items, key=lambda x: x.id))

            perms: set[str] = set()
            for i in annotated_items:
                perms.update(i.permissions)
            permissions = tuple(sorted(perms))

            provenance = tuple(i.provenance for i in annotated_items)
            compiled_ts = compiled_at or datetime.now(timezone.utc)
            pkg_id = package_id or str(uuid4())

            package = ContextPackage(
                task=task,
                context_items=annotated_items,
                provenance=provenance,
                unknowns=unknowns_t,
                conflicts=conflicts,
                permissions=permissions,
                compiled_at=_iso(compiled_ts) or "",
                compiler_version=self.version,
                package_id=pkg_id,
                suggested_next_action=suggested_next_action,
            )

            elapsed_ms = (time.perf_counter() - started) * 1000.0
            evidence.source_systems = sorted({i.owner_system for i in annotated_items})
            evidence.source_objects = sorted({i.source_ref for i in annotated_items})
            evidence.context_item_ids = [i.id for i in annotated_items]
            evidence.unknowns = [u.to_dict() for u in unknowns_t]
            evidence.conflicts = [c.to_dict() for c in conflicts]
            evidence.package_id = package.package_id
            evidence.material_fingerprint = package.material_fingerprint()
            evidence.completed_at = _iso(datetime.now(timezone.utc))
            evidence.elapsed_ms = elapsed_ms
            evidence.verification_result = None
            evidence.accepted_state_reference = None
            evidence.execution_reference = None

            return CompilationResult(
                package=package,
                evidence=evidence,
                intermediate_items=annotated_items,
            )
        except CompilationError as e:
            evidence.error = str(e)
            evidence.completed_at = _iso(datetime.now(timezone.utc))
            evidence.elapsed_ms = (time.perf_counter() - started) * 1000.0
            raise

    def _normalize(self, src: SourceContribution) -> ContextItem:
        status = src.epistemic_status
        item_id = _stable_item_id(src.owner_system, src.source_object_id, src.claim_key)
        prov = ProvenanceRecord(
            owner_system=src.owner_system,
            source_ref=src.source_object_id,
            provenance_reference=src.provenance_reference,
            access_authority=src.access_authority,
            retrieved_at=_iso(src.retrieval_timestamp) or "",
            source_time=_iso(src.source_timestamp),
        )
        return ContextItem(
            id=item_id,
            owner_system=src.owner_system,
            source_ref=src.source_object_id,
            observed_state=src.observed_state,
            retrieved_at=_iso(src.retrieval_timestamp) or "",
            epistemic_status=status,
            provenance=prov,
            source_time=_iso(src.source_timestamp),
            confidence=src.confidence,
            claim_key=src.claim_key,
            conflicts=(),
            permissions=tuple(src.permissions),
        )

    def _expose_conflicts(self, items: Sequence[ContextItem]) -> tuple[Conflict, ...]:
        by_key: dict[str, list[ContextItem]] = defaultdict(list)
        for item in items:
            if item.claim_key and item.epistemic_status is not EpistemicStatus.UNKNOWN:
                by_key[item.claim_key].append(item)

        conflicts: list[Conflict] = []
        for claim_key, group in sorted(by_key.items()):
            states = {g.observed_state for g in group}
            if len(states) > 1:
                item_ids = tuple(sorted(g.id for g in group))
                observations = tuple(sorted({g.observed_state for g in group}))
                conflicts.append(
                    Conflict(
                        conflict_id=_stable_conflict_id(claim_key, item_ids),
                        claim_key=claim_key,
                        item_ids=item_ids,
                        observations=observations,
                        resolved=False,
                        resolution=None,
                    )
                )
        return tuple(sorted(conflicts, key=lambda c: c.conflict_id))
