"""Improvement Core governing episode: infer obligations, select mode/package, delegate, verify, TRC, reenter."""
from dataclasses import dataclass
from hf_controller import decide,trc
from controller_episode import run_episode
from delegation import delegate

@dataclass
class ICResult:
    status:str
    rounds:int
    mode:str
    package:tuple
    results:tuple
    final_packet:dict

def improve(packet,package_index,workers,mode_policy,max_rounds=8):
    current=dict(packet)
    results=[]
    seen=set()
    for n in range(1,max_rounds+1):
        flags=mode_policy(current)
        d=decide(current,package_index,flags)
        sig=(d.projection.obligations,d.package,d.mode)
        if d.action=="CLOSE_RELATIVE":
            return ICResult("CLOSED_RELATIVE",n-1,d.mode,d.package,tuple(results),current)
        if d.action!="EXECUTE" or sig in seen:
            return ICResult("OPEN",n-1,d.mode,d.package,tuple(results),current)
        seen.add(sig)
        before=dict(current)
        for pid in d.package:
            worker=workers.get(pid)
            if worker is None:
                return ICResult("OPEN",n-1,d.mode,d.package,tuple(results),current)
            authority=frozenset(current.get("authority",()))
            local=frozenset(current.get("local_authority",authority))
            def local_worker(payload,_w=worker):
                return _w(payload)
            def episode_worker(binding,_pid=pid,_lw=local_worker):
                out,receipt=delegate(episode=f"ic-{n}",program_id=_pid,authority_in=authority,authority_local=local,payload=current,worker=_lw)
                return {"output":out,"delegation":receipt}
            ep=run_episode(episode=f"ic-{n}-{pid}",program_id=pid,target_id=str(current.get("identity","object")),job=str(current.get("job","improve")),authority=authority,worker=episode_worker,observation_only="_OBSERVE_" in d.mode)
            if not ep.complete:
                return ICResult("OPEN",n,d.mode,d.package,tuple(results),current)
            out=ep.result["output"]
            results.append((pid,out))
            if isinstance(out,dict):
                current.update(out)
        material=current!=before
        action=trc(material,before,current)
        if action=="NO_REENTRY":
            return ICResult("CLOSED_RELATIVE",n,d.mode,d.package,tuple(results),current)
    return ICResult("OPEN",max_rounds,d.mode,d.package,tuple(results),current)
