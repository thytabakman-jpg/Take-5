"""Machine-readable evidence spine for Take-5 readiness claims."""
from dataclasses import dataclass, field, asdict
from typing import Any
import json

@dataclass
class EvidenceLedger:
    identities: dict[str,dict[str,Any]]=field(default_factory=dict)
    activations: list[dict[str,Any]]=field(default_factory=list)
    reconstructions: list[dict[str,Any]]=field(default_factory=list)
    validations: list[dict[str,Any]]=field(default_factory=list)

    def register_identity(self,key:str,**links):
        self.identities[key]=dict(links)

    def record_activation(self,*,episode:str,program_id:str,selected:bool,bound:bool,
                          dispatched:bool,started:bool,executed:bool,captured:bool,
                          consumed:bool,evidence_ref:str=""):
        row=locals().copy(); row.pop("self")
        self.activations.append(row); return row

    def activation_complete(self,episode:str,program_id:str)->bool:
        for r in reversed(self.activations):
            if r["episode"]==episode and r["program_id"]==program_id:
                return all(r[k] for k in ("selected","bound","dispatched","started","executed","captured","consumed"))
        return False

    def record_reconstruction(self,*,historical_id:str,successor_id:str,frozen_job:str,
                              predecessor_witness:str,successor_witness:str,
                              relation:str,disposition:str):
        row=locals().copy(); row.pop("self")
        self.reconstructions.append(row); return row

    def historically_reconstructed(self,historical_id:str)->bool:
        return any(r["historical_id"]==historical_id and r["disposition"]=="PASS"
                   and all(r[k] for k in ("successor_id","frozen_job","predecessor_witness","successor_witness","relation"))
                   for r in self.reconstructions)

    def validate(self,claim:str,status:str,evidence_ref:str):
        self.validations.append({"claim":claim,"status":status,"evidence_ref":evidence_ref})

    def readiness(self,required_historical=()):
        return {
            "activation_evidence": any(all(r[k] for k in ("selected","bound","dispatched","started","executed","captured","consumed")) for r in self.activations),
            "historical_reconstruction": all(self.historically_reconstructed(x) for x in required_historical),
            "no_failed_required_validation": not any(v["status"]=="FAIL" for v in self.validations),
        }

    def to_json(self):
        return json.dumps(asdict(self),indent=2,sort_keys=True)
