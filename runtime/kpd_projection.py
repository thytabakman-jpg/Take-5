"""K_PD projection: preserve routing-relevant distinctions before recursive work."""
from dataclasses import dataclass

FIELDS=("identity","type","scope","job","readings","result_sensitive","selectors","authority","provenance","open")

@dataclass(frozen=True)
class KPDProjection:
    values:dict
    obligations:tuple[str,...]

def project(packet):
    values={k:packet.get(k) for k in FIELDS}
    missing=tuple(k for k,v in values.items() if v is None)
    obligations=list(packet.get("obligations",()))
    obligations.extend("RESOLVE_"+k.upper() for k in missing)
    return KPDProjection(values,tuple(dict.fromkeys(obligations)))

def obligation_equivalent(a,b):
    return set(project(a).obligations)==set(project(b).obligations)
