"""Configured Multi-Object + MT connection/shake program."""
from dataclasses import dataclass
from itertools import combinations

SCOPES=("SYSTEM","SUBSYSTEM","COMPONENT","INTERFACE","BOUNDARY_DECOMPOSITION","CROSS_LAYER")
MODE_FACES=("EXPAND","CONTRACT","INWARD","OUTWARD","ISOLATE","COUPLE")

@dataclass(frozen=True)
class Challenge:
    objects:tuple
    scope:str
    mode_face:str

def pair_challenges(objects,scopes=SCOPES,modes=MODE_FACES):
    return tuple(Challenge(pair,s,m) for pair in combinations(tuple(objects),2) for s in scopes for m in modes)

def higher_order_challenges(objects,arity=3,scopes=SCOPES,modes=MODE_FACES):
    return tuple(Challenge(group,s,m) for group in combinations(tuple(objects),arity) for s in scopes for m in modes)

def high_information_first(challenges,priority_modes=("ISOLATE","COUPLE","CONTRACT","OUTWARD","INWARD","EXPAND")):
    rank={m:i for i,m in enumerate(priority_modes)}
    return tuple(sorted(challenges,key=lambda c:(rank.get(c.mode_face,99),c.scope,c.objects)))
