"""Conversation entry contract for Take-5 / ICC turns.

The entry contract is bound before substantive controller work. It freezes the
external target, controller identity and initial mode so the host/interface
cannot silently drift into a different controller or begin goal-directed work
before an observer-first episode.

Mode selection is a preflight classification step, not substantive optimization.
It may select OBSERVE_DECOUPLED when the request itself creates contamination
risk, even if the user does not literally say "observer mode".
"""
from dataclasses import dataclass
from controller_lease import ControllerLease

ICC_CONTROLLER = "IC-028"
MODE_GOAL_DIRECTED = "GOAL_DIRECTED"
MODE_OBSERVE_DECOUPLED = "OBSERVE_DECOUPLED"

_ICC_ALIASES = (
    "icc",
    "improvement core",
    "improvecore",
)

_EXPLICIT_OBSERVER_ALIASES = (
    "observer mode",
    "observation mode",
    "observe first",
    "observer-first",
    "goal-decoupled",
    "goal decoupled",
    "dos",
)

# These are preflight contamination-risk markers, not substantive task answers.
# They encode the current DOS rule: inspect independently before optimization
# when the object/plan/system itself is being diagnosed or structurally examined.
_AUTO_OBSERVER_MARKERS = (
    "on itself",
    "self apply",
    "self-apply",
    "self application",
    "self-application",
    "root cause",
    "audit",
    "whole system",
    "architect",
    "architecture",
)

@dataclass(frozen=True)
class EntryContract:
    frozen_target:str
    controller:str
    initial_mode:str
    boundary:str|None
    authority:frozenset[str]
    receipt:str
    raw_request:str
    mode_basis:str

@dataclass(frozen=True)
class EntryBinding:
    contract:EntryContract
    lease:ControllerLease

def _norm(text):
    return " ".join(str(text).lower().replace("_"," ").split())

def resolve_controller(user_text, default=ICC_CONTROLLER):
    text=_norm(user_text)
    if any(alias in text for alias in _ICC_ALIASES):
        return ICC_CONTROLLER
    return default

def preflight_mode(user_text, *, observer_risk=None):
    """Classify only the initial control mode; do not solve/optimize the task."""
    text=_norm(user_text)
    if any(alias in text for alias in _EXPLICIT_OBSERVER_ALIASES):
        return MODE_OBSERVE_DECOUPLED,"EXPLICIT_OBSERVER"
    if observer_risk is True:
        return MODE_OBSERVE_DECOUPLED,"CALLER_CONTAMINATION_RISK"
    if observer_risk is False:
        return MODE_GOAL_DIRECTED,"CALLER_NO_CONTAMINATION_RISK"
    if any(marker in text for marker in _AUTO_OBSERVER_MARKERS):
        return MODE_OBSERVE_DECOUPLED,"PREFLIGHT_CONTAMINATION_RISK"
    return MODE_GOAL_DIRECTED,"PREFLIGHT_NO_CONTAMINATION_RISK"

def resolve_initial_mode(user_text, explicit_mode=None, observer_risk=None):
    if explicit_mode is not None:
        mode=str(explicit_mode).upper()
        if mode not in {MODE_GOAL_DIRECTED,MODE_OBSERVE_DECOUPLED}:
            raise ValueError(f"unsupported entry mode: {explicit_mode}")
        return mode,"EXPLICIT_MODE_ARGUMENT"
    return preflight_mode(user_text,observer_risk=observer_risk)

def bind_entry_contract(user_text, *, target, job, basis, authority=frozenset(),
                        boundary=None, explicit_mode=None, observer_risk=None,
                        episode_id="chat"):
    controller=resolve_controller(user_text)
    mode,mode_basis=resolve_initial_mode(user_text,explicit_mode,observer_risk)
    receipt=f"{episode_id}:ENTRY_BOUND:{controller}:{mode}"
    contract=EntryContract(
        frozen_target=str(target),
        controller=controller,
        initial_mode=mode,
        boundary=None if boundary is None else str(boundary),
        authority=frozenset(authority),
        receipt=receipt,
        raw_request=str(user_text),
        mode_basis=mode_basis,
    )
    lease=ControllerLease(
        episode_id=str(episode_id),
        controller=controller,
        job=str(job),
        basis=str(basis),
    )
    return EntryBinding(contract,lease)

def entry_is_bound(binding):
    return (
        isinstance(binding,EntryBinding)
        and bool(binding.contract.receipt)
        and binding.lease.controller==binding.contract.controller
        and not binding.lease.terminal
    )
