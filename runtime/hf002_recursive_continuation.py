"""HF-002 generic capability-level recursive continuation substrate.

HF2 reapplies the same configured capability to its changed normalized successor
while a material local delta and live local frontier remain under a stable
upstream basis. It owns local recurrence, not global episode selection.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any, Callable

TERMINAL={"RELATIVE_CLOSE","RETURN_REENTER","OPEN","BLOCKED","CONFLICT","RESOURCE_STOP"}

@dataclass
class HF2Round:
    round_index:int
    state_before:dict[str,Any]
    raw_result:dict[str,Any]
    normalized_result:dict[str,Any]
    delta:dict[str,Any]
    hf1:dict[str,Any]
    state_after:dict[str,Any]
    disposition:str

@dataclass
class HF002RecursiveContinuation:
    run_capability:Callable[[dict[str,Any],dict[str,Any]],dict[str,Any]]
    admit_normalize:Callable[[dict[str,Any],dict[str,Any],dict[str,Any]],tuple[dict[str,Any],dict[str,Any]]]
    trc_verify:Callable[[dict[str,Any],dict[str,Any],dict[str,Any]],dict[str,Any]]
    hf1_classify:Callable[[dict[str,Any],dict[str,Any],dict[str,Any]],dict[str,Any]]
    live_local:Callable[[dict[str,Any],dict[str,Any]],bool]
    local_close:Callable[[dict[str,Any],dict[str,Any]],bool]
    max_rounds:int=32
    trace:list[HF2Round]=field(default_factory=list)

    @staticmethod
    def _material(delta:dict[str,Any])->bool:
        return bool(
            delta.get("material_result_delta")
            or delta.get("material_search_delta")
            or delta.get("material_discovery_delta")
            or delta.get("negative_evidence")
            or delta.get("open_refinement")
            or delta.get("changed_representation")
        )

    def run(self,state:dict[str,Any],memory:dict[str,Any])->dict[str,Any]:
        x=dict(state); m=dict(memory)
        seen_failed=set(m.get("hf2_failed_equivalence",[]))

        for i in range(self.max_rounds):
            raw=self.run_capability(x,m)
            execution_truth=str(raw.get("execution_truth",""))
            if execution_truth in {"BLOCKED","OPEN","CONFLICT"}:
                return {"status":execution_truth,"state":x,"memory":m,"trace":[asdict(t) for t in self.trace]}
            if execution_truth not in {"FULL_MATCH","IMPLEMENTATION_EXECUTED","SEMANTICALLY_APPLIED"}:
                raise RuntimeError("HF002_EXECUTION_TRUTH_INVALID")

            normalized,delta=self.admit_normalize(raw,x,m)
            receipt=self.trc_verify(x,normalized,delta)
            if not receipt.get("terminal",False):
                return {
                    "status":"OPEN","state":x,"memory":m,
                    "trace":[asdict(t) for t in self.trace],
                    "open":["TRC_NOT_TERMINAL"],
                }

            hf1=self.hf1_classify(x,normalized,delta)
            if hf1.get("disposition")=="REENTER":
                self.trace.append(HF2Round(i,x,raw,normalized,delta,hf1,normalized,"RETURN_REENTER"))
                return {
                    "status":"RETURN_REENTER",
                    "targets":hf1.get("targets",[]),
                    "state":normalized,"memory":m,
                    "trace":[asdict(t) for t in self.trace],
                }
            if hf1.get("disposition") in {"OPEN","BLOCKED","CONFLICT"}:
                status=hf1["disposition"]
                self.trace.append(HF2Round(i,x,raw,normalized,delta,hf1,normalized,status))
                return {"status":status,"state":normalized,"memory":m,"trace":[asdict(t) for t in self.trace]}

            route_eq=delta.get("route_equivalence")
            if route_eq and route_eq in seen_failed and not delta.get("invalidating_evidence"):
                raise RuntimeError("HF002_EQUIVALENT_FAILED_ROUTE_REPEAT")
            if delta.get("certified_no_gain") and route_eq:
                seen_failed.add(route_eq)
                m["hf2_failed_equivalence"]=sorted(seen_failed)

            material=self._material(delta)
            live=bool(self.live_local(normalized,m))
            if material and live:
                self.trace.append(HF2Round(i,x,raw,normalized,delta,hf1,normalized,"REAPPLY_C"))
                x=normalized
                continue

            if self.local_close(normalized,m):
                self.trace.append(HF2Round(i,x,raw,normalized,delta,hf1,normalized,"RELATIVE_CLOSE"))
                return {
                    "status":"RELATIVE_CLOSE","state":normalized,"memory":m,
                    "trace":[asdict(t) for t in self.trace],
                }

            self.trace.append(HF2Round(i,x,raw,normalized,delta,hf1,normalized,"OPEN"))
            return {
                "status":"OPEN","state":normalized,"memory":m,
                "trace":[asdict(t) for t in self.trace],
                "open":["LOCAL_FRONTIER_NOT_CLOSED"],
            }

        return {
            "status":"RESOURCE_STOP","state":x,"memory":m,
            "trace":[asdict(t) for t in self.trace],
        }
