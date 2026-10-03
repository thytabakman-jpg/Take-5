"""Fail-closed host relay for canonical ICC128.

This module gives an external chat host a transport-only surface:

    user message -> canonical ICC128 runtime -> ICC-authored response -> host

The relay performs no semantic interpretation, tool substitution, answer drafting,
or fallback reasoning. Any missing canonical runtime binding, OPEN/BLOCKED
controller state, or absent ICC-authored response is returned as OPEN/BLOCKED.

A host using this surface may transport the final response string unchanged.
It may not replace a failed ICC run with host reasoning while still claiming an
ICC response.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Callable, Mapping

from icc128_entry_binding import bind_icc128_entry_contract
from icc_entry import ICC128RuntimeBindings, run_icc


ICC_RELAY_BASIS = "ICC128_HOST_RELAY_V1"
ICC_RESPONSE_FIELD = "icc_user_response"


@dataclass(frozen=True)
class ICCRelayRequest:
    request_id: str
    message: str
    conversation: tuple[Mapping[str, Any], ...] = ()


@dataclass(frozen=True)
class ICCRelayBindings:
    controller_bindings: ICC128RuntimeBindings
    assert_observer_fn: Callable
    goal_observer_fn: Callable
    observe_fn: Callable
    formalize_fn: Callable
    packetize_fn: Callable
    closure_fn: Callable
    update_fn: Callable
    jane_update_fn: Callable | None
    result_fn: Callable
    reentry_fn: Callable | None = None
    relevance_fn: Callable | None = None
    result_equivalent_fn: Callable | None = None
    max_rounds: int = 16


@dataclass(frozen=True)
class ICCRelayReceipt:
    request_id: str
    controller: str
    basis: str
    input_sha256: str
    response_sha256: str | None
    runtime_status: str
    relay_status: str
    blocker: str | None
    host_fallback_used: bool = False


@dataclass(frozen=True)
class ICCRelayResult:
    status: str
    response: str | None
    receipt: ICCRelayReceipt
    state: Any


def _request_hash(request: ICCRelayRequest) -> str:
    payload = {
        "request_id": str(request.request_id),
        "message": str(request.message),
        "conversation": list(request.conversation),
    }
    raw = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str,
    ).encode("utf-8")
    return sha256(raw).hexdigest()


def _response_hash(response: str | None) -> str | None:
    if response is None:
        return None
    return sha256(response.encode("utf-8")).hexdigest()


def _extract_icc_response(state: Any) -> str | None:
    if not isinstance(state, Mapping):
        return None
    value = state.get(ICC_RESPONSE_FIELD)
    if value is None:
        return None
    if not isinstance(value, str):
        raise TypeError("ICC_RELAY_RESPONSE_MUST_BE_STRING")
    return value


def _blocked_result(
    request: ICCRelayRequest,
    input_sha: str,
    runtime_status: str,
    blocker: str,
    state: Any,
    *,
    host_fallback_used: bool = False,
) -> ICCRelayResult:
    receipt = ICCRelayReceipt(
        request.request_id,
        "ICC128",
        ICC_RELAY_BASIS,
        input_sha,
        None,
        runtime_status,
        "BLOCKED",
        blocker,
        host_fallback_used,
    )
    return ICCRelayResult("BLOCKED", None, receipt, state)


def relay_icc128(
    request: ICCRelayRequest,
    *,
    bindings: ICCRelayBindings,
    authority=frozenset(),
    boundary: str | None = "HOST_RELAY",
) -> ICCRelayResult:
    """Transport one request through the canonical ICC128 entry surface.

    The relay itself never generates candidate goals, questions, work, tool
    results, or prose. Those remain inside the canonical ICC runtime bindings.

    The user-visible response must already exist in the ICC128 controller result
    before closure/update callbacks can project it back to the host. This makes a
    host-injected answer detectable and fail-closed.
    """
    if not isinstance(request, ICCRelayRequest):
        raise TypeError("ICC_RELAY_REQUEST_REQUIRED")
    if not isinstance(bindings, ICCRelayBindings):
        raise TypeError("ICC_RELAY_BINDINGS_REQUIRED")
    if not request.request_id:
        raise ValueError("ICC_RELAY_REQUEST_ID_REQUIRED")

    input_sha = _request_hash(request)
    binding = bind_icc128_entry_contract(
        request.message,
        target=f"conversation:{request.request_id}",
        job="GOVERN_USER_REQUEST",
        basis=ICC_RELAY_BASIS,
        authority=frozenset(authority),
        boundary=boundary,
        episode_id=f"icc-host-relay:{request.request_id}",
    )

    initial_state = {
        "request_id": request.request_id,
        "user_message": request.message,
        "conversation": tuple(dict(x) for x in request.conversation),
        "relay_input_sha256": input_sha,
        "host_fallback_used": False,
    }

    authored = {"seen": False, "response": None}

    def closure_with_authorship(previous, icc_result, packet):
        controller_state = getattr(icc_result, "state", None)
        response = _extract_icc_response(controller_state)
        if response is not None:
            authored["seen"] = True
            authored["response"] = response
        return bindings.closure_fn(previous, icc_result, packet)

    out = run_icc(
        binding,
        initial_state,
        {},
        controller_bindings=bindings.controller_bindings,
        assert_observer_fn=bindings.assert_observer_fn,
        goal_observer_fn=bindings.goal_observer_fn,
        observe_fn=bindings.observe_fn,
        formalize_fn=bindings.formalize_fn,
        packetize_fn=bindings.packetize_fn,
        closure_fn=closure_with_authorship,
        update_fn=bindings.update_fn,
        jane_update_fn=bindings.jane_update_fn,
        result_fn=bindings.result_fn,
        reentry_fn=bindings.reentry_fn,
        relevance_fn=bindings.relevance_fn,
        result_equivalent_fn=bindings.result_equivalent_fn,
        max_rounds=int(bindings.max_rounds),
    )

    runtime_status = str(out.status)
    blocker = out.blocker
    state = out.state

    if isinstance(state, Mapping) and bool(state.get("host_fallback_used", False)):
        return _blocked_result(
            request,
            input_sha,
            runtime_status,
            "ICC_RELAY_HOST_FALLBACK_FORBIDDEN",
            state,
            host_fallback_used=True,
        )

    response = _extract_icc_response(state)
    closed = runtime_status in {"COMPLETE", "CLOSED", "CLOSED_RELATIVE", "RELATIVE_CLOSE"}

    if not closed:
        status = runtime_status if runtime_status in {"OPEN", "BLOCKED", "CONFLICT"} else "OPEN"
        receipt = ICCRelayReceipt(
            request.request_id,
            "ICC128",
            ICC_RELAY_BASIS,
            input_sha,
            None,
            runtime_status,
            status,
            blocker or f"ICC_RELAY_RUNTIME_{runtime_status}",
            False,
        )
        return ICCRelayResult(status, None, receipt, state)

    if not authored["seen"]:
        return _blocked_result(
            request,
            input_sha,
            runtime_status,
            "ICC_RELAY_RESPONSE_NOT_AUTHORED_BY_ICC",
            state,
        )

    if response != authored["response"]:
        return _blocked_result(
            request,
            input_sha,
            runtime_status,
            "ICC_RELAY_RESPONSE_MUTATED_AFTER_ICC",
            state,
        )

    receipt = ICCRelayReceipt(
        request.request_id,
        "ICC128",
        ICC_RELAY_BASIS,
        input_sha,
        _response_hash(response),
        runtime_status,
        "COMPLETE",
        None,
        False,
    )
    return ICCRelayResult("COMPLETE", response, receipt, state)
