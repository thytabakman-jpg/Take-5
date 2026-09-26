"""Goal-independent object recovery before object-specific mathematics.

The operator preserves plurality instead of choosing a convenient singleton target.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any,Callable,Iterable

class IdentificationStatus(str,Enum):
    IDENTIFIED="IDENTIFIED"
    PLURAL="PLURAL"
    OPEN="OPEN"
    BLOCKED="BLOCKED"

@dataclass(frozen=True)
class ObjectRecovery:
    status:IdentificationStatus
    survivors:tuple[Any,...]
    equivalence_classes:tuple[tuple[Any,...],...]
    common_invariants:frozenset[Any]
    rival_models:tuple[Any,...]

def recover_object_space(
    evidence:Any,
    candidates:Iterable[Any],
    *,
    fit:Callable[[Any,Any],bool],
    equivalent:Callable[[Any,Any],bool],
    invariants:Callable[[Any],Iterable[Any]],
    model:Callable[[Any],Any]=lambda x:x,
)->ObjectRecovery:
    universe=tuple(candidates)
    if not universe:
        return ObjectRecovery(IdentificationStatus.OPEN,(),(),frozenset(),())

    survivors=tuple(x for x in universe if fit(x,evidence))
    if not survivors:
        return ObjectRecovery(IdentificationStatus.BLOCKED,(),(),frozenset(),())

    classes=[]
    unused=list(survivors)
    while unused:
        head=unused.pop(0)
        cls=[head]
        rest=[]
        for x in unused:
            if equivalent(head,x):
                cls.append(x)
            else:
                rest.append(x)
        classes.append(tuple(cls))
        unused=rest

    inv_sets=[set(invariants(x)) for x in survivors]
    common=frozenset.intersection(*(frozenset(s) for s in inv_sets)) if inv_sets else frozenset()
    status=IdentificationStatus.IDENTIFIED if len(classes)==1 else IdentificationStatus.PLURAL
    return ObjectRecovery(status,survivors,tuple(classes),common,tuple(model(x) for x in survivors))
