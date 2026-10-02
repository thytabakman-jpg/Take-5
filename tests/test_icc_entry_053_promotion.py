import inspect
import sys
sys.path.insert(0,"runtime")

from dataclasses import dataclass

from icc128_entry_binding import bind_icc128_entry_contract
from icc_bootstrap import ToolRunReceipt
from icc_entry import ICC128RuntimeBindings, run_icc, run_icc_debug_injected
from tool_run_registry import CONFIGURED_RUNS


@dataclass(frozen=True)
class Cert:
    status:str


@dataclass(frozen=True)
class Closure:
    state:dict
    certificate:Cert


def _assert_observer(target,binding):
    return ToolRunReceipt("ASSERT",True,True,True,True,True,True,{"asserted":True})


def _goal_observer(target,asserted,binding):
    return ToolRunReceipt("GOAL",True,True,True,True,True,True,{"goal":"governing"})


def _controller_bindings():
    def gq(z,m):
        return [{"id":"q1"}]

    def gw(q,z,m):
        return [{
            "id":"w1",
            "jobs":(),
            "operation_class":"OBSERVE",
            "effect_class":"EVIDENCE_ONLY",
        }]

    def admit(results,z,m):
        return {"material_result_delta":bool(results),"results":tuple(results)}

    def update(z,m,d):
        z=dict(z); m=dict(m)
        z["terminal"]="COMPLETE"
        z["admitted_continuation"]=False
        m["last_delta"]=d
        return z,m

    def execute(item,z,m):
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":{"ok":True},
            "material_delta":False,
            "evidence":("canonical:icc128",),
        }

    return ICC128RuntimeBindings(
        generate_questions=gq,
        generate_work=gw,
        admit_results=admit,
        update_controller_state=update,
        generic_execute=execute,
    )


def _binding():
    return bind_icc128_entry_contract(
        "ICC, finish it",
        target="kernel-053",
        job="canonical-icc128",
        basis="KERNEL_053",
        episode_id="promotion-test",
    )


def test_canonical_run_icc_has_no_arbitrary_parent_controller_injection():
    params=inspect.signature(run_icc).parameters
    assert "ic_fn" not in params
    assert "icc128_adapter" not in params
    assert "controller_bindings" in params
    assert "goal_project_fn" not in params
    assert "ic_fn" in inspect.signature(run_icc_debug_injected).parameters


def test_canonical_run_icc_constructs_and_executes_current_icc128_controller():
    out=run_icc(
        _binding(),
        {"answer":1},
        {},
        controller_bindings=_controller_bindings(),
        assert_observer_fn=_assert_observer,
        goal_observer_fn=_goal_observer,
        observe_fn=lambda s,b:s,
        formalize_fn=lambda o,b:{"m":"fixed"},
        packetize_fn=lambda m,g,s,b:{
            "type":"system",
            "scope":"canonical",
            "selectors":[],
            "open":[],
            "obligations":[],
        },
        closure_fn=lambda p,i,a:Closure(dict(p),Cert("CLOSED")),
        update_fn=lambda p,c:c.state,
        jane_update_fn=None,
        result_fn=lambda s:s["answer"],
    )
    assert out.status=="CLOSED_RELATIVE"
    assert len(out.rounds)==1


def test_registry_types_icc128_as_top_level_and_improvementcore_as_delegated():
    icc=CONFIGURED_RUNS["ICC128"]
    improvement=CONFIGURED_RUNS["ImprovementCore"]
    assert "ICC128_CANONICAL_TOP_LEVEL_SUBSTANTIVE_OWNERSHIP" in icc.protected_behaviors
    assert "IMPROVEMENTCORE_DELEGATED_EPISODE_CONTROLLER_OWNERSHIP" in improvement.protected_behaviors
    assert "IMPROVEMENTCORE_CONTROLLER_OWNERSHIP" not in improvement.protected_behaviors
