import sys
sys.path.insert(0,"runtime")

from dataclasses import dataclass

from icc128_entry_binding import ICC128_CONTROLLER
from icc_bootstrap import ToolRunReceipt
from icc_entry import ICC128RuntimeBindings
from icc_host_relay import ICCRelayBindings, ICCRelayRequest, relay_icc128


@dataclass(frozen=True)
class Cert:
    status: str


@dataclass(frozen=True)
class Closure:
    state: dict
    certificate: Cert


def _assert_observer(target,binding):
    return ToolRunReceipt(
        "ASSERT",True,True,True,True,True,True,{"asserted":True}
    )


def _goal_observer(target,asserted,binding):
    return ToolRunReceipt(
        "GOAL",True,True,True,True,True,True,{"goal":"relay-goal"}
    )


def _controller_bindings(response="ICC direct result"):
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
        if response is not None:
            z["icc_user_response"]=response
        m["last_delta"]=d
        return z,m

    def execute(item,z,m):
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":{"ok":True},
            "material_delta":False,
            "evidence":("test:icc-runtime",),
        }

    return ICC128RuntimeBindings(
        generate_questions=gq,
        generate_work=gw,
        admit_results=admit,
        update_controller_state=update,
        generic_execute=execute,
    )


def _bindings(response="ICC direct result", *, fallback=False, mutate_response=None):
    controller=_controller_bindings(response)

    def closure_fn(previous,icc_result,packet):
        state=dict(previous)
        authored=icc_result.state.get("icc_user_response")
        if authored is not None:
            state["icc_user_response"]=authored
        if mutate_response is not None:
            state["icc_user_response"]=mutate_response
        if fallback:
            state["host_fallback_used"]=True
        return Closure(state,Cert("CLOSED"))

    return ICCRelayBindings(
        controller_bindings=controller,
        assert_observer_fn=_assert_observer,
        goal_observer_fn=_goal_observer,
        observe_fn=lambda s,b:s,
        formalize_fn=lambda o,b:{"relay":"fixed"},
        packetize_fn=lambda m,g,s,b:{
            "type":"system",
            "scope":"host-relay",
            "selectors":[],
            "open":[],
            "obligations":[],
        },
        closure_fn=closure_fn,
        update_fn=lambda previous,closure:closure.state,
        jane_update_fn=None,
        result_fn=lambda s:s.get("icc_user_response"),
    )


def test_relay_routes_raw_message_through_canonical_icc128_and_returns_icc_response():
    request=ICCRelayRequest(
        "r1",
        "ICC, handle this",
        ({"role":"user","content":"earlier context"},),
    )
    out=relay_icc128(request,bindings=_bindings("ICC direct result"))
    assert out.status=="COMPLETE"
    assert out.response=="ICC direct result"
    assert out.receipt.controller==ICC128_CONTROLLER
    assert out.receipt.host_fallback_used is False
    assert out.receipt.input_sha256
    assert out.receipt.response_sha256
    assert out.state["user_message"]=="ICC, handle this"
    assert out.state["conversation"][0]["content"]=="earlier context"


def test_relay_blocks_when_icc_runtime_emits_no_user_response():
    request=ICCRelayRequest("r2","do it")
    out=relay_icc128(request,bindings=_bindings(None))
    assert out.status=="BLOCKED"
    assert out.response is None
    assert out.receipt.blocker=="ICC_RELAY_RESPONSE_NOT_AUTHORED_BY_ICC"


def test_relay_blocks_host_rewrite_of_icc_response():
    request=ICCRelayRequest("r3","keep ICC in control")
    out=relay_icc128(
        request,
        bindings=_bindings("ICC result",mutate_response="host rewrite"),
    )
    assert out.status=="BLOCKED"
    assert out.response is None
    assert out.receipt.blocker=="ICC_RELAY_RESPONSE_MUTATED_AFTER_ICC"


def test_relay_blocks_any_host_fallback_substitution():
    request=ICCRelayRequest("r4","run MT")
    out=relay_icc128(request,bindings=_bindings(fallback=True))
    assert out.status=="BLOCKED"
    assert out.response is None
    assert out.receipt.blocker=="ICC_RELAY_HOST_FALLBACK_FORBIDDEN"
    assert out.receipt.host_fallback_used is True
