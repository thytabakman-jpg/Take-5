"""LambdaMath: set-valued entry-state reconstruction with continuation quotienting."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Iterable, Mapping, Any, Tuple

COORDS=("G_ext","T","M","C","S","F")

@dataclass(frozen=True)
class EntryState:
    G_ext: Any
    T: Any
    M: Any
    C: Any
    S: Any
    F: Any

    def as_map(self):
        return {k:getattr(self,k) for k in COORDS}

@dataclass(frozen=True)
class LambdaResult:
    status:str
    candidates:Tuple[EntryState,...]
    equivalence_classes:Tuple[Tuple[EntryState,...],...]
    common_core:Tuple[Tuple[str,Any],...]
    ambiguous_coordinates:Tuple[str,...]

def _classes(candidates, equivalent):
    unused=list(candidates)
    classes=[]
    while unused:
        head=unused.pop(0)
        group=[head]
        rest=[]
        for item in unused:
            if equivalent(head,item):
                group.append(item)
            else:
                rest.append(item)
        classes.append(tuple(group))
        unused=rest
    return tuple(classes)

def _common_core(candidates):
    if not candidates:
        return ()
    maps=[c.as_map() for c in candidates]
    out=[]
    for d in COORDS:
        first=maps[0][d]
        if all(m[d]==first for m in maps[1:]):
            out.append((d,first))
    return tuple(out)

def reconstruct(
    candidates:Iterable[EntryState],
    *,
    consistent:Callable[[EntryState],bool],
    continuation_equivalent:Callable[[EntryState,EntryState],bool],
    result_sensitive:Callable[[str],bool],
)->LambdaResult:
    survivors=tuple(c for c in candidates if consistent(c))
    if not survivors:
        return LambdaResult("EMPTY",(),(),(),())

    classes=_classes(survivors,continuation_equivalent)
    core=_common_core(survivors)

    ambiguous=[]
    for d in COORDS:
        vals=[c.as_map()[d] for c in survivors]
        if any(v!=vals[0] for v in vals[1:]) and result_sensitive(d):
            ambiguous.append(d)

    if len(classes)==1:
        status="IDENTIFIED"
    elif ambiguous:
        status="CLARIFY"
    else:
        status="PLURAL_SAFE"

    return LambdaResult(status,survivors,classes,core,tuple(ambiguous))
