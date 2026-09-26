"""QuestionWorthAsking: select the highest-value live question without false uniqueness."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Tuple

EPS=1e-12

@dataclass(frozen=True)
class QuestionCandidate:
    question_id:str
    text:str
    result_sensitivity:float
    information_gain:float
    dependency_unlock:float
    actionability:float
    answer_cost:float
    narrowing_risk:float
    blocked:bool=False

    def __post_init__(self):
        for name in ("result_sensitivity","information_gain","dependency_unlock","actionability","answer_cost","narrowing_risk"):
            v=getattr(self,name)
            if not 0.0 <= v <= 1.0:
                raise ValueError(f"{name} must be in [0,1]")

    @property
    def value(self):
        return self.result_sensitivity+self.information_gain+self.dependency_unlock+self.actionability

    @property
    def burden(self):
        return self.answer_cost+self.narrowing_risk

    @property
    def worth(self):
        return self.value/(1.0+self.burden)

@dataclass(frozen=True)
class WorthResult:
    status:str
    selected:Tuple[QuestionCandidate,...]
    frontier:Tuple[QuestionCandidate,...]
    blocked:Tuple[QuestionCandidate,...]

def dominates(a,b):
    ba=(a.result_sensitivity,a.information_gain,a.dependency_unlock,a.actionability)
    bb=(b.result_sensitivity,b.information_gain,b.dependency_unlock,b.actionability)
    ca=(a.answer_cost,a.narrowing_risk)
    cb=(b.answer_cost,b.narrowing_risk)
    weak=all(x+EPS>=y for x,y in zip(ba,bb)) and all(x<=y+EPS for x,y in zip(ca,cb))
    strict=any(x>y+EPS for x,y in zip(ba,bb)) or any(x+EPS<y for x,y in zip(ca,cb))
    return weak and strict

def nondominated(questions:Iterable[QuestionCandidate]):
    qs=tuple(questions)
    return tuple(q for q in qs if not any(o.question_id!=q.question_id and dominates(o,q) for o in qs))

def select_question(questions:Iterable[QuestionCandidate]):
    qs=tuple(questions)
    if not qs:
        return WorthResult("EMPTY",(),(),())
    blocked=tuple(q for q in qs if q.blocked)
    answerable=tuple(q for q in qs if not q.blocked)
    if not answerable:
        return WorthResult("OPEN",(),(),blocked)
    frontier=nondominated(answerable)
    best=max(q.worth for q in frontier)
    selected=tuple(q for q in frontier if abs(q.worth-best)<=EPS)
    return WorthResult("SELECTED" if len(selected)==1 else "TIE",selected,frontier,blocked)
