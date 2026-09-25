"""Post-migration maturity/currentness audit for active C capabilities."""
from dataclasses import dataclass
from enum import Enum
from a5_programs import REGISTRY
from capability_router import TRIGGER_TAGS

class Maturity(str,Enum):
    CURRENT="A_CURRENT"
    REVALIDATE="B_REVALIDATE"
    REPAIR="C_REPAIR"
    SUPERSEDED="D_SUPERSEDED"

@dataclass(frozen=True)
class ToolMaturity:
    program_id:str
    disposition:Maturity
    reasons:tuple[str,...]

def active_capability_ids():
    return tuple(sorted(x for x in REGISTRY.ids() if x.startswith("C") and x[1:].isdigit()))

def historical_witness_ids():
    return tuple(sorted(x for x in REGISTRY.ids() if x.startswith("CAP-")))

def audit_one(pid,material_basis_change=False,fixture_current=True,host_consumed=True):
    s=REGISTRY.get(pid); reasons=[]
    if pid not in TRIGGER_TAGS: reasons.append("missing trigger contract")
    if not s.executable: reasons.append("not runtime bound")
    if not host_consumed: reasons.append("host services not consumed")
    if not fixture_current: reasons.append("result-sensitive fixture/currentness missing")
    if reasons: return ToolMaturity(pid,Maturity.REPAIR,tuple(reasons))
    if material_basis_change: return ToolMaturity(pid,Maturity.REVALIDATE,("material basis change requires semantic revalidation",))
    return ToolMaturity(pid,Maturity.CURRENT,())

def audit_all(changed_ids=(),fixture_stale=(),host_missing=()):
    changed=set(changed_ids); stale=set(fixture_stale); missing=set(host_missing)
    return tuple(audit_one(pid,pid in changed,pid not in stale,pid not in missing) for pid in active_capability_ids())
