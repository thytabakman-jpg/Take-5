"""Parent-level user-return gate for ImprovementCore.

A completed child, work package, tool run, HF2 local fixed point, or material
strict-gain step is not sufficient to end the governing ImprovementCore job.

The parent may return to the user only after a fresh post-HF2 verifier
dispositions the whole governing job.  A verifier may instead return CONTINUE;
the caller must then re-enter the complete ImprovementCore capability, including
its normal HF2 layer, on the updated state.

This module validates the verifier's claim.  It does not invent semantic
closure on behalf of the active host/model.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Callable, Mapping

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


def _reachable_recoverable_open(state:Mapping[str,Any])->tuple[dict[str,Any],...]:
    """Return result-sensitive OPEN residuals with an explicit reachable recovery route.

    A residual is parent-owned recovery work only when the semantic producer has
    supplied the route.  The gate does not invent tools or authority.
    """
    raw=state.get("open_residuals",())
    if isinstance(raw,Mapping):
        raw=(raw,)
    if not isinstance(raw,(list,tuple)):
        return ()
    out=[]
    for row in raw:
        if not isinstance(row,Mapping):
            continue
        if not bool(row.get("result_sensitive",True)):
            continue
        if not bool(row.get("reachable",False)):
            continue
        route=str(row.get("recovery_route","")).strip()
        if not route:
            continue
        out.append({
            "residual_id":str(row.get("residual_id") or row.get("id") or route),
            "recovery_route":route,
            "owner":str(row.get("owner","ImprovementCore")),
            "authority_ref":row.get("authority_ref"),
        })
    return tuple(out)


def _unclosed_authoritative_formal_claims(state:Mapping[str,Any])->tuple[str,...]:
    """Return authoritative formal claims that are not admission-closed.

    The active semantic provider may attach these receipts only when the
    governing job makes a CURRENT/CANONICAL/EXACT_CURRENT formal claim.  Their
    absence creates no obligation for ordinary jobs.  Once present, however, a
    non-PASS receipt forbids COMPLETE user return.
    """
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
)->ParentReturnOutcome:
    """Validate a whole-job return/continue decision.

    Required RETURN claims:
    - consequence_closed=True
    - owned_work_remaining=False
    - non-empty evidence
    - COMPLETE additionally requires goal_closed=True
    - OPEN/BLOCKED/CONFLICT require a typed blocker

    CONTINUE claims require owned_work_remaining=True or recheck_required=True.
    The gate clears terminality and reactivates parent continuation before
    handing state back for a fresh complete ImprovementCore+HF2 pass.
    """
    z=dict(state)
    m=dict(memory or {})
    ctx=dict(context)

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

    recoverable_open=_reachable_recoverable_open(proposed_state)

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
        "formal_claim_receipt_required":formal_claim_receipt_required,
        "authoritative_formal_claims_present":formal_claims_present,
        "authoritative_formal_claim_residuals":formal_claim_residuals,
        "recoverable_open":recoverable_open,
    }

    # A result-sensitive OPEN with a declared reachable recovery route is not a
    # terminal external boundary.  It becomes parent-owned work and re-enters
    # the complete ImprovementCore capability before any user return.
    if disposition=="RETURN" and recoverable_open:
        next_state={**z,**state_patch}
        next_memory={**m,**memory_patch}
        next_state["terminal"]="CONTINUE"
        next_state["admitted_continuation"]=True
        next_state["parent_return_continuation"]=True
        next_state["owned_recovery_work"]=recoverable_open
        receipt["disposition"]="CONTINUE"
        receipt["forced_recovery_reentry"]=True
        receipt["reason"]="REACHABLE_RESULT_SENSITIVE_OPEN"
        return ParentReturnOutcome(
            disposition="CONTINUE",
            terminal="CONTINUE",
            blocker=None,
            next_state=next_state,
            next_memory=next_memory,
            receipt=receipt,
        )

    if disposition=="CONTINUE":
        if not (owned or recheck):
            raise RuntimeError(
                "IC_PARENT_RETURN_GATE_CONTINUE_WITHOUT_LIVE_WORK_OR_RECHECK"
            )
        next_state={**z,**state_patch}
        next_memory={**m,**memory_patch}
        next_state["terminal"]="CONTINUE"
        next_state["admitted_continuation"]=True
        # Parent-level continuation is not the same coordinate as recursive
        # child-manager liveness.  The verifier may set live_continuation
        # explicitly in state_patch when recursive child work is in fact live.
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
