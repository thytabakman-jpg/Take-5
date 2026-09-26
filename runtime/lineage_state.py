"""Append-only episode lineage used to prove cross-episode inheritance."""
from dataclasses import dataclass,field
from state_commit import CommitReceipt,StateRole,require_role

@dataclass
class LineageState:
    version:int=0
    values:dict=field(default_factory=dict)
    events:list=field(default_factory=list)

    def apply(self,event_type,delta,provenance,*,commit_receipt:CommitReceipt):
        require_role(commit_receipt,StateRole.LINEAGE)
        previous=self.version
        self.values.update(delta)
        self.version+=1
        self.events.append({
            "from":previous,
            "to":self.version,
            "type":event_type,
            "delta":dict(delta),
            "provenance":provenance,
            "commit":{
                "effect":commit_receipt.effect,
                "target":commit_receipt.target,
                "job":commit_receipt.job,
                "baseline":commit_receipt.baseline,
                "status":commit_receipt.status,
            },
        })
        return self.version

    def inherits(self,earlier_version,key,value):
        return self.version>=earlier_version and self.values.get(key)==value
