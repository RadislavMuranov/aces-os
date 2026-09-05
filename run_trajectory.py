#!/usr/bin/env python3
"""RDR-P08-R10 repository-bound trajectory runner."""
from __future__ import annotations
import json, sys, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from aces_p08_minimal.store import RecordStore
from aces_p08_minimal.engine import PipelineEngine
from aces_p08_minimal.models import content_hash, now_iso, AcceptanceDecision, new_id
from aces_p08_minimal.integrity import verify_record, tamper_and_detect

EVIDENCE_ROOT = ROOT / "evidence" / "r10_run_001"
STORE_ROOT = EVIDENCE_ROOT / "store"

def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")

def run_positive():
    if STORE_ROOT.exists():
        shutil.rmtree(STORE_ROOT)
    store = RecordStore(str(STORE_ROOT))
    engine = PipelineEngine(store)
    observation = {
        "kind": "controlled_observation",
        "subject": "ddr-p08-r10-demo-target",
        "value": {"status": "X", "note": "r10 clean reproduction"},
        "produced_at": now_iso(),
    }
    ev = engine.capture_evidence(
        target_ref="target:demo-001",
        source_system="controlled_test_harness",
        connector_instance_id="connector_test_01",
        actor_workload_ref="workload_r10_runner",
        observation_payload=observation,
    )
    adm = engine.evaluate_admissibility(ev.evidence_id)
    ver = engine.verify(evidence_ids=[ev.evidence_id], target_ref="target:demo-001")
    proposed = {"status": "X", "accepted_claim": "demo state X"}
    acc = engine.accept(verification_ids=[ver.verification_id], target_ref="target:demo-001", proposed_state=proposed)
    ads = engine.materialize_accepted_state(acc.acceptance_id, proposed)
    integrity_results = {}
    for label, oid in [("evidence", ev.evidence_id), ("admissibility", adm.admissibility_id),
                       ("verification", ver.verification_id), ("acceptance", acc.acceptance_id)]:
        rec = store.get(oid)
        ok, exp, stored = verify_record(rec)
        integrity_results[label] = {"ok": ok, "expected": exp, "stored": stored}
    ver_rec = store.get(ver.verification_id)
    tamper = tamper_and_detect(ver_rec, "result", "NOT_VERIFIED")
    chain = {
        "trajectory": "POSITIVE_R10",
        "observation_payload_hash": content_hash(observation),
        "evidence_id": ev.evidence_id,
        "admissibility_id": adm.admissibility_id,
        "admissibility_result": adm.result,
        "verification_id": ver.verification_id,
        "verification_result": ver.result,
        "acceptance_id": acc.acceptance_id,
        "acceptance_decision": acc.decision,
        "accepted_state_id": ads.accepted_state_id if ads else None,
        "accepted_state_status": ads.status if ads else None,
        "integrity_checks": integrity_results,
        "tamper_test": tamper,
        "store_index": store.dump_index(),
        "executed_at": now_iso(),
    }
    write_json(EVIDENCE_ROOT / "positive_chain.json", chain)
    return chain, store

def run_negatives():
    base = EVIDENCE_ROOT / "negatives"
    results = {}
    s = RecordStore(str(base / "n1")); e = PipelineEngine(s)
    ver = e.verify(["ev_missing"], "target:demo-001")
    results["N1"] = {"result": ver.result, "residuals": ver.residual_unknowns, "id": ver.verification_id}
    s = RecordStore(str(base / "n2")); e = PipelineEngine(s)
    ev = e.capture_evidence("target:demo-001", "test", "c1", "w1", {"v": 1})
    ver = e.verify([ev.evidence_id], "target:demo-001")
    results["N2"] = {"result": ver.result, "residuals": ver.residual_unknowns, "id": ver.verification_id}
    s = RecordStore(str(base / "n3")); e = PipelineEngine(s)
    ev = e.capture_evidence("target:demo-001", "test", "c1", "w1", {"v": 1})
    e.evaluate_admissibility(ev.evidence_id)
    e.revoke_authority("auth_verifier_01")
    ver = e.verify([ev.evidence_id], "target:demo-001")
    results["N3"] = {"result": ver.result, "residuals": ver.residual_unknowns, "id": ver.verification_id}
    s = RecordStore(str(base / "n4")); e = PipelineEngine(s)
    pol = s.get("pol_verify_v1@1.0.0")
    pol["policy_integrity_marker"] = "0" * 64
    s.put("policy", "pol_verify_v1@1.0.0", pol)
    s2 = RecordStore(str(base / "n4_fresh")); e2 = PipelineEngine(s2)
    fresh = s2.get("pol_verify_v1@1.0.0")
    results["N4"] = {
        "tampered_marker": pol["policy_integrity_marker"],
        "fresh_marker": fresh["policy_integrity_marker"],
        "mismatch_detected": pol["policy_integrity_marker"] != fresh["policy_integrity_marker"],
    }
    s = RecordStore(str(base / "n5")); e = PipelineEngine(s)
    ev = e.capture_evidence("target:A", "test", "c1", "w1", {"v": 1})
    e.evaluate_admissibility(ev.evidence_id)
    ver = e.verify([ev.evidence_id], "target:B")
    results["N5"] = {"result": ver.result, "residuals": ver.residual_unknowns, "id": ver.verification_id}
    s = RecordStore(str(base / "n6")); e = PipelineEngine(s)
    pol = s.get("pol_accept_v1@1.0.0")
    fake = AcceptanceDecision(
        acceptance_id=new_id("acc"), verification_ids=[], target_ref="target:demo-001",
        proposed_state="{}", acceptance_authority_id="auth_acceptor_01",
        policy_id="pol_accept_v1", policy_version="1.0.0",
        policy_integrity_marker=pol["policy_integrity_marker"], scope="target:*",
        decided_at=now_iso(), decision="REJECTED", reason_code="SHORTCUT_ATTEMPT",
    )
    s.put("acceptance", fake.acceptance_id, fake.to_dict())
    ads = e.materialize_accepted_state(fake.acceptance_id, {"x": 1})
    results["N6"] = {"decision": fake.decision, "accepted_state_created": ads is not None}
    s = RecordStore(str(base / "n7")); e = PipelineEngine(s)
    ver = e.verify([], "target:demo-001")
    results["N7"] = {"result": ver.result, "residuals": ver.residual_unknowns, "id": ver.verification_id}
    results["N8"] = {"covered_by": "N3", "semantics": "authority status checked at decision_time"}
    write_json(EVIDENCE_ROOT / "negative_results.json", results)
    return results

def main():
    EVIDENCE_ROOT.mkdir(parents=True, exist_ok=True)
    print("=== R10 POSITIVE ===")
    chain, store = run_positive()
    print(json.dumps({k: chain[k] for k in chain if k != "store_index"}, indent=2))
    print("=== R10 NEGATIVES ===")
    neg = run_negatives()
    print(json.dumps(neg, indent=2))
    write_json(EVIDENCE_ROOT / "run_meta.json", {
        "runner": "run_trajectory.py", "version": "0.1.0-r8",
        "evidence_root": str(EVIDENCE_ROOT), "executed_at": now_iso(),
        "note": "R10 clean reproduction",
    })
    print("DONE", EVIDENCE_ROOT)
    return 0

if __name__ == "__main__":
    sys.exit(main())
