from tool_manifest import manifest_for,reconstructs,require_reconstruction

def test_mt_manifest_reconstructs_black_box_gate():
    m=manifest_for("MT")
    assert m.complete()
    assert "MT_BLACK_BOX_SEMANTIC_RETURN_GATE" in m.behavior_ids()
    assert reconstructs("MT",("MT_BLACK_BOX_SEMANTIC_RETURN_GATE",))

def test_assert_manifest_reconstructs_canonical_compound_and_full36_behavior():
    required=(
        "ASSERT_COMPOUND_STAGE_ORDER",
        "ASSERT_SECOND_COMPARE_REQUIRED",
        "ASSERT_DISCOVERY_WORLD_FIXED_POINT_REENTRY",
        "ASSERT_FULL36_THREE_SURFACE_COVERAGE",
    )
    m=manifest_for("ASSERT")
    assert m.complete()
    assert set(required)<=m.behavior_ids()
    assert reconstructs("ASSERT",required)

def test_missing_protected_behavior_fails_closed():
    try:
        require_reconstruction("MT",("NONEXISTENT_PROTECTED_BEHAVIOR",))
    except RuntimeError as exc:
        assert "TOOL_PROTECTED_BEHAVIOR_UNRECOVERED:MT" in str(exc)
    else:
        raise AssertionError("missing protected behavior did not fail closed")

def test_generic_tool_manifest_still_has_common_wrapper_contracts():
    m=manifest_for("PD")
    assert m.complete()
    assert {
        "CONFIGURED_RUN_WRAPPER",
        "TOOL_RUN_CLOSURE",
        "REENTRY_REQUIRED",
        "OPEN_PRESERVATION",
    } <= m.behavior_ids()
