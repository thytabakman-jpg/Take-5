import pytest
from activation_bridge import Selection,ExecutionReceipt,bind,activation_complete,execution_stage,Stage

def sel(obs=False):
    return Selection("e1","s1","DOS","project","observe",frozenset({"observe"}),obs)

def test_successful_activation_path():
    s=sel(); b=bind(s); e=ExecutionReceipt("e1",b.contract_id,"fixture",True,True,True,True,True)
    assert activation_complete(s,b,e)

def test_selected_behavior_cannot_disappear_in_binding():
    with pytest.raises(ValueError): bind(sel(),program_id="OTHER")

def test_authority_cannot_expand_in_binding():
    with pytest.raises(PermissionError): bind(sel(),authority_out=frozenset({"observe","mutate"}))

def test_bound_but_unscheduled_is_not_activation():
    s=sel(); b=bind(s); e=ExecutionReceipt("e1",b.contract_id,"github",False,False,False,False,False,"SCHEDULING")
    assert not activation_complete(s,b,e)
    assert execution_stage(e)==Stage.BLOCKED

def test_started_dependency_failure_is_not_activation():
    s=sel(); b=bind(s); e=ExecutionReceipt("e1",b.contract_id,"fixture",True,True,False,False,False,"DEPENDENCY")
    assert not activation_complete(s,b,e)

def test_executed_but_unconsumed_is_not_activation():
    s=sel(); b=bind(s); e=ExecutionReceipt("e1",b.contract_id,"fixture",True,True,True,True,False)
    assert not activation_complete(s,b,e)
    assert execution_stage(e)==Stage.RESULT_CAPTURED

def test_zero_request_observation_cannot_become_substantive():
    with pytest.raises(PermissionError): bind(sel(True),observation_only=False)
