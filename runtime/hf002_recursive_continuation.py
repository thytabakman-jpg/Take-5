"""HF-002 generic capability-level recursive continuation substrate.

HF2 reapplies the same configured capability after a material local successor
when upstream control permits local continuation, even if the successor reports
its local frontier inactive. A subsequent non-material pass must establish
local closure without unresolved affected scope. It owns local recurrence,
not global episode selection.
"""
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, asdict, field
from typing import Any, Callable, Mapping

TERMINAL={"RELATIVE_CLOSE","RETURN_REENTER","OPEN","BLOCKED","CONFLICT","RESOURCE_STOP"}

MATERIAL_DELTA_KEYS=(
    "material_result_delta", "material_search_delta", "material_discovery_delta",
    "negative_evidence", "open_refinement", "changed_representation",
    "material_relation_delta", "goal_gap_reduced", "execution_truth_strengthened",
    "resolved_open", "resolved_blocked", "resolved_conflict",
)


def material_delta_present(delta:Mapping[str,Any])->bool:
    """Authoritative HF002 material-change vocabulary shared with its consumers."""
    return any(bool(delta.get(key)) for key in MATERIAL_DELTA_KEYS)

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

    _material = staticmethod(material_delta_present)

    @staticmethod
    def _affected_frontier_open(delta:dict[str,Any])->bool:
        """Treat unresolved affected scope as an independent HF2 closure blocker.

        Domain adapters own the meaning and completeness of these fields;
        the generic recurrence engine only refuses to call them terminal.
        """
        def unresolved(value:Any)->bool:
            if isinstance(value,dict):
                return any(unresolved(v) for v in value.values())
            if isinstance(value,(tuple,list,set,frozenset)):
                return any(unresolved(v) for v in value)
            return bool(value)

        return (unresolved(delta.get("affected_frontier"))
                or unresolved(delta.get("scope_deltas")))

    def _record(self,*args):
        # Freeze receipts at the time of the round, not at episode return.
        self.trace.append(deepcopy(HF2Round(*args)))

    def run(self,state:dict[str,Any],memory:dict[str,Any])->dict[str,Any]:
        # A new episode must not inherit execution receipts from an earlier run.
        self.trace.clear()
        x=deepcopy(state); m=deepcopy(memory)
        seen_failed=set(m.get("hf2_failed_equivalence",[]))

        for i in range(self.max_rounds):
            before=deepcopy(x)
            raw=self.run_capability(x,m)
            execution_truth=str(raw.get("execution_truth",""))
            if execution_truth in {"BLOCKED","OPEN","CONFLICT"}:
                self._record(i,before,raw,x,{}, {},before,execution_truth)
                return {"status":execution_truth,"state":before,"memory":m,"trace":[asdict(t) for t in self.trace]}
            if execution_truth not in {"FULL_MATCH","IMPLEMENTATION_EXECUTED","SEMANTICALLY_APPLIED"}:
                raise RuntimeError("HF002_EXECUTION_TRUTH_INVALID")

            normalized,delta=self.admit_normalize(raw,x,m)
            receipt=self.trc_verify(deepcopy(before),normalized,delta)
            if receipt.get("terminal") is not True:
                self._record(i,before,raw,normalized,delta,{},before,"OPEN")
                return {
                    "status":"OPEN","state":before,"memory":m,
                    "trace":[asdict(t) for t in self.trace],
                    "open":["TRC_NOT_TERMINAL"],
                }

            hf1=self.hf1_classify(deepcopy(before),normalized,delta)
            if not isinstance(hf1,Mapping) or hf1.get("disposition") not in (
                "STABLE","REENTER","OPEN","BLOCKED","CONFLICT",
            ):
                self._record(i,before,raw,normalized,delta,hf1,before,"BLOCKED")
                return {
                    "status":"BLOCKED","state":before,"memory":m,
                    "trace":[asdict(t) for t in self.trace],
                    "open":["HF002_HF1_DISPOSITION_INVALID"],
                }
            if hf1.get("disposition")=="REENTER":
                self._record(i,before,raw,normalized,delta,hf1,normalized,"RETURN_REENTER")
                return {
                    "status":"RETURN_REENTER",
                    "targets":hf1.get("targets",[]),
                    "state":normalized,"memory":m,
                    "trace":[asdict(t) for t in self.trace],
                }
            if hf1.get("disposition") in {"OPEN","BLOCKED","CONFLICT"}:
                status=hf1["disposition"]
                self._record(i,before,raw,normalized,delta,hf1,normalized,status)
                return {"status":status,"state":normalized,"memory":m,"trace":[asdict(t) for t in self.trace]}

            route_eq=delta.get("route_equivalence")
            if route_eq and route_eq in seen_failed and not delta.get("invalidating_evidence"):
                raise RuntimeError("HF002_EQUIVALENT_FAILED_ROUTE_REPEAT")
            if delta.get("certified_no_gain") and route_eq:
                seen_failed.add(route_eq)
                m["hf2_failed_equivalence"]=sorted(seen_failed)

            material=self._material(delta)
            live=bool(self.live_local(normalized,m))

            # A material successor cannot certify its own fixed point.  Always
            # reapply the same capability to the changed normalized successor.
            # The next round must independently produce a non-material result
            # before RELATIVE_CLOSE is available.  This closes the historical
            # "second run finds something new" gap even when the producer has
            # already marked its local frontier inactive.
            if material:
                self._record(i,before,raw,normalized,delta,hf1,normalized,"REAPPLY_C")
                x=normalized
                continue

            # Material successors already reenter above.  A clean result with
            # outstanding affected scope is still NOT a verified fixed point.
            if self._affected_frontier_open(delta):
                self._record(i,before,raw,normalized,delta,hf1,normalized,"OPEN")
                return {
                    "status":"OPEN","state":normalized,"memory":m,
                    "trace":[asdict(t) for t in self.trace],
                    "open":["AFFECTED_FRONTIER_NOT_CLOSED"],
                }

            if live:
                self._record(i,before,raw,normalized,delta,hf1,normalized,"OPEN")
                return {
                    "status":"OPEN","state":normalized,"memory":m,
                    "trace":[asdict(t) for t in self.trace],
                    "open":["LIVE_LOCAL_FRONTIER_WITHOUT_MATERIAL_PROGRESS"],
                }

            if self.local_close(normalized,m):
                self._record(i,before,raw,normalized,delta,hf1,normalized,"RELATIVE_CLOSE")
                return {
                    "status":"RELATIVE_CLOSE","state":normalized,"memory":m,
                    "trace":[asdict(t) for t in self.trace],
                }

            self._record(i,before,raw,normalized,delta,hf1,normalized,"OPEN")
            return {
                "status":"OPEN","state":normalized,"memory":m,
                "trace":[asdict(t) for t in self.trace],
                "open":["LOCAL_FRONTIER_NOT_CLOSED"],
            }

        return {
            "status":"RESOURCE_STOP","state":x,"memory":m,
            "trace":[asdict(t) for t in self.trace],
        }
