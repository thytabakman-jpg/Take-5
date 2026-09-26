from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "integration" / "IC128_LEGACY_BEHAVIOR_BENCHMARK_129.yaml"

REQUIRED = {
    "REAL_GOAL_RECOVERY",
    "ENDOGENOUS_QUESTION_GENERATION",
    "DISCRIMINATING_WORK_GENERATION",
    "CHEAP_DIRECT_PATH",
    "NONDOMINATED_PLURALITY",
    "RESULT_SENSITIVE_RESELECTION",
    "NO_PREMATURE_TERMINALITY",
    "INTERNAL_AUTONOMY",
    "MEMORY_WITHOUT_CONTEXT_BLOAT",
    "EXECUTION_TRUTH",
    "DURABLE_MATERIAL_CAPTURE",
    "RESPONSE_DISCIPLINE",
}


def test_legacy_restoration_benchmark_is_complete_and_bound_to_frozen_reference():
    text = PATH.read_text(encoding="utf-8")

    assert "status: CURRENT_RESTORATION_BENCHMARK" in text
    assert "source_commit: e4c76c595b44a35fd9efc02cde8979e656ef54e8" in text
    assert "controller_loop: [G_Q, G_W, S, E, A, U, G_Q]" in text

    for behavior in REQUIRED:
        assert f"id: {behavior}" in text

    assert "unlike_domains_minimum: 4" in text
    assert "no_user_tool_sequence: true" in text
    assert "newer_or_more_complex_is_not_gain: true" in text
    assert "unchanged_repair_route: NO_GAIN" in text
