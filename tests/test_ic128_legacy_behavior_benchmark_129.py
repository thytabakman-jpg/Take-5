from pathlib import Path
import yaml

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
    data = yaml.safe_load(PATH.read_text(encoding="utf-8"))

    assert data["status"] == "CURRENT_RESTORATION_BENCHMARK"
    assert data["reference"]["source_commit"] == "e4c76c595b44a35fd9efc02cde8979e656ef54e8"
    assert data["reference"]["controller_loop"] == ["G_Q", "G_W", "S", "E", "A", "U", "G_Q"]

    behaviors = {
        row["id"] for row in data["protected_behaviors"]
        if row.get("required")
    }
    assert behaviors == REQUIRED

    assert data["holdout_requirements"]["unlike_domains_minimum"] >= 4
    assert data["holdout_requirements"]["no_user_tool_sequence"] is True
    assert data["promotion"]["newer_or_more_complex_is_not_gain"] is True
    assert data["anti_churn"]["unchanged_repair_route"] == "NO_GAIN"
