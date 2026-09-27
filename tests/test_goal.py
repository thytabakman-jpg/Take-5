import sys
sys.path.insert(0,"runtime")

from goal import GoalCandidate, GoalObject, recover_goal
from portable_tool_conductor import compilation_witness
from tool_manifest import manifest_for
from tool_run_registry import CONFIGURED_RUNS, PROTECTED_BEHAVIORS


def _goal(target="recover the governing goal"):
    return GoalObject(
        X="dynamic inquiry system",
        T=target,
        I="job-relative evidence basis",
        Sigma="one admitted governing goal with explicit completion condition",
    )


def _candidate(candidate_id="g1", goal=None, constraints=("preserve OPEN",), evidence=("e1",)):
    return GoalCandidate(
        candidate_id=candidate_id,
        goal=goal or _goal(),
        constraints=constraints,
        evidence=evidence,
        grounded=True,
        authority_typed=True,
        determinate_enough=True,
    )


def test_goal_recovers_unique_admissible_governing_goal():
    out=recover_goal((_candidate(),))
    assert out.status=="CLOSED_RELATIVE"
    assert out.active_goal==_goal()
    assert out.active_candidate_ids==("g1",)
    assert out.constraint_sets==(("preserve OPEN",),)
    assert out.evidence==("e1",)


def test_goal_keeps_constraints_outside_x_t_i_sigma_identity():
    same=_goal()
    out=recover_goal((
        _candidate("g1",same,("c1",),("e1",)),
        _candidate("g2",same,("c2",),("e2",)),
    ))
    assert out.status=="CLOSED_RELATIVE"
    assert out.active_goal==same
    assert out.constraint_sets==(("c1",),("c2",))
    assert out.active_candidate_ids==("g1","g2")


def test_goal_fails_open_without_admissible_grounded_evidence():
    bad=GoalCandidate("g1",_goal(),evidence=(),grounded=True,authority_typed=True,determinate_enough=True)
    out=recover_goal((bad,))
    assert out.status=="OPEN"
    assert out.blocker=="NO_ADMISSIBLE_GOVERNING_GOAL"
    assert out.active_goal is None


def test_goal_fails_open_on_plural_distinct_governing_goals():
    out=recover_goal((
        _candidate("g1",_goal("target one"),evidence=("e1",)),
        _candidate("g2",_goal("target two"),evidence=("e2",)),
    ))
    assert out.status=="OPEN"
    assert out.blocker=="PLURAL_GOVERNING_GOALS"
    assert out.active_goal is None


def test_goal_detects_conflicting_reuse_of_candidate_identity():
    out=recover_goal((
        _candidate("g1",_goal("target one")),
        _candidate("g1",_goal("target two")),
    ))
    assert out.status=="CONFLICT"
    assert out.blocker=="GOAL_CANDIDATE_ID_CONFLICT:g1"


def test_goal_has_explicit_manifest_and_native_compilation_witness():
    protected=set(PROTECTED_BEHAVIORS["GOAL"])
    manifest=manifest_for("GOAL")
    assert protected <= set(manifest.behavior_ids())
    assert CONFIGURED_RUNS["GOAL"].complete()

    witness=compilation_witness("GOAL")
    assert witness.entrypoint=="goal.recover_goal"
    assert witness.status=="PROGRAM_WITH_ENVIRONMENT"
    assert witness.required_environment==("goal_candidates",)
