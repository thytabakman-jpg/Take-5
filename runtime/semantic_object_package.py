"""Durable semantic-object package generator.

Creates one core semantic page plus the canonical 6x6 directed scope-transition
surface. Unknown cells are explicit OPEN pages. Evidence is append-only.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from scope_ontology import Scope, required_handoff

SEMANTIC_STATUSES={"DEFINED","PARTIAL","BLACK_BOX_OPEN"}

@dataclass(frozen=True)
class SemanticObjectSpec:
    object_id:str
    term:str
    object_type:str
    status:str
    definition:str
    known:tuple[str,...]=()
    open_coordinates:tuple[str,...]=()
    dependencies:tuple[str,...]=()
    protected_uses:tuple[str,...]=()

    def __post_init__(self):
        if self.status not in SEMANTIC_STATUSES:
            raise ValueError("invalid semantic status")
        if not self.object_id or not self.term or not self.object_type:
            raise ValueError("identity/type required")
        if self.status=="BLACK_BOX_OPEN" and not self.open_coordinates:
            raise ValueError("BLACK_BOX_OPEN requires open_coordinates")

def slug(value:str)->str:
    out=[]
    for ch in value.lower():
        out.append(ch if ch.isalnum() else "-")
    return "-".join(filter(None,"".join(out).split("-")))

def transition_name(source:Scope,target:Scope)->str:
    return f"{source.value.lower()}__to__{target.value.lower()}.md"

def expected_transition_names()->tuple[str,...]:
    return tuple(transition_name(a,b) for a in Scope for b in Scope)

def _bullets(values:Iterable[str])->str:
    xs=tuple(values)
    return "\n".join(f"- {x}" for x in xs) if xs else "- none"

def render_core(spec:SemanticObjectSpec)->str:
    return f"""# {spec.term}

Object ID: {spec.object_id}
Type: {spec.object_type}
Status: {spec.status}

## Current definition

{spec.definition}

## Known

{_bullets(spec.known)}

## OPEN coordinates

{_bullets(spec.open_coordinates)}

## Dependencies

{_bullets(spec.dependencies)}

## Protected uses

{_bullets(spec.protected_uses)}

## Update rule

This page is the current projection. New evidence is retained append-only under evidence/.
Do not delete unresolved coordinates merely because a newer summary is shorter.
"""

def render_transition(spec:SemanticObjectSpec,source:Scope,target:Scope)->str:
    handoff=required_handoff(source,target)
    h="SELF" if handoff is None else handoff.value
    return f"""# {spec.term}: {source.value} -> {target.value}

Object ID: {spec.object_id}
Source scope: {source.value}
Target scope: {target.value}
Handoff: {h}
Disposition: OPEN

## Current evidence

No cell-specific semantic evidence has been admitted yet.

## OPEN

- determine whether this object has a result-sensitive role on this directed scope transition
- preserve identity, provenance, authority, protected behavior, and OPEN status during any handoff

## Rule

OPEN is explicit coverage, not absence of a page.
"""

def render_manifest(spec:SemanticObjectSpec)->str:
    names=expected_transition_names()
    rows="\n".join(f"- transitions/{name}" for name in names)
    return f"""# Semantic Object Package: {spec.term}

Object ID: {spec.object_id}
Package status: {spec.status}
Transition-page count: {len(names)}

## Required pages

- CORE.md
- MANIFEST.md
{rows}

## Evidence

Evidence entries are append-only under evidence/.
"""

def package_files(spec:SemanticObjectSpec)->dict[str,str]:
    root=slug(spec.object_id)
    files={
        f"{root}/CORE.md":render_core(spec),
        f"{root}/MANIFEST.md":render_manifest(spec),
    }
    for source in Scope:
        for target in Scope:
            files[f"{root}/transitions/{transition_name(source,target)}"]=render_transition(spec,source,target)
    return files

def materialize_package(base:Path,spec:SemanticObjectSpec,*,allow_existing:bool=True)->tuple[Path,...]:
    written=[]
    for rel,content in package_files(spec).items():
        path=base/rel
        path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists():
            if not allow_existing:
                raise FileExistsError(path)
            continue
        path.write_text(content,encoding="utf-8")
        written.append(path)
    return tuple(written)

def append_evidence(base:Path,spec:SemanticObjectSpec,evidence_id:str,content:str)->Path:
    if not evidence_id.strip():
        raise ValueError("evidence_id required")
    root=base/slug(spec.object_id)/"evidence"
    root.mkdir(parents=True,exist_ok=True)
    path=root/f"{slug(evidence_id)}.md"
    if path.exists():
        raise FileExistsError("evidence entries are immutable")
    path.write_text(content,encoding="utf-8")
    return path

def package_complete(paths:Iterable[str])->bool:
    ps=set(paths)
    required={"CORE.md","MANIFEST.md"}
    transition_paths={f"transitions/{n}" for n in expected_transition_names()}
    return required <= ps and transition_paths <= ps


def verify_materialized_package(base:Path, object_id:str)->bool:
    """Verify package reality from durable storage rather than caller assertion."""
    root=base/slug(object_id)
    if not (root/"CORE.md").is_file() or not (root/"MANIFEST.md").is_file():
        return False
    transitions=root/"transitions"
    if not transitions.is_dir():
        return False
    actual={p.name for p in transitions.iterdir() if p.is_file()}
    return set(expected_transition_names()) <= actual
