"""Native fixed-frame PD result-sensitivity core.

PD identifies result-changing distinctions relative to an admitted case set,
result map/equivalence, and one or more explicit coordinate representations.
Unknown or absent semantic bindings remain OPEN.
"""
from __future__ import annotations
from typing import Any, Callable, Mapping
from copy import deepcopy

def _callable(value:Any,name:str)->Callable:
    if not callable(value):
        raise TypeError(f"{name}_CALLABLE_REQUIRED")
    return value

class _InvalidEquivalence(ValueError):
    pass


def _fixed_partition(cases,rho,approx):
    # Snapshot each result once, including providers that reuse mutable buffers.
    results=tuple(deepcopy(rho(case)) for case in cases)
    groups=[]
    classes=[]
    for i,result in enumerate(results):
        if approx(deepcopy(result),deepcopy(result)) is not True:
            raise _InvalidEquivalence("PD_EQUIVALENCE_REFLEXIVITY_OR_TYPE")
        matched=set()
        for j,prior in enumerate(results[:i]):
            forward=approx(deepcopy(result),deepcopy(prior))
            reverse=approx(deepcopy(prior),deepcopy(result))
            if type(forward) is not bool or type(reverse) is not bool:
                raise _InvalidEquivalence("PD_EQUIVALENCE_BOOLEAN_REQUIRED")
            if forward != reverse:
                raise _InvalidEquivalence("PD_EQUIVALENCE_ASYMMETRIC")
            if forward:
                matched.add(j)
        if matched:
            class_id=classes[min(matched)]
            expected={j for j,c in enumerate(classes) if c==class_id}
            if matched!=expected:
                raise _InvalidEquivalence("PD_EQUIVALENCE_NONTRANSITIVE")
        else:
            class_id=len(groups)
            groups.append({"representative":result,"cases":[]})
        groups[class_id]["cases"].append(cases[i])
        classes.append(class_id)
    return tuple(groups),tuple(classes)


def result_partition(cases,*,rho:Callable,approx:Callable):
    return _fixed_partition(tuple(cases),rho,approx)[0]

def minimal_sensitive_sets(cases,*,rho:Callable,approx:Callable,representation:Callable):
    cases=tuple(cases)
    _,classes=_fixed_partition(cases,rho,approx)
    return _minimal_sensitive_sets(cases,classes,representation)


def _minimal_sensitive_sets(cases,classes,representation):
    values=[deepcopy(tuple(representation(case))) for case in cases]
    if not values:
        return ()
    width=len(values[0])
    if any(len(value)!=width for value in values):
        raise ValueError("PD_REPRESENTATION_ARITY_DRIFT")

    # A differing-result pair witnesses exactly the coordinates on which
    # its representations differ, and every superset of those coordinates.
    # Therefore the minimal witnesses are the inclusion-minimal pair supports;
    # enumerating the entire coordinate powerset is unnecessary.
    supports=set()
    for i,left in enumerate(cases):
        for j in range(i+1,len(cases)):
            if classes[i]!=classes[j]:
                supports.add(tuple(k for k in range(width) if values[i][k]!=values[j][k]))
    sensitive=[]
    for support in sorted(supports,key=lambda x:(len(x),x)):
        if not any(set(prev).issubset(support) for prev in sensitive):
            sensitive.append(support)
    return tuple(sensitive)

def run_pd(
    cases,
    *,
    rho:Callable,
    approx:Callable,
    representations:Mapping[str,Callable],
    allow_empty_domain:bool=False,
)->dict[str,Any]:
    """Recover quotient result classes, fibers, and representation-relative MinSens."""
    cases=tuple(cases)
    if not cases and allow_empty_domain is not True:
        return {"status":"OPEN","blocker":"PD_CASE_DOMAIN_REQUIRED","result":None}
    rho=_callable(rho,"PD_RHO")
    approx=_callable(approx,"PD_APPROX")
    if not isinstance(representations,Mapping) or not representations:
        return {"status":"OPEN","blocker":"PD_REPRESENTATION_REQUIRED","result":None}

    reps={}
    for name,fn in representations.items():
        key=str(name)
        if key in reps:
            return {"status":"OPEN","blocker":"PD_REPRESENTATION_ID_COLLISION:"+key,"result":None}
        reps[key]=_callable(fn,f"PD_REPRESENTATION_{name}")

    try:
        groups,classes=_fixed_partition(cases,rho,approx)
    except _InvalidEquivalence as exc:
        return {"status":"OPEN","blocker":str(exc),"result":None}
    minimal={
        name:_minimal_sensitive_sets(cases,classes,fn)
        for name,fn in reps.items()
    }
    delta=tuple(
        (left,cases[j])
        for i,left in enumerate(cases)
        for j in range(i+1,len(cases))
        if classes[i]!=classes[j]
    )
    collapse=tuple(name for name,sets in minimal.items() if () in sets)

    result={
        "result_classes":tuple(group["representative"] for group in groups),
        "fibers":tuple(tuple(group["cases"]) for group in groups),
        "minimal_sensitive":minimal,
        "pair_difference_relation":delta,
        "representation_collapse":collapse,
        "OPEN":(),
    }
    return {"status":"RELATIVE_CLOSE","result":result}
