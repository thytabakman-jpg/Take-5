"""Single-controller episode lease.

Prevents historical challenger controllers from issuing competing action selections
inside one episode. Challengers may observe and return evidence.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class ControllerLease:
    episode_id:str
    controller:str
    job:str
    basis:str
    allowed_helpers:tuple=()
    terminal:bool=False

def may_select_actions(lease, controller):
    return (not lease.terminal) and controller == lease.controller

def helper_mode(lease, controller):
    if controller == lease.controller:
        return "CONTROLLER"
    if controller in lease.allowed_helpers:
        return "OBSERVE_CHALLENGE_ONLY"
    return "NOT_ADMITTED"
