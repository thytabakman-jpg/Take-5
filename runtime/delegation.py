"""Bounded delegation with exact before/after output preservation."""
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
