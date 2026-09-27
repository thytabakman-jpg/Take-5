import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"runtime"))

from configured_hf2_execution import execute_configured_with_hf2
from global_tool_execution import build_tool_execution_plan
from goal import GoalCandidate,GoalObject,recover_goal
from mt_semantic_return_gate import run_mt_with_before_return_gate
from pd import run_pd
from tool_run_registry import CONFIGURED_RUNS


def _configured(tool_id,native):
    plan=build_tool_execution_plan(CONFIGURED_RUNS[tool_id])
    assert plan.complete
    assert len(plan.cells)==36
    assert len(plan.questions)==792
    assert len(plan.cognitive)==144
    def adapter(state,plan):
        result=native(state.get("packet"))
        return {
            "status":"EXECUTED",
            "execution_truth":"IMPLEMENTATION_EXECUTED",
            "result":result,
            "state":state,
            "material_delta":False,
            "hf2_live_local":False,
            "hf2_local_close":True,
            "trc_terminal":True,
            "hf1_disposition":"STABLE",
            "evidence":("tests/test_project_definition_requested_sequence.py",),
        }
    out=execute_configured_with_hf2(
        tool_id=tool_id,
        plan=plan,
        state={"packet":{"target":"preproject-definition-gate"}},
        adapter=adapter,
    )
    assert out.status=="RELATIVE_CLOSE"
    assert out.recurrence_engine=="HF002"
    return out.last_raw["result"]


def _mt(_):
    initial={"target":"preproject-definition-gate"}
    def run_mt(state):
        return state,{
            "distinctions":(
                "IDEA!=ADMITTED_PROJECT",
                "DEFINITION_READY!=HUMAN_APPROVED",
                "EVIDENCE_ONLY!=TARGET_TRANSFORM",
                "PROCESS_GOAL!=CANDIDATE_PROJECT_GOAL",
            ),
            "black_boxes":(),
        }
    out=run_mt_with_before_return_gate(
        initial,
        run_mt=run_mt,
        detect_black_boxes=lambda state,result:result["black_boxes"],
        execute_stage=lambda tool_id,object_id,state:(state,"CLOSED_RELATIVE",False),
    )
    assert out.status=="CLOSED_RELATIVE"
    return out.mt_result


def _pd(_):
    cases=(
        (0,0,0),
        (1,0,0),
        (1,1,0),
        (1,0,1),
    )
    def rho(case):
        complete,blocking,approved=case
        if not complete or blocking:
            return "EXPLORATION_OPEN"
        return "PROMOTION_READY" if approved else "DEFINITION_READY"
    return run_pd(
        cases,
        rho=rho,
        approx=lambda a,b:a==b,
        representations={"admission":lambda c:c},
    )


PROCESS_GOAL=GoalObject(
    X="an idea or candidate project plus current accepted project state",
    T="a durable definition-ready candidate that has not been promoted prematurely",
    I="ProjectManager preproject definition gate with evidence-only exploration",
    Sigma="full project creation requires definition readiness plus explicit user approval",
)


def _goal(_):
    return recover_goal((
        GoalCandidate(
            "PREPROJECT_PROCESS_GOAL",
            PROCESS_GOAL,
            constraints=(
                "preserve accepted projects",
                "no automatic promotion",
                "human approval remains external authority",
            ),
            evidence=("user-request:highest-level-approval-before-build",),
            grounded=True,
            authority_typed=True,
            determinate_enough=True,
        ),
    ))


def _sequence_signature():
    mt=_configured("MT",_mt)
    pd=_configured("PD",_pd)
    g1=_configured("GOAL",_goal)
    g2=_configured("GOAL",_goal)
    assert g1.status=="CLOSED_RELATIVE"
    assert g2.status=="CLOSED_RELATIVE"
    assert g1.active_goal==g2.active_goal==PROCESS_GOAL
    return (
        tuple(mt["distinctions"]),
        pd["status"],
        tuple(pd["result"]["result_classes"]),
        g1.active_goal,
        g2.active_goal,
    )


def test_requested_mt_pd_goal_goal_sequence_uses_full_configured_hf2_and_outer_supervisory_fixpoint():
    first=_sequence_signature()
    second=_sequence_signature()
    assert first==second
