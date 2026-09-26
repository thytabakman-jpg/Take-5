from improvement_core_learning_memory import LearningMemory
from improvement_core_math import (
    ActionCandidate,AugmentedControllerState,admissible_actions,material_delta,
)

def test_same_semantic_state_different_memory_changes_action_frontier():
    action=ActionCandidate(
        action_id="a1",
        route_id="route-x",
        basis_id="b0",
        dependency_footprint=frozenset({"evidence"}),
    )

    empty=AugmentedControllerState({"problem":"same"},LearningMemory())
    learned_memory=LearningMemory()
    learned_memory.record("route-x","b0","NO_GAIN",{"evidence"},{"why":"failed"})
    learned=AugmentedControllerState({"problem":"same"},learned_memory)

    assert admissible_actions(empty,(action,))==(action,)
    assert admissible_actions(learned,(action,))==()

def test_relevant_dependency_change_reopens_learned_route():
    memory=LearningMemory()
    memory.record("route-x","b0","NO_GAIN",{"evidence"},{"why":"failed"})
    action=ActionCandidate(
        action_id="a1",
        route_id="route-x",
        basis_id="b0",
        dependency_footprint=frozenset({"evidence"}),
    )
    state=AugmentedControllerState(
        {"problem":"same"},
        memory,
        changed_coordinates=frozenset({"evidence"}),
    )
    assert admissible_actions(state,(action,))==(action,)

def test_recursive_child_action_is_in_same_admissible_action_space():
    child=ActionCandidate(
        action_id="child-1",
        route_id="child-route",
        basis_id="b0",
        dependency_footprint=frozenset({"representation"}),
        kind="CHILD",
    )
    state=AugmentedControllerState({},LearningMemory())
    assert admissible_actions(state,(),(child,))==(child,)

def test_materiality_predicate_matches_recursive_manager_progress_law():
    assert material_delta({"negative_evidence":True})
    assert material_delta({"certified_no_gain":True})
    assert not material_delta({})
