"""Recursive ImprovementCore parent/child manager.

Parent ImprovementCore owns continuation. Learned negative routes are filtered
before frontier construction. Admitted child returns count as gain only through
the canonical strict-progress relation, and explicit no-effect semantic cycles
are durably blocked.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, field
from typing import Any, Callable

from improvement_core_learning_memory import LearningMemory
from improvement_core_math_spine import ControllerOption, nondominated_frontier
from improvement_core_progress_relation import (
    ClaimScope,
    EffectKind,
    EffectWitness,
    EvaluationTarget,
    SemanticStep,
    TransitionComparison,
    cycle_no_gain,
    silent_regressions,
    strict_progress,
    valid_effects,
)


TERMINAL={"COMPLETE","OPEN","BLOCKED","CONFLICT"}
ADMISSION={"ADMIT","REJECT","RECONCILE","OPEN","NO_GAIN"}

_EFFECT_KEYS=(
    ("material_result_delta",EffectKind.ACTION_CHANGED),
    ("material_search_delta",EffectKind.NEW_REACHABLE_WORK),
    ("open_refinement",EffectKind.MATERIAL_DISTINCTION_DISCOVERED),
    ("negative_evidence",EffectKind.NEGATIVE_ROUTE_CLOSED),
    ("changed_representation",EffectKind.COVERAGE_STRENGTHENED),
    ("goal_gap_reduced",EffectKind.GOAL_GAP_REDUCED),
    ("execution_truth_strengthened",EffectKind.EXECUTION_TRUTH_STRENGTHENED),
    ("resolved_open",EffectKind.OPEN_RESOLVED),
    ("resolved_blocked",EffectKind.BLOCKED_RESOLVED),
    ("resolved_conflict",EffectKind.CONFLICT_RESOLVED),
)


@dataclass
class ChildJob:
    id:str
    job:dict[str,Any]
    basis_id:str


@dataclass
class ChildReturn:
    child_id:str
    job_id:str
    execution_truth:str
    result:dict[str,Any]
    basis_id:str


@dataclass
class ManagerTrace:
    iteration:int
    selected_job:dict[str,Any]
    child_return:dict[str,Any]
    admission:str
    delta:dict[str,Any]
    state_after:dict[str,Any]
    strict_progress:bool=False
    progress_effects:tuple[str,...]=()


def _semantic_class(state:dict[str,Any])->str|None:
    for key in ("continuation_class","semantic_class"):
        value=state.get(key)
        if value not in (None,""):
            return str(value)
    return None


def _effect_witnesses(
    selected:dict[str,Any],
    basis:str,
    delta:dict[str,Any],
)->tuple[EffectWitness,...]:
    route_id=str(selected.get("route_id") or selected.get("id"))
    out=[]
    for key,kind in _EFFECT_KEYS:
        value=delta.get(key)
        if value:
            out.append(EffectWitness(
                kind=kind,
                target=EvaluationTarget.CONTROLLER,
                basis_id=basis,
                boundary="PARENT_STATE",
                evidence={"delta_key":key,"value":value},
                route_id=route_id,
            ))
    return tuple(out)


def _transition_comparison(
    before:dict[str,Any],
    after:dict[str,Any],
    selected:dict[str,Any],
    basis:str,
    delta:dict[str,Any],
)->TransitionComparison:
    pre_semantic=_semantic_class(before) or "UNCLASSIFIED_PRE"
    post_semantic=_semantic_class(after) or "UNCLASSIFIED_POST"
    scope=ClaimScope(
        target=EvaluationTarget.CONTROLLER,
        job_id=str(selected.get("id")),
        basis_id=basis,
        representation_id=str(
            after.get("representation_id")
            or before.get("representation_id")
            or "IMPLICIT_PARENT_STATE"
        ),
        boundary="PARENT_STATE",
    )
    return TransitionComparison(
        scope=scope,
        pre_semantic_class=pre_semantic,
        post_semantic_class=post_semantic,
        pre_basis_id=basis,
        post_basis_id=basis,
        protected_before=frozenset(
            str(x) for x in before.get("protected_behavior_ids",())
        ),
        protected_after=frozenset(
            str(x) for x in after.get("protected_behavior_ids",())
        ),
        explicitly_disposed_losses=frozenset(
            str(x) for x in delta.get("explicitly_disposed_losses",())
        ),
        effects=_effect_witnesses(selected,basis,delta),
        obligation_states=tuple(
            str(x) for x in delta.get("obligation_states",())
        ),
        boundary_verified=True,
        basis_reconciled=bool(delta.get("basis_reconciled",False)),
    )


@dataclass
class RecursiveImprovementCoreManager:
    select_child_job:Callable[[dict[str,Any],dict[str,Any]], dict[str,Any] | list[dict[str,Any]] | tuple[dict[str,Any],...] | None]
    run_child:Callable[[ChildJob], ChildReturn]
    admit_child:Callable[[ChildReturn,dict[str,Any],dict[str,Any]], tuple[str,dict[str,Any]]]
    update_parent:Callable[[dict[str,Any],dict[str,Any],str,dict[str,Any]], tuple[dict[str,Any],dict[str,Any]]]
    max_iterations:int=32
    learning_memory:LearningMemory|None=None
    traces:list[ManagerTrace]=field(default_factory=list)
    semantic_history:list[SemanticStep]=field(default_factory=list)

    def _retry_flags(self,z:dict[str,Any])->dict[str,bool]:
        return {
            "failure_signature_defeated":bool(z.get("failure_signature_defeated")),
            "representation_changed":bool(z.get("representation_changed")),
            "executability_changed":bool(z.get("executability_changed")),
            "new_interaction_package":bool(z.get("new_interaction_package")),
        }

    def _route_blocked(
        self,
        selected:dict[str,Any],
        z:dict[str,Any],
        fallback_basis:str,
    )->bool:
        if self.learning_memory is None:
            return False
        basis=str(selected.get("basis_id") or z.get("basis_id") or fallback_basis)
        route_id=str(selected.get("route_id") or selected.get("id"))
        return self.learning_memory.unchanged_rerun_blocked(
            route_id,
            basis,
            set(z.get("changed_coordinates",())),
            **self._retry_flags(z),
        )

    def _record_route(
        self,
        selected:dict[str,Any],
        basis:str,
        admission:str,
        delta:dict[str,Any],
        material:bool,
    )->None:
        if self.learning_memory is None:
            return
        route_id=str(selected.get("route_id") or selected.get("id"))
        deps=set(str(x) for x in selected.get("dependency_footprint",()))
        if admission=="NO_GAIN" or delta.get("certified_no_gain"):
            disposition="NO_GAIN"
        elif admission=="REJECT":
            disposition="REJECTED"
        elif admission=="OPEN":
            disposition="OPEN"
        elif material:
            disposition="GAIN"
        else:
            return
        self.learning_memory.record(route_id,basis,disposition,deps,dict(delta))

    def _record_cycle(
        self,
        selected:dict[str,Any],
        basis:str,
        delta:dict[str,Any],
    )->None:
        if self.learning_memory is None:
            return
        self.learning_memory.record(
            str(selected.get("route_id") or selected.get("id")),
            basis,
            "CYCLE_NO_GAIN",
            set(str(x) for x in selected.get("dependency_footprint",())),
            {"reason":"SEMANTIC_CYCLE_NO_GAIN","delta":dict(delta)},
        )

    def run(self,state:dict[str,Any],memory:dict[str,Any])->dict[str,Any]:
        z=dict(state)
        m=dict(memory)

        initial_semantic=_semantic_class(z)
        if initial_semantic and not self.semantic_history:
            self.semantic_history.append(SemanticStep(
                semantic_class=initial_semantic,
                basis_id=str(z.get("basis_id","UNSPECIFIED")),
                effects=(),
                resolved_unresolved_state=False,
            ))

        for i in range(self.max_iterations):
            terminal=str(z.get("terminal","CONTINUE"))
            if terminal in TERMINAL:
                return {
                    "status":terminal,
                    "state":z,
                    "memory":m,
                    "traces":[asdict(t) for t in self.traces],
                    "blocker":None,
                }

            selected=self.select_child_job(z,m)
            if selected is None:
                if z.get("live_continuation"):
                    raise RuntimeError(
                        "IC_MANAGER_LIVENESS_FAILURE:live_continuation_without_child_or_other_action"
                    )
                z["terminal"]="OPEN"
                return {
                    "status":"OPEN",
                    "state":z,
                    "memory":m,
                    "traces":[asdict(t) for t in self.traces],
                    "blocker":None,
                }

            if isinstance(selected,(list,tuple)):
                blocked_ids=[]
                raw_candidates=[]
                for candidate in selected:
                    if self._route_blocked(candidate,z,f"basis:{i}"):
                        blocked_ids.append(str(candidate.get("route_id") or candidate.get("id")))
                    else:
                        raw_candidates.append(candidate)

                if not raw_candidates:
                    return {
                        "status":"OPEN",
                        "state":z,
                        "memory":m,
                        "traces":[asdict(t) for t in self.traces],
                        "blocker":"IC_MANAGER_ALL_CANDIDATES_BLOCKED_BY_LEARNING",
                        "blocked_routes":tuple(blocked_ids),
                    }

                raw_candidates=tuple(raw_candidates)
                options=tuple(
                    ControllerOption(
                        option_id=str(x.get("id")),
                        goal_gain=float(x.get("goal_gain",0.0)),
                        information_gain=float(x.get("information_gain",0.0)),
                        search_gain=float(x.get("search_gain",0.0)),
                        cost=float(x.get("cost",0.0)),
                        risk=float(x.get("risk",0.0)),
                        reversible=bool(x.get("reversible",True)),
                        preserves_protected=bool(x.get("preserves_protected",True)),
                        authorized=bool(x.get("authorized",True)),
                        reachable=bool(x.get("reachable",True)),
                        status=str(x.get("status","CANDIDATE")),
                        metadata=x,
                    )
                    for x in raw_candidates
                )
                frontier=nondominated_frontier(options)
                if not frontier.nondominated:
                    return {
                        "status":"OPEN","state":z,"memory":m,
                        "traces":[asdict(t) for t in self.traces],
                        "blocker":"IC_MANAGER_NO_ADMISSIBLE_CHILD_JOB",
                        "frontier":{"rejected":frontier.rejected},
                    }
                by_id={str(x.get("id")):x for x in raw_candidates}
                if len(frontier.nondominated)>1:
                    requested=str(z.get("frontier_choice_id",""))
                    frontier_ids=tuple(x.option_id for x in frontier.nondominated)
                    if requested not in frontier_ids:
                        return {
                            "status":"OPEN","state":z,"memory":m,
                            "traces":[asdict(t) for t in self.traces],
                            "blocker":"IC_MANAGER_PLURAL_NONDOMINATED_CHILD_FRONTIER",
                            "frontier":{
                                "nondominated":frontier_ids,
                                "rejected":frontier.rejected,
                                "learning_blocked":tuple(blocked_ids),
                            },
                        }
                    selected=by_id[requested]
                else:
                    selected=by_id[frontier.nondominated[0].option_id]

            basis=str(selected.get("basis_id") or z.get("basis_id") or f"basis:{i}")
            route_id=str(selected.get("route_id") or selected.get("id"))
            changed=set(z.get("changed_coordinates",()))
            if self._route_blocked(selected,z,basis):
                return {
                    "status":"OPEN",
                    "state":z,
                    "memory":m,
                    "traces":[asdict(t) for t in self.traces],
                    "blocker":"IC_MANAGER_LEARNING_BLOCKED_UNCHANGED_ROUTE",
                }

            job=ChildJob(id=f"child:{i}",job=selected,basis_id=basis)

            ret=self.run_child(job)
            if ret.job_id!=selected.get("id"):
                raise RuntimeError("IC_MANAGER_RETURN_MISMATCH:job_id")
            if ret.basis_id!=basis:
                raise RuntimeError("IC_MANAGER_RETURN_MISMATCH:basis_id")
            if ret.execution_truth not in {
                "FULL_MATCH","IMPLEMENTATION_EXECUTED","SEMANTICALLY_APPLIED",
                "OPEN","BLOCKED"
            }:
                raise RuntimeError("IC_MANAGER_EXECUTION_TRUTH_INVALID")

            admission,delta=self.admit_child(ret,z,m)
            if admission not in ADMISSION:
                raise RuntimeError("IC_MANAGER_ADMISSION_INVALID")

            z2,m2=self.update_parent(z,m,admission,delta)
            comparison=_transition_comparison(z,z2,selected,basis,delta)
            material=strict_progress(comparison)
            regressions=silent_regressions(comparison)
            effects=tuple(effect.kind.value for effect in valid_effects(comparison))

            self.traces.append(ManagerTrace(
                iteration=i,
                selected_job=selected,
                child_return=asdict(ret),
                admission=admission,
                delta=delta,
                state_after=z2,
                strict_progress=material,
                progress_effects=effects,
            ))

            if regressions:
                raise RuntimeError(
                    "IC_MANAGER_STRICT_PROGRESS_REJECTED:PROTECTED_REGRESSION:"
                    + ",".join(sorted(regressions))
                )

            self._record_route(selected,basis,admission,delta,material)

            post_semantic=_semantic_class(z2)
            if post_semantic:
                resolved=any(
                    effect.kind in {
                        EffectKind.OPEN_RESOLVED,
                        EffectKind.BLOCKED_RESOLVED,
                        EffectKind.CONFLICT_RESOLVED,
                    }
                    for effect in valid_effects(comparison)
                )
                self.semantic_history.append(SemanticStep(
                    semantic_class=post_semantic,
                    basis_id=basis,
                    effects=effects,
                    resolved_unresolved_state=resolved,
                ))
                if cycle_no_gain(self.semantic_history):
                    self._record_cycle(selected,basis,delta)
                    return {
                        "status":"OPEN",
                        "state":z2,
                        "memory":m2,
                        "traces":[asdict(t) for t in self.traces],
                        "blocker":"IC_MANAGER_SEMANTIC_CYCLE_NO_GAIN",
                    }

            if (
                admission=="ADMIT"
                and any(delta.get(key) for key,_ in _EFFECT_KEYS)
                and not material
            ):
                raise RuntimeError(
                    "IC_MANAGER_STRICT_PROGRESS_REJECTED:UNCERTIFIED_EFFECT"
                )

            if not material and str(z2.get("terminal","CONTINUE"))=="CONTINUE":
                raise RuntimeError(
                    "IC_MANAGER_NO_PROGRESS:child_return_without_canonical_strict_progress"
                )

            z,m=z2,m2

        raise RuntimeError("IC_MANAGER_RESOURCE_BOUND:max_iterations")
