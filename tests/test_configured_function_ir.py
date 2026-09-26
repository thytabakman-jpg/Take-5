import sys
sys.path.insert(0,"runtime")

from configured_function_ir import HOLDOUT, audit_holdout, encode


def test_branch_coupled_carrier_is_not_flattened():
    row=encode("MT")
    assert "P(B_{MT})" in row.output_carrier
    assert "D^b_{MT}" in row.branch_carrier
    assert "W^b_{MT}" in row.branch_carrier
    assert "D^i_{MT}" in row.output_carrier
    assert "W^i_{MT}" in row.output_carrier


def test_registered_holdout_uses_one_generic_encoder_without_alias_substitution():
    report=audit_holdout()
    ids=tuple(row["object_id"] for row in report["rows"])
    assert ids==HOLDOUT
    assert "ICC123" in report["blocked_unregistered"]
    assert "ICC128" in report["blocked_unregistered"]
    assert encode("ICC123").residuals==("UNREGISTERED_NAMED_OBJECT",)
    assert encode("ICC128").residuals==("UNREGISTERED_NAMED_OBJECT",)


def test_semantic_identity_and_runtime_realization_are_separate_coordinates():
    mt=encode("MT")
    assert mt.configured_identity_status=="CLOSED_RELATIVE"
    assert mt.realization_status=="ENVIRONMENT_BOUND"
    assert mt.runtime_entrypoint

    conductor=encode("ToolConductor")
    assert conductor.configured_identity_status=="OPEN"
    assert conductor.realization_status=="SELF_CONTAINED"
    assert "GENERIC_ONLY_MANIFEST" in conductor.residuals


def test_pd_and_architecture_fail_closed_instead_of_becoming_green_by_function_notation():
    for name in ("PD","PDAudit","Architecture"):
        row=encode(name)
        assert row.configured_identity_status=="OPEN"
        assert "GENERIC_ONLY_MANIFEST" in row.residuals
        assert row.realization_status=="UNRECOVERED"
        assert "NATIVE_RUNTIME_UNRECOVERED" in row.residuals


def test_improvementcore_outer_function_does_not_hide_environment_or_manifest_gaps():
    row=encode("ImprovementCore")
    assert row.configured_identity_status=="OPEN"
    assert row.realization_status=="ENVIRONMENT_BOUND"
    assert "GENERIC_ONLY_MANIFEST" in row.residuals
    assert set(row.required_environment)=={"handlers","authority","controller_context"}


def test_holdout_is_not_promotion_ready_and_does_not_change_pd_goal():
    report=audit_holdout()
    assert not report["promotion_ready"]
    assert report["pd_goal_changed"] is False
