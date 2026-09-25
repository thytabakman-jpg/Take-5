"""Curiosity-first Inquiry Compiler.

Question identity is refined before formalization. PD may reenter after
formalization when the mathematical representation exposes new distinctions.
"""
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

def compile_question(raw_question,pd_question,root_translate,pd_audit=None):
    refined=pd_question(raw_question)
    formal=root_translate(refined)
    if pd_audit is not None:
        audited=pd_audit(formal)
        if audited is not None:
            formal=audited
    return formal,expand36(formal)
