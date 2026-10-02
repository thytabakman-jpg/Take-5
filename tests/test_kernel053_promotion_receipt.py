import sys
sys.path.insert(0,"runtime")

from kernel053_promotion_receipt import build_kernel053_repository_receipt


def test_kernel053_candidate_crosses_full_configured_hf2_and_pti_path():
    receipt=build_kernel053_repository_receipt()
    assert receipt["status"]=="VERIFIED"
    assert receipt["tool_id"]=="ICC128"
    assert receipt["invocation_profile"]=="FULL_CONFIGURED_HF2_V1"
    assert receipt["mode"]=="OBSERVER"
    assert receipt["geometry"]=="D36_C"
    assert receipt["cell_count"]==36
    assert receipt["native_count"]==36
    assert receipt["question_count"]==22*36
    assert receipt["cognitive_count"]==4*36
    assert receipt["recurrence_engine"]=="HF002"
    assert set(receipt["protected_transition"]["coordinates"].values())=={"VERIFIED"}
    assert receipt["external_host_interception"]=="EXTERNAL_NOT_OWNED"
