"""Jane synchronization hook for configured recursive rounds."""
from dataclasses import dataclass

@dataclass(frozen=True)
class JaneSyncReceipt:
    material:bool
    supervisory_relevant:bool
    synced:bool
    delta_ref:str|None=None
    execution_ref:str|None=None

def jane_sync(*,material,supervisory_relevant,update,delta,delta_ref=None,execution_ref=None):
    if not material or not supervisory_relevant:
        return JaneSyncReceipt(material,supervisory_relevant,False,delta_ref,execution_ref)
    update(delta)
    return JaneSyncReceipt(True,True,True,delta_ref,execution_ref)
