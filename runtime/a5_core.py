"""A5 nonproduction behavioral architecture skeleton."""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable

class Decision(str, Enum):
    ALLOW="ALLOW"; DENY="DENY"; DEFER="DEFER"

@dataclass(frozen=True)
class Disposition:
    decision: Decision
    epistemic: str="OPEN"
    execution: str="UNBOUND"
    identity_relation: str="NOVEL"
    reason: str=""

@dataclass
class Witness:
    proposal_id: str
    state_before: int
    effect_scope: str
    evidence: list[str]=field(default_factory=list)
    authority: list[str]=field(default_factory=list)
    admission: Disposition|None=None
    state_after: int|None=None
    provenance: list[str]=field(default_factory=list)
    verification_obligations: list[str]=field(default_factory=list)

@dataclass
class State:
    version: int=0
    values: dict[str,Any]=field(default_factory=dict)
    evidence: list[str]=field(default_factory=list)
    authority: set[str]=field(default_factory=set)
    history: list[dict[str,Any]]=field(default_factory=list)
    failures: set[str]=field(default_factory=set)

class ContractK:
    def effect_allowed(self,state:State,effect:str,w:Witness)->bool:
        return effect in w.authority and w.effect_scope==effect

class OperatorO:
    @staticmethod
    def differentiate(xs,key=lambda x:x): return {key(x) for x in xs}
    @staticmethod
    def relate(a,b,relation): return relation(a,b)
    @staticmethod
    def reconstruct(parts,fn): return fn(parts)
    @staticmethod
    def strengthen(base,candidates,gain): return [x for x in candidates if gain(base,x)]

class GeneratorG:
    def generate(self,fn:Callable[...,list[Any]],*args,**kwargs): return fn(*args,**kwargs)

class ModifierM:
    def apply(self,fn:Callable[...,Any],op:Callable[...,Any],*args,**kwargs):
        return fn(op,*args,**kwargs)

class AdmissionC:
    def __init__(self,k:ContractK): self.k=k
    def evaluate(self,state:State,w:Witness,effect:str)->Disposition:
        if self.k.effect_allowed(state,effect,w):
            return Disposition(Decision.ALLOW,"SUPPORTED","BOUND",reason="effect-scoped authority")
        return Disposition(Decision.DEFER,"OPEN","BLOCKED",reason="missing effect-scoped authority")

class RouterR:
    def eligible(self,candidates):
        return [x for x in candidates if x.get("material",False) and x.get("reachable",False) and x.get("licensed",False)]
    def frontier(self,candidates,dominates):
        return [x for x in candidates if not any(y is not x and dominates(y,x) for y in candidates)]

class UpdaterU:
    def apply(self,state:State,w:Witness,effect:str,delta:dict[str,Any],admission:Disposition)->State:
        if admission.decision != Decision.ALLOW:
            raise PermissionError("effect not admitted")
        if effect != w.effect_scope:
            raise PermissionError("effect scope mismatch")
        nxt=State(state.version+1,dict(state.values),list(state.evidence),set(state.authority),list(state.history),set(state.failures))
        nxt.values.update(delta)
        nxt.history.append({"proposal":w.proposal_id,"effect":effect,"from":state.version,"to":nxt.version})
        w.admission=admission; w.state_after=nxt.version
        return nxt

class A5:
    def __init__(self):
        self.K=ContractK(); self.S=State(); self.O=OperatorO(); self.G=GeneratorG(); self.M=ModifierM()
        self.C=AdmissionC(self.K); self.R=RouterR(); self.U=UpdaterU()
    def transition(self,w:Witness,effect:str,delta:dict[str,Any]):
        a=self.C.evaluate(self.S,w,effect)
        self.S=self.U.apply(self.S,w,effect,delta,a)
        return self.S,w


@dataclass(frozen=True)
class ProgramSpec:
    program_id: str
    source: str
    job: str
    required_roles: tuple[str,...]
    protected_outputs: tuple[str,...]
    validation_target: str
    executable: bool=False

class ProgramRegistry:
    VALID_ROLES={"K","S","O","G","M","C","R","U"}
    def __init__(self): self._items={}
    def register(self,spec:ProgramSpec):
        if spec.program_id in self._items: raise ValueError("duplicate program id")
        if not spec.required_roles or not set(spec.required_roles)<=self.VALID_ROLES:
            raise ValueError("invalid or missing role binding")
        if not spec.protected_outputs: raise ValueError("missing protected output")
        if not spec.validation_target: raise ValueError("missing validation target")
        self._items[spec.program_id]=spec
    def get(self,pid): return self._items[pid]
    def ids(self): return set(self._items)
    def coverage(self,prefix): return {x for x in self._items if x.startswith(prefix)}
    def executable_ids(self): return {x for x,s in self._items.items() if s.executable}
