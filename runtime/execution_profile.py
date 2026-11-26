"""Shared configured execution profile identities and recurrence selection."""

DEFAULT_GEOMETRY="D36_C"
DEFAULT_MODE="OBSERVER"
DEFAULT_RECURRENCE_ENGINE="HF002"
SELF_RECURRENCE_ENGINE="SELF"
FULL_INVOCATION_PROFILE="FULL_CONFIGURED_HF2_V1"
QUESTION_FAMILIES=tuple(f"Q{i:02d}" for i in range(1,23))
COGNITIVE_OPERATORS=("DIFFERENTIATE","RELATE","RECONSTRUCT","STRENGTHEN")


def recurrence_engine_for(tool_id: str) -> str:
    """HF002 owns its own recurrence; ordinary tools use the shared engine."""
    return SELF_RECURRENCE_ENGINE if tool_id == "HF002" else DEFAULT_RECURRENCE_ENGINE
