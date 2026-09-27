#!/usr/bin/env python3
"""Schema-enforcing adapter for ICC-128 semantic G_Q/G_W generation."""
from __future__ import annotations
from typing import Any, Protocol

class SemanticModel(Protocol):
    def __call__(self,payload:dict[str,Any])->dict[str,Any]: ...

Q_FIELDS={
 "question_id","question","live_candidate_answers","enabling_discovery_or_distinction",
 "unresolved_structure","downstream_dependency"
}
W_FIELDS={
 "work_id","question_id","probe_or_test","candidate_answers_discriminated",
 "expected_search_space_effect","required_inputs_or_sources","execution_or_semantic_route"
}
UPSTREAM_FIELDS={
 "origin_mode","source_job_id","job_basis","source_relations","candidate_universe_delta"
}

def _require(obj:dict[str,Any],fields:set[str],kind:str)->None:
    missing=fields-set(obj)
    if missing: raise ValueError(f"{kind}_MISSING_FIELDS:{sorted(missing)}")

def _validate_upstream(upstream_context:dict[str,Any]|None)->dict[str,Any]|None:
    if upstream_context is None:
        return None
    _require(upstream_context,UPSTREAM_FIELDS,"UPSTREAM_CONTEXT")
    if upstream_context["origin_mode"] not in {"ZERO_REQUEST","DIRECTED_UPSTREAM_DISCOVERY"}:
        raise ValueError("UPSTREAM_ORIGIN_MODE_INVALID")
    if upstream_context["origin_mode"]=="ZERO_REQUEST":
        if upstream_context.get("job_basis")=="user_supplied_substantive_job":
            raise ValueError("ZERO_REQUEST_ORIGIN_CONTAMINATION")
    return dict(upstream_context)

def generate(model:SemanticModel,state:dict[str,Any],memory:dict[str,Any],
             upstream_context:dict[str,Any]|None=None)->dict[str,Any]:
    upstream=_validate_upstream(upstream_context)
    payload={
      "mode":"ICC128_OLD_RECURSIVE_PD_GENERATOR",
      "state":state,
      "memory":memory,
      "upstream_context":upstream,
      "instructions":[
        "reconstruct current epistemic state",
        "preserve live competing interpretations",
        "identify candidate-space before",
        "identify the distinction/discovery that changes the inquiry",
        "generate only questions newly available from unresolved current structure",
        "for each question generate a discriminating test/probe",
        "record expected candidate-space/search-space effect",
        "when upstream_context exists, preserve its origin/job/relation basis through question and work generation"
      ]
    }
    out=model(payload)
    qs=out.get("questions",[])
    ws=out.get("work",[])
    for q in qs: _require(q,Q_FIELDS,"QUESTION")
    for w in ws: _require(w,W_FIELDS,"WORK")
    qids={q["question_id"] for q in qs}
    for w in ws:
        if w["question_id"] not in qids:
            raise ValueError(f"WORK_ORPHAN:{w['work_id']}")
    if state.get("unresolved") and state.get("admitted_continuation") and not qs:
        raise ValueError("GQ_LIVENESS_FAILURE")

    # Preserve endogenous-origin evidence across the handoff.
    origin_witness=None
    if upstream is not None:
        returned=out.get("upstream_origin_witness")
        if returned is None:
            raise ValueError("UPSTREAM_ORIGIN_WITNESS_MISSING")
        _require(returned,{"source_job_id","job_basis","source_relations"},"UPSTREAM_ORIGIN_WITNESS")
        for k in ("source_job_id","job_basis"):
            if returned[k] != upstream[k]:
                raise ValueError(f"UPSTREAM_ORIGIN_WITNESS_MISMATCH:{k}")
        if list(returned["source_relations"]) != list(upstream["source_relations"]):
            raise ValueError("UPSTREAM_ORIGIN_WITNESS_MISMATCH:source_relations")
        origin_witness=dict(returned)

    return {
        "questions":qs,
        "work":ws,
        "search_space_delta":out.get("search_space_delta",{}),
        "upstream_origin_witness":origin_witness,
    }
