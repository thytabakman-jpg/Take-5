"""Project-local Jewish Holiday Booklet greenfield design program.
Separates generative curriculum design from existing-artifact repair/release.
"""
from dataclasses import dataclass

STAGES=("BOOK_SEED","DESIGN_BRIEF","ROUTE_LOCK","SOURCE_LOCK","PAGE_ROUTE","STUDENT_SPEC","ACTIVITY_SPEC","ARTIFACT_AUDIT","VISUAL_MASTER","RENDER","QA","CLASSROOM_VALIDATION","RELEASE")

@dataclass(frozen=True)
class BookletBrief:
    audience:str
    setting:str
    holiday:str
    phenomenon:str
    human_problem:str
    jewish_operation:str
    holiday_embodiment:str
    transfer:str
    non_goals:tuple=()

@dataclass(frozen=True)
class GreenfieldState:
    brief:BookletBrief
    completed:tuple=()
    open_items:tuple=()

def next_stage(state):
    done=set(state.completed)
    for s in STAGES:
        if s not in done:
            return s
    return "COMPLETE"

def route_contract(brief):
    return (
        brief.phenomenon,
        brief.human_problem,
        brief.jewish_operation,
        brief.holiday_embodiment,
        brief.transfer,
    )

def release_allowed(state):
    return next_stage(state)=="COMPLETE" and not state.open_items
