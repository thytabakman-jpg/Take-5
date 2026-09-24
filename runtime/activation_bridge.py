"""Activation bridge across L3 controller, L2 binding, and L1 execution."""
from dataclasses import dataclass
from enum import Enum

class Stage(str, Enum):
    SELECTED="SELECTED"; BOUND="BOUND"; DISPATCHED="DISPATCHED"; STARTED="STARTED"
    EXECUTED="EXECUTED"; RESULT_CAPTURED="RESULT_CAPTURED"; CONSUMED="CONSUMED"
    BLOCKED="BLOCKED"

@dataclass(frozen=True)
class Selection:
    episode:str
    selection_id:str
    program_id:str
    target_id:str
    job:str
    authority:frozenset[str]
    observation_only:bool=False

@dataclass(frozen=True)
class BindingReceipt:
    episode:str
    selection_id:str
    program_id:str
    target_id:str
    job:str
    authority_in:frozenset[str]
    authority_out:frozenset[str]
    contract_id:str
    status:str="BOUND"
    observation_only:bool=False

@dataclass(frozen=True)
class ExecutionReceipt:
    episode:str
    contract_id:str
    environment:str
    dispatched:bool=False
    started:bool=False
    executed:bool=False
    result_captured:bool=False
    consumed:bool=False
    failure_stage:str|None=None

def bind(selection:Selection, *, program_id:str|None=None, target_id:str|None=None,
         job:str|None=None, authority_out:frozenset[str]|None=None,
         observation_only:bool|None=None)->BindingReceipt:
    p=program_id or selection.program_id
    t=target_id or selection.target_id
    j=job or selection.job
    a=selection.authority if authority_out is None else authority_out
    obs=selection.observation_only if observation_only is None else observation_only
    if not a <= selection.authority:
        raise PermissionError("binding expands authority")
    if t != selection.target_id:
        raise ValueError("silent target substitution")
    if j != selection.job:
        raise ValueError("silent job substitution")
    if p != selection.program_id:
        raise ValueError("silent program substitution")
    if selection.observation_only and not obs:
        raise PermissionError("observation contract converted to substantive action")
    return BindingReceipt(selection.episode,selection.selection_id,p,t,j,selection.authority,a,
                          f"{selection.episode}:{selection.selection_id}:{p}",observation_only=obs)

def activation_complete(selection:Selection,binding:BindingReceipt,execution:ExecutionReceipt)->bool:
    return (
        binding.episode==selection.episode
        and binding.selection_id==selection.selection_id
        and binding.program_id==selection.program_id
        and binding.authority_out <= binding.authority_in
        and execution.contract_id==binding.contract_id
        and execution.dispatched and execution.started and execution.executed
        and execution.result_captured and execution.consumed
    )

def execution_stage(r:ExecutionReceipt)->Stage:
    if r.failure_stage: return Stage.BLOCKED
    if r.consumed: return Stage.CONSUMED
    if r.result_captured: return Stage.RESULT_CAPTURED
    if r.executed: return Stage.EXECUTED
    if r.started: return Stage.STARTED
    if r.dispatched: return Stage.DISPATCHED
    return Stage.BOUND
