"""Basis-relative cheap-route versus broad-attack calibration.

The cheap route uses the existing generic observer.  The broad route adds
relation-structure inspection that is intentionally more expensive.

The policy is not a universal scalar optimum.  It is a validated current-basis
rule:
- flat/nonrelational corpora may use CHEAP when the cheap pass leaves no OPEN
  structural signal;
- corpora containing internal relation structure require BROAD because the
  cheap observer does not inspect resolved-cycle / higher-order relation shape.
"""
from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict
from autonomous_observer import observe_records


@dataclass(frozen=True)
class RouteCalibration:
    route:str
    reason:str
    cheap_findings:int
    broad_findings:int


def _graph(records):
    graph=defaultdict(list)
    known=set()
    for i,r in enumerate(records):
        if isinstance(r,dict):
            node=str(r.get("id",i))
            known.add(node)
            for ref in r.get("refs",()):
                graph[node].append(str(ref))
    return graph,known


def _cycles(records):
    graph,known=_graph(records)
    cycles=set()
    visiting=set()
    visited=set()

    def dfs(node,path):
        if node in visiting:
            if node in path:
                i=path.index(node)
                cyc=tuple(path[i:]+[node])
                cycles.add(cyc)
            return
        if node in visited:
            return
        visiting.add(node)
        for nxt in graph.get(node,()):
            if nxt in known:
                dfs(nxt,path+[nxt])
        visiting.remove(node)
        visited.add(node)

    for node in sorted(known):
        dfs(node,[node])
    return tuple(sorted(cycles))


def broad_observe_records(records):
    base=observe_records(records)
    findings=list(base["findings"])
    for cycle in _cycles(records):
        findings.append({"type":"REFERENCE_CYCLE","cycle":cycle})
    return {"status":"ACCEPT","findings":findings,"count":len(tuple(records))}


def select_route(records)->RouteCalibration:
    rows=tuple(records)
    cheap=observe_records(rows)
    broad=broad_observe_records(rows)

    graph,known=_graph(rows)
    has_internal_relations=any(
        target in known
        for source,targets in graph.items()
        for target in targets
    )

    if has_internal_relations:
        return RouteCalibration(
            "BROAD",
            "INTERNAL_RELATION_STRUCTURE_REQUIRES_RELATION_CHALLENGE",
            len(cheap["findings"]),
            len(broad["findings"]),
        )

    return RouteCalibration(
        "CHEAP",
        "NO_INTERNAL_RELATION_STRUCTURE_ON_CURRENT_BASIS",
        len(cheap["findings"]),
        len(broad["findings"]),
    )
