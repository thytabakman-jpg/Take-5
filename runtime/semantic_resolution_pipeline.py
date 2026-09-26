"""Configured black-box semantic resolution pipeline.

Composes existing configured tools/question families rather than inventing a new
question atom. Mandatory stages run for every BLACK_BOX_OPEN object. Conditional
stages are activated only by typed residuals produced by earlier stages.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

MANDATORY_STAGES=(
    ("PD","Q03","Difference Math"),
    ("PDAudit","Q18","Verify Math"),
    ("MTA","Q01","Basic Math"),
    ("MT","Q02","Change Math"),
    ("PDAudit","Q18","Verify Math"),
    ("C47","Q19","Completion Check"),
)

CONDITIONAL_STAGES={
    "TYPE_OPEN":("C01","Q13","Type Check"),
    "IDENTITY_OPEN":("C02","Q14","Identity Check"),
    "CURRENTNESS_OPEN":("CurrentnessAudit","Q12","Current Check"),
    "DEPENDENCY_OPEN":("C06","Q15","Dependency Math"),
    "RELATION_OPEN":("C09","Q16","Relation Math"),
    "STRUCTURE_OPEN":("Architecture","Q05","Structure Math"),
    "INTERACTION_OPEN":("MultiObject","Q04","Together Math"),
    "CAUSE_OPEN":("Diagnosis","Q06","Cause Math"),
    "DISCOVERY_OPEN":("C19","Q22","Discovery Math"),
    "REALITY_OPEN":("C44","Q18","Verify Math"),
    "NOVELTY_OPEN":("C15","Q17","Novelty Check"),
}

@dataclass(frozen=True)
class PipelineStage:
    tool_id:str
    question_family:str
    question_name:str
    reason:str
    conditional_on:str|None=None

@dataclass(frozen=True)
class SemanticResolutionPlan:
    object_id:str
    stages:tuple[PipelineStage,...]
    residuals:tuple[str,...]

def plan_black_box_resolution(object_id:str,residuals:Iterable[str]=())->SemanticResolutionPlan:
    rs=tuple(dict.fromkeys(str(r) for r in residuals))
    stages=[
        PipelineStage(t,q,n,"mandatory black-box semantic resolution spine")
        for t,q,n in MANDATORY_STAGES
    ]
    for residual in rs:
        spec=CONDITIONAL_STAGES.get(residual)
        if spec is None:
            continue
        t,q,n=spec
        stages.append(PipelineStage(t,q,n,f"typed residual:{residual}",residual))
    return SemanticResolutionPlan(object_id,tuple(stages),rs)

def configured_work_obligations(plan:SemanticResolutionPlan)->tuple[str,...]:
    return tuple(f"RUN_CONFIGURED:{s.tool_id}:{plan.object_id}" for s in plan.stages)

def unexplained_residuals(plan:SemanticResolutionPlan)->tuple[str,...]:
    known=set(CONDITIONAL_STAGES)
    return tuple(r for r in plan.residuals if r not in known)
