"""External evidence/tool acquisition policy for ImprovementCore.

ImprovementCore must not default to expensive internal reconstruction when a
live outside source/tool can reduce uncertainty or execution cost.

This module is host-agnostic.  Hosts expose outside capabilities as named
adapters.  The policy decides whether to use them, continue internally, or
leave a typed OPEN gap.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Mapping

class ExternalDisposition(str, Enum):
    NOT_NEEDED="NOT_NEEDED"
    ACQUIRE="ACQUIRE"
    OPEN_GAP="OPEN_GAP"

@dataclass(frozen=True)
class ExternalAcquisitionDecision:
    disposition: ExternalDisposition
    preferred: tuple[str,...]
    reasons: tuple[str,...]
    allow_internal_fallback: bool
    expected_value: float

@dataclass(frozen=True)
class ExternalAcquisitionReceipt:
    decision: ExternalAcquisitionDecision
    used: tuple[str,...]
    outputs: tuple[dict,...]
    unresolved: tuple[str,...]

# High-value source order.  A host may bind any subset.
DEFAULT_PRIORITY=(
    "connected_sources",
    "repository_research",
    "web_search",
    "external_tools",
)

EXTERNAL_SIGNAL_KEYS={
    "external_dependency",
    "currentness_unknown",
    "fresh_information_required",
    "outside_evidence_required",
    "prior_art_required",
    "literature_required",
    "research_needed",
    "external_tool_candidate",
    "tool_gap",
    "unknown_external_fact",
}

def _truthy_signals(state:Any)->tuple[str,...]:
    if not isinstance(state,dict):
        return ()
    found=[]
    for key in EXTERNAL_SIGNAL_KEYS:
        if state.get(key):
            found.append(key)
    tags=set(state.get("tags",()) or ())
    if {"external_dependency","novelty","prior_art","stale_version","currentness"} & tags:
        found.extend(sorted({"tag:"+x for x in tags & {"external_dependency","novelty","prior_art","stale_version","currentness"}}))
    return tuple(sorted(set(found)))

def decide_external_acquisition(
    state:Any,
    *,
    available:tuple[str,...]=(),
    force_external:bool=False,
    allow_gap:bool=True,
    internal_cost:float=1.0,
    external_cost:float=0.25,
    uncertainty_reduction:float=1.0,
)->ExternalAcquisitionDecision:
    """Choose external acquisition only when it has material expected value.

    expected_value > 0 means expected uncertainty/cost gain from outside
    acquisition exceeds its acquisition cost.
    """
    signals=_truthy_signals(state)
    needed=force_external or bool(signals)
    if not needed:
        return ExternalAcquisitionDecision(
            ExternalDisposition.NOT_NEEDED,(),(),True,0.0
        )

    preferred=tuple(x for x in DEFAULT_PRIORITY if x in set(available))
    ev=float(uncertainty_reduction + internal_cost - external_cost)

    if preferred and ev>0:
        return ExternalAcquisitionDecision(
            ExternalDisposition.ACQUIRE,
            preferred,
            signals or ("forced_external",),
            False,
            ev,
        )

    if allow_gap:
        return ExternalAcquisitionDecision(
            ExternalDisposition.OPEN_GAP,
            preferred,
            signals or ("forced_external",),
            False,
            ev,
        )

    return ExternalAcquisitionDecision(
        ExternalDisposition.NOT_NEEDED,
        (),
        signals or ("forced_external",),
        True,
        ev,
    )

def acquire_external(
    state:Any,
    adapters:Mapping[str,Callable[[Any],dict]]|None,
    *,
    force_external:bool=False,
    allow_gap:bool=True,
)->ExternalAcquisitionReceipt:
    adapters=dict(adapters or {})
    decision=decide_external_acquisition(
        state,
        available=tuple(adapters),
        force_external=force_external,
        allow_gap=allow_gap,
    )
    if decision.disposition!=ExternalDisposition.ACQUIRE:
        unresolved=decision.reasons if decision.disposition==ExternalDisposition.OPEN_GAP else ()
        return ExternalAcquisitionReceipt(decision,(),(),tuple(unresolved))

    used=[]
    outputs=[]
    unresolved=[]
    for name in decision.preferred:
        fn=adapters.get(name)
        if fn is None:
            continue
        out=fn(state)
        used.append(name)
        if isinstance(out,dict):
            outputs.append(out)
            if out.get("status") in {"OPEN","BLOCKED","CONFLICT"}:
                unresolved.append(f"{name}:{out.get('status')}")
            # Stop early once an adapter explicitly certifies that the outside
            # information need is satisfied.  This avoids tool-smash.
            if out.get("external_need_satisfied"):
                break
        else:
            outputs.append({"value":out})
    if not used:
        unresolved.extend(decision.reasons)

    return ExternalAcquisitionReceipt(
        decision,
        tuple(used),
        tuple(outputs),
        tuple(unresolved),
    )

def merge_external_outputs(state:Any, receipt:ExternalAcquisitionReceipt):
    if not isinstance(state,dict):
        return state
    out=dict(state)
    out["external_acquisition_receipt"]={
        "disposition":receipt.decision.disposition.value,
        "preferred":receipt.decision.preferred,
        "reasons":receipt.decision.reasons,
        "expected_value":receipt.decision.expected_value,
        "used":receipt.used,
        "unresolved":receipt.unresolved,
    }
    evidence=list(out.get("external_evidence",()) or ())
    for item in receipt.outputs:
        evidence.append(item)
    out["external_evidence"]=tuple(evidence)
    return out
