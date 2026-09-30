"""Native contract-relative architecture-analysis semantic core."""
from __future__ import annotations
from typing import Any, Callable, Mapping, Iterable

REQUIRED_OUTPUTS=(
    "ArchClass","Violations","LocalizationFamilies","DependencyState",
    "InteractionState","TransformationFrontier","SuccessorFrontier",
    "Coverage","OpenConflictBlocked","Provenance",
)

def run_architecture_analysis(
    architecture:Any,
    contract:Any,
    *,
    analyze_architecture:Callable[[Any,Any],Mapping[str,Any]],
    protected_constraints:Iterable[str]=(),
)->dict[str,Any]:
    """Return the current AA_K(A) carrier while preserving OPEN/CONFLICT/BLOCKED."""
    if not callable(analyze_architecture):
        raise TypeError("ARCHITECTURE_ANALYZER_CALLABLE_REQUIRED")

    raw=analyze_architecture(architecture,contract)
    if not isinstance(raw,Mapping):
        return {"status":"BLOCKED","blocker":"ARCHITECTURE_INVALID_RETURN","result":raw}

    result=dict(raw)
    missing=tuple(k for k in REQUIRED_OUTPUTS if k not in result)
    if missing:
        return {
            "status":"OPEN",
            "blocker":"ARCHITECTURE_OUTPUT_MISSING:"+",".join(missing),
            "result":result,
        }

    protected=tuple(dict.fromkeys(str(x) for x in protected_constraints if str(x)))
    if protected:
        state=result.get("ProtectedConstraintState")
        if not isinstance(state,Mapping):
            return {
                "status":"OPEN",
                "blocker":"ARCHITECTURE_PROTECTED_CONSTRAINT_STATE_MISSING",
                "result":result,
            }
        bad=[]
        for constraint_id in protected:
            status=str(state.get(constraint_id,"MISSING")).upper()
            if status not in {"PRESERVED","PASS","VERIFIED"}:
                bad.append(f"{constraint_id}:{status}")
        if bad:
            return {
                "status":"OPEN",
                "blocker":"ARCHITECTURE_PROTECTED_CONSTRAINT_UNPRESERVED:"+",".join(bad),
                "result":result,
            }

    boundary=result["OpenConflictBlocked"]
    if boundary:
        labels={str(x).upper() for x in boundary} if isinstance(boundary,(list,tuple,set,frozenset)) else {str(boundary).upper()}
        if "CONFLICT" in labels:
            status="CONFLICT"
        elif "BLOCKED" in labels:
            status="BLOCKED"
        else:
            status="OPEN"
    else:
        status="RELATIVE_CLOSE"

    return {"status":status,"result":result}
