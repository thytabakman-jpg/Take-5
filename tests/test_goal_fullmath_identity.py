from pathlib import Path
import sys
sys.path.insert(0,"runtime")

from specification_before_transformation import SpecificationPacket, assess_transformation
from portable_tool_conductor import compilation_witness
from tool_manifest import manifest_for
from tool_run_registry import PROTECTED_BEHAVIORS


IDENTITY_PATH="architecture/GOAL_FULL_TOOL_MATH_002_2026-09-30.md"


def test_goal_fullmath_artifact_reconstructs_five_identity_coordinates():
    text=Path(IDENTITY_PATH).read_text(encoding="utf-8")
    for token in (
        "FullMath_(J,K)(GOAL)",
        "N_GOAL",
        "W_GOAL",
        "G_GOAL",
        "P_GOAL",
        "L_GOAL",
        "GOAL_ROBUST_MT_PREREQUISITE",
        "MT_BLACK_BOX_SEMANTIC_RETURN_GATE",
        "FULL_CONFIGURED_HF2_V1",
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
        basis_id="GOAL_FULL_TOOL_MATH_002_2026-09-30",
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


def test_goal_source_map_resolves_one_live_spec_and_preserves_older_lineage():
    """Reject GOAL source-map regressions to a legacy or cross-repository selector."""
    text=Path("projects/tool-system/current-tools/goal/SOURCE_MAP.md").read_text(encoding="utf-8")
    live_heading="## Live GOAL binding"
    assert text.count(live_heading)==1
    live=text.split(live_heading,1)[1].split("\n## ",1)[0]
    spec=manifest_for("GOAL").lineage_contract
    entrypoint=compilation_witness("GOAL").entrypoint

    # Follow the machine-selected current contract, not a manually selected date.
    assert spec=="architecture/GOAL_FULL_TOOL_MATH_002_2026-09-30.md"
    assert f"](../../../../{spec})" in live
    assert f"`{entrypoint}`" in live
    assert "manifest_for(\"GOAL\").lineage_contract" in live

    # The predecessor and external semantic sources remain discoverable,
    # but cannot masquerade as this configured-tool's live selector.
    assert "GOAL_FULL_TOOL_MATH_001_2026-09-27.md" not in live
    assert "Reaserch/blob/" not in live
    assert "**Earlier historical basis, not an alternate current selector:**" in text
    assert "GOAL_FULL_TOOL_MATH_001_2026-09-27.md" in text
    assert "Cross-repository GOAL provenance (discovery only; not configured-tool authority)" in text
    assert "If the manifest, configured entrypoint, and this source map disagree" in live


def test_goal_open_question_preserves_only_unresolved_cross_repo_authority():
    """An unresolved Reaserch transfer is not an unresolved Take-5 selector."""
    question=Path("projects/tool-system/current-tools/goal/OPEN_QUESTIONS.md").read_text(encoding="utf-8")
    source_map=Path("projects/tool-system/current-tools/goal/SOURCE_MAP.md").read_text(encoding="utf-8")
    spec=manifest_for("GOAL").lineage_contract
    entry=compilation_witness("GOAL").entrypoint

    assert spec=="architecture/GOAL_FULL_TOOL_MATH_002_2026-09-30.md"
    assert entry=="goal.recover_goal_configured"
    assert spec in question and spec in source_map
    assert entry in question and entry in source_map
    assert "**Resolved for configured Take-5 GOAL invocations:**" in question
    assert "**Still OPEN — cross-repository handoff/equivalence:**" in question
    assert "No admitted cross-repository equivalence, transfer" in question
    assert "If the concrete consumer's owner cannot be resolved" in question
    assert "Which contract governs each invocation remains" not in question
