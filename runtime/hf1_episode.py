"""HF1 governed episode.

HF1 composes K_PD projection, exact sufficient package selection, mode selection,
execution, Tool Run Closure status, typed delta classification, and reentry.
The older activation loop is treated as the execution sub-transition, not a
competing controller loop.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Any, Callable

from kpd_projection import project
from mode_selector import select_mode
from hf_controller import hf1_reentry_route


class HF1Terminal(str, Enum):
    CONTINUE="CONTINUE"
    RELATIVE_CLOSE="RELATIVE_CLOSE"
    OPEN="OPEN"
    BLOCKED="BLOCKED"


@dataclass(frozen=True)
class HF1Execution:
    packet:dict
    value:Any=None
    executed:bool=True
    consumed:bool=True


@dataclass(frozen=True)
class HF1Closure:
    packet:dict
    status:str="CLOSED"


@dataclass(frozen=True)
class HF1Delta:
    world_changed:bool
    discovery_changed:bool
    result_sensitive_delta:bool


@dataclass(frozen=True)
class HF1RoundReceipt:
    round:int
    obligations:tuple[str,...]
    package:tuple[str,...]
    mode:str
    closure_status:str
    reentry_action:str
    terminal:str


@dataclass(frozen=True)
class HF1EpisodeResult:
    packet:dict
    terminal:HF1Terminal
    receipts:tuple[HF1RoundReceipt,...]
    blocker:str|None=None


SIGNATURE_KEYS=("world_state","discovery_state","result_sensitive_state")


def classify_delta(previous:dict,next_packet:dict)->HF1Delta:
    missing=[k for k in SIGNATURE_KEYS if k not in previous or k not in next_packet]
    if missing:
        raise ValueError("HF1_DELTA_SIGNATURE_MISSING:"+",".join(missing))
    return HF1Delta(
        previous["world_state"]!=next_packet["world_state"],
        previous["discovery_state"]!=next_packet["discovery_state"],
        previous["result_sensitive_state"]!=next_packet["result_sensitive_state"],
    )


def select_sufficient_package(obligations,package_index,costs=None):
    """Exact least-cost sufficient cover over currently reachable package ids."""
    obligations=set(obligations)
    if not obligations:
        return ()
    ids=tuple(sorted(package_index))
    costs=costs or {}
    best=None
    for size in range(1,len(ids)+1):
        for subset in combinations(ids,size):
            covered=set()
            for pid in subset:
                covered.update(package_index[pid])
            if not obligations<=covered:
                continue
            score=(sum(float(costs.get(pid,1.0)) for pid in subset),len(subset),subset)
            if best is None or score<best[0]:
                best=(score,subset)
    return () if best is None else tuple(best[1])


def run_hf1_episode(
    initial_packet:dict,
    *,
    package_index:dict,
    mode_flags:dict|Callable[[dict],dict],
    execute_fn:Callable[[tuple[str,...],str,dict],HF1Execution],
    closure_fn:Callable[[HF1Execution,dict],HF1Closure],
    verify_fn:Callable[[dict],bool]|None=None,
    package_costs:dict|None=None,
    max_rounds:int=32,
)->HF1EpisodeResult:
    packet=dict(initial_packet)
    receipts=[]

    for i in range(1,max_rounds+1):
        p=project(packet)
        obligations=tuple(p.obligations)
        if not obligations:
            receipts.append(HF1RoundReceipt(round=i,obligations=(),package=(),mode="NOT_SELECTED",closure_status="NOT_REQUIRED",reentry_action="NOT_REQUIRED",terminal=HF1Terminal.RELATIVE_CLOSE.value))
            return HF1EpisodeResult(packet,HF1Terminal.RELATIVE_CLOSE,tuple(receipts))

        package=select_sufficient_package(obligations,package_index,package_costs)
        if not package:
            receipts.append(HF1RoundReceipt(round=i,obligations=obligations,package=(),mode="NOT_SELECTED",closure_status="NOT_RUN",reentry_action="NOT_RUN",terminal=HF1Terminal.BLOCKED.value))
            return HF1EpisodeResult(packet,HF1Terminal.BLOCKED,tuple(receipts),"NO_SUFFICIENT_PACKAGE")

        flags=mode_flags(packet) if callable(mode_flags) else dict(mode_flags)
        mode=select_mode(**flags)
        if mode=="OPEN":
            receipts.append(HF1RoundReceipt(round=i,obligations=obligations,package=package,mode=mode,closure_status="NOT_RUN",reentry_action="NOT_RUN",terminal=HF1Terminal.OPEN.value))
            return HF1EpisodeResult(packet,HF1Terminal.OPEN,tuple(receipts),"MODE_UNRESOLVED")

        execution=execute_fn(package,mode,packet)
        if not isinstance(execution,HF1Execution) or not execution.executed or not execution.consumed:
            receipts.append(HF1RoundReceipt(round=i,obligations=obligations,package=package,mode=mode,closure_status="NOT_RUN",reentry_action="NOT_RUN",terminal=HF1Terminal.OPEN.value))
            return HF1EpisodeResult(packet,HF1Terminal.OPEN,tuple(receipts),"EXECUTION_NOT_CONSUMED")

        closure=closure_fn(execution,packet)
        if not isinstance(closure,HF1Closure):
            return HF1EpisodeResult(packet,HF1Terminal.OPEN,tuple(receipts),"CLOSURE_RESULT_INVALID")
        if closure.status=="BLOCKED":
            receipts.append(HF1RoundReceipt(round=i,obligations=obligations,package=package,mode=mode,closure_status="BLOCKED",reentry_action="NOT_RUN",terminal=HF1Terminal.BLOCKED.value))
            return HF1EpisodeResult(closure.packet,HF1Terminal.BLOCKED,tuple(receipts),"TOOL_RUN_CLOSURE_BLOCKED")
        if closure.status!="CLOSED":
            receipts.append(HF1RoundReceipt(round=i,obligations=obligations,package=package,mode=mode,closure_status=closure.status,reentry_action="NOT_RUN",terminal=HF1Terminal.OPEN.value))
            return HF1EpisodeResult(closure.packet,HF1Terminal.OPEN,tuple(receipts),"TOOL_RUN_CLOSURE_OPEN")

        try:
            delta=classify_delta(packet,closure.packet)
        except ValueError as exc:
            receipts.append(HF1RoundReceipt(round=i,obligations=obligations,package=package,mode=mode,closure_status="CLOSED",reentry_action="UNRESOLVED",terminal=HF1Terminal.OPEN.value))
            return HF1EpisodeResult(closure.packet,HF1Terminal.OPEN,tuple(receipts),str(exc))

        route=hf1_reentry_route(
            world_changed=delta.world_changed,
            discovery_changed=delta.discovery_changed,
            result_sensitive_delta=delta.result_sensitive_delta,
        )
        next_packet=dict(closure.packet)

        if route.action=="REVERIFY":
            if verify_fn is None:
                receipts.append(HF1RoundReceipt(round=i,obligations=obligations,package=package,mode=mode,closure_status="CLOSED",reentry_action=route.action,terminal=HF1Terminal.OPEN.value))
                return HF1EpisodeResult(next_packet,HF1Terminal.OPEN,tuple(receipts),"REVERIFY_HANDLER_REQUIRED")
            if not verify_fn(next_packet):
                receipts.append(HF1RoundReceipt(round=i,obligations=obligations,package=package,mode=mode,closure_status="CLOSED",reentry_action=route.action,terminal=HF1Terminal.OPEN.value))
                return HF1EpisodeResult(next_packet,HF1Terminal.OPEN,tuple(receipts),"REVERIFICATION_FAILED")

        next_obligations=tuple(project(next_packet).obligations)
        if not next_obligations:
            receipts.append(HF1RoundReceipt(round=i,obligations=obligations,package=package,mode=mode,closure_status="CLOSED",reentry_action=route.action,terminal=HF1Terminal.RELATIVE_CLOSE.value))
            return HF1EpisodeResult(next_packet,HF1Terminal.RELATIVE_CLOSE,tuple(receipts))

        if route.action=="NO_REENTRY":
            receipts.append(HF1RoundReceipt(round=i,obligations=obligations,package=package,mode=mode,closure_status="CLOSED",reentry_action=route.action,terminal=HF1Terminal.OPEN.value))
            return HF1EpisodeResult(next_packet,HF1Terminal.OPEN,tuple(receipts),"NO_PROGRESS_WITH_LIVE_OBLIGATIONS")

        receipts.append(HF1RoundReceipt(round=i,obligations=obligations,package=package,mode=mode,closure_status="CLOSED",reentry_action=route.action,terminal=HF1Terminal.CONTINUE.value))
        packet=next_packet

    return HF1EpisodeResult(packet,HF1Terminal.OPEN,tuple(receipts),"HF1_MAX_ROUNDS")
