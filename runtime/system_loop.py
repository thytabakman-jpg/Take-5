"""Top-level endogenous research loop.
The system owns work existence/closure. Improvement Core owns adaptive execution policy.
"""
from dataclasses import dataclass
from endogenous_work import generate_obligations,select_work,closure_status,WorkStatus
from improvement_core import improve

@dataclass(frozen=True)
class SystemResult:
    status:WorkStatus
    rounds:int
    state:dict
    discharged:tuple[str,...]
    open_coordinates:tuple[str,...]

def run_system(state,job,discover,package_index,workers,mode_policy,max_rounds=16):
    current=dict(state)
    discharged=set(current.get("discharged",()))
    open_coordinates=tuple(current.get("open_coordinates",()))
    for n in range(1,max_rounds+1):
        generated=generate_obligations(current,job=job,discover=discover)
        items=tuple(generated)
        status=closure_status(items,discharged,open_coordinates)
        if status!=WorkStatus.ACTIVE:
            return SystemResult(status,n-1,current,tuple(sorted(discharged)),open_coordinates)
        selection=select_work(items)
        if not selection.selected:
            return SystemResult(WorkStatus.BLOCKED,n-1,current,tuple(sorted(discharged)),open_coordinates)
        before=dict(current)
        for work in selection.selected:
            packet=dict(current)
            packet["obligations"]=[work.obligation]
            ic=improve(packet,package_index,workers,mode_policy)
            if ic.status=="OPEN":
                open_coordinates=tuple(dict.fromkeys(open_coordinates+(work.work_id,)))
                continue
            current.update(ic.final_packet)
            discharged.add(work.work_id)
        current["discharged"]=tuple(sorted(discharged))
        if open_coordinates:
            remaining=tuple(w for w in items if w.work_id not in discharged)
            if remaining:
                return SystemResult(WorkStatus.PAUSED_OPEN,n,current,tuple(sorted(discharged)),open_coordinates)
        if current==before:
            return SystemResult(WorkStatus.BLOCKED,n,current,tuple(sorted(discharged)),open_coordinates)
    return SystemResult(WorkStatus.ACTIVE,max_rounds,current,tuple(sorted(discharged)),open_coordinates)
