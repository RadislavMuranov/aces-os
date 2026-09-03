from src.aces_runtime import ACESRuntime, Context, Intent


def test_intent_ir_is_structured_and_context_resolution_records_provenance():
    intent = Intent("I-2-001", "set_state", "demo", {"value": 1})
    context = ACESRuntime.resolve_context(intent, {"source": "fixture"})

    assert intent.intent_id == "I-2-001"
    assert context.values == {"source": "fixture"}
    assert context.provenance == {"source": "deterministic-input"}


def test_minimum_cycle_accepts_verified_state():
    runtime = ACESRuntime()
    intent = Intent("I-1E-001", "set_state", "demo", {"value": 1})
    context = ACESRuntime.resolve_context(intent)
    result = runtime.run(intent, context)

    assert result.status == "ACCEPTED"
    assert result.evidence["verification"]["verified"] is True
    assert result.evidence["accepted_state"] == {"value": 1}
    assert result.evidence["context_provenance"] == {}


def test_policy_denial_is_fail_closed():
    runtime = ACESRuntime()
    intent = Intent("I-1E-002", "set_state", "demo", {"value": 1})
    context = ACESRuntime.resolve_context(intent, {"deny": True})
    result = runtime.run(intent, context)

    assert result.status == "REJECTED"
    assert result.evidence["execution"] is None
    assert result.evidence["accepted_state"] is None


def test_unverified_result_is_not_canonical():
    runtime = ACESRuntime(executor=lambda intent, context: {"value": 0})
    intent = Intent("I-1E-003", "set_state", "demo", {"value": 1})
    context = ACESRuntime.resolve_context(intent)
    result = runtime.run(intent, context)

    assert result.status == "UNVERIFIED"
    assert result.evidence["verification"]["verified"] is False
    assert result.evidence["accepted_state"] is None
