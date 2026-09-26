import sys
sys.path.insert(0,"runtime")

from dataclasses import dataclass
from jane import begin_turn
from math_first_wrapper import run_math_first_wrapper
from icc_bootstrap import ICCBootstrapReceipt, ToolRunReceipt


@dataclass(frozen=True)
class Cert:
    status:str


@dataclass(frozen=True)
class Closure:
    state:dict
    certificate:Cert


def _bootstrap(state,binding):
    a=ToolRunReceipt("ASSERT",True,True,True,True,True,True,{"asserted":True})
    g=ToolRunReceipt("GOAL",True,True,True,True,True,True,{"goal":"observed"})
    return ICCBootstrapReceipt(a,g,True,("ASSERT_OBSERVER","GOAL_OBSERVER"))


def test_unfamiliar_recursive_holdout_reobserves_until_answer_fixed_point():
    binding=begin_turn(
        "IC solve the unfamiliar case in observer mode",
        target="holdout-object",
        job="solve-holdout",
        basis="holdout",
        authority=frozenset(),
        episode_id="holdout-wrapper",
    )
    observations=[]

    def observe(state,b):
        observations.append((state["evidence"],state["answer"]))
        return dict(state)

    def formalize(obs,b):
        return {"need":2,"have":obs["evidence"],"answer":obs["answer"]}

    def architect(math,goal,state,b):
        return {
            "type":"holdout",
            "scope":"local",
            "readings":[],
            "result_sensitive":["answer"],
            "selectors":[],
            "provenance":[],
            "open":[],
            "obligations":[],
        }

    def closure(pre,ic_result,packet):
        nxt=dict(pre)
        if nxt["evidence"] < 2:
            nxt["evidence"] += 1
        elif nxt["answer"] is None:
            nxt["answer"]="SOLVED"
        return Closure(nxt,Cert("CLOSED"))

    out=run_math_first_wrapper(
        binding,
        {"evidence":0,"answer":None},
        {},
        bootstrap_fn=_bootstrap,
        observe_fn=observe,
        formalize_fn=formalize,
        goal_fn=lambda math,b:"produce-answer",
        architect_fn=architect,
        ic_fn=lambda packet:dict(packet),
        closure_fn=closure,
        update_fn=lambda pre,c:c.state,
        jane_update_fn=None,
        result_fn=lambda s:s["answer"],
        reentry_fn=lambda pre,post,delta,frozen,closure:delta.material,
        max_rounds=6,
    )

    assert out.status=="CLOSED_RELATIVE"
    assert out.state=={"evidence":2,"answer":"SOLVED"}
    assert len(observations)==4
    assert observations[0]==(0,None)
    assert observations[-1]==(2,"SOLVED")
    assert out.rounds[-1].result_stable
    assert not out.rounds[-1].reentry
