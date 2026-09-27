"""Fresh whole-job stability challenge.

Local tool/HF2 saturation is not whole-job closure.  Before a COMPLETE parent
return, re-observe the normalized governing state from a fresh challenge context.
A material result/search/discovery/representation/authority/execution delta forces
parent continuation.  Two consecutive fresh no-delta observations are required by
default so "run it again from the top" is executable closure evidence rather than
an informal promise.

The callback remains semantic-host supplied.  Missing semantic re-observation
fails OPEN rather than converting local saturation into global completion.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Callable, Mapping

MATERIAL_KEYS=(
    "material_result_delta",
    "material_search_delta",
    "material_discovery_delta",
    "open_refinement",
    "changed_representation",
    "changed_authority",
    "execution_truth_strengthened",
    "new_question",
    "new_relation",
    "new_capability",
    "new_reachable_work",
)

NONCOMPLETE={"OPEN","BLOCKED","CONFLICT"}


@dataclass(frozen=True)
class FreshChallengeReceipt:
    index:int
    status:str
    material:bool
    owned_work_remaining:bool
    evidence:tuple[str,...]
    challenge_id:str
    state_patch:dict[str,Any]
    memory_patch:dict[str,Any]


@dataclass(frozen=True)
class WholeJobStabilityResult:
    disposition:str
    terminal:str
    blocker:str|None
    state:dict[str,Any]
    memory:dict[str,Any]
    receipts:tuple[FreshChallengeReceipt,...]


def _mapping(value:Any,name:str)->dict[str,Any]:
    if value is None:
        return {}
    if not isinstance(value,Mapping):
        raise RuntimeError("WHOLE_JOB_STABILITY_INVALID_"+name.upper())
    return dict(value)


def run_whole_job_stability(
    *,
    state:Mapping[str,Any],
    memory:Mapping[str,Any]|None,
    context:Mapping[str,Any],
    reobserve:Callable[[dict[str,Any],dict[str,Any],dict[str,Any]],Mapping[str,Any]]|None,
    stable_passes_required:int=2,
    max_passes:int=6,
)->WholeJobStabilityResult:
    """Require repeated fresh no-delta re-observation before COMPLETE.

    Each challenge receives the current normalized state and persistent memory,
    plus reset_ephemeral=True in context.  The semantic provider is responsible
    for rebuilding the whole-job question/work frontier rather than reusing the
    prior local selection trace.

    Any material delta or owned executable work returns CONTINUE immediately so
    the complete parent ImprovementCore+HF2 path can consume it.
    """
    z=dict(state)
    m=dict(memory or {})
    ctx=dict(context)

    if reobserve is None:
        return WholeJobStabilityResult(
            "RETURN","OPEN","FRESH_WHOLE_JOB_REOBSERVATION_REQUIRED",z,m,()
        )
    if stable_passes_required < 1:
        raise ValueError("WHOLE_JOB_STABILITY_STABLE_PASSES_REQUIRED")
    if max_passes < stable_passes_required:
        raise ValueError("WHOLE_JOB_STABILITY_MAX_PASSES_TOO_SMALL")

    receipts=[]
    stable=0
    for index in range(max_passes):
        challenge_context={
            **ctx,
            "whole_job_fresh_challenge":True,
            "reset_ephemeral":True,
            "challenge_index":index,
            "stable_passes_required":int(stable_passes_required),
        }
        raw=reobserve(dict(z),dict(m),challenge_context)
        if not isinstance(raw,Mapping):
            raise RuntimeError("WHOLE_JOB_STABILITY_INVALID_REOBSERVATION")
        row=dict(raw)
        status=str(row.get("status","STABLE")).upper()
        evidence=tuple(str(x) for x in row.get("evidence",()) if str(x))
        if not evidence:
            raise RuntimeError("WHOLE_JOB_STABILITY_EVIDENCE_REQUIRED")
        state_patch=_mapping(row.get("state_patch"),"state_patch")
        memory_patch=_mapping(row.get("memory_patch"),"memory_patch")
        owned=bool(row.get("owned_work_remaining",False))
        material=owned or any(bool(row.get(k)) for k in MATERIAL_KEYS)
        challenge_id=str(row.get("challenge_id") or f"fresh:{index}")

        receipt=FreshChallengeReceipt(
            index=index,
            status=status,
            material=material,
            owned_work_remaining=owned,
            evidence=evidence,
            challenge_id=challenge_id,
            state_patch=state_patch,
            memory_patch=memory_patch,
        )
        receipts.append(receipt)

        z={**z,**state_patch}
        m={**m,**memory_patch}

        if status in NONCOMPLETE:
            blocker=str(row.get("blocker") or f"FRESH_REOBSERVATION_{status}")
            z["terminal"]=status
            z["admitted_continuation"]=False
            z["parent_return_continuation"]=False
            return WholeJobStabilityResult(
                "RETURN",status,blocker,z,m,tuple(receipts)
            )

        if material:
            z["terminal"]="CONTINUE"
            z["admitted_continuation"]=True
            z["parent_return_continuation"]=True
            return WholeJobStabilityResult(
                "CONTINUE","CONTINUE",None,z,m,tuple(receipts)
            )

        if status not in {"STABLE","NO_GAIN","CLOSED_RELATIVE"}:
            raise RuntimeError("WHOLE_JOB_STABILITY_UNKNOWN_STATUS:"+status)

        stable += 1
        if stable >= stable_passes_required:
            return WholeJobStabilityResult(
                "STABLE","COMPLETE",None,z,m,tuple(receipts)
            )

    z["terminal"]="OPEN"
    z["admitted_continuation"]=False
    z["parent_return_continuation"]=False
    return WholeJobStabilityResult(
        "RETURN","OPEN","FRESH_WHOLE_JOB_STABILITY_RESOURCE_STOP",z,m,tuple(receipts)
    )


def receipt_dict(result:WholeJobStabilityResult)->dict[str,Any]:
    return {
        "disposition":result.disposition,
        "terminal":result.terminal,
        "blocker":result.blocker,
        "receipts":tuple(asdict(x) for x in result.receipts),
    }
