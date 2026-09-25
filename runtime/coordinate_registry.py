"""Typed coordinate registry prevents cardinality-driven architectural conflation."""
from dataclasses import dataclass
from enum import Enum

class CoordinateRole(str,Enum):
    SCOPE="SCOPE"
    EDGE="EDGE"
    MODE="MODE"
    TRAVERSAL="TRAVERSAL"
    TRANSITION="TRANSITION"
    BRIDGE="BRIDGE"

@dataclass(frozen=True)
class CoordinateSpec:
    name:str
    role:CoordinateRole
    cardinality:int
    independent:bool
    result_sensitive:bool
    consumer_effect:bool
    canonical:bool=False

def product_factor_admissible(c:CoordinateSpec):
    return c.independent and c.result_sensitive and c.consumer_effect

def same_cardinality_is_not_equivalence(a:CoordinateSpec,b:CoordinateSpec):
    return a.cardinality==b.cardinality and a.role!=b.role

SCOPE=CoordinateSpec("six_scope",CoordinateRole.SCOPE,6,True,True,True,True)
SCOPE_EDGE=CoordinateSpec("directed_scope_edge",CoordinateRole.EDGE,36,True,True,True,True)
MODE_FACE=CoordinateSpec("mode_faces",CoordinateRole.MODE,6,False,True,True,False)
IOOC=CoordinateSpec("iooc_axes",CoordinateRole.TRAVERSAL,6,True,True,True,False)
TRANSITION_KIND=CoordinateSpec("transition_kinds",CoordinateRole.TRANSITION,6,False,True,True,False)
BRIDGE_KIND=CoordinateSpec("bridge_kinds",CoordinateRole.BRIDGE,6,False,True,False,False)

CURRENT=(SCOPE,SCOPE_EDGE,MODE_FACE,IOOC,TRANSITION_KIND,BRIDGE_KIND)
