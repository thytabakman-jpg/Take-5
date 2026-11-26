import random
import sys
sys.path.insert(0,'runtime')
from architecture_analysis import cyclic_components


def reference(graph):
    reach={}
    for start in graph:
        visited=set()
        pending=[start]
        while pending:
            node=pending.pop()
            if node in visited or node not in graph:
                continue
            visited.add(node)
            pending.extend(graph[node])
        reach[start]=visited
    remaining=set(graph)
    out=[]
    while remaining:
        start=min(remaining)
        group=sorted(x for x in reach[start] if start in reach[x])
        remaining.difference_update(group)
        if len(group)>1 or start in graph[start]:
            out.append(group)
    return out


def test_scc_matches_prior_semantics_exhaustive_three_nodes():
    nodes=('a','b','c')
    edges=[(a,b) for a in nodes for b in nodes]
    for mask in range(1<<len(edges)):
        graph={a:[] for a in nodes}
        for i,(a,b) in enumerate(edges):
            if mask & (1<<i):
                graph[a].append(b)
        graph['a'].append('dangling')
        assert cyclic_components(graph)==reference(graph)


def test_scc_matches_reference_on_seeded_graphs():
    rng=random.Random(1024)
    for n in range(1,35):
        nodes=[str(i) for i in range(n)]
        graph={a:[b for b in nodes if rng.random()<0.12] for a in nodes}
        assert cyclic_components(graph)==reference(graph)
        assert cyclic_components(dict(reversed(tuple(graph.items()))))==reference(graph)


def test_scc_long_chain_and_cycle_without_recursion_or_quadratic_reachability():
    n=5000
    graph={i:[i+1] for i in range(n-1)}
    graph[n-1]=[n]
    assert cyclic_components(graph)==[]
    graph[n-1]=[0]
    assert cyclic_components(graph)==[list(range(n))]
