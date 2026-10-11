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
