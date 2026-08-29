from src.p0_pilot.harness import Condition, ScenarioVariant, run_session


VARIANT_A = ScenarioVariant(
    name="A",
    change="Change X",
    preferred_option="A",
    constraint="Option B requires additional testing and does not fit the timeline.",
)

VARIANT_B = ScenarioVariant(
    name="B",
    change="Change Y",
    preferred_option="B",
    constraint="Option A is scalable but exceeds the available delivery window.",
)


def test_baseline_completes_without_automation():
    telemetry = run_session("p01", "s01", Condition.BASELINE, VARIANT_A)
    assert len(telemetry.events) == 8
    assert not any(e["system"] == "coordinator" for e in telemetry.events)


def test_treatment_records_deterministic_interventions():
    telemetry = run_session("p01", "s02", Condition.TREATMENT, VARIANT_B)
    coordinator_events = [e for e in telemetry.events if e["system"] == "coordinator"]
    assert len(coordinator_events) == 8
    assert all(e["action"] == "suggest" for e in coordinator_events)


def test_treatment_preserves_required_artifact_chain():
    telemetry = run_session("p02", "s03", Condition.TREATMENT, VARIANT_A)
    systems = [e["system"] for e in telemetry.events if e["system"] != "coordinator"]
    assert systems == ["gmail", "docs", "chat", "github", "calendar", "github", "github", "github"]


def test_wrong_order_is_detectable():
    from src.p0_pilot.harness import PilotHarness, Telemetry
    from datetime import datetime, timezone

    telemetry = Telemetry("p03", "s04", Condition.BASELINE, datetime.now(timezone.utc))
    harness = PilotHarness(telemetry)
    harness.state.artifacts["ci"] = "not-run"
    harness._apply("github", "receive_approval", VARIANT_A)
    assert "D2: approval before CI pass" in harness.state.errors
