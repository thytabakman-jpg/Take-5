import sys
sys.path.insert(0,"runtime")

from direct_tool_command_gateway import (
    bind_direct_tool_commands,
    execute_direct_tool_commands,
)
from tool_manifest import reconstructs
from tool_run_registry import CONFIGURED_RUNS


def test_mt_fresh_direct_invocation_satisfies_sigma_four_gate_classifier():
    """Real regression: 'run MT' must reach the full current MT with no chat-history rescue."""
    request="run MT"
    initial_state={"round":0}

    # Delta — the current registered MT identity is definition/reconstruction closed.
    spec=CONFIGURED_RUNS["MT"]
    delta=spec.complete()

    # Omega — the direct command is bound to every required full-run obligation.
    bound=bind_direct_tool_commands(request,state=initial_state)
    assert bound.complete
    assert bound.tool_ids==("MT",)
    binding=bound.bindings[0]
    plan=binding.plan
    omega=all((
        plan.complete,
        plan.wrapper_required is True,
        plan.mode=="OBSERVER",
        plan.geometry=="D36_C",
        len(plan.cells)==36,
        len(plan.questions)==22*36,
        len(plan.cognitive)==4*36,
        plan.recurrence_required is True,
        plan.recurrence_engine=="HF002",
        plan.invocation_profile=="FULL_CONFIGURED_HF2_V1",
        binding.summary["configured_hf2_execution"]=="SHARED_GATE",
    ))

    # Phi — an actual configured realization is available and executes.
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
            "evidence":["fresh-mt-round:1"],
        }

    out=execute_direct_tool_commands(
        request,
        state=initial_state,
        adapters={"MT":mt_adapter},
    )
    phi=(
        out.status=="EXECUTED"
        and out.state["direct_tool_command_status"]=="EXECUTED_FULL_CONFIGURED"
        and len(out.executions)==1
    )

    # Xi — the protected MT behavior survives the real invocation path.
    execution=out.executions[0]
    xi=all((
        "MT_BLACK_BOX_SEMANTIC_RETURN_GATE" in spec.protected_behaviors,
        reconstructs(
            "MT",
            (
                "MT_BLACK_BOX_SEMANTIC_RETURN_GATE",
                "PROTECTED_TRANSITION_INTEGRITY",
                "CONFIGURED_HF2_RECURRENCE",
                "FULL_CONFIGURED_INVOCATION_PROFILE",
            ),
        ),
        execution.recurrence_engine=="HF002",
        execution.recurrence_status=="RELATIVE_CLOSE",
        execution.recurrence_rounds==2,
        calls==[(1,"MT",36,True),(2,"MT",36,True)],
    ))

    sigma=int(delta and omega and phi and xi)

    assert {"Delta":delta,"Omega":omega,"Phi":phi,"Xi":xi} == {
        "Delta":True,"Omega":True,"Phi":True,"Xi":True
    }
    assert sigma==1

    # The test supplies only the direct command and an empty problem-state seed.
    # No conversation/history corpus is available to rescue the invocation.
    forbidden={"conversation","conversation_history","chat_history","prior_chat","memory"}
    assert forbidden.isdisjoint(initial_state)
    assert forbidden.isdisjoint(out.state)


def test_mt_fresh_direct_invocation_fails_closed_without_realizer():
    """A missing semantic adapter must not masquerade as a successful full MT run."""
    out=execute_direct_tool_commands("run MT",state={},adapters={})
    assert out.status=="OPEN"
    assert out.blocker=="CONFIGURED_TOOL_ADAPTER_REQUIRED:MT"
