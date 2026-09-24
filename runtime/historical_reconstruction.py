"""Historical reconstruction relation. Evidence-first; never infers equivalence from names."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ReconstructionCase:
    historical_id:str
    successor_id:str
    frozen_job:str
    protected:tuple[str,...]
    predecessor_result:object
    successor_result:object
    predecessor_witness:str
    successor_witness:str
    context:str=""

@dataclass(frozen=True)
class ReconstructionDisposition:
    status:str
    relation:str
    reason:str

def compare(case:ReconstructionCase)->ReconstructionDisposition:
    if not case.frozen_job or not case.protected:
        return ReconstructionDisposition("OPEN","UNESTABLISHED","job/protected basis incomplete")
    if not case.predecessor_witness or not case.successor_witness:
        return ReconstructionDisposition("OPEN","UNESTABLISHED","missing execution witness")
    if case.predecessor_result == case.successor_result:
        return ReconstructionDisposition("PASS","MATCHED_PROTECTED_RESULT","matched result on frozen case")
    return ReconstructionDisposition("FAIL","RESULT_DIVERGENCE","successor changed protected result")

def contextual_equivalence(cases)->ReconstructionDisposition:
    cases=tuple(cases)
    if not cases:
        return ReconstructionDisposition("OPEN","UNESTABLISHED","no matched cases")
    ds=[compare(c) for c in cases]
    if any(d.status=="FAIL" for d in ds):
        return ReconstructionDisposition("FAIL","CONTEXTUAL_DIVERGENCE","at least one licensed context diverged")
    if any(d.status=="OPEN" for d in ds):
        return ReconstructionDisposition("OPEN","INCOMPLETE_CONTEXTUAL_EVIDENCE","at least one context lacks evidence")
    return ReconstructionDisposition("PASS","CONTEXTUAL_MATCH","all supplied licensed contexts matched")
