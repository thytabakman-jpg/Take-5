"""Mandatory post-run self-improvement pass for ImprovementCore.

Every governed ImprovementCore episode gets exactly one after-run learning pass.
The pass always updates the improvement frontier and learning memory.  It may
propose a structural successor, but it cannot self-promote one without an
explicit strict-gain evaluator and optional authorized applier.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Callable
import hashlib
import json

from improvement_core_learning_memory import LearningMemory

TERMINAL_GAIN={"COMPLETE","RELATIVE_CLOSE","CLOSED_RELATIVE"}
TERMINAL_GAP={"OPEN","BLOCKED","CONFLICT","RESOURCE_STOP"}

@dataclass(frozen=True)
class AfterRunObservation:
    episode_id:str
    basis_id:str
    status:str
    blocker:str|None
    material_signals:tuple[str,...]
    protected_gain:bool
    unresolved:tuple[str,...]
    evidence:dict[str,Any]

@dataclass(frozen=True)
class SelfImprovementCandidate:
    candidate_id:str
    target:str
    reason:str
    dependency_footprint:frozenset[str]
    expected_gain:str
    evidence:dict[str,Any]

@dataclass(frozen=True)
class AfterRunReceipt:
    tool_id:str
    observation:AfterRunObservation
    candidate:SelfImprovementCandidate|None
    disposition:str
    applied:bool
    learning_recorded:bool
    next_frontier:tuple[str,...]
    open:tuple[str,...]

def _stable_id(payload:dict[str,Any])->str:
    raw=json.dumps(payload,sort_keys=True,default=str,separators=(",",":")).encode()
    return hashlib.sha256(raw).hexdigest()[:16]

def _signals(state:Any)->tuple[str,...]:
    if not isinstance(state,dict):
        return ()
    keys=(
        "live_continuation","unmapped_questions","open","blocked","conflict",
        "learning_events","external_acquisition_receipt","material_delta",
        "changed_coordinates","invalidated_dependencies",
    )
    return tuple(k for k in keys if state.get(k))

def observe_after_run(*, episode_id:str, basis_id:str, status:str,
                      blocker:str|None, state:Any,
                      recursive_result:dict|None=None)->AfterRunObservation:
    recursive_result=recursive_result or {}
    unresolved=[]
    if blocker:
        unresolved.append(str(blocker))
    if isinstance(state,dict):
        for key in ("open","blocked","conflict","unmapped_questions"):
            value=state.get(key)
            if value:
                if isinstance(value,(list,tuple,set)):
                    unresolved.extend(str(x) for x in value)
                else:
                    unresolved.append(f"{key}:{value}")
    if recursive_result.get("open"):
        unresolved.extend(str(x) for x in recursive_result["open"])

    sig=_signals(state)
    protected_gain=status in TERMINAL_GAIN and not unresolved
    return AfterRunObservation(
        episode_id=episode_id,
        basis_id=basis_id,
        status=status,
        blocker=blocker,
        material_signals=sig,
        protected_gain=protected_gain,
        unresolved=tuple(dict.fromkeys(unresolved)),
        evidence={
            "recursive_status":recursive_result.get("status"),
            "recursive_blocker":recursive_result.get("blocker"),
            "state_type":type(state).__name__,
        },
    )

def generate_candidate(obs:AfterRunObservation)->SelfImprovementCandidate|None:
    """Generate a self-improvement target only from an actual residual or lesson."""
    if obs.unresolved:
        target="remove_residual_blocker"
        reason="; ".join(obs.unresolved[:4])
        deps=frozenset({"routing","capability_binding","currentness","evidence"})
        gain="close a previously live blocker without losing protected behavior"
    elif obs.status not in TERMINAL_GAIN:
        target="improve_episode_closure"
        reason=f"episode ended {obs.status}"
        deps=frozenset({"closure","reentry","verification"})
        gain="convert nonterminal episode into typed relative closure"
    elif obs.material_signals:
        target="reuse_successful_episode_learning"
        reason="material run signals exposed reusable control information"
        deps=frozenset(obs.material_signals)
        gain="reduce future cost or increase reliability on the same dependency class"
    else:
        # A clean success still teaches the controller that this route is viable.
        # That learning is recorded even when no structural change is warranted.
        return None

    data={
        "episode":obs.episode_id,
        "basis":obs.basis_id,
        "target":target,
        "reason":reason,
    }
    return SelfImprovementCandidate(
        candidate_id="IC-AFTER:"+_stable_id(data),
        target=target,
        reason=reason,
        dependency_footprint=deps,
        expected_gain=gain,
        evidence={"observation":asdict(obs)},
    )

def run_afterrun_improvement(
    *,
    episode_id:str,
    basis_id:str,
    status:str,
    blocker:str|None,
    state:Any,
    learning_memory:LearningMemory,
    recursive_result:dict|None=None,
    strict_gain_evaluator:Callable[[SelfImprovementCandidate,AfterRunObservation],dict]|None=None,
    authorized_applier:Callable[[SelfImprovementCandidate,dict],dict]|None=None,
)->AfterRunReceipt:
    obs=observe_after_run(
        episode_id=episode_id,basis_id=basis_id,status=status,
        blocker=blocker,state=state,recursive_result=recursive_result,
    )
    candidate=generate_candidate(obs)

    # Every use produces learning, even when the correct structural disposition is NO_GAIN.
    route_id=f"improvecore:episode:{episode_id}"
    if obs.protected_gain:
        learning_disp="GAIN"
    elif status in {"BLOCKED"}:
        learning_disp="BLOCKED"
    elif status in {"CONFLICT"}:
        learning_disp="CONFLICT"
    elif status in TERMINAL_GAP or obs.unresolved:
        learning_disp="OPEN"
    else:
        learning_disp="NO_GAIN"

    learning_memory.record(
        route_id,basis_id,learning_disp,
        set(candidate.dependency_footprint if candidate else obs.material_signals),
        {
            "status":status,
            "blocker":blocker,
            "candidate_id":candidate.candidate_id if candidate else None,
            "unresolved":obs.unresolved,
        },
    )

    if candidate is None:
        return AfterRunReceipt(
            "ImproveCoreAfterRun",obs,None,"NO_STRUCTURAL_GAIN",False,True,(),()
        )

    frontier=(candidate.target,)
    if strict_gain_evaluator is None:
        return AfterRunReceipt(
            "ImproveCoreAfterRun",obs,candidate,"CANDIDATE_OPEN",False,True,
            frontier,("STRICT_GAIN_EVALUATOR_UNBOUND",)
        )

    verdict=dict(strict_gain_evaluator(candidate,obs) or {})
    disposition=str(verdict.get("disposition","OPEN"))
    if disposition not in {"STRICT_GAIN","NO_GAIN","REJECTED","OPEN","BLOCKED","CONFLICT"}:
        raise ValueError("IC_AFTERRUN_INVALID_STRICT_GAIN_DISPOSITION")

    applied=False
    open_items=[]
    if disposition=="STRICT_GAIN":
        if authorized_applier is None:
            open_items.append("AUTHORIZED_APPLIER_UNBOUND")
        else:
            applied_result=dict(authorized_applier(candidate,verdict) or {})
            applied=bool(applied_result.get("applied"))
            if not applied:
                open_items.append(str(applied_result.get("blocker","APPLY_NOT_CONFIRMED")))

    return AfterRunReceipt(
        "ImproveCoreAfterRun",obs,candidate,disposition,applied,True,
        frontier,tuple(open_items)
    )
