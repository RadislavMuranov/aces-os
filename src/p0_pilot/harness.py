"""Deterministic, side-effect-free P0.3 pilot harness.

This harness models the experiment boundary only. Real MCP adapters can be
plugged in later; no production systems are touched by this module.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable


class Condition(str, Enum):
    BASELINE = "baseline"
    TREATMENT = "treatment"


@dataclass(frozen=True)
class ScenarioVariant:
    name: str
    change: str
    preferred_option: str
    constraint: str


@dataclass
class Telemetry:
    participant_id: str
    session_id: str
    condition: Condition
    started_at: datetime
    events: list[dict[str, Any]] = field(default_factory=list)

    def record(self, system: str, action: str, **data: Any) -> None:
        self.events.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system": system,
            "action": action,
            **data,
        })


@dataclass
class PilotState:
    current_step: int = 0
    artifacts: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    automation_interventions: int = 0
    automation_failures: int = 0
    human_corrections: int = 0


STEPS = (
    ("gmail", "receive_request"),
    ("docs", "read_spec"),
    ("chat", "review_discussion"),
    ("github", "create_pr"),
    ("calendar", "schedule_review"),
    ("github", "request_review"),
    ("github", "ci_complete"),
    ("github", "receive_approval"),
)


class PilotHarness:
    """Runs the synthetic scenario without external side effects."""

    def __init__(self, telemetry: Telemetry, coordinator: Callable[[str, PilotState], str] | None = None):
        self.telemetry = telemetry
        self.state = PilotState()
        self.coordinator = coordinator

    def execute(self, variant: ScenarioVariant) -> PilotState:
        for index, (system, action) in enumerate(STEPS, start=1):
            self.state.current_step = index
            if self.coordinator is not None:
                suggestion = self.coordinator(action, self.state)
                self.state.automation_interventions += 1
                self.telemetry.record("coordinator", "suggest", target=action, suggestion=suggestion)
            self._apply(system, action, variant)
        return self.state

    def _apply(self, system: str, action: str, variant: ScenarioVariant) -> None:
        self.telemetry.record(system, action, change=variant.change)
        if action == "receive_request":
            self.state.artifacts["email"] = f"request:{variant.change}"
        elif action == "read_spec":
            self.state.artifacts["spec"] = f"spec:{variant.change}"
        elif action == "review_discussion":
            self.state.artifacts["discussion"] = variant.constraint
        elif action == "create_pr":
            self.state.artifacts["pr"] = f"pr:{variant.change}"
        elif action == "schedule_review":
            self.state.artifacts["calendar"] = f"review:{variant.change}:15:00"
        elif action == "request_review":
            if "pr" not in self.state.artifacts:
                self.state.errors.append("D3: request-review without PR")
        elif action == "ci_complete":
            self.state.artifacts["ci"] = "passed"
        elif action == "receive_approval":
            if self.state.artifacts.get("ci") != "passed":
                self.state.errors.append("D2: approval before CI pass")
            self.state.artifacts["approval"] = "team-lead-1:approved"


def default_coordinator(action: str, state: PilotState) -> str:
    """Reference coordinator policy; deterministic and explainable."""
    next_steps = {
        "receive_request": "find related spec, discussion, PR and review event",
        "read_spec": "review discussion constraints before choosing implementation",
        "review_discussion": "create/update PR with source links",
        "create_pr": "schedule review and request review after CI",
        "schedule_review": "request review when CI passes",
        "request_review": "wait for CI/review state",
        "ci_complete": "record CI result and continue review flow",
        "receive_approval": "confirm completion state",
    }
    return next_steps[action]


def run_session(participant_id: str, session_id: str, condition: Condition, variant: ScenarioVariant) -> Telemetry:
    telemetry = Telemetry(
        participant_id=participant_id,
        session_id=session_id,
        condition=condition,
        started_at=datetime.now(timezone.utc),
    )
    coordinator = default_coordinator if condition is Condition.TREATMENT else None
    PilotHarness(telemetry, coordinator).execute(variant)
    return telemetry
