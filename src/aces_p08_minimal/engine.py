"""Minimal pipeline engine implementing R6 contract semantics (R8/R10)."""
from __future__ import annotations
from typing import Dict, Any, Optional, List, Tuple
from .models import (
    Evidence, AdmissibilityEvaluation, VerificationRecord,
    AcceptanceDecision, AcceptedDigitalWorldState, AuthorityEntry,
    new_id, now_iso, content_hash
)
from .store import RecordStore

class PipelineEngine:
    def __init__(self, store: RecordStore):
        self.store = store
        self._bootstrap_authorities_and_policy()

    def _bootstrap_authorities_and_policy(self):
        root = AuthorityEntry(
            authority_id="auth_root_architectural",
            role="ROOT",
            scope="*",
            policy_id="pol_root",
            current_status="ACTIVE",
            status_as_of=now_iso(),
            status_history=[{"status": "ACTIVE", "at": now_iso(), "by": "bootstrap"}],
            trust_root_ref="architectural_authority_root",
        )
        self.store.put("authority", root.authority_id, root.to_dict())

        for aid, role, pol in [
            ("auth_verifier_01", "VERIFICATION", "pol_verify_v1"),
            ("auth_acceptor_01", "ACCEPTANCE", "pol_accept_v1"),
            ("auth_admissibility_01", "ADMISSIBILITY", "pol_admiss_v1"),
        ]:
            a = AuthorityEntry(
                authority_id=aid,
                role=role,
                scope="target:*",
                policy_id=pol,
                current_status="ACTIVE",
                status_as_of=now_iso(),
                status_history=[{"status": "ACTIVE", "at": now_iso(), "by": "auth_root_architectural"}],
                trust_root_ref="auth_root_architectural",
            )
            self.store.put("authority", a.authority_id, a.to_dict())

        for pid, ver, body in [
            ("pol_admiss_v1", "1.0.0", {"rule": "require target_ref, source, observed_at, integrity or UNKNOWN"}),
            ("pol_verify_v1", "1.0.0", {"rule": "require admissible evidence; procedure=content_match"}),
            ("pol_accept_v1", "1.0.0", {"rule": "require VERIFIED; acceptance authority distinct"}),
            ("pol_root", "1.0.0", {"rule": "root issuance only"}),
        ]:
            pol = {
                "policy_id": pid,
                "policy_version": ver,
                "body": body,
                "effective_from": "2026-01-01T00:00:00Z",
                "effective_until": None,
                "scope": "*",
            }
            pol["policy_integrity_marker"] = content_hash(pol)
            self.store.put("policy", f"{pid}@{ver}", pol)

    def _get_authority(self, authority_id: str) -> Optional[Dict[str, Any]]:
        return self.store.get(authority_id)

    def _authority_active_at(self, authority_id: str, decision_time: str, required_role: str) -> Tuple[bool, str]:
        auth = self._get_authority(authority_id)
        if not auth:
            return False, "AUTHORITY_NOT_FOUND"
        if auth.get("role") != required_role and auth.get("role") != "ROOT":
            return False, "ROLE_MISMATCH"
        if auth.get("current_status") != "ACTIVE":
            return False, f"STATUS_{auth.get('current_status')}"
        return True, "OK"

    def _get_policy(self, policy_id: str, version: str) -> Optional[Dict[str, Any]]:
        return self.store.get(f"{policy_id}@{version}")

    def capture_evidence(self, target_ref, source_system, connector_instance_id, actor_workload_ref, observation_payload, observed_at=None):
        obs_at = observed_at or now_iso()
        payload_ref = new_id("obs")
        ch = content_hash(observation_payload)
        self.store.put("evidence", f"raw_{payload_ref}", {"payload": observation_payload, "hash": ch})
        ev = Evidence(
            evidence_id=new_id("ev"),
            target_ref=target_ref,
            source_system=source_system,
            connector_instance_id=connector_instance_id,
            actor_workload_ref=actor_workload_ref or "UNKNOWN",
            observation_payload_ref=payload_ref,
            content_hash=ch,
            observed_at=obs_at,
            received_at=now_iso(),
            status="CAPTURED",
            integrity_marker=ch,
        )
        self.store.put("evidence", ev.evidence_id, ev.to_dict())
        return ev

    def evaluate_admissibility(self, evidence_id: str, evaluator_ref: str = "evaluator_01"):
        ev = self.store.get(evidence_id)
        if not ev:
            raise ValueError("EVIDENCE_NOT_FOUND")
        decision_time = now_iso()
        ok, reason = self._authority_active_at("auth_admissibility_01", decision_time, "ADMISSIBILITY")
        pol = self._get_policy("pol_admiss_v1", "1.0.0")
        if not pol:
            raise ValueError("POLICY_NOT_FOUND")
        result = "ADMISSIBLE"
        unknowns = []
        if not ev.get("target_ref"):
            result = "INADMISSIBLE"
        if not ev.get("source_system"):
            result = "INADMISSIBLE"
        if not ev.get("observed_at"):
            result = "INADMISSIBLE"
        if not ev.get("integrity_marker") and not ev.get("content_hash"):
            unknowns.append("integrity_unknown")
            if result == "ADMISSIBLE":
                result = "UNKNOWN"
        if not ok:
            result = "INADMISSIBLE"
            unknowns.append(reason)
        adm = AdmissibilityEvaluation(
            admissibility_id=new_id("adm"),
            evidence_id=evidence_id,
            evaluator_ref=evaluator_ref,
            evaluator_authority_id="auth_admissibility_01",
            policy_id="pol_admiss_v1",
            policy_version="1.0.0",
            policy_integrity_marker=pol["policy_integrity_marker"],
            target_ref=ev.get("target_ref", ""),
            evaluated_at=decision_time,
            result=result,
            residual_unknowns=unknowns,
        )
        data = adm.to_dict()
        self.store.put("admissibility", adm.admissibility_id, data)
        if result == "INADMISSIBLE":
            ev["status"] = "INADMISSIBLE"
        elif result == "UNKNOWN":
            ev["status"] = "UNKNOWN"
        self.store.put("evidence", evidence_id, ev)
        return adm

    def verify(self, evidence_ids, target_ref, verifier_ref="verifier_01", procedure_ref="procedure_content_match_v1"):
        decision_time = now_iso()
        ok, reason = self._authority_active_at("auth_verifier_01", decision_time, "VERIFICATION")
        pol = self._get_policy("pol_verify_v1", "1.0.0")
        if not pol:
            raise ValueError("POLICY_NOT_FOUND")

        def make_nv(residuals):
            rec = VerificationRecord(
                verification_id=new_id("ver"),
                evidence_ids=evidence_ids,
                target_ref=target_ref,
                procedure_ref=procedure_ref,
                verifier_ref=verifier_ref,
                verification_authority_id="auth_verifier_01",
                policy_id="pol_verify_v1",
                policy_version="1.0.0",
                policy_integrity_marker=pol["policy_integrity_marker"],
                scope="target:*",
                verified_at=decision_time,
                result="NOT_VERIFIED",
                residual_unknowns=residuals,
            )
            self.store.put("verification", rec.verification_id, rec.to_dict())
            return rec

        if not evidence_ids:
            return make_nv(["EMPTY_EVIDENCE_IDS"])

        for eid in evidence_ids:
            adm_ids = [i for i in self.store.list_ids("admissibility")
                       if (self.store.get(i) or {}).get("evidence_id") == eid]
            if not adm_ids:
                return make_nv(["MISSING_ADMISSIBILITY_EVALUATION"])
            adm = self.store.get(adm_ids[-1])
            if adm.get("result") != "ADMISSIBLE":
                return make_nv([f"ADMISSIBILITY_{adm.get('result')}"])
            if adm.get("target_ref") != target_ref:
                return make_nv(["TARGET_MISMATCH"])

        if not ok:
            return make_nv([reason])

        result = "VERIFIED"
        unknowns = []
        for eid in evidence_ids:
            ev = self.store.get(eid)
            if not ev or not ev.get("content_hash"):
                result = "UNKNOWN"
                unknowns.append("MISSING_CONTENT_HASH")

        rec = VerificationRecord(
            verification_id=new_id("ver"),
            evidence_ids=evidence_ids,
            target_ref=target_ref,
            procedure_ref=procedure_ref,
            verifier_ref=verifier_ref,
            verification_authority_id="auth_verifier_01",
            policy_id="pol_verify_v1",
            policy_version="1.0.0",
            policy_integrity_marker=pol["policy_integrity_marker"],
            scope="target:*",
            verified_at=decision_time,
            result=result,
            residual_unknowns=unknowns,
        )
        self.store.put("verification", rec.verification_id, rec.to_dict())
        return rec

    def accept(self, verification_ids, target_ref, proposed_state, acceptor_ref="acceptor_01"):
        decision_time = now_iso()
        ok, reason = self._authority_active_at("auth_acceptor_01", decision_time, "ACCEPTANCE")
        pol = self._get_policy("pol_accept_v1", "1.0.0")
        if not pol:
            raise ValueError("POLICY_NOT_FOUND")
        decision = "ACCEPTED"
        reason_code = "OK"
        evidence_ids = []
        if not ok:
            decision = "REJECTED"
            reason_code = reason
        else:
            for vid in verification_ids:
                ver = self.store.get(vid)
                if not ver:
                    decision = "REJECTED"
                    reason_code = "VERIFICATION_NOT_FOUND"
                    break
                if ver.get("result") != "VERIFIED":
                    decision = "REJECTED"
                    reason_code = f"VERIFICATION_{ver.get('result')}"
                    break
                if ver.get("target_ref") != target_ref:
                    decision = "REJECTED"
                    reason_code = "TARGET_MISMATCH"
                    break
                if ver.get("verification_authority_id") == "auth_acceptor_01":
                    decision = "REJECTED"
                    reason_code = "SELF_APPROVAL_FORBIDDEN"
                    break
                evidence_ids.extend(ver.get("evidence_ids") or [])
        acc = AcceptanceDecision(
            acceptance_id=new_id("acc"),
            verification_ids=verification_ids,
            target_ref=target_ref,
            proposed_state=str(proposed_state),
            acceptance_authority_id="auth_acceptor_01",
            policy_id="pol_accept_v1",
            policy_version="1.0.0",
            policy_integrity_marker=pol["policy_integrity_marker"],
            scope="target:*",
            decided_at=decision_time,
            decision=decision,
            reason_code=reason_code,
            evidence_ids=list(set(evidence_ids)),
        )
        self.store.put("acceptance", acc.acceptance_id, acc.to_dict())
        return acc

    def materialize_accepted_state(self, acceptance_id, state_payload):
        acc = self.store.get(acceptance_id)
        if not acc or acc.get("decision") != "ACCEPTED":
            return None
        st = AcceptedDigitalWorldState(
            accepted_state_id=new_id("ads"),
            target_ref=acc["target_ref"],
            state_payload=state_payload,
            acceptance_id=acceptance_id,
            verification_ids=acc.get("verification_ids") or [],
            accepted_at=now_iso(),
            scope=acc.get("scope") or "target:*",
            status="ACTIVE",
            version="1",
            evidence_ids=acc.get("evidence_ids") or [],
        )
        self.store.put("accepted_state", st.accepted_state_id, st.to_dict())
        return st

    def revoke_authority(self, authority_id: str) -> bool:
        auth = self._get_authority(authority_id)
        if not auth:
            return False
        auth["current_status"] = "REVOKED"
        auth["status_as_of"] = now_iso()
        auth["status_history"].append({"status": "REVOKED", "at": auth["status_as_of"], "by": "auth_root_architectural"})
        auth["integrity_marker"] = content_hash({k: v for k, v in auth.items() if k != "integrity_marker"})
        self.store.put("authority", authority_id, auth)
        return True
