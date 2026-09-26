from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_take5_north_star_and_gap_ledger_are_recoverable():
    north=(ROOT/"architecture/TAKE5_TARGET_SYSTEM_091.md").read_text(encoding="utf-8")
    gaps=(ROOT/"architecture/TAKE5_TARGET_GAP_LEDGER_091.yaml").read_text(encoding="utf-8")
    migration=(ROOT/"MIGRATION_STATE.yaml").read_text(encoding="utf-8")

    assert "canonical operating system for a cumulative autonomous" in north
    assert "No repeated user instruction" in north
    assert "G01" in gaps and "entry_state_reconstruction" in gaps
    assert "G05" in gaps and "discovery_to_work_to_reentry" in gaps
    assert "restore_closed_loop_before_expanding_capability_count" in gaps
    assert "TAKE5_TARGET_SYSTEM_091.md" in migration
    assert "TAKE5_TARGET_GAP_LEDGER_091.yaml" in migration

def test_take5_target_preserves_role_boundaries():
    north=(ROOT/"architecture/TAKE5_TARGET_SYSTEM_091.md").read_text(encoding="utf-8")
    assert "ImprovementCore is not the whole system." in north
    assert "Jane is the direct continuity supervisor/facade, not the primary solver." in north
    assert "The kernel does not own every useful tool" in north
