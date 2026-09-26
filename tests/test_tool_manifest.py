from tool_manifest import manifest_for,reconstructs,require_reconstruction

def test_mt_manifest_reconstructs_black_box_gate():
    m=manifest_for("MT")
    assert m.complete()
    assert "MT_BLACK_BOX_SEMANTIC_RETURN_GATE" in m.behavior_ids()
    assert reconstructs("MT",("MT_BLACK_BOX_SEMANTIC_RETURN_GATE",))

def test_hf1_manifest_reconstructs_unified_governed_episode():
    required=("HF001_GOVERNED_EPISODE",)
    m=manifest_for("HF001")
    assert m.complete()
    assert set(required)<=m.behavior_ids()
    assert reconstructs("HF001",required)

def test_hf2_manifest_reconstructs_local_recursive_continuation():
    required=("HF002_LOCAL_RECURSIVE_CONTINUATION",)
    m=manifest_for("HF002")
    assert m.complete()
    assert set(required)<=m.behavior_ids()
    assert reconstructs("HF002",required)

def test_root_cause_manifest_reconstructs_hf2_and_parent_handoff():
    required=(
        "ROOT_CAUSE_ROOTNESS_SELECTOR",
        "ROOT_CAUSE_HF002_LOCAL_RECURRENCE",
        "ROOT_CAUSE_IMPROVEMENTCORE_PARENT_HANDOFF",
    )
    m=manifest_for("RootCause")
    assert m.complete()
    assert set(required)<=m.behavior_ids()
    assert reconstructs("RootCause",required)

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


def test_mt_manifest_reconstructs_full_historical_witness_basis_w1_w8():
    required=(
        "MT_W1_WHOLE_OBJECT_RECONNAISSANCE",
        "MT_W2_SELF_GENERATED_LOCAL_QUESTIONS",
        "MT_W3_RECONNAISSANCE_NONMUTATION",
        "MT_W4_REOBSERVE_AFTER_MATERIAL_CHANGE",
        "MT_W5_FULL_CONSEQUENCE_CLOSURE",
        "MT_W6_ROOT_OBJECT_PRESERVATION",
        "MT_W7_CROSS_OBJECT_CROSS_SCALE_DISCOVERY",
        "MT_W8_BEHAVIORAL_EQUIVALENCE_NOT_FINAL_ANSWER_ONLY",
    )
    m=manifest_for("MT")
    assert set(required)<=m.behavior_ids()
    assert reconstructs("MT",required)
