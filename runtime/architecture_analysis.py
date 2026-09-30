"""Native contract-relative architecture-analysis semantic core."""
from __future__ import annotations
from typing import Any, Callable, Mapping, Iterable

REQUIRED_OUTPUTS=(
    "ArchClass","Violations","LocalizationFamilies","DependencyState",
    "InteractionState","TransformationFrontier","SuccessorFrontier",
    "Coverage","OpenConflictBlocked","Provenance",
)

UNIT_JOB_PURITY="UNIT_JOB_PURITY"


def _normalized_jobs(value:Any)->tuple[str,...]:
    if value is None:
        return ()
    if isinstance(value,str):
        return (value,) if value else ()
    try:
        return tuple(dict.fromkeys(str(x) for x in value if str(x)))
    except TypeError:
        return (str(value),)

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
    native_preserved=set()

    if UNIT_JOB_PURITY in protected:
        unit_jobs=result.get("UnitJobState")
        if not isinstance(unit_jobs,Mapping):
            return {
                "status":"OPEN",
                "blocker":"ARCHITECTURE_UNIT_JOB_STATE_MISSING",
                "result":result,
            }
        unit_job_evidence=result.get("UnitJobEvidence")
        if not unit_job_evidence:
            return {
                "status":"OPEN",
                "blocker":"ARCHITECTURE_UNIT_JOB_EVIDENCE_MISSING",
                "result":result,
            }
        exceptions={
            str(x) for x in result.get("UnitJobExceptions",()) if str(x)
        }
        bad=[]
        for unit_id,raw_jobs in unit_jobs.items():
            uid=str(unit_id)
            if uid in exceptions:
                continue
            jobs=_normalized_jobs(raw_jobs)
            if len(jobs)>1:
                bad.append(uid+"="+"/".join(jobs))
        if bad:
            return {
                "status":"OPEN",
                "blocker":"ARCHITECTURE_UNIT_JOB_PURITY_VIOLATION:"+",".join(bad),
                "result":result,
            }
        native_preserved.add(UNIT_JOB_PURITY)

    remaining=tuple(x for x in protected if x not in native_preserved)
    if remaining:
        state=result.get("ProtectedConstraintState")
        if not isinstance(state,Mapping):
            return {
                "status":"OPEN",
                "blocker":"ARCHITECTURE_PROTECTED_CONSTRAINT_STATE_MISSING",
                "result":result,
            }
        bad=[]
        for constraint_id in remaining:
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
