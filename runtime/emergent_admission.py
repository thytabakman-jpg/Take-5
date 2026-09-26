"""Emergent load-bearing object admission guard."""
from dataclasses import dataclass
from enum import Enum

class Admission(str,Enum):
    ACCEPT="ACCEPT"; MERGE="MERGE"; OPEN="OPEN"; REJECT="REJECT"

@dataclass(frozen=True)
class ObjectCandidate:
    object_id:str
    object_type:str
    load_bearing:bool|None
    known_equivalent:str|None=None
    executable_claim:bool=False
    bound:bool=False
 
def admit(o:ObjectCandidate, package_verifier=None):
    if o.load_bearing is False:
        return Admission.REJECT
    if o.load_bearing is None:
        return Admission.OPEN
    if o.known_equivalent:
        return Admission.MERGE
    if not o.object_id or not o.object_type:
        return Admission.OPEN
    if o.executable_claim and not o.bound:
        return Admission.OPEN
    verified = bool(package_verifier(o.object_id)) if package_verifier is not None else False
    if not verified:
        return Admission.OPEN
    return Admission.ACCEPT
