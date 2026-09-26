"""Unified prospective lifecycle for new ideas, projects, tools and semantic objects.

The historical durable package is CORE + MANIFEST + 36 directed scope-transition
pages.  Unknown coordinates are explicit OPEN.  New projects additionally receive
typed project-bootstrap obligations; ideas remain candidates until disposition.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from semantic_object_package import (
    SemanticObjectSpec,
    materialize_package,
    verify_materialized_package,
)

MANAGED_KINDS={"IDEA","PROJECT","TOOL","META_TOOL","PROGRAM","SEMANTIC_OBJECT","TERM"}


@dataclass(frozen=True)
class ObjectLifecycleCandidate:
    object_id:str
    term:str
    kind:str
    definition:str
    source:str
    load_bearing:bool|None=True
    created_here:bool=True
    math_complete_for_use:bool=False
    open_coordinates:tuple[str,...]=()


@dataclass(frozen=True)
class ObjectLifecycleReceipt:
    object_id:str
    kind:str
    disposition:str
    package_current:bool
    files_created:int
    obligations:tuple[str,...]
    open:tuple[str,...]


def _kind(value:str)->str:
    k=str(value).upper().strip()
    if k not in MANAGED_KINDS:
        raise ValueError("UNSUPPORTED_OBJECT_KIND")
    return k


def needs_semantic_package(candidate:ObjectLifecycleCandidate)->bool:
    k=_kind(candidate.kind)
    if k in {"IDEA","PROJECT","TOOL","META_TOOL","PROGRAM"}:
        return True
    return candidate.load_bearing is not False


def _open(candidate:ObjectLifecycleCandidate)->tuple[str,...]:
    out=list(candidate.open_coordinates)
    if candidate.load_bearing is None:
        out.append("load_bearingness")
    if not candidate.definition.strip():
        out.append("exact_definition")
    if _kind(candidate.kind) in {"TOOL","META_TOOL","PROGRAM"} and not candidate.math_complete_for_use:
        out.append("mathematics_complete_for_advertised_use")
    return tuple(dict.fromkeys(out))


def semantic_spec(candidate:ObjectLifecycleCandidate)->SemanticObjectSpec:
    opened=_open(candidate)
    status="BLACK_BOX_OPEN" if opened else "DEFINED"
    definition=candidate.definition.strip() or "Unresolved candidate object captured before semantic loss."
    return SemanticObjectSpec(
        object_id=candidate.object_id,
        term=candidate.term,
        object_type=_kind(candidate.kind),
        status=status,
        definition=definition,
        known=(f"source: {candidate.source}",),
        open_coordinates=opened,
        protected_uses=("preserve identity","preserve provenance","prevent silent semantic drift"),
    )


def project_bootstrap_obligations()->tuple[str,...]:
    return (
        "PORTFOLIO_REGISTRATION",
        "PROJECT_ID_AND_KIND",
        "ORIENTATION_PROJECT_PAGE",
        "CURRENT_STATE_HOME",
        "PROVENANCE_AUTHORITY_HOME",
        "TASK_ENTRY_ROUTE",
        "UNFINISHED_WORK_ROUTE",
        "CAPABILITY_INHERITANCE_ROUTE",
    )


def idea_bootstrap_obligations()->tuple[str,...]:
    return (
        "PRESERVE_SOURCE",
        "TYPE_AND_RELATE",
        "DISPOSITION_ACCEPT_MERGE_REJECT_OPEN",
        "PROMOTE_TO_PROJECT_OR_TOOL_ONLY_WITH_TYPED_TRANSITION",
    )


def bootstrap_object(base:Path,candidate:ObjectLifecycleCandidate)->ObjectLifecycleReceipt:
    k=_kind(candidate.kind)
    if not needs_semantic_package(candidate):
        return ObjectLifecycleReceipt(
            candidate.object_id,k,"NOT_LOAD_BEARING",False,0,(),()
        )

    spec=semantic_spec(candidate)
    written=materialize_package(base,spec,allow_existing=True)
    current=verify_materialized_package(base,candidate.object_id)

    obligations=[]
    if k=="PROJECT":
        obligations.extend(project_bootstrap_obligations())
    elif k=="IDEA":
        obligations.extend(idea_bootstrap_obligations())
    elif k in {"TOOL","META_TOOL","PROGRAM"} and not candidate.math_complete_for_use:
        obligations.append("COMPLETE_REQUIRED_MATHEMATICS_BEFORE_ADMISSION")

    opened=list(_open(candidate))
    if not current:
        opened.append("SEMANTIC_PACKAGE_NOT_CURRENT")

    disposition="BOOTSTRAPPED" if current else "OPEN"
    if opened and current:
        disposition="BOOTSTRAPPED_WITH_OPEN_COORDINATES"

    return ObjectLifecycleReceipt(
        candidate.object_id,k,disposition,current,len(written),
        tuple(obligations),tuple(dict.fromkeys(opened)),
    )


def candidates_from_state(state:Any)->tuple[ObjectLifecycleCandidate,...]:
    if not isinstance(state,dict):
        return ()
    raw=state.get("new_objects",())
    out=[]
    for item in raw:
        if not isinstance(item,dict):
            continue
        if not item.get("object_id") or not item.get("term") or not item.get("kind"):
            continue
        out.append(ObjectLifecycleCandidate(
            object_id=str(item["object_id"]),
            term=str(item["term"]),
            kind=str(item["kind"]),
            definition=str(item.get("definition","")),
            source=str(item.get("source","improvecore")),
            load_bearing=item.get("load_bearing",True),
            created_here=bool(item.get("created_here",True)),
            math_complete_for_use=bool(item.get("math_complete_for_use",False)),
            open_coordinates=tuple(str(x) for x in item.get("open_coordinates",())),
        ))
    return tuple(out)


def bootstrap_state_objects(base:Path,state:Any)->tuple[ObjectLifecycleReceipt,...]:
    return tuple(bootstrap_object(base,c) for c in candidates_from_state(state))
