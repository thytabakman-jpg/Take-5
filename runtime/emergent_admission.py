"""Emergent load-bearing object admission guard."""
from dataclasses import dataclass
from enum import Enum

class Admission(str,Enum):
    ACCEPT="ACCEPT"; MERGE="MERGE"; OPEN="OPEN"; REJECT="REJECT"

@dataclass(frozen=True)
class ObjectCandidate:
    object_id:str
    object_type:str
    load_bearing:bool
    known_equivalent:str|None=None
    executable_claim:bool=False
    bound:bool=False
    semantic_package_current:bool=False

def admit(o:ObjectCandidate):
    if not o.load_bearing:
        return Admission.REJECT
    if o.known_equivalent:
        return Admission.MERGE
    if not o.object_id or not o.object_type:
        return Admission.OPEN
    if o.executable_claim and not o.bound:
        return Admission.OPEN
    if not o.semantic_package_current:
        return Admission.OPEN
    return Admission.ACCEPT
