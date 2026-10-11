"""Bounded in-process delegation with exact input/output receipt hashes.

The receipt field ``reintegrated`` records that the worker result was paired with
and returned alongside its receipt *within this function call*. It is not proof
of a durable parent-state commit, downstream consumer admission, scheduler
execution, or external reintegration. Those require independent evidence from
the owning consumer or state-commit machinery. Runtime boolean behavior is
preserved for compatibility with tests/test_delegation_lineage.py.
"""
from dataclasses import dataclass
from hashlib import sha256
import json

@dataclass(frozen=True)
class DelegationReceipt:
    episode:str
    program_id:str
    authority_in:frozenset[str]
    authority_local:frozenset[str]
    input_hash:str
    output_hash:str
    executed:bool
    reintegrated:bool

def _hash(x):
    return sha256(json.dumps(x,sort_keys=True,default=str).encode()).hexdigest()

def delegate(*,episode,program_id,authority_in,authority_local,payload,worker):
    if not authority_local <= authority_in:
        raise PermissionError("delegation expands authority")
    before=_hash(payload)
    output=worker(payload)
    receipt=DelegationReceipt(episode,program_id,authority_in,authority_local,before,_hash(output),True,True)
    return output,receipt
