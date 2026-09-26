"""Conversation entry contract for Take-5 / ICC turns.

The entry contract freezes target, controller identity, and a mode-cube profile
before substantive controller work. Breadth, direction, and coupling are
orthogonal execution coordinates:

EXPAND / CONTRACT
OBSERVE / ACT
DECOUPLED / COUPLED

Legacy initial_mode remains as a compatibility projection used for stage order.
"""
from dataclasses import dataclass
from controller_lease import ControllerLease

ICC_CONTROLLER = "IC-028"
MODE_GOAL_DIRECTED = "GOAL_DIRECTED"
MODE_OBSERVE_DECOUPLED = "OBSERVE_DECOUPLED"

EXPAND="EXPAND"
CONTRACT="CONTRACT"
OBSERVE="OBSERVE"
ACT="ACT"
DECOUPLED="DECOUPLED"
COUPLED="COUPLED"

_ICC_ALIASES = ("icc","improvement core","improvecore")

_EXPLICIT_OBSERVER_ALIASES = (
    "observer mode","observation mode","observe first","observer-first",
    "goal-decoupled","goal decoupled","dos",
)
_EXPLICIT_FOCUS_ALIASES = (
    "focused mode","focus mode","focused resolution","focus on",
    "exact discriminant","freeze question","proposition freeze",
)
_AUTO_OBSERVER_MARKERS = (
    "on itself","self apply","self-apply","self application","self-application",
    "root cause","audit","whole system","architect","architecture",
)

@dataclass(frozen=True)
class ModeProfile:
    breadth:str
    direction:str
    coupling:str
    basis:str

    @property
    def mode_id(self)->str:
        return f"{self.breadth}_{self.direction}_{self.coupling}"

@dataclass(frozen=True)
class EntryContract:
    frozen_target:str
    controller:str
    initial_mode:str
    mode_profile:ModeProfile
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

def preflight_mode_profile(user_text, *, observer_risk=None):
    """Classify mode geometry only; do not perform substantive optimization."""
    text=_norm(user_text)

    if any(alias in text for alias in _EXPLICIT_FOCUS_ALIASES):
        return ModeProfile(CONTRACT,OBSERVE,DECOUPLED,"EXPLICIT_FOCUSED_OBSERVATION")

    if any(alias in text for alias in _EXPLICIT_OBSERVER_ALIASES):
        return ModeProfile(EXPAND,OBSERVE,DECOUPLED,"EXPLICIT_BROAD_OBSERVER")

    if observer_risk is True or any(marker in text for marker in _AUTO_OBSERVER_MARKERS):
        basis="CALLER_CONTAMINATION_RISK" if observer_risk is True else "PREFLIGHT_CONTAMINATION_RISK"
        return ModeProfile(EXPAND,OBSERVE,DECOUPLED,basis)

    if observer_risk is False:
        return ModeProfile(EXPAND,ACT,COUPLED,"CALLER_NO_CONTAMINATION_RISK")

    return ModeProfile(EXPAND,ACT,COUPLED,"PREFLIGHT_DEFAULT_SYSTEM_IMPROVEMENT")

def _legacy_mode(profile:ModeProfile)->str:
    if profile.direction==OBSERVE:
        return MODE_OBSERVE_DECOUPLED
    return MODE_GOAL_DIRECTED

def preflight_mode(user_text, *, observer_risk=None):
    profile=preflight_mode_profile(user_text,observer_risk=observer_risk)
    return _legacy_mode(profile),profile.basis

def resolve_initial_mode(user_text, explicit_mode=None, observer_risk=None):
    if explicit_mode is not None:
        mode=str(explicit_mode).upper()
        if mode==MODE_OBSERVE_DECOUPLED:
            return mode,"EXPLICIT_MODE_ARGUMENT"
        if mode==MODE_GOAL_DIRECTED:
            return mode,"EXPLICIT_MODE_ARGUMENT"
        raise ValueError(f"unsupported entry mode: {explicit_mode}")
    return preflight_mode(user_text,observer_risk=observer_risk)

def resolve_mode_profile(user_text, explicit_mode=None, observer_risk=None):
    if explicit_mode is not None:
        mode=str(explicit_mode).upper()
        if mode==MODE_OBSERVE_DECOUPLED:
            return ModeProfile(EXPAND,OBSERVE,DECOUPLED,"EXPLICIT_MODE_ARGUMENT")
        if mode==MODE_GOAL_DIRECTED:
            return ModeProfile(EXPAND,ACT,COUPLED,"EXPLICIT_MODE_ARGUMENT")
        raise ValueError(f"unsupported entry mode: {explicit_mode}")
    return preflight_mode_profile(user_text,observer_risk=observer_risk)

def bind_entry_contract(user_text, *, target, job, basis, authority=frozenset(),
                        boundary=None, explicit_mode=None, observer_risk=None,
                        episode_id="chat"):
    controller=resolve_controller(user_text)
    profile=resolve_mode_profile(user_text,explicit_mode,observer_risk)
    mode=_legacy_mode(profile)
    receipt=f"{episode_id}:ENTRY_BOUND:{controller}:{profile.mode_id}"
    contract=EntryContract(
        frozen_target=str(target),
        controller=controller,
        initial_mode=mode,
        mode_profile=profile,
        boundary=None if boundary is None else str(boundary),
        authority=frozenset(authority),
        receipt=receipt,
        raw_request=str(user_text),
        mode_basis=profile.basis,
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
