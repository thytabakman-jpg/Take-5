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
from typing import Any, Callable, Mapping, Iterable

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


AFFECTED_SCOPE_KEYS=("affected_frontier","scope_deltas")


def affected_scope_open(delta:Mapping[str,Any])->bool:
    """Outstanding affected scope is independent of material progress."""
    def unresolved(value:Any)->bool:
        if isinstance(value,Mapping):
            return any(unresolved(v) for v in value.values())
        if isinstance(value,(tuple,list,set,frozenset)):
            return any(unresolved(v) for v in value)
        return bool(value)
    return any(unresolved(delta.get(key)) for key in AFFECTED_SCOPE_KEYS)


def carry_affected_scope(delta:dict[str,Any], pending:dict[str,Any])->None:
    """Carry omitted scope forward; explicit empty snapshots clear it.

    Nonempty mapping updates are partial: omitted entries retain their last
    disposition. None is absence of evidence, not a clearance receipt.
    """
    for key in AFFECTED_SCOPE_KEYS:
        value=delta.get(key)
        if value is None:
            if key in pending:
                delta[key]=deepcopy(pending[key])
            continue
        old=pending.get(key)
        if isinstance(old,Mapping) and isinstance(value,Mapping) and value:
            value={**old,**value}
        pending[key]=deepcopy(value)
        delta[key]=deepcopy(value)


def hf2_fixed_point_witness(trace:Iterable[Mapping[str,Any]])->bool:
    """Verify a complete HF002 episode ending in a clean local close."""
    try:
        rounds=tuple(trace)
    except TypeError:
        return False
    if not rounds:
        return False
    pending:dict[str,Any]={}
    previous=None
    for i,row in enumerate(rounds):
        if not isinstance(row,Mapping) or type(row.get("round_index")) is not int or row["round_index"]!=i:
            return False
        if not all(key in row for key in ("state_before","state_after","normalized_result")):
            return False
        if i and row["state_before"]!=previous:
            return False
        if row["state_after"]!=row["normalized_result"]:
            return False
        previous=row["state_after"]
        raw=row.get("raw_result")
        hf1=row.get("hf1")
        delta=row.get("delta")
        if not isinstance(raw,Mapping) or raw.get("execution_truth") not in (
            "FULL_MATCH","IMPLEMENTATION_EXECUTED","SEMANTICALLY_APPLIED",
        ) or raw.get("status") in {"OPEN","BLOCKED","CONFLICT"} or not isinstance(hf1,Mapping) or hf1.get("disposition")!="STABLE" or not isinstance(delta,Mapping):
            return False
        effective=dict(delta)
        carry_affected_scope(effective,pending)
        receipt=row.get("trc")
        if not isinstance(receipt,Mapping) or receipt.get("terminal") is not True:
            return False
        if i<len(rounds)-1:
            if row.get("disposition")!="REAPPLY_C" or not material_delta_present(effective):
                return False
            continue
        return (row.get("disposition")=="RELATIVE_CLOSE"
                and not material_delta_present(effective)
                and not affected_scope_open(effective)
                and row.get("live_local") is False and row.get("local_close") is True)
    return False


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
    trc:dict[str,Any]|None=None
    live_local:bool|None=None
    local_close:bool|None=None

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

    _affected_frontier_open = staticmethod(affected_scope_open)

    def _record(self,*args,**kwargs):
        # Freeze receipts at the time of the round, not at episode return.
        self.trace.append(deepcopy(HF2Round(*args,**kwargs)))

    def run(self,state:dict[str,Any],memory:dict[str,Any])->dict[str,Any]:
        # A new episode must not inherit execution receipts from an earlier run.
        self.trace.clear()
        x=deepcopy(state); m=deepcopy(memory)
        seen_failed=set(m.get("hf2_failed_equivalence",[]))
        pending_scope:dict[str,Any]={}

        for i in range(self.max_rounds):
            before=deepcopy(x)
            raw=self.run_capability(x,m)
            execution_truth=str(raw.get("execution_truth",""))
            # Native callers can bypass configured receipt normalization. A
            # non-success result status must still prevent a clean fixed point.
            result_status=str(raw.get("status",""))
            non_success={"BLOCKED","OPEN","CONFLICT"}
            if result_status in non_success:
                if execution_truth in non_success and execution_truth!=result_status:
                    execution_truth="CONFLICT"
                else:
                    execution_truth=result_status
            if execution_truth in non_success:
                self._record(i,before,raw,x,{}, {},before,execution_truth)
                return {"status":execution_truth,"state":before,"memory":m,"trace":[asdict(t) for t in self.trace]}
            if execution_truth not in {"FULL_MATCH","IMPLEMENTATION_EXECUTED","SEMANTICALLY_APPLIED"}:
                raise RuntimeError("HF002_EXECUTION_TRUTH_INVALID")

            normalized,delta=self.admit_normalize(raw,x,m)
            delta=dict(delta)
            carry_affected_scope(delta,pending_scope)
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
            live=self.live_local(normalized,m)
            if type(live) is not bool:
                self._record(i,before,raw,normalized,delta,hf1,before,"OPEN")
                return {"status":"OPEN","state":before,"memory":m,
                        "trace":[asdict(t) for t in self.trace],
                        "open":["HF002_LIVE_LOCAL_BOOLEAN_REQUIRED"]}

            # A material successor cannot certify its own fixed point.  Always
            # reapply the same capability to the changed normalized successor.
            # The next round must independently produce a non-material result
            # before RELATIVE_CLOSE is available.  This closes the historical
            # "second run finds something new" gap even when the producer has
            # already marked its local frontier inactive.
            if material:
                self._record(i,before,raw,normalized,delta,hf1,normalized,"REAPPLY_C",
                             trc=receipt,live_local=live)
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

            if self.local_close(normalized,m) is True:
                self._record(i,before,raw,normalized,delta,hf1,normalized,"RELATIVE_CLOSE",
                             trc=receipt,live_local=False,local_close=True)
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
