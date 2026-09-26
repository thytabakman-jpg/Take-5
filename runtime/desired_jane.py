"""Recover the user's desired Jane contract from explicit evidence.

This tool answers a role-design question. It does not redesign Jane by itself and it
does not treat recency, repetition, or attractive wording as authority.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

class DesireStatus(str,Enum):
    REQUIRED="REQUIRED"
    PROHIBITED="PROHIBITED"
    OPEN="OPEN"
    CONFLICT="CONFLICT"

@dataclass(frozen=True)
class DesireEvidence:
    coordinate:str
    polarity:str
    source_ref:str
    statement:str

@dataclass(frozen=True)
class DesireDisposition:
    coordinate:str
    status:DesireStatus
    grounds:tuple[str,...]
    source_refs:tuple[str,...]

@dataclass(frozen=True)
class DesiredJaneContract:
    required:tuple[str,...]
    prohibited:tuple[str,...]
    open:tuple[str,...]
    conflicts:tuple[str,...]
    dispositions:tuple[DesireDisposition,...]

VALID_POLARITIES={"WANT","DO_NOT_WANT","UNKNOWN"}

def recover_desired_jane(evidence:Iterable[DesireEvidence])->DesiredJaneContract:
    rows={}
    for e in evidence:
        if e.polarity not in VALID_POLARITIES:
            raise ValueError(f"INVALID_POLARITY:{e.polarity}")
        rows.setdefault(e.coordinate,[]).append(e)

    dispositions=[]
    for coordinate in sorted(rows):
        xs=rows[coordinate]
        wants=[x for x in xs if x.polarity=="WANT"]
        avoids=[x for x in xs if x.polarity=="DO_NOT_WANT"]
        unknown=[x for x in xs if x.polarity=="UNKNOWN"]

        if wants and avoids:
            status=DesireStatus.CONFLICT
            grounds=tuple(x.statement for x in wants+avoids)
            refs=tuple(dict.fromkeys(x.source_ref for x in wants+avoids))
        elif wants:
            status=DesireStatus.REQUIRED
            grounds=tuple(x.statement for x in wants)
            refs=tuple(dict.fromkeys(x.source_ref for x in wants))
        elif avoids:
            status=DesireStatus.PROHIBITED
            grounds=tuple(x.statement for x in avoids)
            refs=tuple(dict.fromkeys(x.source_ref for x in avoids))
        else:
            status=DesireStatus.OPEN
            grounds=tuple(x.statement for x in unknown)
            refs=tuple(dict.fromkeys(x.source_ref for x in unknown))

        dispositions.append(DesireDisposition(coordinate,status,grounds,refs))

    required=tuple(x.coordinate for x in dispositions if x.status==DesireStatus.REQUIRED)
    prohibited=tuple(x.coordinate for x in dispositions if x.status==DesireStatus.PROHIBITED)
    open_items=tuple(x.coordinate for x in dispositions if x.status==DesireStatus.OPEN)
    conflicts=tuple(x.coordinate for x in dispositions if x.status==DesireStatus.CONFLICT)
    return DesiredJaneContract(required,prohibited,open_items,conflicts,tuple(dispositions))

def assertion_safe(contract:DesiredJaneContract)->bool:
    """A design contract is assertion-safe only when no live coordinate conflicts."""
    return not contract.conflicts


# Frozen first-run evidence recovered from the user's repeated Jane/ICC design directives.
# These rows are evidence for the current DesiredJane instance, not universal Jane semantics.
TZVI_JANE_EVIDENCE=(
    DesireEvidence("direct_conversation_interface","WANT","user-history","Jane is the direct user-facing entry into ICC rather than a competing interpretation layer."),
    DesireEvidence("entry_state_reconstruction","WANT","user-history","Jane recovers target, job, constraints, relevant state and finish conditions instead of making the user restate them."),
    DesireEvidence("canonical_currentness_bootstrap","WANT","user-history","Jane starts from current authoritative Take-5 state instead of stale chat reconstruction."),
    DesireEvidence("continuity_supervision","WANT","user-history","Jane preserves continuity across turns, chats, tools, versions and admitted deltas."),
    DesireEvidence("question_frontier_supervision","WANT","user-history","Jane notices unresolved questions and hands them into the active work system."),
    DesireEvidence("capability_visibility","WANT","user-history","Jane knows what capabilities exist and exposes relevant capability coverage to ICC."),
    DesireEvidence("delegation_packaging","WANT","user-history","Jane packages work and handoffs while authority remains typed."),
    DesireEvidence("admitted_delta_sync","WANT","user-history","Jane synchronizes only admitted material continuity-relevant deltas."),
    DesireEvidence("discovery_to_work_bridge","WANT","user-history","Jane helps turn discoveries into cumulative system work so the user is not the scheduler and reentry trigger."),
    DesireEvidence("automatic_reentry_support","WANT","user-history","Jane preserves and surfaces the need to reenter when material state, representation, question or currentness changes."),
    DesireEvidence("short_faithful_external_surface","WANT","user-history","Jane returns a short faithful user-facing result rather than dumping internal machinery."),
    DesireEvidence("primary_problem_solver","DO_NOT_WANT","user-history","Jane is not a second ICC or a competing solver."),
    DesireEvidence("primary_action_selection","DO_NOT_WANT","user-history","IC/ICC owns adaptive action and tool selection while it holds the controller lease."),
    DesireEvidence("self_authorization","DO_NOT_WANT","user-history","Jane does not turn evidence, relevance or continuity into new authority."),
    DesireEvidence("silent_math_redefinition","DO_NOT_WANT","user-history","Jane preserves frozen mathematics and cannot silently redefine other system factors."),
    DesireEvidence("silent_currentness_claim","DO_NOT_WANT","user-history","Jane does not claim stale or merely persisted state is current."),
)

def what_tzvi_wants_jane_to_be()->DesiredJaneContract:
    return recover_desired_jane(TZVI_JANE_EVIDENCE)
