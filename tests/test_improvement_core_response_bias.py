import sys
sys.path.insert(0,"runtime")

from improvement_core_response_bias import (
    CURRENT_RESPONSE_PROFILE,
    scan_bias_risks,
    response_release_contract,
)

def test_response_profile_preserves_result_first_and_execution_truth():
    assert "RESULT_FIRST" in CURRENT_RESPONSE_PROFILE.protected_behaviors
    assert "REPORT_ACTUAL_ACTIONS_NOT_INTENTIONS" in CURRENT_RESPONSE_PROFILE.protected_behaviors
    assert "FALSE_CLOSURE" in CURRENT_RESPONSE_PROFILE.anti_behaviors

def test_bias_scan_treats_prompt_pressure_as_framing_risk():
    r=scan_bias_risks(
        "First run PD then MT and solve all of my projects; use the six markdown files always."
    )
    assert "CLOSURE_SCOPE_PRESSURE" in r.input_framing_risks
    assert "REMEMBERED_NUMERIC_ANCHOR" in r.input_framing_risks
    assert "SEQUENCE_ANCHOR_AFTER_EXPLICITLY_REQUIRED_PREFIX" in r.input_framing_risks
    assert "UNIVERSALITY_PRESSURE" in r.input_framing_risks
    assert "TREAT_USER_FRAMING_AS_EVIDENCE_EXCEPT_EXPLICIT_REQUIRED_PREFIX" in r.corrections

def test_preference_never_becomes_truth_authority():
    contract=response_release_contract()
    assert contract["truth_precedence"]=="EVIDENCE_AND_TYPED_STATUS_OVERRIDES_STYLE_PREFERENCE"
