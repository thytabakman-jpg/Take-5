import sys
sys.path.insert(0,"runtime")

from dataclasses import dataclass

from jane import begin_turn
from jane_supervisor import JaneSupervisoryState
from math_first_wrapper import run_math_first_wrapper
from representation_discovery import DiscoveryDelta


@dataclass(frozen=True)
class Cert:
    status:str


@dataclass(frozen=True)
class Closure:
    state:dict
    certificate:Cert


@dataclass(frozen=True)
class DiscoveryClosure:
    state:dict
    certificate:Cert
    discovery_delta:DiscoveryDelta


def _binding():
    return begin_turn(
        "IC use observer mode and solve this",
        target="wrapper",
        job="finish-wrapper",
        basis="current",
        authority=frozenset(),
        episode_id="math-wrapper-test",
    )


def test_math_first_order_and_external_job_protection():
    calls=[]
    binding=_binding()

    def observe(state,b):
        calls.append("OBSERVE")
        return {"seen":state["x"]}

    def formalize(observation,b):
        calls.append("FORMALIZE")
        return {"equation":"m","seen":observation["seen"]}

    def goal(math,b):
        calls.append("GOAL")
        return "operational"

    def architect(math,goal,state,b):
        calls.append("ARCHITECT")
        return {
            "type":"system",
            "scope":"local",
            "readings":[],
            "result_sensitive":[],
            "selectors":[],
            "provenance":[],
            "open":[],
            "obligations":[],
        }

    captured={}
    def ic(packet):
        calls.append("IC")
        captured.update(packet)
        return dict(packet)

    def close(pre,ic_result,packet):
        calls.append("CLOSURE")
        return Closure(dict(pre),Cert("CLOSED"))

    def update(pre,closure):
        calls.append("UPDATE")
        return closure.state

    out=run_math_first_wrapper(
        binding,
        {"x":1},
        JaneSupervisoryState(),
        observe_fn=observe,
        formalize_fn=formalize,
        goal_fn=goal,
        architect_fn=architect,
        ic_fn=ic,
        closure_fn=close,
        update_fn=update,
        jane_update_fn=None,
        result_fn=lambda s:s["x"],
    )

    assert out.status=="CLOSED_RELATIVE"
    assert calls==["OBSERVE","FORMALIZE","GOAL","ARCHITECT","IC","CLOSURE","UPDATE"]
    assert captured["job"]=="finish-wrapper"
    assert captured["external_job"]=="finish-wrapper"
    assert captured["operational_goal"]=="operational"
    assert captured["identity"]=="wrapper"


def test_frozen_math_mutation_is_blocked_before_admission():
    binding=_binding()

    def ic(packet):
        packet=dict(packet)
        packet["frozen_math"]={"equation":"changed"}
        return packet

    out=run_math_first_wrapper(
        binding,
        {"answer":0},
        {},
        observe_fn=lambda s,b:s,
        formalize_fn=lambda o,b:{"equation":"fixed"},
        goal_fn=lambda m,b:"g",
        architect_fn=lambda m,g,s,b:{
            "type":"system","scope":"local","readings":[],"result_sensitive":[],
            "selectors":[],"provenance":[],"open":[],"obligations":[],
        },
        ic_fn=ic,
        closure_fn=lambda p,i,a:Closure(p,Cert("CLOSED")),
        update_fn=lambda p,c:c.state,
        jane_update_fn=None,
        result_fn=lambda s:s["answer"],
    )
    assert out.status=="BLOCKED"
    assert out.blocker=="FROZEN_MATH_MUTATION"


def test_open_closure_is_preserved_as_nonclosure():
    binding=_binding()
    out=run_math_first_wrapper(
        binding,
        {"answer":0},
        {},
        observe_fn=lambda s,b:s,
        formalize_fn=lambda o,b:{"m":1},
        goal_fn=lambda m,b:"g",
        architect_fn=lambda m,g,s,b:{
            "type":"system","scope":"local","readings":[],"result_sensitive":[],
            "selectors":[],"provenance":[],"open":[],"obligations":[],
        },
        ic_fn=lambda p:dict(p),
        closure_fn=lambda p,i,a:Closure({**p,"open":("X",)},Cert("OPEN")),
        update_fn=lambda p,c:c.state,
        jane_update_fn=None,
        result_fn=lambda s:s["answer"],
    )
    assert out.status=="OPEN"
    assert out.state["open"]==("X",)


def test_jane_sync_runs_only_for_supervisory_relevant_admitted_delta():
    binding=_binding()

    def close(pre,ic_result,packet):
        return Closure({**pre,"provenance":"v2"},Cert("CLOSED"))

    def update_jane(jane_state,delta):
        x=dict(jane_state)
        x["syncs"]=x.get("syncs",0)+1
        x["changed"]=delta.changed
        return x

    out=run_math_first_wrapper(
        binding,
        {"answer":1,"provenance":"v1"},
        {"syncs":0},
        observe_fn=lambda s,b:s,
        formalize_fn=lambda o,b:{"m":1},
        goal_fn=lambda m,b:"g",
        architect_fn=lambda m,g,s,b:{
            "type":"system","scope":"local","readings":[],"result_sensitive":[],
            "selectors":[],"provenance":[],"open":[],"obligations":[],
        },
        ic_fn=lambda p:dict(p),
        closure_fn=close,
        update_fn=lambda p,c:c.state,
        jane_update_fn=update_jane,
        result_fn=lambda s:s["answer"],
        reentry_fn=lambda *args:False,
    )
    assert out.status=="CLOSED_RELATIVE"
    assert out.jane_state["syncs"]==1
    assert "provenance" in out.jane_state["changed"]
    assert out.rounds[0].jane_synced


def test_take_two_discovery_delta_reenters_without_world_state_change():
    """A new view/candidate cannot be mistaken for closure just because state is stable."""
    binding=_binding()
    rounds={"n":0}

    def close(pre,ic_result,packet):
        rounds["n"] += 1
        material = rounds["n"] == 1
        return DiscoveryClosure(
            dict(pre),
            Cert("CLOSED"),
            DiscoveryDelta(
                view_changed=material,
                candidate_universe_changed=material,
            ),
        )

    out=run_math_first_wrapper(
        binding,
        {"answer":"same"},
        {},
        observe_fn=lambda s,b:s,
        formalize_fn=lambda o,b:{"m":"same"},
        goal_fn=lambda m,b:"g",
        architect_fn=lambda m,g,s,b:{
            "type":"system","scope":"local","readings":[],"result_sensitive":[],
            "selectors":[],"provenance":[],"open":[],"obligations":[],
        },
        ic_fn=lambda p:dict(p),
        closure_fn=close,
        update_fn=lambda p,c:c.state,
        jane_update_fn=None,
        result_fn=lambda s:s["answer"],
    )

    assert out.status=="CLOSED_RELATIVE"
    assert len(out.rounds)==2
    assert out.rounds[0].result_stable
    assert out.rounds[0].discovery_material
    assert out.rounds[0].reentry
    assert not out.rounds[1].discovery_material
    assert not out.rounds[1].reentry
