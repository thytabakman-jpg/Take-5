"""Finite current-repertoire configured execution reachability evidence.

This audit distinguishes three claims that were previously collapsed:
identity reconstruction, configured execution-plan construction, and crossing
ImprovementCore's selected-tool execution bridge into an invoked adapter.

The bridge audit uses a synthetic witness adapter only to prove controller
reachability. It does not claim that every historical tool has a standalone
native semantic adapter.
"""
from dataclasses import dataclass

from current_portfolio_identity import audit_current_portfolio_identity
from protected_transition_portfolio import audit_protected_transition_portfolio
from improvement_core_tool_bridge import bind_selected_tools, execute_bound_tools
from tool_run_registry import CONFIGURED_RUNS


@dataclass(frozen=True)
class RepertoireReachability:
    status:str
    identity_checked:int
    transition_checked:int
    bridge_execution_checked:int
    failures:tuple[str,...]


def _audit_controller_bridge()->tuple[int,tuple[str,...]]:
    failures=[]
    checked=0

    for tool_id in CONFIGURED_RUNS:
        calls=[]
        try:
            state,bindings=bind_selected_tools({"selected_tool":tool_id})
            def witness_adapter(current,plan,_tool_id=tool_id):
                calls.append((plan.tool_id,len(plan.cells),plan.wrapper_required))
                return {
                    "status":"EXECUTED",
                    "execution_truth":"IMPLEMENTATION_EXECUTED",
                    "result":{"bridge_witness":_tool_id},
                    "material_delta":True,
                    "evidence":("repertoire-reachability:synthetic-adapter",),
                }
            out=execute_bound_tools(state,bindings,{tool_id:witness_adapter})
            checked+=1
            if out.status!="EXECUTED":
                failures.append(f"{tool_id}:BRIDGE_STATUS:{out.status}")
            if calls!=[(tool_id,36,True)]:
                failures.append(f"{tool_id}:ADAPTER_NOT_ACTUALLY_INVOKED")
            outputs=tuple(out.state.get("configured_tool_outputs",())) if isinstance(out.state,dict) else ()
            if not outputs or outputs[-1].get("tool_id")!=tool_id:
                failures.append(f"{tool_id}:RESULT_NOT_CONSUMED")
        except Exception as exc:
            failures.append(f"{tool_id}:BRIDGE_EXECUTION:{type(exc).__name__}")

    return checked,tuple(failures)


def audit_current_repertoire_reachability()->RepertoireReachability:
    identity=audit_current_portfolio_identity()
    transition=audit_protected_transition_portfolio()
    bridge_checked,bridge_failures=_audit_controller_bridge()
    failures=tuple(identity.failures)+tuple(transition.failures)+tuple(bridge_failures)
    return RepertoireReachability(
        "CLOSED_RELATIVE" if not failures else "OPEN",
        identity.checked,
        transition.checked,
        bridge_checked,
        failures,
    )
