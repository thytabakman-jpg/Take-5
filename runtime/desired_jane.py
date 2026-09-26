"""Recover the user's desired Jane contract from explicit evidence.

This tool answers a role-design question. It does not redesign Jane by itself and it
does not treat recency, repetition, or attractive wording as authority.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

class DesireStatus(str,Enum):
    REQUIRED="REQUIRED"
    PROHIBITED="PROHIBITED"
    OPEN="OPEN"
    CONFLICT="CONFLICT"

@dataclass(frozen=True)
class DesireEvidence:
    coordinate:str
    polarity:str
    source_ref:str
    statement:str

@dataclass(frozen=True)
class DesireDisposition:
    coordinate:str
    status:DesireStatus
    grounds:tuple[str,...]
    source_refs:tuple[str,...]

@dataclass(frozen=True)
class DesiredJaneContract:
    required:tuple[str,...]
    prohibited:tuple[str,...]
    open:tuple[str,...]
    conflicts:tuple[str,...]
    dispositions:tuple[DesireDisposition,...]

VALID_POLARITIES={"WANT","DO_NOT_WANT","UNKNOWN"}

def recover_desired_jane(evidence:Iterable[DesireEvidence])->DesiredJaneContract:
    rows={}
    for e in evidence:
        if e.polarity not in VALID_POLARITIES:
            raise ValueError(f"INVALID_POLARITY:{e.polarity}")
        rows.setdefault(e.coordinate,[]).append(e)

    dispositions=[]
    for coordinate in sorted(rows):
        xs=rows[coordinate]
        wants=[x for x in xs if x.polarity=="WANT"]
        avoids=[x for x in xs if x.polarity=="DO_NOT_WANT"]
        unknown=[x for x in xs if x.polarity=="UNKNOWN"]

        if wants and avoids:
            status=DesireStatus.CONFLICT
            grounds=tuple(x.statement for x in wants+avoids)
            refs=tuple(dict.fromkeys(x.source_ref for x in wants+avoids))
        elif wants:
            status=DesireStatus.REQUIRED
            grounds=tuple(x.statement for x in wants)
            refs=tuple(dict.fromkeys(x.source_ref for x in wants))
        elif avoids:
            status=DesireStatus.PROHIBITED
            grounds=tuple(x.statement for x in avoids)
            refs=tuple(dict.fromkeys(x.source_ref for x in avoids))
        else:
            status=DesireStatus.OPEN
            grounds=tuple(x.statement for x in unknown)
            refs=tuple(dict.fromkeys(x.source_ref for x in unknown))

        dispositions.append(DesireDisposition(coordinate,status,grounds,refs))

    required=tuple(x.coordinate for x in dispositions if x.status==DesireStatus.REQUIRED)
    prohibited=tuple(x.coordinate for x in dispositions if x.status==DesireStatus.PROHIBITED)
    open_items=tuple(x.coordinate for x in dispositions if x.status==DesireStatus.OPEN)
    conflicts=tuple(x.coordinate for x in dispositions if x.status==DesireStatus.CONFLICT)
    return DesiredJaneContract(required,prohibited,open_items,conflicts,tuple(dispositions))

def assertion_safe(contract:DesiredJaneContract)->bool:
    """A design contract is assertion-safe only when no live coordinate conflicts."""
    return not contract.conflicts
