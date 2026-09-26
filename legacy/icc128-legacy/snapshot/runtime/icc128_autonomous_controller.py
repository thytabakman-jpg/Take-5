#!/usr/bin/env python3
"""Historical ICC-128 autonomous controller substrate.

This restores the endogenous control loop:
G_Q -> G_W -> S -> E -> A -> U -> G_Q.

Semantic intelligence is injected through adapters so the controller does not fake
open-ended question generation with hard-coded rules.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Protocol, Sequence

TERMINAL={"COMPLETE","OPEN","BLOCKED","CONFLICT"}

class QuestionGenerator(Protocol):
    def __call__(self,state:dict[str,Any],memory:dict[str,Any])->list[dict[str,Any]]: ...
class WorkGenerator(Protocol):
    def __call__(self,questions:list[dict[str,Any]],state:dict[str,Any],memory:dict[str,Any])->list[dict[str,Any]]: ...
class Selector(Protocol):
    def __call__(self,questions:list[dict[str,Any]],work:list[dict[str,Any]],state:dict[str,Any],memory:dict[str,Any])->list[dict[str,Any]]: ...
class Executor(Protocol):
    def __call__(self,selected:list[dict[str,Any]],state:dict[str,Any],memory:dict[str,Any])->list[dict[str,Any]]: ...
class Admitter(Protocol):
    def __call__(self,results:list[dict[str,Any]],state:dict[str,Any],memory:dict[str,Any])->dict[str,Any]: ...
class Updater(Protocol):
    def __call__(self,state:dict[str,Any],memory:dict[str,Any],delta:dict[str,Any])->tuple[dict[str,Any],dict[str,Any]]: ...

class DiscoveryClosure(Protocol):
    def __call__(self,delta:dict[str,Any],state:dict[str,Any],memory:dict[str,Any])->dict[str,Any]: ...

@dataclass
class ICC128Trace:
    iteration:int
    questions:list[dict[str,Any]]
    work:list[dict[str,Any]]
    selected:list[dict[str,Any]]
    results:list[dict[str,Any]]
    admitted_delta:dict[str,Any]
    state_after:dict[str,Any]
    memory_after:dict[str,Any]
    terminal:str

@dataclass
class ICC128Controller:
    gq: QuestionGenerator
    gw: WorkGenerator
    select: Selector
    execute: Executor
    admit: Admitter
    update: Updater
    dcc: DiscoveryClosure | None = None
    max_iterations:int=64
    traces:list[ICC128Trace]=field(default_factory=list)

    def run(self,state:dict[str,Any],memory:dict[str,Any])->dict[str,Any]:
        z=dict(state); mi=dict(memory)
        for i in range(self.max_iterations):
            terminal=str(z.get("terminal","CONTINUE"))
            if terminal in TERMINAL:
                return {"status":terminal,"state":z,"memory":mi,"traces":[asdict(t) for t in self.traces]}

            # G_Q
            q=self.gq(z,mi)
            admitted_continuation=bool(z.get("admitted_continuation",False))
            if admitted_continuation and not q:
                raise RuntimeError("ICC128_LIVENESS_FAILURE:G_Q_empty_with_admitted_continuation")

            # G_W
            w=self.gw(q,z,mi)

            # S / rho_128
            selected=self.select(q,w,z,mi)
            if q and not selected and not z.get("selection_blocked"):
                raise RuntimeError("ICC128_SELECTION_FAILURE:live_questions_without_selected_or_blocked_work")

            # E
            results=self.execute(selected,z,mi)

            # A
            delta=self.admit(results,z,mi)

            # DCC mandatory discovery-closure gate.
            # Producers may emit candidate discovery deltas, but they may not
            # directly mutate authoritative discovery-closure state.
            discovery_candidates=delta.get("candidate_discovery_deltas",[])
            if discovery_candidates:
                if self.dcc is None:
                    raise RuntimeError("ICC128_DCC_REQUIRED:discovery_delta_without_dcc_binding")
                delta=self.dcc(delta,z,mi)
                if not delta.get("dcc_receipt"):
                    raise RuntimeError("ICC128_DCC_RECEIPT_MISSING:normalized_delta_without_receipt")

            # U + MI sync
            z2,mi2=self.update(z,mi,delta)
            terminal2=str(z2.get("terminal","CONTINUE"))

            self.traces.append(ICC128Trace(
                iteration=i,questions=q,work=w,selected=selected,results=results,
                admitted_delta=delta,state_after=z2,memory_after=mi2,terminal=terminal2
            ))
            z,mi=z2,mi2

            # Historical anti-stall guard: work-package completion is not controller completion.
            if terminal2=="CONTINUE" and not z.get("admitted_continuation",False):
                # CONTINUE without a live continuation is a typed controller defect.
                raise RuntimeError("ICC128_REENTRY_FAILURE:CONTINUE_without_admitted_continuation")

        raise RuntimeError("ICC128_RESOURCE_BOUND:max_iterations")

