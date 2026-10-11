from configured_hf2_execution import _raw_mapping


def test_false_and_zero_outputs_count_as_real_hf2_full_match_results():
    for result in (False, 0, 0.0):
        receipt = _raw_mapping({
            "status": "FULL_MATCH",
            "execution_truth": "FULL_MATCH",
            "result": result,
        })
        assert receipt["status"] == "FULL_MATCH"
        assert receipt["execution_truth"] == "FULL_MATCH"


def test_missing_and_empty_outputs_still_fail_full_match_closed():
    for receipt in ({}, {"result": None}, {"result": ""}, {"result": {}}, {"result": []}):
        out = _raw_mapping({
            "status": "FULL_MATCH",
            "execution_truth": "FULL_MATCH",
            **receipt,
        })
        assert out["status"] == "OPEN"
        assert out["blocker"] == "CONFIGURED_HF2_FULL_MATCH_WITHOUT_EXECUTION_WITNESS"


def test_blocked_adapter_without_result_remains_open():
    out = _raw_mapping(None)
    assert out["status"] == "OPEN"
    assert out["execution_truth"] == "OPEN"


def test_success_status_cannot_override_failed_execution_truth():
    for truth in ("OPEN", "BLOCKED", "CONFLICT"):
        out = _raw_mapping({
            "status": "EXECUTED", "execution_truth": truth,
            "result": {"claimed": "success"}, "material_delta": True,
        })
        assert out["status"] == truth
        assert out["execution_truth"] == truth
        assert out["material_delta"] is False
        assert out["blocker"] == "CONFIGURED_HF2_SUCCESS_WITH_NON_SUCCESS_TRUTH"


def test_failure_status_cannot_keep_success_execution_truth():
    out = _raw_mapping({
        "status": "BLOCKED", "execution_truth": "FULL_MATCH",
        "result": {"claimed": "success"},
    })
    assert out["status"] == "BLOCKED"
    assert out["execution_truth"] == "BLOCKED"
