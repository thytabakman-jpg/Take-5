"""Parent-level user-return gate for ImprovementCore.

A completed child, work package, tool run, HF2 local fixed point, or material
strict-gain step is not sufficient to end the governing ImprovementCore job.

For COMPLETE, the gate now requires two independent coordinates:

1. fresh whole-job stability: regenerate/re-observe the normalized state from a
   fresh challenge context and require repeated no-delta passes;
2. semantic return verification: goal closed, no owned work, consequences closed,
   evidence bound, and any formal-currentness claims admission-closed.

A material fresh challenge forces a complete parent re-entry.  Missing fresh
re-observation fails OPEN.  This prevents "HF2 locally stopped" from being
misreported as "a brand-new overview would find nothing."
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Callable, Mapping

from whole_job_stability import run_whole_job_stability, receipt_dict as stability_receipt_dict

RETURNABLE={"COMPLETE","OPEN","BLOCKED","CONFLICT"}
DISPOSITIONS={"RETURN","CONTINUE"}


def _authoritative_formal_claims_present(state:Mapping[str,Any])->bool:
    raw=state.get("authoritative_formal_claims",None)
    if raw is None:
        return False
    if isinstance(raw,Mapping):
        return True
    if isinstance(raw,(list,tuple)):
        return bool(raw)
    return True


def _unclosed_authoritative_formal_claims(state:Mapping[str,Any])->tuple[str,...]:
    raw=state.get("authoritative_formal_claims",())
    if isinstance(raw,Mapping):
        raw=(raw,)
    if not isinstance(raw,(list,tuple)):
        return ("INVALID_AUTHORITATIVE_FORMAL_CLAIMS",)
    residuals=[]
    for i,row in enumerate(raw):
        if not isinstance(row,Mapping):
            residuals.append(f"INVALID_FORMAL_CLAIM_RECEIPT:{i}")
            continue
        status=str(row.get("status","")).upper()
        if status!="PASS":
            object_id=str(row.get("root_object_id") or row.get("object_id") or i)
            residuals.append(f"FORMAL_CLAIM_NOT_PASS:{object_id}:{status or 'MISSING'}")
            for item in row.get("residuals",()):
                residuals.append(f"FORMAL_CLAIM_RESIDUAL:{object_id}:{item}")
    return tuple(residuals)


@dataclass(frozen=True)
class ParentReturnOutcome:
    disposition:str
    terminal:str
    blocker:str|None
    next_state:dict[str,Any]
    next_memory:dict[str,Any]
    receipt:dict[str,Any]


def _mapping(value:Any, name:str)->dict[str,Any]:
    if value is None:
        return {}
    if not isinstance(value,Mapping):
        raise RuntimeError(f"IC_PARENT_RETURN_GATE_INVALID_{name.upper()}")
    return dict(value)


def evaluate_parent_return(
    *,
    candidate_status:str,
    candidate_blocker:str|None,
    state:Mapping[str,Any],
    memory:Mapping[str,Any]|None,
    context:Mapping[str,Any],
    verifier:Callable[[dict[str,Any],dict[str,Any],dict[str,Any]],Mapping[str,Any]]|None,
    fresh_reobserve:Callable[[dict[str,Any],dict[str,Any],dict[str,Any]],Mapping[str,Any]]|None=None,
    stable_passes_required:int=2,
)->ParentReturnOutcome:
    """Validate whole-job completion and user-return permission.

    COMPLETE is impossible from the pre-existing parent state alone.  It must
    survive a fresh whole-job re-observation challenge first.  Any material
    challenge delta or owned work returns CONTINUE and forces a new full parent
    ImprovementCore+HF2 round.

    Non-complete candidates preserve their typed terminal status and continue to
    use the semantic verifier for legal return.
    """
    z=dict(state)
    m=dict(memory or {})
    ctx=dict(context)
    stability_receipt=None

    if str(candidate_status).upper()=="COMPLETE":
        stability=run_whole_job_stability(
            state=z,
            memory=m,
            context=ctx,
            reobserve=fresh_reobserve,
            stable_passes_required=int(stable_passes_required),
        )
        stability_receipt=stability_receipt_dict(stability)
        z=dict(stability.state)
        m=dict(stability.memory)

        if stability.disposition=="CONTINUE":
            return ParentReturnOutcome(
                disposition="CONTINUE",
                terminal="CONTINUE",
                blocker=None,
                next_state=z,
                next_memory=m,
                receipt={
                    "gate":"PARENT_RETURN_GATE",
                    "disposition":"CONTINUE",
                    "candidate_status":str(candidate_status),
                    "candidate_blocker":candidate_blocker,
                    "reason":"FRESH_WHOLE_JOB_DELTA",
                    "whole_job_stability":stability_receipt,
                    "context":ctx,
                },
            )

        if stability.terminal!="COMPLETE":
            return ParentReturnOutcome(
                disposition="RETURN",
                terminal=stability.terminal,
                blocker=stability.blocker,
                next_state=z,
                next_memory=m,
                receipt={
                    "gate":"PARENT_RETURN_GATE",
                    "disposition":"RETURN",
                    "candidate_status":str(candidate_status),
                    "candidate_blocker":candidate_blocker,
                    "reason":"FRESH_WHOLE_JOB_NONCLOSURE",
                    "whole_job_stability":stability_receipt,
                    "context":ctx,
                },
            )

    if verifier is None:
        z["terminal"]="OPEN"
        z["admitted_continuation"]=False
        z["parent_return_continuation"]=False
        if "live_continuation" in z:
            z["live_continuation"]=False
        return ParentReturnOutcome(
            disposition="RETURN",
            terminal="OPEN",
            blocker="PARENT_RETURN_GATE_REQUIRED",
            next_state=z,
            next_memory=m,
            receipt={
                "gate":"PARENT_RETURN_GATE",
                "status":"OPEN",
                "reason":"NO_RETURN_VERIFIER",
                "candidate_status":str(candidate_status),
                "whole_job_stability":stability_receipt,
            },
        )

    raw=verifier(dict(z),dict(m),dict(ctx))
    if not isinstance(raw,Mapping):
        raise RuntimeError("IC_PARENT_RETURN_GATE_INVALID_DECISION")
    decision=dict(raw)

    disposition=str(decision.get("disposition","")).upper()
    if disposition not in DISPOSITIONS:
        raise RuntimeError("IC_PARENT_RETURN_GATE_INVALID_DISPOSITION")

    owned=bool(decision.get("owned_work_remaining",False))
    consequence_closed=bool(decision.get("consequence_closed",False))
    goal_closed=bool(decision.get("goal_closed",False))
    recheck=bool(decision.get("recheck_required",False))
    evidence=tuple(str(x) for x in decision.get("evidence",()) if str(x))
    state_patch=_mapping(decision.get("state_patch"),"state_patch")
    memory_patch=_mapping(decision.get("memory_patch"),"memory_patch")

    proposed_state={**z,**state_patch}
    formal_claims_present=_authoritative_formal_claims_present(proposed_state)
    formal_claim_residuals=_unclosed_authoritative_formal_claims(proposed_state)
    formal_claim_receipt_required=bool(ctx.get("formal_claim_receipt_required",False))

    receipt={
        "gate":"PARENT_RETURN_GATE",
        "disposition":disposition,
        "candidate_status":str(candidate_status),
        "candidate_blocker":candidate_blocker,
        "goal_closed":goal_closed,
        "owned_work_remaining":owned,
        "consequence_closed":consequence_closed,
        "recheck_required":recheck,
        "evidence":evidence,
        "reason":str(decision.get("reason","")),
        "context":ctx,
        "whole_job_stability":stability_receipt,
        "formal_claim_receipt_required":formal_claim_receipt_required,
        "authoritative_formal_claims_present":formal_claims_present,
        "authoritative_formal_claim_residuals":formal_claim_residuals,
    }

    if disposition=="CONTINUE":
        if not (owned or recheck):
            raise RuntimeError(
                "IC_PARENT_RETURN_GATE_CONTINUE_WITHOUT_LIVE_WORK_OR_RECHECK"
            )
        next_state={**z,**state_patch}
        next_memory={**m,**memory_patch}
        next_state["terminal"]="CONTINUE"
        next_state["admitted_continuation"]=True
        next_state["parent_return_continuation"]=True
        return ParentReturnOutcome(
            disposition="CONTINUE",
            terminal="CONTINUE",
            blocker=None,
            next_state=next_state,
            next_memory=next_memory,
            receipt=receipt,
        )

    terminal=str(decision.get("terminal") or candidate_status).upper()
    if terminal not in RETURNABLE:
        raise RuntimeError("IC_PARENT_RETURN_GATE_INVALID_RETURN_TERMINAL")
    candidate=str(candidate_status).upper()
    if candidate in {"OPEN","BLOCKED","CONFLICT"} and terminal!=candidate:
        raise RuntimeError("IC_PARENT_RETURN_GATE_ILLEGAL_TERMINAL_UPGRADE")
    if owned:
        raise RuntimeError("IC_PARENT_RETURN_GATE_RETURN_WITH_OWNED_WORK")
    if not consequence_closed:
        raise RuntimeError("IC_PARENT_RETURN_GATE_RETURN_WITH_OPEN_CONSEQUENCE")
    if not evidence:
        raise RuntimeError("IC_PARENT_RETURN_GATE_RETURN_WITHOUT_EVIDENCE")
    if terminal=="COMPLETE" and not goal_closed:
        raise RuntimeError("IC_PARENT_RETURN_GATE_COMPLETE_WITHOUT_GOAL_CLOSURE")
    if terminal=="COMPLETE" and stability_receipt is None:
        raise RuntimeError(
            "IC_PARENT_RETURN_GATE_COMPLETE_WITHOUT_FRESH_STABILITY_RECEIPT"
        )
    if terminal=="COMPLETE" and formal_claim_receipt_required and not formal_claims_present:
        raise RuntimeError(
            "IC_PARENT_RETURN_GATE_COMPLETE_WITHOUT_FORMAL_CLAIM_RECEIPT"
        )
    if terminal=="COMPLETE" and formal_claim_residuals:
        raise RuntimeError(
            "IC_PARENT_RETURN_GATE_COMPLETE_WITH_UNCLOSED_AUTHORITATIVE_FORMAL_CLAIM"
        )

    blocker=decision.get("blocker") or candidate_blocker
    if terminal in {"OPEN","BLOCKED","CONFLICT"} and not blocker:
        raise RuntimeError("IC_PARENT_RETURN_GATE_NONCOMPLETE_WITHOUT_BLOCKER")

    next_state={**z,**state_patch}
    next_memory={**m,**memory_patch}
    next_state["terminal"]=terminal
    next_state["admitted_continuation"]=False
    next_state["parent_return_continuation"]=False
    if "live_continuation" not in state_patch:
        next_state["live_continuation"]=False

    return ParentReturnOutcome(
        disposition="RETURN",
        terminal=terminal,
        blocker=None if terminal=="COMPLETE" else str(blocker),
        next_state=next_state,
        next_memory=next_memory,
        receipt=receipt,
    )


def receipt_dict(outcome:ParentReturnOutcome)->dict[str,Any]:
    return asdict(outcome)
