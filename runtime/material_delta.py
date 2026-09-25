"""Derived affected-cone propagation for admitted material deltas."""
from dataclasses import dataclass
from collections import deque

@dataclass(frozen=True)
class MaterialDelta:
    changed:tuple
    result_sensitive:bool=True
    supervisory_relevant:bool=True

@dataclass(frozen=True)
class AffectedCone:
    roots:tuple
    affected:tuple

def affected_cone(delta:MaterialDelta,dependents:dict):
    seen=set(delta.changed)
    q=deque(delta.changed)
    while q:
        x=q.popleft()
        for y in dependents.get(x,()):
            if y not in seen:
                seen.add(y); q.append(y)
    return AffectedCone(tuple(delta.changed),tuple(seen))

def propagation_work(delta:MaterialDelta,dependents:dict):
    cone=affected_cone(delta,dependents)
    return tuple({"target":x,"reason":"AFFECTED_BY_MATERIAL_DELTA"} for x in cone.affected)
