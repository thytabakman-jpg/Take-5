"""Native MTA semantic core.

This module realizes the current MTA nucleus without absorbing shared wrapper,
closure, recurrence, or controller semantics. Domain-specific semantic work is
supplied explicitly by typed callables and missing bindings fail closed.
"""
from __future__ import annotations
from typing import Any, Callable, Mapping

REQUIRED_OUTPUTS=(
    "Model","Findings","FactorBasis","Residual","MaterialDeltas",
    "DiscoveryDeltas","NewOrChangedObjects","Evidence","Coverage",
    "VerificationObligations","OPEN",
)

def _required_callable(value:Any,name:str)->Callable:
    if not callable(value):
        raise TypeError(f"{name}_CALLABLE_REQUIRED")
    return value

def run_mta(
    target:Any,
    shared_math:Any,
    evidence:Any,
    contract:Any,
    *,
    generate_structural_hypotheses:Callable,
    select_analysis_package:Callable,
    reconstruct_protected_model:Callable,
)->dict[str,Any]:
    """MTA_sem=<GenerateStructuralHypotheses,SelectAnalysisPackage,ReconstructProtectedModel>."""
    generate=_required_callable(generate_structural_hypotheses,"MTA_GENERATOR")
    select=_required_callable(select_analysis_package,"MTA_SELECTOR")
    reconstruct=_required_callable(reconstruct_protected_model,"MTA_RECONSTRUCTOR")

    hypotheses=generate(target,shared_math,evidence,contract)
    package=select(target,hypotheses,shared_math,evidence,contract)
    raw=reconstruct(target,hypotheses,package,shared_math,evidence,contract)

    if not isinstance(raw,Mapping):
        return {"status":"BLOCKED","blocker":"MTA_INVALID_RETURN","result":raw}

    result=dict(raw)
    missing=tuple(k for k in REQUIRED_OUTPUTS if k not in result)
    if missing:
        return {
            "status":"OPEN",
            "blocker":"MTA_OUTPUT_MISSING:"+",".join(missing),
            "result":result,
        }

    return {
        "status":"OPEN" if bool(result["OPEN"]) else "RELATIVE_CLOSE",
        "result":result,
        "hypotheses":hypotheses,
        "analysis_package":package,
    }
