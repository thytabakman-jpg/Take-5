"""Executable closure semantics for Recursive Compiler.

The compiler is hierarchical and fail-closed. Local success never implies global
success. A manuscript may close only after every node gate, hierarchy edge,
protected constraint, admitted delta lineage, stale-state check, and HF2
fixed-point witness passes over the same frozen successor state.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Iterable, Any

from hf002_recursive_continuation import material_delta_present as _material


@dataclass(frozen=True)
class CompilerNode:
    node_id:str
    level:str
    parent_id:str|None=None
    gates:Mapping[str,bool]|None=None
    protected_constraints:tuple[str,...]=()
    delta_ids:tuple[str,...]=()
    stale:bool=False


@dataclass(frozen=True)
class RecursiveCompilerClosure:
    status:str
    reasons:tuple[str,...]
    checked_nodes:int
    checked_edges:int
    checked_deltas:int

    @property
    def closed(self)->bool:
        return self.status=="GLOBAL_CLOSED"


def validate_execution_profile(
    *,
    cell_count:int,
    mode_trace:Iterable[str],
)->None:
    """Fail closed on 36D downgrade or observer/focused/observer drift."""
    if type(cell_count) is not int or cell_count!=36:
        raise RuntimeError(f"RECURSIVE_COMPILER_36D_DOWNGRADE:{cell_count}")
    modes=tuple(str(x).upper() for x in mode_trace)
    if modes!=("OBSERVER","FOCUSED","OBSERVER"):
        raise RuntimeError(
            "RECURSIVE_COMPILER_MODE_SEQUENCE_INVALID:"+",".join(modes)
        )


def hf2_fixed_point_witness(trace:Iterable[Mapping[str,Any]])->bool:
    """Require a terminal clean pass over the final successor state."""
    rounds=tuple(trace)
    if not rounds:
        return False
    last=rounds[-1]
    if not isinstance(last,Mapping) or last.get("disposition")!="RELATIVE_CLOSE":
        return False
    delta=last.get("delta")
    return isinstance(delta,Mapping) and not _material(delta)


def affected_cone(nodes:Iterable[CompilerNode],changed_ids:Iterable[str])->frozenset[str]:
    """Return changed nodes plus every dependent ancestor and descendant."""
    ns=tuple(nodes)
    by_id={n.node_id:n for n in ns}
    children={n.node_id:set() for n in ns}
    for n in ns:
        if n.parent_id in children:
            children[n.parent_id].add(n.node_id)

    out={str(x) for x in changed_ids if str(x) in by_id}
    frontier=list(out)
    while frontier:
        nid=frontier.pop()
        parent=by_id[nid].parent_id
        if parent and parent in by_id and parent not in out:
            out.add(parent)
            frontier.append(parent)
        for child in children.get(nid,()):
            if child not in out:
                out.add(child)
                frontier.append(child)
    return frozenset(out)


def evaluate_global_closure(
    *,
    nodes:Iterable[CompilerNode],
    edge_receipts:Mapping[tuple[str,str],bool],
    constraint_receipts:Mapping[tuple[str,str],bool],
    admitted_delta_hashes:Mapping[str,str],
    realized_delta_hashes:Mapping[str,str],
    hf2_trace:Iterable[Mapping[str,Any]],
)->RecursiveCompilerClosure:
    ns=tuple(nodes)
    reasons:list[str]=[]
    ids=[n.node_id for n in ns]
    by_id={n.node_id:n for n in ns}

    if len(ids)!=len(set(ids)):
        reasons.append("DUPLICATE_NODE_ID")

    roots=[n for n in ns if n.parent_id is None]
    if len(roots)!=1:
        reasons.append("HIERARCHY_REQUIRES_EXACTLY_ONE_ROOT")

    # A single root and existing parents do not exclude disconnected cycles.
    for node in ns:
        visited=set()
        current=node
        while current is not None:
            if current.node_id in visited:
                reasons.append(f"HIERARCHY_CYCLE:{node.node_id}")
                break
            visited.add(current.node_id)
            current=by_id.get(current.parent_id) if current.parent_id is not None else None

    checked_edges=0
    required_deltas=set(admitted_delta_hashes)

    for n in ns:
        if n.parent_id is not None:
            checked_edges+=1
            if n.parent_id not in by_id:
                reasons.append(f"MISSING_PARENT:{n.node_id}:{n.parent_id}")
            elif edge_receipts.get((n.parent_id,n.node_id)) is not True:
                reasons.append(f"UNRECONCILED_EDGE:{n.parent_id}->{n.node_id}")

        if n.stale:
            reasons.append(f"STALE_NODE:{n.node_id}")

        gates=dict(n.gates or {})
        if not gates:
            reasons.append(f"NODE_GATES_MISSING:{n.node_id}")
        for gate,passed in gates.items():
            if passed is not True:
                reasons.append(f"NODE_GATE_OPEN:{n.node_id}:{gate}")

        for constraint in n.protected_constraints:
            if constraint_receipts.get((n.node_id,constraint)) is not True:
                reasons.append(f"PROTECTED_CONSTRAINT_OPEN:{n.node_id}:{constraint}")

        required_deltas.update(n.delta_ids)

    for delta_id in sorted(required_deltas):
        expected=admitted_delta_hashes.get(delta_id)
        actual=realized_delta_hashes.get(delta_id)
        if not isinstance(expected,str) or not expected.strip():
            reasons.append(f"DELTA_ADMISSION_MISSING:{delta_id}")
        if not isinstance(actual,str) or not actual.strip():
            reasons.append(f"DELTA_MISSING:{delta_id}")
        elif isinstance(expected,str) and expected.strip() and actual!=expected:
            reasons.append(f"DELTA_SEMANTIC_DRIFT:{delta_id}")

    # Realization without an admitted lineage is not allowed to masquerade as
    # preservation evidence.
    for delta_id in sorted(set(realized_delta_hashes)-required_deltas):
        reasons.append(f"UNADMITTED_DELTA_REALIZATION:{delta_id}")

    if not hf2_fixed_point_witness(hf2_trace):
        reasons.append("HF2_ZERO_NEW_DELTA_FIXED_POINT_MISSING")

    return RecursiveCompilerClosure(
        status="GLOBAL_CLOSED" if not reasons else "OPEN",
        reasons=tuple(reasons),
        checked_nodes=len(ns),
        checked_edges=checked_edges,
        checked_deltas=len(required_deltas),
    )


def require_global_closure(**kwargs)->RecursiveCompilerClosure:
    out=evaluate_global_closure(**kwargs)
    if not out.closed:
        raise RuntimeError("RECURSIVE_COMPILER_GLOBAL_CLOSE_BLOCKED:"+"|".join(out.reasons))
    return out
