"""Conversation entry contract for Take-5 / ICC turns.

The entry contract is bound before substantive controller work.  It freezes the
external target, controller identity and initial mode so the host/interface
cannot silently drift into a different controller or begin goal-directed work
before an observer-first episode.
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

_OBSERVER_ALIASES = (
    "observer mode",
    "observation mode",
    "observe first",
    "observer-first",
    "goal-decoupled",
    "goal decoupled",
    "dos",
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

def resolve_initial_mode(user_text, explicit_mode=None):
    if explicit_mode is not None:
        mode=str(explicit_mode).upper()
        if mode not in {MODE_GOAL_DIRECTED,MODE_OBSERVE_DECOUPLED}:
            raise ValueError(f"unsupported entry mode: {explicit_mode}")
        return mode
    text=_norm(user_text)
    if any(alias in text for alias in _OBSERVER_ALIASES):
        return MODE_OBSERVE_DECOUPLED
    return MODE_GOAL_DIRECTED

def bind_entry_contract(user_text, *, target, job, basis, authority=frozenset(),
                        boundary=None, explicit_mode=None, episode_id="chat"):
    controller=resolve_controller(user_text)
    mode=resolve_initial_mode(user_text,explicit_mode)
    receipt=f"{episode_id}:ENTRY_BOUND:{controller}:{mode}"
    contract=EntryContract(
        frozen_target=str(target),
        controller=controller,
        initial_mode=mode,
        boundary=None if boundary is None else str(boundary),
        authority=frozenset(authority),
        receipt=receipt,
        raw_request=str(user_text),
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
