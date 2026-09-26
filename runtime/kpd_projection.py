"""K_PD projection: preserve routing-relevant distinctions before recursive work.

Selection-cost optimization is downstream of the protected objective.  When an
episode explicitly asks for MOST_EFFECTIVE selection, the result-sensitive
effectiveness coordinates must first be compiled into obligations.  Otherwise
the episode remains OPEN rather than silently treating minimum execution cost as
the governing objective.
"""
from dataclasses import dataclass
import re

FIELDS=("identity","type","scope","job","readings","result_sensitive","selectors","authority","provenance","open")

@dataclass(frozen=True)
class KPDProjection:
    values:dict
    obligations:tuple[str,...]

def _objective_token(value):
    token=re.sub(r"[^A-Z0-9]+","_",str(value).strip().upper()).strip("_")
    return token

def effectiveness_obligations(packet):
    objective=_objective_token(packet.get("selection_objective",""))
    if objective!="MOST_EFFECTIVE":
        return ()
    coordinates=tuple(
        _objective_token(x)
        for x in packet.get("protected_effectiveness",())
        if _objective_token(x)
    )
    if not coordinates:
        return ("RESOLVE_EFFECTIVENESS_OBJECTIVE",)
    return tuple(f"EFFECTIVENESS_{x}" for x in dict.fromkeys(coordinates))

def project(packet):
    values={k:packet.get(k) for k in FIELDS}
    missing=tuple(k for k,v in values.items() if v is None)
    obligations=list(packet.get("obligations",()))
    obligations.extend(effectiveness_obligations(packet))
    obligations.extend("RESOLVE_"+k.upper() for k in missing)
    return KPDProjection(values,tuple(dict.fromkeys(obligations)))

def obligation_equivalent(a,b):
    return set(project(a).obligations)==set(project(b).obligations)
