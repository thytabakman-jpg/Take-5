"""Experimental binding-topology relation graph.

Research-only representation for testing whether item/tool/host/state relations add
result-sensitive information beyond existing configured-run coordinates.
"""
from dataclasses import dataclass
from enum import Enum

class NodeKind(str, Enum):
    ITEM="ITEM"
    TOOL="TOOL"
    HOST="HOST"
    STATE="STATE"
    VIEW="VIEW"
    CANDIDATE_UNIVERSE="CANDIDATE_UNIVERSE"
    RESULT="RESULT"

class EdgeKind(str, Enum):
    READS="READS"
    WRITES="WRITES"
    CONTAINS="CONTAINS"
    DELEGATES="DELEGATES"
    UPDATES="UPDATES"
    SELECTS="SELECTS"
    CONSTRAINS="CONSTRAINS"

@dataclass(frozen=True, order=True)
class BindingEdge:
    source:NodeKind
    target:NodeKind
    kind:EdgeKind

@dataclass(frozen=True)
class BindingTopology:
    edges:tuple[BindingEdge,...]

    def normalized(self):
        return tuple(sorted(set(self.edges)))

    def has_edge(self, source, target, kind=None):
        return any(
            e.source==source and e.target==target and (kind is None or e.kind==kind)
            for e in self.edges
        )

    def reachable(self, source, target):
        graph={n:set() for n in NodeKind}
        for e in self.edges:
            graph[e.source].add(e.target)
        frontier=[source]
        seen={source}
        while frontier:
            cur=frontier.pop()
            if cur==target:
                return True
            for nxt in graph[cur]:
                if nxt not in seen:
                    seen.add(nxt)
                    frontier.append(nxt)
        return False

    def item_can_change_future_selection(self):
        """Detect a feedback path from item/result into future selection machinery."""
        sources=(NodeKind.ITEM,NodeKind.RESULT)
        targets=(NodeKind.CANDIDATE_UNIVERSE,NodeKind.HOST,NodeKind.TOOL)
        return any(self.reachable(s,t) for s in sources for t in targets)

    def differs_from(self, other):
        return self.normalized()!=other.normalized()

def primitive_coordinate_admissible(*,distinct_role,result_sensitive,consumer_effect,nonreconstructible):
    """Take-5 coordinate-admission gate. Cardinality alone is irrelevant."""
    return all((distinct_role,result_sensitive,consumer_effect,nonreconstructible))
