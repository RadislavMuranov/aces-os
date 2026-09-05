#!/usr/bin/env python3
"""RDR-P08-R10-R1 targeted integrity repair evidence runner."""
from __future__ import annotations
import json, sys, shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from aces_p08_minimal.store import RecordStore
from aces_p08_minimal.engine import PipelineEngine
from aces_p08_minimal.models import content_hash, now_iso
from aces_p08_minimal.integrity import verify_policy
EV = ROOT / "evidence" / "r10_r1_run_001"
def wj(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
def positive():
    sr = EV / "positive" / "store"
    if sr.exists(): shutil.rmtree(sr)
    store = RecordStore(str(sr)); eng = PipelineEngine(store)
    obs = {"kind": "r10r1_obs", "value": {"status": "X"}, "t": now_iso()}
    ev = eng.capture_evidence("target:demo-001", "harness", "c1", "w_r10r1", obs)
    adm = eng.evaluate_admissibility(ev.evidence_id)
    ver = eng.verify([ev.evidence_id], "target:demo-001")
    acc = eng.accept([ver.verification_id], "target:demo-001", {"status": "X"})
    ads = eng.materialize_accepted_state(acc.acceptance_id, {"status": "X"})
    chain = {"trajectory": "POSITIVE_R10_R1", "evidence_id": ev.evidence_id,
             "admissibility_id": adm.admissibility_id, "verification_id": ver.verification_id,
             "verification_result": ver.result, "acceptance_id": acc.acceptance_id,
             "acceptance_decision": acc.decision,
             "accepted_state_id": ads.accepted_state_id if ads else None, "executed_at": now_iso()}
    wj(EV / "positive" / "chain.json", chain); return chain
def r1():
    sr = EV / "r1_tampered_obs" / "store"
    if sr.exists(): shutil.rmtree(sr)
    store = RecordStore(str(sr)); eng = PipelineEngine(store)
    obs = {"kind": "r10r1_obs", "value": {"status": "X"}, "t": now_iso()}
    ev = eng.capture_evidence("target:demo-001", "harness", "c1", "w_r10r1", obs)
    eng.evaluate_admissibility(ev.evidence_id)
    raw = store.get(f"raw_{ev.observation_payload_ref}")
    oh = ev.content_hash
    raw["payload"] = {"kind": "r10r1_obs", "value": {"status": "TAMPERED"}, "t": now_iso()}
    store.put("evidence", f"raw_{ev.observation_payload_ref}", raw)
    ver = eng.verify([ev.evidence_id], "target:demo-001")
    r = {"test": "R1_TAMPERED_OBSERVATION", "original_content_hash": oh,
         "recomputed_after_tamper": content_hash(raw["payload"]), "verification_result": ver.result,
         "residuals": ver.residual_unknowns,
         "pass": ver.result == "NOT_VERIFIED" and any("CONTENT_HASH_MISMATCH" in x for x in ver.residual_unknowns)}
    wj(EV / "r1_tampered_obs" / "result.json", r); return r
def r2():
    sr = EV / "r2_tampered_policy" / "store"
    if sr.exists(): shutil.rmtree(sr)
    store = RecordStore(str(sr)); eng = PipelineEngine(store)
    obs = {"kind": "r10r1_obs", "value": {"status": "X"}, "t": now_iso()}
    ev = eng.capture_evidence("target:demo-001", "harness", "c1", "w_r10r1", obs)
    eng.evaluate_admissibility(ev.evidence_id)
    pol = store.get("pol_verify_v1@1.0.0"); om = pol["policy_integrity_marker"]
    pol["policy_integrity_marker"] = "0" * 64; store.put("policy", "pol_verify_v1@1.0.0", pol)
    ver = eng.verify([ev.evidence_id], "target:demo-001")
    r = {"test": "R2_TAMPERED_POLICY", "original_marker": om, "tampered_marker": pol["policy_integrity_marker"],
         "verification_result": ver.result, "residuals": ver.residual_unknowns,
         "pass": ver.result == "NOT_VERIFIED" and any("POLICY_INTEGRITY_MISMATCH" in x for x in ver.residual_unknowns)}
    wj(EV / "r2_tampered_policy" / "result.json", r); return r
def r3():
    sr = EV / "r3_temporal" / "store"
    if sr.exists(): shutil.rmtree(sr)
    store = RecordStore(str(sr)); eng = PipelineEngine(store)
    obs = {"kind": "r10r1_obs", "value": {"status": "X"}, "t": now_iso()}
    ev = eng.capture_evidence("target:demo-001", "harness", "c1", "w_r10r1", obs)
    eng.evaluate_admissibility(ev.evidence_id)
    ver_t2 = eng.verify([ev.evidence_id], "target:demo-001")
    eng.revoke_authority("auth_verifier_01")
    ver_t4 = eng.verify([ev.evidence_id], "target:demo-001")
    reloaded = store.get(ver_t2.verification_id)
    r = {"test": "R3_TEMPORAL_AUTHORITY", "t2_result": ver_t2.result, "t4_result": ver_t4.result,
         "t4_residuals": ver_t4.residual_unknowns, "t2_record_unchanged": reloaded.get("result") == ver_t2.result,
         "pass": ver_t2.result == "VERIFIED" and ver_t4.result == "NOT_VERIFIED"
                 and any("STATUS_AT_DECISION" in x for x in ver_t4.residual_unknowns)}
    wj(EV / "r3_temporal" / "result.json", r); return r
def main():
    EV.mkdir(parents=True, exist_ok=True)
    pos, a, b, c = positive(), r1(), r2(), r3()
    meta = {"r1_pass": a["pass"], "r2_pass": b["pass"], "r3_pass": c["pass"],
            "positive_verification": pos["verification_result"], "executed_at": now_iso()}
    wj(EV / "run_meta.json", meta)
    print(json.dumps(meta, indent=2))
    return 0 if all([a["pass"], b["pass"], c["pass"], pos["verification_result"] == "VERIFIED"]) else 1
if __name__ == "__main__":
    sys.exit(main())
