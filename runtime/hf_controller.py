"""HF-001 guarded reentry controller over K_PD, obligations, packages, mode and TRC."""
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
    candidates=[]
    for pid,covers in package_index.items():
        hit=set(obligations)&set(covers)
        if hit:
            candidates.append((len(hit),pid))
    if not candidates:
        return ()
    best=max(x[0] for x in candidates)
    return tuple(sorted(pid for n,pid in candidates if n==best))

def decide(packet,package_index,mode_flags):
    p=project(packet)
    if not p.obligations:
        return HFDecision(p,(),"OPEN","CLOSE_RELATIVE")
    package=select_package(p.obligations,package_index)
    if not package:
        return HFDecision(p,(),"OPEN","BLOCKED_OPEN")
    mode=select_mode(**mode_flags)
    return HFDecision(p,package,mode,"EXECUTE" if mode!="OPEN" else "OPEN")

def trc(material_delta,previous_packet,next_packet):
    if not material_delta:
        return "NO_REENTRY"
    return "REENTER_KPD" if project(previous_packet)!=project(next_packet) else "REVERIFY"
