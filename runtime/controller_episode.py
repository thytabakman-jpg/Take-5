"""Minimal governed controller episode proving L3->L2->L1->L3 activation."""
from dataclasses import dataclass
from activation_bridge import Selection,ExecutionReceipt,bind,activation_complete
from evidence_ledger import EvidenceLedger

@dataclass
class EpisodeResult:
    complete: bool
    result: object
    ledger: EvidenceLedger

def run_episode(*,episode:str,program_id:str,target_id:str,job:str,authority:frozenset[str],
                worker,observation_only:bool=False,environment:str="local")->EpisodeResult:
    ledger=EvidenceLedger()
    selection=Selection(episode,f"{episode}:selection",program_id,target_id,job,authority,observation_only)
    binding=bind(selection)
    dispatched=True
    started=True
    try:
        result=worker(binding)
        executed=True
        captured=True
        failure=None
    except Exception as exc:
        result={"error":type(exc).__name__,"message":str(exc)}
        executed=False
        captured=True
        failure="EXECUTION"
    # Consumption means L3 actually receives and records the returned result.
    consumed=True
    er=ExecutionReceipt(episode,binding.contract_id,environment,dispatched,started,executed,captured,consumed,failure)
    complete=activation_complete(selection,binding,er)
    ledger.record_activation(episode=episode,program_id=program_id,selected=True,bound=True,
        dispatched=dispatched,started=started,executed=executed,captured=captured,
        consumed=consumed,evidence_ref=binding.contract_id)
    return EpisodeResult(complete,result,ledger)
