"""Append-only episode lineage used to prove cross-episode inheritance."""
from dataclasses import dataclass,field

@dataclass
class LineageState:
    version:int=0
    values:dict=field(default_factory=dict)
    events:list=field(default_factory=list)

    def apply(self,event_type,delta,provenance):
        previous=self.version
        self.values.update(delta)
        self.version+=1
        self.events.append({"from":previous,"to":self.version,"type":event_type,"delta":dict(delta),"provenance":provenance})
        return self.version

    def inherits(self,earlier_version,key,value):
        return self.version>=earlier_version and self.values.get(key)==value
