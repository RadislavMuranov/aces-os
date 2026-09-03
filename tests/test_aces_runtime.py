import json

from src.aces_runtime import ACESRuntime, Intent


def test_minimum_cycle_accepts_verified_state():
    runtime = ACESRuntime()
    intent = Intent("I-1E-001", "set_state", "demo", {"value": 1})
    context = runtime.resolve_context(intent, {})
    result = runtime.run(intent, context)

    assert result.status == "ACCEPTED"
    assert result.evidence["verification"]["verified"] is True
    assert result.evidence["acceptance"]["accepted"] is True
    assert result.evidence["accepted_state"] == {"value": 1}


def test_policy_denial_is_fail_closed():
    runtime = ACESRuntime()
    intent = Intent("I-1E-002", "set_state", "demo", {"value": 1})
    context = runtime.resolve_context(intent, {"deny": True})
    result = runtime.run(intent, context)

    assert result.status == "REJECTED"
    assert result.evidence["execution"] is None
    assert result.evidence["accepted_state"] is None


def test_unverified_result_is_not_canonical():
    runtime = ACESRuntime(executor=lambda intent, context: {"value": 0})
    intent = Intent("I-1E-003", "set_state", "demo", {"value": 1})
    result = runtime.run(intent, runtime.resolve_context(intent, {}))

    assert result.status == "UNVERIFIED"
    assert result.evidence["verification"]["verified"] is False
    assert result.evidence["acceptance"]["accepted"] is False
    assert result.evidence["accepted_state"] is None


def test_authority_decision_is_separate_from_connector():
    runtime = ACESRuntime()
    intent = Intent("I-3-001", "set_state", "demo", {"value": 2})
    context = runtime.resolve_context(intent, {})
    decision = runtime.authorize(intent, context)
    plan = runtime.resolve_connector(intent, context, decision)

    assert decision.allowed is True
    assert decision.policy_id != plan.connector_id
    assert plan.capability == runtime.CAPABILITY
    assert plan.protocol == runtime.PROTOCOL


def test_connector_resolution_cannot_bypass_denied_authority():
    runtime = ACESRuntime()
    intent = Intent("I-4-001", "set_state", "demo", {"value": 3})
    context = runtime.resolve_context(intent, {"deny": True})
    decision = runtime.authorize(intent, context)

    assert decision.allowed is False
    assert runtime.resolve_connector(intent, context, decision) is None


def test_observation_has_source_and_provenance():
    runtime = ACESRuntime()
    intent = Intent("I-5-001", "set_state", "demo", {"value": 5})
    result = runtime.run(intent, runtime.resolve_context(intent, {}))

    observation = result.evidence["observation"]
    assert observation["state"] == {"value": 5}
    assert observation["source"] == runtime.OBSERVATION_SOURCE
    assert observation["provenance"] == "execution-receipt:cycle-000001"


def test_evidence_bundle_is_persisted(tmp_path):
    evidence_path = tmp_path / "evidence.jsonl"
    runtime = ACESRuntime(evidence_path=str(evidence_path))
    intent = Intent("I-5-002", "set_state", "demo", {"value": 6})
    result = runtime.run(intent, runtime.resolve_context(intent, {}))

    records = [json.loads(line) for line in evidence_path.read_text(encoding="utf-8").splitlines()]
    assert len(records) == 1
    assert records[0]["evidence_id"] == result.evidence["evidence_id"]
    assert records[0]["status"] == "ACCEPTED"


def test_rejected_cycle_also_persists_evidence(tmp_path):
    evidence_path = tmp_path / "evidence.jsonl"
    runtime = ACESRuntime(evidence_path=str(evidence_path))
    intent = Intent("I-5-003", "set_state", "demo", {"value": 7})
    result = runtime.run(intent, runtime.resolve_context(intent, {"deny": True}))

    records = [json.loads(line) for line in evidence_path.read_text(encoding="utf-8").splitlines()]
    assert result.status == "REJECTED"
    assert records[0]["status"] == "REJECTED"


def test_accepted_state_is_persisted_and_replayed(tmp_path):
    state_path = tmp_path / "accepted-state.json"
    intent = Intent("I-6-001", "set_state", "demo", {"value": 9})

    first = ACESRuntime(accepted_state_path=str(state_path))
    result = first.run(intent, first.resolve_context(intent, {}))
    assert result.status == "ACCEPTED"
    assert state_path.exists()

    second = ACESRuntime(accepted_state_path=str(state_path))
    assert second.replay_accepted_state("demo") == {"value": 9}


def test_unverified_state_is_never_persisted(tmp_path):
    state_path = tmp_path / "accepted-state.json"
    runtime = ACESRuntime(
        executor=lambda intent, context: {"value": 0},
        accepted_state_path=str(state_path),
    )
    intent = Intent("I-6-002", "set_state", "demo", {"value": 1})
    result = runtime.run(intent, runtime.resolve_context(intent, {}))

    assert result.status == "UNVERIFIED"
    assert not state_path.exists()
    assert runtime.replay_accepted_state("demo") is None
