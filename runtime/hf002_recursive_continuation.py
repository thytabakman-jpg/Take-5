"""HF-002 generic capability-level recursive continuation substrate.

HF2 reapplies the same configured capability to its changed normalized successor
until a clean post-mutation verification pass establishes a relative fixed
point. It owns local recurrence, not global episode selection.
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

    @staticmethod
    def _affected_frontier_open(delta:dict[str,Any])->bool:
        frontier=delta.get("affected_frontier")
        if isinstance(frontier,dict):
            if any(bool(v) for v in frontier.values()):
                return True
        elif isinstance(frontier,(tuple,list,set,frozenset)):
            if bool(frontier):
                return True
        elif frontier:
            return True

        scope_deltas=delta.get("scope_deltas")
        if isinstance(scope_deltas,dict):
            if any(bool(v) for v in scope_deltas.values()):
                return True
        elif scope_deltas:
            return True
        return False

    def run(self,state:dict[str,Any],memory:dict[str,Any])->dict[str,Any]:
        x=dict(state); m=dict(memory)
        seen_failed=set(m.get("hf2_failed_equivalence",[]))
        dirty=False

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
            affected_open=self._affected_frontier_open(delta)

            # Fixed-point invariant: a material change can never be the final
            # round. Re-run the same configured capability on its successor so
            # closure is established only by a clean post-mutation pass.
            if material:
                dirty=True
                self.trace.append(HF2Round(
                    i,x,raw,normalized,delta,hf1,normalized,
                    "REAPPLY_C"
                ))
                x=normalized
                continue

            # A clean round can discharge DIRTY only when every represented
            # affected frontier is closed. Live work or unresolved affected
            # scope remains OPEN rather than being converted into false close.
            if affected_open:
                self.trace.append(HF2Round(i,x,raw,normalized,delta,hf1,normalized,"OPEN"))
                return {
                    "status":"OPEN","state":normalized,"memory":m,
                    "trace":[asdict(t) for t in self.trace],
                    "open":["AFFECTED_FRONTIER_NOT_CLOSED"],
                }

            if live:
                self.trace.append(HF2Round(i,x,raw,normalized,delta,hf1,normalized,"OPEN"))
                return {
                    "status":"OPEN","state":normalized,"memory":m,
                    "trace":[asdict(t) for t in self.trace],
                    "open":["LOCAL_FRONTIER_NOT_CLOSED"],
                }

            if self.local_close(normalized,m):
                self.trace.append(HF2Round(i,x,raw,normalized,delta,hf1,normalized,"RELATIVE_CLOSE"))
                return {
                    "status":"RELATIVE_CLOSE","state":normalized,"memory":m,
                    "trace":[asdict(t) for t in self.trace],
                    "clean_verification":True,
                    "post_mutation_clean_pass":bool(dirty),
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
            "open":["FIXED_POINT_NOT_REACHED_WITHIN_MAX_ROUNDS"],
        }
