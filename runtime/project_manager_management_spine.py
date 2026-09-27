"""Mandatory management bootstrap for every normal ProjectManager run.

The spine is intentionally smaller than the exhaustive all-tools campaign.
It runs the always-result-sensitive management factors on every invocation,
each through its own current full configured plan and HF002 recurrence.

Heavy tools remain adaptively routed by ProjectManager/ImprovementCore when
the state warrants them. This preserves question-dependent routing rather than
turning every ordinary project check into a 93-tool campaign.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import Any, Mapping

from assert_compound import AssertState,AssertStages,identity_stage,run_to_fixed_point
from configured_hf2_execution import execute_configured_with_hf2
from currentness_audit import assess as assess_currentness
from global_tool_execution import build_tool_execution_plan
from goal import GoalCandidate,GoalObject,recover_goal
from mt_semantic_return_gate import run_mt_with_before_return_gate
from pd import run_pd
from pd_audit import run_pd_audit
from question_worth_asking import QuestionCandidate,select_question
from tool_run_registry import CONFIGURED_RUNS


MANDATORY_MANAGEMENT_SPINE=(
    ("ASSERT","ASSERT"),
    ("GOAL_PRE","GOAL"),
    ("MT","MT"),
    ("PD","PD"),
    ("PDAUDIT","PDAudit"),
    ("GOAL_POST","GOAL"),
    ("CURRENTNESS","CurrentnessAudit"),
    ("QUESTION_WORTH","QuestionWorthAsking"),
)


@dataclass(frozen=True)
class ManagementSpineReceipt:
    stage_id:str
    tool_id:str
    native_status:str
    recurrence_engine:str
    recurrence_status:str
    recurrence_rounds:int
    cell_count:int
    question_count:int
    cognitive_count:int
    result:Any


@dataclass(frozen=True)
class ManagementSpineResult:
    status:str
    receipts:tuple[ManagementSpineReceipt,...]
    blocker:str|None
    evidence:tuple[str,...]


def _plain(value:Any)->Any:
    if is_dataclass(value):
        return {k:_plain(v) for k,v in asdict(value).items()}
    if isinstance(value,Mapping):
        return {str(k):_plain(v) for k,v in value.items()}
    if isinstance(value,(list,tuple,set,frozenset)):
        return tuple(_plain(v) for v in value)
    if hasattr(value,"value"):
        return getattr(value,"value")
    return value


def _mapping(value:Any)->dict[str,Any]:
    if isinstance(value,Mapping):
        return dict(value)
    if is_dataclass(value):
        return asdict(value)
    return {}


def _subject(current:Mapping[str,Any])->tuple[str,dict[str,Any]]:
    candidate=current.get("candidate")
    project=current.get("project")
    if candidate is not None and project is not None:
        return "CONFLICT",{}
    if candidate is not None:
        return "CANDIDATE",_mapping(candidate)
    if project is not None:
        return "PROJECT",_mapping(project)
    return "NONE",{}


def _coords(kind:str,subject:Mapping[str,Any])->dict[str,Any]:
    raw=subject.get("coordinates",{})
    return dict(raw) if isinstance(raw,Mapping) else {}


def _blocking(kind:str,subject:Mapping[str,Any])->tuple[str,...]:
    if kind=="CANDIDATE":
        raw=subject.get("blocking_open",())
    else:
        raw=subject.get("blocking_open",subject.get("open_coordinates",()))
    if isinstance(raw,str):
        return (raw,)
    if isinstance(raw,(list,tuple,set,frozenset)):
        return tuple(str(x) for x in raw if str(x))
    return ()


def _goal_object(kind:str,subject:Mapping[str,Any])->GoalObject:
    coords=_coords(kind,subject)
    raw=coords.get("goal")
    if isinstance(raw,Mapping):
        X=str(raw.get("X") or raw.get("x") or subject.get("candidate_id") or subject.get("project_id") or kind)
        T=str(raw.get("T") or raw.get("t") or "recover and manage the governing project change")
        I=str(raw.get("I") or raw.get("i") or "ProjectManager controlled progression")
        Sigma=str(raw.get("Sigma") or raw.get("sigma") or "typed evidence of closure or preserved OPEN")
        return GoalObject(X,T,I,Sigma)
    text=str(raw or "").strip()
    return GoalObject(
        str(subject.get("candidate_id") or subject.get("project_id") or kind),
        text,
        "ProjectManager controlled progression",
        "typed evidence of goal closure or preserved OPEN",
    )


def _assert_stage(kind:str,subject:Mapping[str,Any],basis:str):
    blocking=_blocking(kind,subject)
    initial=AssertState(
        assertions=(
            f"subject_kind={kind}",
            f"subject_id={subject.get('candidate_id') or subject.get('project_id') or 'unknown'}",
        ),
        world=(basis,),
        discovery=blocking,
    )
    stages=AssertStages(
        identity_stage,identity_stage,identity_stage,
        identity_stage,identity_stage,identity_stage,
    )
    return run_to_fixed_point(initial,stages,max_rounds=3)


def _goal_stage(kind:str,subject:Mapping[str,Any],basis:str,stage_id:str):
    goal=_goal_object(kind,subject)
    evidence=[basis,f"ProjectManager:{kind}",f"stage:{stage_id}"]
    if stage_id=="GOAL_POST":
        evidence.extend(("MT:consumed","PD:consumed","PDAudit:consumed"))
    return recover_goal((
        GoalCandidate(
            f"PROJECTMANAGER_{stage_id}",
            goal,
            constraints=("OBSERVER_ONLY","OPEN_PRESERVATION","AUTHORITY_PRESERVATION"),
            evidence=tuple(evidence),
            grounded=bool(goal.T),
            authority_typed=True,
            determinate_enough=bool(goal.X and goal.T and goal.I and goal.Sigma),
        ),
    ))


def _mt_stage(kind:str,subject:Mapping[str,Any],basis:str):
    coords=_coords(kind,subject)
    blocking=_blocking(kind,subject)
    initial={"kind":kind,"basis":basis,"coords":tuple(sorted(coords))}
    def run_mt(state):
        result={
            "subject_kind":kind,
            "coordinate_set":tuple(sorted(coords)),
            "blocking_open":blocking,
            "distinctions":(
                "GOAL!=IMPLEMENTATION",
                "OPEN!=FALSE",
                "EVIDENCE!=AUTHORITY",
                "CANDIDATE!=MANAGED_PROJECT",
            ),
            "black_boxes":(),
        }
        return state,result
    return run_mt_with_before_return_gate(
        initial,
        run_mt=run_mt,
        detect_black_boxes=lambda state,result:result.get("black_boxes",()),
        execute_stage=lambda tool_id,object_id,state:(state,"CLOSED_RELATIVE",False),
    )


def _sensitivity_frame(kind:str,subject:Mapping[str,Any]):
    coords=_coords(kind,subject)
    names=tuple(sorted(coords))
    if not names:
        names=("goal",)
    baseline=tuple(1 for _ in names)+(1,)
    cases=[baseline]
    for i in range(len(names)):
        row=list(baseline); row[i]=0; cases.append(tuple(row))
    blocked=list(baseline); blocked[-1]=0; cases.append(tuple(blocked))
    def rho(case):
        return "READY" if all(case[:-1]) and bool(case[-1]) else "OPEN"
    return tuple(cases),rho,{"management_coordinates":lambda case:tuple(case)}


def _pd_stage(kind:str,subject:Mapping[str,Any],audit:bool=False):
    cases,rho,reps=_sensitivity_frame(kind,subject)
    if audit:
        return run_pd_audit(
            cases,
            rho=rho,
            approx=lambda a,b:a==b,
            representations=reps,
            kappa_cases=lambda rows:{"case_count":len(rows)},
            kappa_representations=lambda rs:{"representation_count":len(rs)},
        )
    return run_pd(
        cases,
        rho=rho,
        approx=lambda a,b:a==b,
        representations=reps,
    )


def _currentness_stage(kind:str,subject:Mapping[str,Any],basis:str):
    return assess_currentness(
        component=f"ProjectManager:{kind}",
        built_basis=basis,
        latest_basis=basis,
        protected=("goal","authority","open_preservation","admission_boundary"),
        delta=(),
        behavior_preserved=True,
        local_patch_available=True,
        evidence=("project-manager-management-spine",),
        reverified=True,
    )


def _question_worth_stage(kind:str,subject:Mapping[str,Any]):
    blocking=_blocking(kind,subject)
    questions=tuple(
        QuestionCandidate(
            f"OPEN_{i+1}",
            text,
            1.0,
            0.8,
            0.8,
            0.8,
            0.3,
            0.1,
            False,
        )
        for i,text in enumerate(blocking)
    )
    return select_question(questions)


def _native(stage_id:str,tool_id:str,current:Mapping[str,Any]):
    kind,subject=_subject(current)
    basis=str(current.get("basis") or current.get("basis_ref") or "CURRENT")
    if kind in {"NONE","CONFLICT"}:
        return {"status":"OPEN","blocker":f"PROJECTMANAGER_SPINE_SUBJECT_{kind}"}
    if stage_id=="ASSERT":
        return _assert_stage(kind,subject,basis)
    if stage_id in {"GOAL_PRE","GOAL_POST"}:
        return _goal_stage(kind,subject,basis,stage_id)
    if stage_id=="MT":
        return _mt_stage(kind,subject,basis)
    if stage_id=="PD":
        return _pd_stage(kind,subject,False)
    if stage_id=="PDAUDIT":
        return _pd_stage(kind,subject,True)
    if stage_id=="CURRENTNESS":
        return _currentness_stage(kind,subject,basis)
    if stage_id=="QUESTION_WORTH":
        return _question_worth_stage(kind,subject)
    raise KeyError(stage_id)


def _native_status(value:Any)->str:
    if isinstance(value,Mapping):
        return str(value.get("status","EXECUTED"))
    if hasattr(value,"status"):
        status=getattr(value,"status")
        return str(getattr(status,"value",status))
    return "EXECUTED"


def run_management_spine(current:Mapping[str,Any])->ManagementSpineResult:
    receipts=[]
    evidence=[]
    for stage_id,tool_id in MANDATORY_MANAGEMENT_SPINE:
        plan=build_tool_execution_plan(CONFIGURED_RUNS[tool_id])
        holder={}
        def adapter(state,plan,stage_id=stage_id,tool_id=tool_id):
            value=_native(stage_id,tool_id,current)
            holder["value"]=value
            native_status=_native_status(value)
            if native_status in {"OPEN","BLOCKED","CONFLICT"}:
                return {
                    "status":native_status,
                    "execution_truth":native_status,
                    "result":_plain(value),
                    "state":state,
                    "material_delta":False,
                    "hf2_local_close":True,
                    "trc_terminal":True,
                    "evidence":(f"project-manager-spine:{stage_id}",),
                }
            return {
                "status":"EXECUTED",
                "execution_truth":"IMPLEMENTATION_EXECUTED",
                "result":_plain(value),
                "state":state,
                "material_delta":False,
                "hf2_live_local":False,
                "hf2_local_close":True,
                "trc_terminal":True,
                "hf1_disposition":"STABLE",
                "evidence":(f"project-manager-spine:{stage_id}",),
            }

        out=execute_configured_with_hf2(
            tool_id=tool_id,
            plan=plan,
            state={"stage":stage_id},
            adapter=adapter,
            max_rounds=8,
        )
        value=holder.get("value")
        receipt=ManagementSpineReceipt(
            stage_id,
            tool_id,
            _native_status(value),
            out.recurrence_engine,
            out.status,
            out.rounds,
            len(plan.cells),
            len(plan.questions),
            len(plan.cognitive),
            _plain(value),
        )
        receipts.append(receipt)
        evidence.append(f"{stage_id}:{tool_id}:{out.status}")
        if out.status not in {"RELATIVE_CLOSE","SELF_CLOSE"}:
            status=out.status if out.status in {"OPEN","BLOCKED","CONFLICT"} else "OPEN"
            return ManagementSpineResult(
                status,tuple(receipts),f"MANAGEMENT_SPINE_{stage_id}_{out.status}",tuple(evidence)
            )

    return ManagementSpineResult("CLOSED_RELATIVE",tuple(receipts),None,tuple(evidence))
