"""Native contract-relative architecture-analysis semantic core."""
from __future__ import annotations
from typing import Any, Callable, Mapping, Iterable

# I. Architecture contract and input normalization.
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
    if isinstance(value, Mapping):
        raise ValueError("UNIT_JOB_IDENTITIES_REQUIRED")
    try:
        jobs=tuple(value)
    except TypeError as exc:
        raise ValueError("UNIT_JOB_IDENTITIES_REQUIRED") from exc
    if any(not isinstance(job,str) for job in jobs):
        raise ValueError("UNIT_JOB_IDENTITIES_REQUIRED")
    return tuple(dict.fromkeys(job for job in jobs if job))

def _unit_ids(value:Any)->set[str]:
    if not isinstance(value,(list,tuple,set,frozenset)) or any(
        not isinstance(x,str) or not x.strip() for x in value
    ):
        raise ValueError("UNIT_ID_COLLECTION_REQUIRED")
    return set(value)


# II. Native protected-constraint checks.
def _unit_job_failure(result, exceptions, expected_units):
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
    try:
        reported_exceptions=_unit_ids(result.get("UnitJobExceptions",()))
    except ValueError:
        return {"status":"OPEN","blocker":"ARCHITECTURE_UNIT_JOB_EXCEPTIONS_INVALID","result":result}
    if reported_exceptions-exceptions:
        return {"status":"OPEN","blocker":"ARCHITECTURE_UNIT_JOB_EXCEPTIONS_UNAUTHORIZED:"+",".join(sorted(reported_exceptions-exceptions)),"result":result}
    if any(not isinstance(uid,str) or not uid.strip() for uid in unit_jobs):
        return {"status":"OPEN","blocker":"ARCHITECTURE_UNIT_JOB_IDS_INVALID","result":result}
    if expected_units is not None:
        observed=set(unit_jobs)
        if observed!=expected_units or len(observed)!=len(unit_jobs):
            return {"status":"OPEN","blocker":"ARCHITECTURE_UNIT_JOB_INVENTORY_MISMATCH","result":result,
                    "missing_units":tuple(sorted(expected_units-observed)),
                    "unexpected_units":tuple(sorted(observed-expected_units))}
    bad=[]
    for unit_id,raw_jobs in unit_jobs.items():
        uid=str(unit_id)
        if uid in exceptions:
            continue
        try:
            jobs=_normalized_jobs(raw_jobs)
        except ValueError:
            return {"status":"OPEN","blocker":"ARCHITECTURE_UNIT_JOB_IDENTITIES_INVALID:"+uid,"result":result}
        if len(jobs)>1:
            bad.append(uid+"="+"/".join(jobs))
    if bad:
        return {
            "status":"OPEN",
            "blocker":"ARCHITECTURE_UNIT_JOB_PURITY_VIOLATION:"+",".join(bad),
            "result":result,
        }
    return None


def _protected_constraint_failure(result, remaining):
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
    return None


# III. Final architecture disposition.
def _architecture_status(result):
    boundary=result["OpenConflictBlocked"]
    if boundary:
        if isinstance(boundary,Mapping):
            labels={str(boundary.get(k,"")).upper() for k in ("status","state","disposition")}
            labels.update(str(k).upper() for k,v in boundary.items() if v and str(k).upper() in {"OPEN","BLOCKED","CONFLICT"})
        elif isinstance(boundary,(list,tuple,set,frozenset)):
            labels={str(x).upper() for x in boundary}
        else:
            labels={str(boundary).upper()}
        if "CONFLICT" in labels:
            status="CONFLICT"
        elif "BLOCKED" in labels:
            status="BLOCKED"
        else:
            status="OPEN"
    else:
        status="RELATIVE_CLOSE"

    return status

# IV. Native architecture analysis orchestration.
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

    protected=tuple(dict.fromkeys(str(x) for x in protected_constraints if str(x)))
    # Freeze governing authority before invoking the external analyzer. The
    # optional contract fields are UnitJobExceptions and ExpectedUnitIds.
    exceptions=set()
    expected_units=None
    if UNIT_JOB_PURITY in protected and isinstance(contract,Mapping):
        try:
            exceptions=_unit_ids(contract.get("UnitJobExceptions",()))
            if "ExpectedUnitIds" in contract:
                expected_units=_unit_ids(contract["ExpectedUnitIds"])
        except ValueError:
            return {"status":"BLOCKED","blocker":"ARCHITECTURE_UNIT_JOB_CONTRACT_INVALID","result":None}

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

    native_preserved=set()

    if UNIT_JOB_PURITY in protected:
        failure=_unit_job_failure(result,exceptions,expected_units)
        if failure is not None:
            return failure
        native_preserved.add(UNIT_JOB_PURITY)

    remaining=tuple(x for x in protected if x not in native_preserved)
    failure=_protected_constraint_failure(result,remaining)
    if failure is not None:
        return failure

    return {"status":_architecture_status(result),"result":result}
