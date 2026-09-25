"""Delegation Officer: bounded background-work planning over typed Work.
This module selects and packages delegable work. Scheduling/external execution remains a separate runtime concern.
"""
from dataclasses import dataclass
from endogenous_work import select_work,WorkStatus

@dataclass(frozen=True)
class Assignment:
    work_id:str
    obligation:str
    authority:tuple
    target:str|None

@dataclass(frozen=True)
class DelegationPlan:
    assignments:tuple[Assignment,...]
    incomparable:tuple[str,...]

def plan_delegation(work_items,max_items=4):
    frontier=select_work(work_items)
    eligible=[w for w in frontier.selected if w.status in {WorkStatus.CANDIDATE,WorkStatus.ACTIVE}]
    chosen=tuple(eligible[:max_items])
    return DelegationPlan(
        tuple(Assignment(w.work_id,w.obligation,w.authority,w.target) for w in chosen),
        tuple(w.work_id for w in frontier.incomparable)
    )
