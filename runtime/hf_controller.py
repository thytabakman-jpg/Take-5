"""HF-001 guarded reentry controller over K_PD, obligations, packages and mode.

Important naming:
- Tool Run Closure is owned by runtime/tool_run_closure.py.
- delta_reentry_route below only decides what a material packet delta means for
  HF reentry. The historical name trc remains as a compatibility alias.
"""
from dataclasses import dataclass
from kpd_projection import project
from mode_selector import select_mode

@dataclass(frozen=True)
class HFDecision:
    projection:object
    package:tuple[str,...]
    mode:str
    action:str

def select_package(obligations,package_index):
    """Historical max-hit selector retained as the default behavior."""
    candidates=[]
    for pid,covers in package_index.items():
        hit=set(obligations)&set(covers)
        if hit:
            candidates.append((len(hit),pid))
    if not candidates:
        return ()
    best=max(x[0] for x in candidates)
    return tuple(sorted(pid for n,pid in candidates if n==best))

def decide(packet,package_index,mode_flags,package_selector=None):
    p=project(packet)
    if not p.obligations:
        return HFDecision(p,(),"OPEN","CLOSE_RELATIVE")
    if package_selector is None:
        package=select_package(p.obligations,package_index)
    else:
        package=tuple(package_selector(p.obligations,package_index,packet))
    if not package:
        return HFDecision(p,(),"OPEN","BLOCKED_OPEN")
    mode=select_mode(**mode_flags)
    return HFDecision(p,package,mode,"EXECUTE" if mode!="OPEN" else "OPEN")

def delta_reentry_route(material_delta,previous_packet,next_packet):
    """Route an already-produced material delta; this is not Tool Run Closure."""
    if not material_delta:
        return "NO_REENTRY"
    return "REENTER_KPD" if project(previous_packet)!=project(next_packet) else "REVERIFY"

def trc(material_delta,previous_packet,next_packet):
    """Compatibility alias for the historical delta-router name."""
    return delta_reentry_route(material_delta,previous_packet,next_packet)


@dataclass(frozen=True)
class HF1ReentryDecision:
    world_changed: bool
    discovery_changed: bool
    result_sensitive_delta: bool
    action: str


def hf1_reentry_route(*, world_changed: bool, discovery_changed: bool,
                      result_sensitive_delta: bool = False) -> HF1ReentryDecision:
    """Wrapper-level HF1 reentry law."""
    if world_changed or discovery_changed:
        action = "REENTER_OBSERVE"
    elif result_sensitive_delta:
        action = "REVERIFY"
    else:
        action = "NO_REENTRY"
    return HF1ReentryDecision(
        bool(world_changed),
        bool(discovery_changed),
        bool(result_sensitive_delta),
        action,
    )
