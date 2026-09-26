"""Executable helpers for ImprovementCore augmented-controller math 086.

The purpose is not to replace the regime runtime. It witnesses the strict-gain
claim that learning memory and recursive child-action identity are
result-sensitive controller coordinates.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable

from improvement_core_learning_memory import LearningMemory


@dataclass(frozen=True)
class ActionCandidate:
    action_id:str
    route_id:str
    basis_id:str
    dependency_footprint:frozenset[str]
    kind:str="BASE"


@dataclass
class AugmentedControllerState:
    semantic_state:Any
    learning_memory:LearningMemory
    changed_coordinates:frozenset[str]=frozenset()


def action_blocked(state:AugmentedControllerState,action:ActionCandidate)->bool:
    return state.learning_memory.unchanged_rerun_blocked(
        action.route_id,
        action.basis_id,
        set(state.changed_coordinates),
    )


def admissible_actions(
    state:AugmentedControllerState,
    base_actions:Iterable[ActionCandidate],
    child_actions:Iterable[ActionCandidate]=(),
)->tuple[ActionCandidate,...]:
    actions=tuple(base_actions)+tuple(child_actions)
    return tuple(a for a in actions if not action_blocked(state,a))


def material_delta(delta:dict)->bool:
    return bool(
        delta.get("material_result_delta")
        or delta.get("material_search_delta")
        or delta.get("open_refinement")
        or delta.get("negative_evidence")
        or delta.get("certified_no_gain")
        or delta.get("changed_representation")
    )
