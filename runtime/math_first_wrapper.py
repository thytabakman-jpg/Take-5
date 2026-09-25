"""Greenfield math-first wrapper around protected Jane + Improvement Core.

Control equation:

    beta = JaneBind(u)
    o    = Observe_beta(z)
    m    = Formalize(o, beta)
    mbar = Freeze(m)
    g    = Goal(mbar, beta)
    a    = Architect(mbar, g, z, beta)
    y    = IC(a, z)
    c    = ToolRunClosure(z, y)
    z'   = AdmitUpdate(z, c)
    j'   = JaneSync(j, delta(z,z'))
    reenter until relative fixed point / OPEN / BLOCKED / budget

IC and Jane remain suboperators.  This module owns ordering, frozen-math
integrity, admission boundary, Jane synchronization, and wrapper termination.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, is_dataclass
from hashlib import sha256
import json
from typing import Any, Callable, Mapping

from entry_contract import EntryBinding, entry_is_bound
from jane_relevance import is_supervisory_relevant
from jane_sync import jane_sync


@dataclass(frozen=True)
class FrozenMath:
    value: Any
    fingerprint: str


@dataclass(frozen=True)
class StateDelta:
    changed: tuple[str, ...]
    material: bool
    before_fingerprint: str
    after_fingerprint: str


@dataclass(frozen=True)
class WrapperRound:
    index: int
    math_fingerprint: str
    closure_status: str
    changed: tuple[str, ...]
    jane_synced: bool
    reentry: bool
    result_stable: bool
    discovery_material: bool = False


@dataclass(frozen=True)
class MathFirstResult:
    state: Any
    jane_state: Any
    status: str
    rounds: tuple[WrapperRound, ...]
    blocker: str | None = None


def _canonical(value: Any):
    if is_dataclass(value):
        return _canonical(asdict(value))
    if isinstance(value, Mapping):
        return {
            str(k): _canonical(v)
            for k, v in sorted(value.items(), key=lambda kv: str(kv[0]))
        }
    if isinstance(value, (list, tuple)):
        return [_canonical(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_canonical(v) for v in value), key=repr)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return {"__repr__": repr(value), "__type__": type(value).__qualname__}


def fingerprint(value: Any) -> str:
    payload = json.dumps(
        _canonical(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return sha256(payload).hexdigest()


def freeze_math(value: Any) -> FrozenMath:
    frozen = deepcopy(value)
    return FrozenMath(frozen, fingerprint(frozen))


def infer_delta(before: Any, after: Any) -> StateDelta:
    before_fp = fingerprint(before)
    after_fp = fingerprint(after)
    if isinstance(before, Mapping) and isinstance(after, Mapping):
        keys = sorted(set(before) | set(after), key=str)
        changed = tuple(
            str(k) for k in keys
            if fingerprint(before.get(k)) != fingerprint(after.get(k))
        )
    else:
        changed = () if before_fp == after_fp else ("STATE",)
    return StateDelta(changed, before_fp != after_fp, before_fp, after_fp)


def _closure_status(closure: Any) -> str:
    certificate = getattr(closure, "certificate", None)
    if certificate is not None and getattr(certificate, "status", None):
        return str(certificate.status)
    if isinstance(closure, Mapping) and closure.get("status") is not None:
        return str(closure["status"])
    status = getattr(closure, "status", None)
    if status is not None:
        return str(status)
    raise RuntimeError("CLOSURE_STATUS_UNAVAILABLE")


def _closure_discovery_material(closure: Any) -> bool:
    """Return whether closure exposed a continuation-relevant discovery delta.

    The closure may carry a DiscoveryDelta object or a mapping.  This keeps the
    wrapper generic while protecting Take-Two-style reentry when representation,
    views, question frontier, candidate universe, relations, evidence/authority,
    or runtime reality change without a world-state mutation.
    """
    delta = getattr(closure, "discovery_delta", None)
    if delta is None and isinstance(closure, Mapping):
        delta = closure.get("discovery_delta")
    if delta is None:
        return False

    material = getattr(delta, "material", None)
    if material is not None:
        return bool(material)

    if isinstance(delta, Mapping):
        if "material" in delta:
            return bool(delta["material"])
        keys = (
            "state_changed",
            "view_changed",
            "question_frontier_changed",
            "candidate_universe_changed",
            "relation_changed",
            "authority_or_evidence_changed",
            "runtime_reality_changed",
        )
        return any(bool(delta.get(key)) for key in keys)

    return bool(delta)


def _ic_final_packet(ic_result: Any):
    packet = getattr(ic_result, "final_packet", None)
    if packet is not None:
        return packet
    if isinstance(ic_result, Mapping):
        if isinstance(ic_result.get("final_packet"), Mapping):
            return ic_result["final_packet"]
        return ic_result
    return None


def _prepare_packet(packet, frozen: FrozenMath, goal: Any, binding: EntryBinding):
    if not isinstance(packet, Mapping):
        raise TypeError("architect_fn must return a mapping")
    out = dict(packet)

    external_job = str(binding.lease.job)
    external_target = str(binding.contract.frozen_target)

    if "job" in out and str(out["job"]) != external_job:
        raise RuntimeError("ARCHITECT_EXTERNAL_JOB_DRIFT")
    if "identity" in out and str(out["identity"]) != external_target:
        raise RuntimeError("ARCHITECT_TARGET_DRIFT")

    requested_authority = frozenset(out.get("authority", binding.contract.authority))
    if not requested_authority <= binding.contract.authority:
        raise RuntimeError("ARCHITECT_AUTHORITY_ESCALATION")

    out["job"] = external_job
    out["identity"] = external_target
    out["authority"] = tuple(sorted(binding.contract.authority))
    out.setdefault("local_authority", out["authority"])
    out["external_job"] = external_job
    out["frozen_target"] = external_target
    out["operational_goal"] = goal
    out["frozen_math"] = deepcopy(frozen.value)
    out["frozen_math_fingerprint"] = frozen.fingerprint
    return out


def run_math_first_wrapper(
    binding: EntryBinding,
    initial_state: Any,
    initial_jane_state: Any,
    *,
    observe_fn: Callable[[Any, EntryBinding], Any],
    formalize_fn: Callable[[Any, EntryBinding], Any],
    goal_fn: Callable[[Any, EntryBinding], Any],
    architect_fn: Callable[[Any, Any, Any, EntryBinding], Mapping[str, Any]],
    ic_fn: Callable[[Mapping[str, Any]], Any],
    closure_fn: Callable[[Any, Any, Mapping[str, Any]], Any],
    update_fn: Callable[[Any, Any], Any],
    jane_update_fn: Callable[[Any, StateDelta], Any] | None,
    result_fn: Callable[[Any], Any],
    reentry_fn: Callable[[Any, Any, StateDelta, FrozenMath, Any], bool] | None = None,
    relevance_fn: Callable[..., bool] = is_supervisory_relevant,
    result_equivalent_fn: Callable[[Any, Any], bool] | None = None,
    max_rounds: int = 16,
) -> MathFirstResult:
    """Execute the math-first wrapper while preserving IC/Jane role boundaries."""
    if not entry_is_bound(binding):
        return MathFirstResult(initial_state, initial_jane_state, "BLOCKED", (), "ENTRY_CONTRACT_REQUIRED")

    equivalent = result_equivalent_fn or (lambda a, b: a == b)
    state = deepcopy(initial_state)
    jane_state = deepcopy(initial_jane_state)
    receipts: list[WrapperRound] = []

    for index in range(1, max_rounds + 1):
        pre_state = deepcopy(state)

        # Observer receives a copy: it cannot mutate the live state by reference.
        observation = observe_fn(deepcopy(state), binding)
        mathematical_object = formalize_fn(observation, binding)
        frozen = freeze_math(mathematical_object)
        goal = goal_fn(deepcopy(frozen.value), binding)

        try:
            packet = _prepare_packet(
                architect_fn(deepcopy(frozen.value), goal, deepcopy(state), binding),
                frozen,
                goal,
                binding,
            )
        except (RuntimeError, TypeError) as exc:
            return MathFirstResult(state, jane_state, "BLOCKED", tuple(receipts), str(exc))

        ic_result = ic_fn(packet)
        ic_packet = _ic_final_packet(ic_result)
        if ic_packet is None:
            return MathFirstResult(state, jane_state, "BLOCKED", tuple(receipts), "IC_STATE_UNAVAILABLE")

        observed_math_fp = ic_packet.get("frozen_math_fingerprint")
        actual_math_fp = fingerprint(ic_packet.get("frozen_math"))
        if observed_math_fp != frozen.fingerprint or actual_math_fp != frozen.fingerprint:
            return MathFirstResult(state, jane_state, "BLOCKED", tuple(receipts), "FROZEN_MATH_MUTATION")

        closure = closure_fn(pre_state, ic_result, packet)
        closure_status = _closure_status(closure)
        state = update_fn(pre_state, closure)
        delta = infer_delta(pre_state, state)
        discovery_material = _closure_discovery_material(closure)

        relevance = bool(
            relevance_fn(delta, frozen_math=frozen, entry_binding=binding)
        )
        synced = False
        if delta.material and relevance and jane_update_fn is not None:
            def _update_jane(d):
                nonlocal jane_state
                jane_state = jane_update_fn(jane_state, d)
            sync_receipt = jane_sync(
                material=True,
                supervisory_relevant=True,
                update=_update_jane,
                delta=delta,
            )
            synced = bool(sync_receipt.synced)

        before_result = result_fn(pre_state)
        after_result = result_fn(state)
        result_stable = bool(equivalent(before_result, after_result))

        if closure_status in {"OPEN", "BLOCKED"}:
            receipts.append(
                WrapperRound(
                    index, frozen.fingerprint, closure_status, delta.changed,
                    synced, False, result_stable, discovery_material,
                )
            )
            return MathFirstResult(state, jane_state, closure_status, tuple(receipts))

        if closure_status not in {"CLOSED", "RELATIVE_CLOSED", "CLOSED_RELATIVE"}:
            receipts.append(
                WrapperRound(
                    index, frozen.fingerprint, closure_status, delta.changed,
                    synced, False, result_stable, discovery_material,
                )
            )
            return MathFirstResult(state, jane_state, "BLOCKED", tuple(receipts), "UNSUPPORTED_CLOSURE_STATUS")

        needs_reentry = (
            reentry_fn(pre_state, state, delta, frozen, closure)
            if reentry_fn is not None
            else delta.material
        )
        needs_reentry = bool(needs_reentry or discovery_material)

        receipts.append(
            WrapperRound(
                index,
                frozen.fingerprint,
                closure_status,
                delta.changed,
                synced,
                bool(needs_reentry),
                result_stable,
                discovery_material,
            )
        )

        if result_stable and not needs_reentry:
            return MathFirstResult(state, jane_state, "CLOSED_RELATIVE", tuple(receipts))

    return MathFirstResult(state, jane_state, "OPEN", tuple(receipts), "MAX_ROUNDS")
