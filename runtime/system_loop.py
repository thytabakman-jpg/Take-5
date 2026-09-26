"""Top-level endogenous research loop.
The system owns work existence/closure. Improvement Core owns adaptive execution policy.
Protected SYSTEM_CONTROL mutations cross the typed commit gate before update/discharge.
"""
from dataclasses import dataclass
from endogenous_work import generate_obligations,select_work,closure_status,WorkStatus
from improvement_core import improve
from state_commit import CommitRequest,StateRole,authorize_commit,CommitBlocked

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

            authority_before=frozenset(current.get("authority",()))
            authority_after=frozenset(ic.final_packet.get("authority",authority_before))
            try:
                authorize_commit(
                    CommitRequest(
                        role=StateRole.SYSTEM_CONTROL,
                        effect="APPLY_IC_RESULT_AND_DISCHARGE_WORK",
                        target=str(current.get("identity","system")),
                        job=str(job),
                        baseline=f"round:{n}:work:{work.work_id}",
                        authority_before=authority_before,
                        authority_after=authority_after,
                        evidence=(f"ic_status:{ic.status}",f"package:{','.join(ic.package)}"),
                        provenance=(f"system_loop:round:{n}",f"work:{work.work_id}"),
                        execution_receipt=(f"ic_results:{len(ic.results)}" if ic.results else None),
                        verification_receipt=f"ic_status:{ic.status}",
                        status=ic.status,
                        material=(ic.final_packet!=current),
                    ),
                    require_execution=True,
                    require_verification=True,
                    require_evidence=True,
                )
            except CommitBlocked:
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
