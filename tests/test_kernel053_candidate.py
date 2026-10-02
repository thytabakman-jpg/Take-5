import inspect
import sys
sys.path.insert(0,"runtime")

from dataclasses import dataclass

from entry_contract import bind_entry_contract
from icc128_entry_binding import bind_icc128_entry_contract
from icc128_episode_adapter import ICC128EpisodeAdapter
from icc_entry_053_candidate import run_icc_053_candidate
from icc_bootstrap import ToolRunReceipt
from kernel053_child_result import project_child_result
from kernel053_durable_execution import Take5InlineBackend, execute_selected_operation
from kernel053_packetize import PacketizeSelectionBlocked, validate_packetize_output


def _packet():
    return {
        "job":"finish-kernel-053",
        "identity":"kernel-053",
        "authority":(),
        "local_authority":(),
        "external_job":"finish-kernel-053",
        "frozen_target":"kernel-053",
        "operational_goal":"finish",
        "frozen_math":{"equation":"S=<K,W,C,J,T,Gamma>"},
        "frozen_math_fingerprint":"fp-053",
        "obligations":(),
    }


def _one_round_adapter(*, delegated=None):
    def gq(z,m):
        return [{"id":"q1"}]

    def gw(q,z,m):
        if delegated:
            return [{
                "id":"w1",
                "delegated_controller":delegated,
                "jobs":(),
                "operation_class":"OBSERVE",
                "effect_class":"EVIDENCE_ONLY",
            }]
        return [{
            "id":"w1",
            "jobs":(),
            "operation_class":"OBSERVE",
            "effect_class":"EVIDENCE_ONLY",
        }]

    def admit(results,z,m):
        return {"material_result_delta":bool(results),"observed":tuple(results)}

    def update(z,m,d):
        z=dict(z); m=dict(m)
        z["terminal"]="COMPLETE"
        z["admitted_continuation"]=False
        m["last_delta"]=d
        return z,m

    return ICC128EpisodeAdapter(
        generate_questions=gq,
        generate_work=gw,
        admit_results=admit,
        update_state=update,
        generic_execute=lambda item,z,m:{
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":{"answer":42},
            "material_delta":True,
            "evidence":("generic:executed",),
        },
        delegated_controller_runners=(
            {}
            if delegated is None
            else {
                delegated:lambda item,z,m:{
                    "status":"COMPLETE",
                    "execution_truth":"IMPLEMENTATION_EXECUTED",
                    "result":{"child_answer":"ok"},
                    "state":{"parent_overwrite":"FORBIDDEN"},
                    "selected_tools":("SHOULD_NOT_ESCAPE",),
                    "terminal":"COMPLETE",
                    "material_delta":True,
                    "evidence":("child:complete",),
                }
            }
        ),
    )


def test_candidate_entry_binding_is_icc128_while_generic_entry_is_still_ic028():
    current=bind_entry_contract(
        "ICC, handle it",
        target="kernel-053",
        job="finish",
        basis="candidate",
    )
    candidate=bind_icc128_entry_contract(
        "ICC, handle it",
        target="kernel-053",
        job="finish",
        basis="candidate",
    )
    assert current.contract.controller=="IC-028"
    assert current.lease.controller=="IC-028"
    assert candidate.contract.controller=="ICC128"
    assert candidate.lease.controller=="ICC128"
    assert "ICC128" in candidate.contract.receipt


def test_packetize_allows_evidence_but_blocks_controller_frontiers_and_selection():
    allowed=validate_packetize_output({
        "selectors":["evidence-only-selector-description"],
        "open":["X"],
        "obligations":[],
    })
    assert allowed["open"]==["X"]

    for key,value in (
        ("question_frontier",[{"id":"q"}]),
        ("work_frontier",[{"id":"w"}]),
        ("selected_work",{"id":"w"}),
        ("selected_tools",["PD"]),
    ):
        try:
            validate_packetize_output({key:value})
        except PacketizeSelectionBlocked as exc:
            assert key in str(exc)
        else:
            raise AssertionError(f"{key} was not blocked")


def test_child_projection_strips_parent_authority_and_preserves_evidence():
    delta=project_child_result(
        "ImprovementCore",
        {
            "status":"COMPLETE",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":{
                "answer":"x",
                "state":{"bad":1},
                "selected_tools":["PD"],
                "terminal":"COMPLETE",
            },
            "state":{"bad":2},
            "terminal":"COMPLETE",
            "material_delta":True,
            "evidence":("child:e1",),
        },
    )
    assert delta["child_status"]=="COMPLETE"
    assert delta["material_result_delta"]
    assert delta["child_evidence"]==("child:e1",)
    assert "state" not in delta["child_result"]
    assert "selected_tools" not in delta["child_result"]
    assert "terminal" not in delta["child_result"]
    assert "terminal" not in delta


def test_current_icc128_adapter_runs_endogenous_loop_without_legacy_loader():
    out=_one_round_adapter()(_packet())
    assert out.status=="COMPLETE"
    assert len(out.traces)==1
    assert len(out.selection_traces)==1
    assert out.selection_traces[0]["selected"]==["w1"]
    assert out.durable_receipts[0]["backend"]=="TAKE5_INLINE"
    assert out.results[0]["result"]["answer"]==42


def test_delegated_controller_cannot_patch_parent_controller_state():
    out=_one_round_adapter(delegated="ImprovementCore")(_packet())
    assert out.status=="COMPLETE"
    delta=out.memory["last_delta"]
    child=delta["child_deltas"][0]
    assert child["child_id"]=="ImprovementCore"
    assert child["child_status"]=="COMPLETE"
    assert "state" not in child["child_result"]
    assert "selected_tools" not in child["child_result"]
    assert "terminal" not in child
    assert "parent_overwrite" not in out.state


def test_durable_backend_receives_already_selected_operation_only():
    calls=[]
    backend=Take5InlineBackend()
    receipt=execute_selected_operation(
        backend,
        episode_id="e1",
        operation_id="generic:w1",
        payload={"id":"w1"},
        invoke=lambda:calls.append("executed") or {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":"ok",
        },
    )
    assert calls==["executed"]
    assert receipt.operation_id=="generic:w1"
    assert receipt.backend=="TAKE5_INLINE"


def test_candidate_entry_surface_has_no_arbitrary_ic_fn_parameter():
    params=inspect.signature(run_icc_053_candidate).parameters
    assert "ic_fn" not in params
    assert "icc128_adapter" in params


@dataclass(frozen=True)
class Cert:
    status:str


@dataclass(frozen=True)
class Closure:
    state:dict
    certificate:Cert


def _assert_observer(target,binding):
    return ToolRunReceipt(
        "ASSERT",True,True,True,True,True,True,{"asserted":True}
    )


def _goal_observer(target,asserted,binding):
    return ToolRunReceipt(
        "GOAL",True,True,True,True,True,True,{"goal":"governing"}
    )


def test_candidate_entry_blocks_old_controller_binding_and_runs_with_icc128_binding():
    old=bind_entry_contract(
        "ICC, handle it",
        target="kernel-053",
        job="finish",
        basis="candidate",
    )
    adapter=_one_round_adapter()
    blocked=run_icc_053_candidate(
        old,
        {"answer":1},
        {},
        assert_observer_fn=_assert_observer,
        goal_observer_fn=_goal_observer,
        observe_fn=lambda s,b:s,
        formalize_fn=lambda o,b:{"m":"fixed"},
        packetize_fn=lambda m,g,s,b:(
            seen_goals.append(g) or {
                "type":"system",
                "scope":"candidate",
                "selectors":[],
                "open":[],
                "obligations":[],
            }
        ),
        icc128_adapter=adapter,
        closure_fn=lambda p,i,a:Closure(dict(p),Cert("CLOSED")),
        update_fn=lambda p,c:c.state,
        jane_update_fn=None,
        result_fn=lambda s:s["answer"],
    )
    assert blocked.status=="BLOCKED"
    assert blocked.blocker=="ICC128_CONTROLLER_BINDING_REQUIRED"

    binding=bind_icc128_entry_contract(
        "ICC, handle it",
        target="kernel-053",
        job="finish-kernel-053",
        basis="candidate",
    )
    seen_goals=[]
    out=run_icc_053_candidate(
        binding,
        {"answer":1},
        {},
        assert_observer_fn=_assert_observer,
        goal_observer_fn=_goal_observer,
        observe_fn=lambda s,b:s,
        formalize_fn=lambda o,b:{"m":"fixed"},
        packetize_fn=lambda m,g,s,b:{
            "type":"system",
            "scope":"candidate",
            "selectors":[],
            "open":[],
            "obligations":[],
        },
        icc128_adapter=adapter,
        closure_fn=lambda p,i,a:Closure(dict(p),Cert("CLOSED")),
        update_fn=lambda p,c:c.state,
        jane_update_fn=None,
        result_fn=lambda s:s["answer"],
    )
    assert out.status=="CLOSED_RELATIVE"
    assert len(out.rounds)==1
    assert seen_goals[0]["governing_goal"]=={"goal":"governing"}


def test_candidate_entry_rejects_packetize_attempt_to_select():
    binding=bind_icc128_entry_contract(
        "ICC, handle it",
        target="kernel-053",
        job="finish-kernel-053",
        basis="candidate",
    )
    out=run_icc_053_candidate(
        binding,
        {"answer":1},
        {},
        assert_observer_fn=_assert_observer,
        goal_observer_fn=_goal_observer,
        observe_fn=lambda s,b:s,
        formalize_fn=lambda o,b:{"m":"fixed"},
        packetize_fn=lambda m,g,s,b:{
            "selected_tools":["PD"],
            "obligations":[],
        },
        icc128_adapter=_one_round_adapter(),
        closure_fn=lambda p,i,a:Closure(dict(p),Cert("CLOSED")),
        update_fn=lambda p,c:c.state,
        jane_update_fn=None,
        result_fn=lambda s:s["answer"],
    )
    assert out.status=="BLOCKED"
    assert "PACKETIZE_SUBSTANTIVE_SELECTION_FORBIDDEN:selected_tools" in out.blocker


def test_target_transform_is_blocked_until_typed_commit_executor_exists():
    calls=[]
    def gq(z,m):
        return [{"id":"q-transform"}]
    def gw(q,z,m):
        return [{
            "id":"w-transform",
            "jobs":(),
            "operation_class":"TRANSFORM",
            "effect_class":"TARGET_TRANSFORM",
            "object_specification":{
                "object_id":"target-x",
                "basis_id":"basis-x",
                "identification_status":"IDENTIFIED",
                "required_coordinates":["content"],
                "resolved_coordinates":["content"],
                "open_coordinates":[],
                "invariant_coordinates":[],
            },
        }]
    adapter=ICC128EpisodeAdapter(
        generate_questions=gq,
        generate_work=gw,
        admit_results=lambda r,z,m:{},
        update_state=lambda z,m,d:(
            {**z,"terminal":"CONTINUE","admitted_continuation":True},
            dict(m),
        ),
        generic_execute=lambda item,z,m:calls.append(item) or {"status":"EXECUTED"},
    )
    out=adapter(_packet())
    assert out.status=="BLOCKED"
    assert calls==[]
    assert out.results[0]["blocker"]=="KERNEL053_TARGET_TRANSFORM_COMMIT_ADAPTER_REQUIRED"
