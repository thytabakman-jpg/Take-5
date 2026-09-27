"""Native fixed-frame PD result-sensitivity core.

PD identifies result-changing distinctions relative to an admitted case set,
result map/equivalence, and one or more explicit coordinate representations.
Unknown or absent semantic bindings remain OPEN.
"""
from __future__ import annotations
from itertools import combinations
from typing import Any, Callable, Mapping

def _callable(value:Any,name:str)->Callable:
    if not callable(value):
        raise TypeError(f"{name}_CALLABLE_REQUIRED")
    return value

def result_partition(cases,*,rho:Callable,approx:Callable):
    groups=[]
    for case in cases:
        result=rho(case)
        for group in groups:
            if approx(result,group["representative"]):
                group["cases"].append(case)
                break
        else:
            groups.append({"representative":result,"cases":[case]})
    return tuple(groups)

def minimal_sensitive_sets(cases,*,rho:Callable,approx:Callable,representation:Callable):
    cases=tuple(cases)
    values=[tuple(representation(case)) for case in cases]
    if not values:
        return ()
    width=len(values[0])
    if any(len(value)!=width for value in values):
        raise ValueError("PD_REPRESENTATION_ARITY_DRIFT")

    sensitive=[]
    # Include J=empty.  It witnesses a representation collapse when two cases
    # have identical represented coordinates but different protected results.
    for size in range(0,width+1):
        for J_tuple in combinations(range(width),size):
            J=frozenset(J_tuple)
            if any(set(prev).issubset(J) for prev in sensitive):
                continue
            outside=tuple(i for i in range(width) if i not in J)
            found=False
            for i,left in enumerate(cases):
                for j in range(i+1,len(cases)):
                    right=cases[j]
                    if (
                        all(values[i][k]==values[j][k] for k in outside)
                        and not approx(rho(left),rho(right))
                    ):
                        found=True
                        break
                if found:
                    break
            if found:
                sensitive.append(tuple(sorted(J)))
    return tuple(sensitive)

def run_pd(
    cases,
    *,
    rho:Callable,
    approx:Callable,
    representations:Mapping[str,Callable],
)->dict[str,Any]:
    """Recover quotient result classes, fibers, and representation-relative MinSens."""
    cases=tuple(cases)
    rho=_callable(rho,"PD_RHO")
    approx=_callable(approx,"PD_APPROX")
    if not isinstance(representations,Mapping) or not representations:
        return {"status":"OPEN","blocker":"PD_REPRESENTATION_REQUIRED","result":None}

    reps={}
    for name,fn in representations.items():
        reps[str(name)]=_callable(fn,f"PD_REPRESENTATION_{name}")

    groups=result_partition(cases,rho=rho,approx=approx)
    minimal={
        name:minimal_sensitive_sets(cases,rho=rho,approx=approx,representation=fn)
        for name,fn in reps.items()
    }
    delta=tuple(
        (left,right)
        for i,left in enumerate(cases)
        for right in cases[i+1:]
        if not approx(rho(left),rho(right))
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
