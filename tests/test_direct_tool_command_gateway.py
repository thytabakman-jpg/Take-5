import sys
sys.path.insert(0,"runtime")

import pytest

from direct_tool_command_gateway import (
    DirectToolCommandBlocked,
    bind_direct_tool_commands,
    direct_tool_ids,
    execute_direct_tool_commands,
)


def test_direct_commands_resolve_registered_tools_in_user_order():
    assert direct_tool_ids("Please run MT on this, then use GOAL on the result.")==(
        "MT","GOAL"
    )


def test_direct_command_binding_uses_current_full_configured_plan():
    bound=bind_direct_tool_commands("run MT")
    assert bound.complete
    assert bound.tool_ids==("MT",)
    binding=bound.bindings[0]
    assert binding.plan.complete
    assert binding.plan.wrapper_required is True
    assert binding.plan.geometry=="D36_C"
    assert len(binding.plan.cells)==36
    assert len(binding.plan.questions)==22*36
    assert len(binding.plan.cognitive)==4*36
    assert binding.plan.recurrence_required is True
    assert binding.plan.recurrence_engine=="HF002"
    assert binding.plan.invocation_profile=="FULL_CONFIGURED_HF2_V1"
    assert binding.summary["configured_hf2_execution"]=="SHARED_GATE"
    assert binding.summary["recurrence_engine"]=="HF002"


def test_direct_command_executes_through_same_hf2_bridge():
    calls=[]

    def mt_adapter(current,plan):
        call_no=len(calls)+1
        calls.append((call_no,plan.tool_id,len(plan.cells),plan.wrapper_required))
        return {
            "status":"EXECUTED",
            "execution_truth":"SEMANTICALLY_APPLIED",
            "state":{**current,"round":1},
            "result":{"round":1},
            "material_delta":call_no==1,
            "hf2_live_local":call_no==1,
            "evidence":["mt-round:1"],
        }

    out=execute_direct_tool_commands(
        "run MT",
        state={"round":0},
        adapters={"MT":mt_adapter},
    )
    assert out.status=="EXECUTED"
    assert calls==[(1,"MT",36,True),(2,"MT",36,True)]
    execution=out.executions[0]
    assert execution.recurrence_engine=="HF002"
    assert execution.recurrence_status=="RELATIVE_CLOSE"
    assert execution.recurrence_rounds==2
    assert out.state["direct_tool_command_status"]=="EXECUTED_FULL_CONFIGURED"


def test_missing_direct_command_adapter_preserves_open():
    out=execute_direct_tool_commands("use GOAL",adapters={})
    assert out.status=="OPEN"
    assert out.blocker=="CONFIGURED_TOOL_ADAPTER_REQUIRED:GOAL"


def test_unregistered_formal_command_fails_closed_instead_of_substitution():
    with pytest.raises(DirectToolCommandBlocked,match="DIRECT_TOOL_NOT_REGISTERED"):
        direct_tool_ids("run ICC123")


def test_direct_tool_none_adapter_cannot_claim_full_execution():
    out=execute_direct_tool_commands(
        "run MT",
        adapters={"MT":lambda state,plan:None},
    )
    assert out.status=="OPEN"
    assert out.blocker=="CONFIGURED_TOOL_HF2_OPEN:MT"
    assert out.state["direct_tool_command_status"]=="OPEN"
    assert out.executions[0].execution_truth=="OPEN"


def test_direct_tool_empty_full_match_cannot_claim_full_execution():
    out=execute_direct_tool_commands(
        "run MT",
        adapters={"MT":lambda state,plan:{
            "status":"FULL_MATCH",
            "execution_truth":"FULL_MATCH",
            "native_receipts":(),
            "cell_receipts":(),
            "question_receipts":(),
            "cognitive_receipts":(),
            "material_delta":False,
        }},
    )
    assert out.status=="OPEN"
    assert out.blocker=="CONFIGURED_TOOL_HF2_OPEN:MT"
    assert out.state["direct_tool_command_status"]=="OPEN"
    assert out.executions[0].execution_truth=="OPEN"


def test_direct_bridge_does_not_invent_material_change():
    out = execute_direct_tool_commands("run MT", adapters={"MT":lambda *_:{"status":"EXECUTED","result":True}})
    assert out.status == "EXECUTED"
    assert out.executions[0].material_delta is False

@pytest.mark.parametrize("request_ids", [("GOAL","MT"), ["GOAL","MT"]])
def test_structured_direct_commands_preserve_exact_order_and_context(request_ids):
    bound=bind_direct_tool_commands(request_ids,state={"selected_tool_id":"NOT_REGISTERED"})
    assert bound.complete
    assert bound.tool_ids==("GOAL","MT")
    assert tuple(b.tool_id for b in bound.bindings)==bound.tool_ids
    assert all(b.plan.complete and b.plan.recurrence_engine=="HF002" for b in bound.bindings)
    assert bound.state["selected_tool_id"]=="NOT_REGISTERED"


@pytest.mark.parametrize("request_ids,reason", [
    ([], "DIRECT_TOOL_COMMAND_NOT_FOUND"),
    (["MT","NOT_REGISTERED"], "DIRECT_TOOL_NOT_REGISTERED"),
    (["MT","Architect"], "DIRECT_TOOL_NOT_REGISTERED"),
    (["MT",None], "DIRECT_TOOL_NOT_REGISTERED"),
    (["MT","MT"], "DIRECT_TOOL_DUPLICATE_ID"),
])
def test_invalid_structured_batch_blocks_before_any_adapter(request_ids,reason):
    calls=[]
    with pytest.raises(DirectToolCommandBlocked,match=reason):
        execute_direct_tool_commands(request_ids,adapters={"MT":lambda s,p:calls.append(p)})
    assert not calls


def test_structured_single_command_uses_same_plan_and_missing_adapter_boundary():
    a=bind_direct_tool_commands("run GOAL")
    b=bind_direct_tool_commands(["GOAL"])
    assert a.bindings==b.bindings
    out=execute_direct_tool_commands(["GOAL"],adapters={})
    assert out.status=="OPEN"
    assert out.blocker=="CONFIGURED_TOOL_ADAPTER_REQUIRED:GOAL"


def test_structured_batch_binds_every_registered_identity():
    from tool_run_registry import CONFIGURED_RUNS
    ids=tuple(CONFIGURED_RUNS)
    bound=bind_direct_tool_commands(ids)
    assert bound.complete and bound.tool_ids==ids
    assert all(b.plan.complete for b in bound.bindings)


@pytest.mark.parametrize("invalid_request", [{"command": "run MT"}, {"run MT"}, b"run MT", None, 12])
def test_non_string_non_sequence_requests_cannot_be_coerced_to_commands(invalid_request):
    with pytest.raises(DirectToolCommandBlocked, match="DIRECT_TOOL_REQUEST_REQUIRES_STRING_OR_ORDERED_IDS"):
        direct_tool_ids(invalid_request)
