"""Inquiry Compiler candidate: question -> formal inquiry -> PD refinement -> 36 probes."""
from dataclasses import dataclass

SCOPES=("SYSTEM","SUBSYSTEM","COMPONENT","INTERFACE","BOUNDARY_DECOMPOSITION","CROSS_LAYER")
MODES=("EXPAND","CONTRACT","INWARD","OUTWARD","ISOLATE","COUPLE")

@dataclass(frozen=True)
class FormalQuestion:
    issue:str
    target:str
    answer_space:tuple
    presuppositions:tuple=()
    success_conditions:tuple=()
    dependencies:tuple=()
    authority:tuple=()

@dataclass(frozen=True)
class InquiryProbe:
    question:FormalQuestion
    scope:str
    mode:str

def expand36(q):
    return tuple(InquiryProbe(q,s,m) for s in SCOPES for m in MODES)

def compile_question(raw_question,root_translate,pd_enrich):
    q=root_translate(raw_question)
    enriched=pd_enrich(q)
    return enriched,expand36(enriched)
