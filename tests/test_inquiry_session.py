import sys
sys.path.insert(0,"runtime")

from jane import begin_turn
from inquiry_session import run_inquiry_session
from recursive_episode import ClosureResult, RoundResult, Terminal
from tool_run_closure import (
    Consequence,
    ConsumerState,
    Disposition,
    StageResult,
    run_tool_run_closure,
)

def _consequence(name):
    return Consequence(
        referent=name,
        effect_class="SESSION_RESULT",
        target_state="CURRENT",
        authority_scope="LOCAL",
        source_version="v1",
        protected_class="INQUIRY",
    )

def _trc_closure(state,rr):
    kind=rr.value["kind"]
    post={**state,"returned":kind}

    def realize(c,s):
        return StageResult(
            {**s,"closed":tuple(s.get("closed",()))+(c.referent,)},
            status="COMPLETED_UNVERIFIED",
        )

    trc=run_tool_run_closure(
        tool_result=rr.value,
        pre_state=state,
        post_state=post,
        harvest_fn=lambda r,p,s:(_consequence(r["kind"]),),
        disposition_fn=lambda c,s:Disposition.REALIZE,
        realize_fn=realize,
        verify_fn=lambda c,s:StageResult(s,status="VERIFIED"),
        consume_fn=lambda c,s:StageResult(s,status=ConsumerState.CONSUMED.value),
        harvest_basis="session-test",
    )
    cert=trc.certificate
    return ClosureResult(
        cert.status,
        value=trc,
        open_coordinates=cert.open_coordinates+cert.pending_coordinates,
        admit_on_terminal=True,
    )

def _update(state,rr,cr):
    return cr.value.state

def test_original_prompt_runs_observer_preparation_before_hf_session():
    binding=begin_turn(
        "Run the equation on itself, then run Goal and then run Architect.",
        target="the equation",
        job="self-apply",
        basis="current",
        episode_id="equation-session",
    )
    events=[]

    def observe(state):
        events.append("OBSERVE")
        return RoundResult({"kind":"observer"},search_delta=True)

    def reconcile(state,rr):
        events.append("OBSERVE_RECONCILE")
        return RoundResult({"kind":"observer"},search_delta=True)

    def observer_close(state,rr):
        events.append("OBSERVE_TRC")
        return _trc_closure(state,rr)

    def core_round(state):
        events.append("CORE_ROUND")
        assert "observer" in state.get("closed",())
        return RoundResult({"kind":"core"},result_delta=True)

    result=run_inquiry_session(
        binding,
        {},
        observer_fn=observe,
        observer_reconcile_fn=reconcile,
        observer_closure_fn=observer_close,
        round_fn=core_round,
        closure_fn=_trc_closure,
        update_fn=_update,
        terminal_fn=lambda s,r,c:Terminal.RELATIVE_CLOSE,
        max_rounds=3,
    )

    assert result.observer_used
    assert result.observer_closure_status=="CLOSED"
    assert result.receipt.terminal==Terminal.RELATIVE_CLOSE
    assert result.state["closed"]==("observer","core")
    assert events==["OBSERVE","OBSERVE_RECONCILE","OBSERVE_TRC","CORE_ROUND"]

def test_observer_open_is_admitted_and_stops_before_core_session():
    binding=begin_turn(
        "Run ICC in observer mode",
        target="object",
        job="inspect",
        basis="current",
        episode_id="observer-open",
    )
    core_calls=[]

    def observer_open(state,rr):
        return ClosureResult(
            "OPEN",
            value=type("X",(),{"state":{**state,"open":("OBS",)}})(),
            open_coordinates=("OBS",),
            admit_on_terminal=True,
        )

    result=run_inquiry_session(
        binding,
        {},
        observer_fn=lambda s:RoundResult({"kind":"observer"},search_delta=True),
        observer_reconcile_fn=lambda s,r:r,
        observer_closure_fn=observer_open,
        round_fn=lambda s:(core_calls.append(True) or RoundResult({"kind":"core"})),
        closure_fn=_trc_closure,
        update_fn=_update,
        terminal_fn=lambda s,r,c:Terminal.RELATIVE_CLOSE,
    )
    assert result.receipt.terminal==Terminal.OPEN
    assert result.state["open"]==("OBS",)
    assert not core_calls
