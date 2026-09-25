"""Representation-coupled discovery state for the endogenous research lifecycle."""
from dataclasses import dataclass
from enum import Enum
from typing import Callable,Iterable

class DiscoveryMode(str,Enum):
    OBSERVE="OBSERVE"
    REFOCUS="REFOCUS"

@dataclass(frozen=True)
class View:
    view_id:str
    payload:object

@dataclass(frozen=True)
class CandidateUniverse:
    classes:tuple[str,...]
    candidates:tuple[str,...]

@dataclass(frozen=True)
class DiscoveryDelta:
    state_changed:bool=False
    view_changed:bool=False
    candidate_universe_changed:bool=False
    relation_changed:bool=False
    authority_or_evidence_changed:bool=False
    runtime_reality_changed:bool=False

    @property
    def material(self):
        return any((self.state_changed,self.view_changed,self.candidate_universe_changed,
                    self.relation_changed,self.authority_or_evidence_changed,
                    self.runtime_reality_changed))

def generate_views(state:dict,generators:Iterable[Callable[[dict],View]]):
    return tuple(g(state) for g in generators)

def candidate_universe(state:dict,views:tuple[View,...],generators):
    found=[]
    classes=[]
    for cls,g in generators.items():
        vals=tuple(g(state,views))
        classes.append(cls)
        found.extend(f"{cls}:{v}" for v in vals)
    return CandidateUniverse(tuple(classes),tuple(dict.fromkeys(found)))

def compare_discovery(before_views,after_views,before_universe,after_universe,relation_changed=False,state_changed=False):
    return DiscoveryDelta(
        state_changed=state_changed,
        view_changed=before_views!=after_views,
        candidate_universe_changed=before_universe!=after_universe,
        relation_changed=relation_changed,
    )

def reentry_required(delta:DiscoveryDelta):
    return delta.material
