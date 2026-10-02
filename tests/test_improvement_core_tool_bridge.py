import sys
sys.path.insert(0,"runtime")

import pytest

from improvement_core_tool_bridge import (
    ToolBridgeBlocked,
    bind_selected_tools,
    execute_bound_tools,
)


def test_selected_registered_tools_bind_full_configured_execution_plans():
    state,bindings=bind_selected_tools({
        "selected_tools":["RootCause","QuestionWorthAsking"],
    })
    assert [x.tool_id for x in bindings]==["RootCause","QuestionWorthAsking"]
    assert all(x.plan.complete for x in bindings)
    assert all(len(x.plan.cells)==36 for x in bindings)
    assert state["configured_tool_binding_status"]=="BOUND"
    assert [x["tool_id"] for x in state["configured_tool_bindings"]]==[
        "RootCause","QuestionWorthAsking"
    ]


def test_bound_tools_are_actually_invoked_and_outputs_are_consumed():
    state,bindings=bind_selected_tools({"selected_tool":"RootCause"})
    calls=[]

    def root_adapter(current,plan):
        calls.append((plan.tool_id,len(plan.cells),plan.wrapper_required))
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":{"root":"TOOL_SELECTION_EXECUTION_SEAM"},
            "evidence":["native:root-cause"],
            "material_delta":len(calls)==1,
        }

    out=execute_bound_tools(state,bindings,{"RootCause":root_adapter})
    assert out.status=="EXECUTED"
    assert out.blocker is None
    assert calls==[("RootCause",36,True),("RootCause",36,True)]
    assert out.executions[0].execution_truth=="IMPLEMENTATION_EXECUTED"
    assert out.executions[0].recurrence_engine=="HF002"
    assert out.executions[0].recurrence_status=="RELATIVE_CLOSE"
    assert out.executions[0].recurrence_rounds==2
    assert out.state["configured_tool_outputs"][0]["result"]["root"]=="TOOL_SELECTION_EXECUTION_SEAM"
    assert out.state["configured_tool_outputs"][0]["material_delta"] is True
    assert out.state["configured_tool_outputs"][0]["recurrence"]["engine"]=="HF002"


def test_missing_adapter_preserves_open_instead_of_faking_execution():
    state,bindings=bind_selected_tools({"selected_tool":"RootCause"})
    out=execute_bound_tools(state,bindings,{})
    assert out.status=="OPEN"
    assert out.blocker=="CONFIGURED_TOOL_ADAPTER_REQUIRED:RootCause"
    assert out.executions==()


def test_unregistered_explicit_tool_fails_closed():
    with pytest.raises(ToolBridgeBlocked,match="CONFIGURED_TOOL_NOT_REGISTERED"):
        bind_selected_tools({"selected_tool":"ImaginaryTool"})



def test_hf2_reapplies_same_bound_tool_when_adapter_exposes_live_local_frontier():
    state,bindings=bind_selected_tools({"selected_tool":"RootCause","round":0})
    calls=[]

    def root_adapter(current,plan):
        n=int(current.get("round",0))+1
        calls.append(n)
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "state":{**current,"round":n},
            "result":{"round":n},
            "evidence":[f"native:round:{n}"],
            "material_delta":n<3,
            "hf2_live_local":n<2,
        }

    out=execute_bound_tools(state,bindings,{"RootCause":root_adapter})
    assert out.status=="EXECUTED"
    assert calls==[1,2,3]
    assert out.executions[0].recurrence_engine=="HF002"
    assert out.executions[0].recurrence_status=="RELATIVE_CLOSE"
    assert out.executions[0].recurrence_rounds==3
    trace=out.state["configured_tool_outputs"][0]["recurrence"]["trace"]
    assert [row["disposition"] for row in trace]==["REAPPLY_C","REAPPLY_C","RELATIVE_CLOSE"]
