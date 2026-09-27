"""Native PDAudit 1.1 fixed-frame evaluator plus current audit controls."""
from __future__ import annotations
from typing import Any, Callable, Mapping
from pd import run_pd

def run_pd_audit(
    cases,
    *,
    rho:Callable,
    approx:Callable,
    representations:Mapping[str,Callable],
    kappa_cases:Callable|None=None,
    kappa_representations:Callable|None=None,
)->dict[str,Any]:
    """PDAudit_1.1=<R_T,Fib_rho,{lambda,MinSens_lambda},kappa_A,kappa_Lambda>."""
    base=run_pd(cases,rho=rho,approx=approx,representations=representations)
    if base["status"]!="RELATIVE_CLOSE":
        return base

    cases=tuple(cases)
    result=dict(base["result"])
    if kappa_cases is not None and not callable(kappa_cases):
        raise TypeError("PDAUDIT_KAPPA_A_CALLABLE_REQUIRED")
    if kappa_representations is not None and not callable(kappa_representations):
        raise TypeError("PDAUDIT_KAPPA_LAMBDA_CALLABLE_REQUIRED")

    result.update({
        "kappa_A":None if kappa_cases is None else kappa_cases(cases),
        "kappa_Lambda":None if kappa_representations is None else kappa_representations(representations),
        "raw_output_immutable":True,
        "normalization_separate":True,
        "analytic_eligibility_separate_from_governance":True,
        "zero_incremental_yield_visible":True,
    })
    return {"status":"RELATIVE_CLOSE","result":result}
