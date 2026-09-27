from pathlib import Path
import sys
sys.path.insert(0,"runtime")

from specification_before_transformation import SpecificationPacket, assess_transformation
from tool_manifest import manifest_for
from tool_run_registry import PROTECTED_BEHAVIORS


IDENTITY_PATH="architecture/GOAL_FULL_TOOL_MATH_001_2026-09-27.md"


def test_goal_fullmath_artifact_reconstructs_five_identity_coordinates():
    text=Path(IDENTITY_PATH).read_text(encoding="utf-8")
    for token in (
        "FullMath_(J,K)(GOAL)",
        "N_GOAL",
        "W_GOAL",
        "G_GOAL",
        "P_GOAL",
        "L_GOAL",
        "GOAL_EVIDENCE_GROUNDED_ADMISSION",
        "GOAL_PLURALITY_FAIL_OPEN",
        "goal.recover_goal",
        "D36_C",
        "HF002",
        "EXTERNAL_NOT_OWNED",
    ):
        assert token in text


def test_goal_manifest_points_to_dedicated_fullmath_identity():
    manifest=manifest_for("GOAL")
    assert manifest.lineage_contract==IDENTITY_PATH
    assert "GOAL_FULL_TOOL_IDENTITY" in manifest.behavior_ids()
    assert "GOAL_FULL_TOOL_IDENTITY" in PROTECTED_BEHAVIORS["GOAL"]


def test_future_goal_transformation_has_explicit_top_level_specification_basis():
    required=frozenset({"N_GOAL","W_GOAL","G_GOAL","P_GOAL","L_GOAL"})
    packet=SpecificationPacket(
        object_id="GOAL",
        basis_id="GOAL_FULL_TOOL_MATH_001_2026-09-27",
        identification_status="IDENTIFIED",
        required_coordinates=required,
        resolved_coordinates=required,
    )
    receipt=assess_transformation(packet,"MODIFY")
    assert receipt.status=="PASS"
    assert receipt.licensed


def test_artifact_preserves_post_hoc_process_defect_and_external_open_boundary():
    text=Path(IDENTITY_PATH).read_text(encoding="utf-8")
    assert "Historical process defect" in text
    assert "before this dedicated" in text
    assert "arbitrary-prose" in text
    assert "OPEN" in text
