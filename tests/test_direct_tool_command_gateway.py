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
