"""Non-destructive project packages for the Take-5 tool/ICC system.

The project package is an organizational overlay. It never becomes a second
semantic authority for tool mathematics or runtime behavior.

Each current configured tool and each admitted historical ICC/IC referent gets
its own durable package with:
- explicit authority routing;
- current projection separated from history/evidence;
- append-only decision/lesson/evidence channels;
- one 36-cell Scope x ModeFace coverage surface.

The distinct 36-cell SourceScope x TargetScope handoff surface remains owned by
semantic-object packages. Equal cardinality never licenses equivalence.

Materialization is fail-closed: an existing file with different bytes is never
silently rewritten.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from run_geometry import ModeFace
from scope_ontology import Scope
from tool_manifest import manifest_for
from tool_run_registry import MATERIAL_TOOLS
from portable_tool_conductor import compilation_witness


class ToolProjectPackageCollision(RuntimeError):
    pass


PACKAGE_ROOT="projects/tool-system"
CORE_FILES=(
    "README.md",
    "MANIFEST.md",
    "AUTHORITY_REGISTRY.md",
    "CURRENT_STATE.md",
    "IDENTITY.md",
    "MATHEMATICS.md",
    "RUNTIME.md",
    "PROTECTED_BEHAVIORS.md",
    "DEPENDENCIES.md",
    "SOURCE_MAP.md",
    "OPEN_QUESTIONS.md",
    "CHANGE_CONTROL.md",
    "REGRESSION_CONTRACT.md",
    "DECISION_LOG.md",
    "LESSONS_LEDGER.md",
    "HANDOFF_SURFACE.md",
    "evidence/README.md",
    "runs/README.md",
    "history/README.md",
    "coverage/README.md",
)

@dataclass(frozen=True)
class ProjectObjectSpec:
    object_id:str
    display_name:str
    species:str
    status:str
    source_refs:tuple[str,...]=()
    aliases:tuple[str,...]=()

    @property
    def current_tool(self)->bool:
        return self.species=="CURRENT_CONFIGURED_TOOL"


def slug(value:str)->str:
    out=[]
    for ch in str(value).lower():
        out.append(ch if ch.isalnum() else "-")
    return "-".join(filter(None,"".join(out).split("-")))


def coverage_cells()->tuple[tuple[int,Scope,ModeFace],...]:
    rows=[]
    n=1
    for scope in Scope:
        for face in ModeFace:
            rows.append((n,scope,face))
            n+=1
    if len(rows)!=36:
        raise RuntimeError("TOOL_PROJECT_COVERAGE_NOT_36")
    return tuple(rows)


def coverage_name(index:int,scope:Scope,face:ModeFace)->str:
    return f"{index:02d}_{scope.value}__{face.value}.md"


def current_tool_specs()->tuple[ProjectObjectSpec,...]:
    return tuple(
        ProjectObjectSpec(
            object_id=str(tool_id),
            display_name=str(tool_id),
            species="CURRENT_CONFIGURED_TOOL",
            status="CURRENT",
            source_refs=(
                "runtime/tool_run_registry.py",
                "runtime/tool_manifest.py",
                "runtime/portable_tool_conductor.py",
                "integration/CURRENT_TOOL_REALITY.md",
            ),
        )
        for tool_id in MATERIAL_TOOLS
    )


# Historical controller variants are deliberately separate from the live
# configured-tool registry. Missing/recovered-only identities remain typed OPEN.
ICC_VARIANTS=(
    # Reaserch immutable version lineage.
    ("IC-001","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-001.yaml"),
    ("IC-002","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-002.yaml"),
    ("IC-003","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-003.yaml"),
    ("IC-004","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-004.yaml"),
    ("IC-005","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-005.yaml"),
    ("IC-006","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-006.yaml"),
    ("IC-007","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-007.yaml"),
    ("IC-008","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-008.yaml"),
    ("IC-009","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-009.yaml"),
    ("IC-010","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-010.yaml"),
    ("IC-011","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-011.yaml"),
    ("IC-012","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-012.yaml"),
    ("IC-013","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-013.yaml"),
    ("IC-014","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-014.yaml"),
    ("IC-015","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-015.yaml"),
    ("IC-017","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-017.yaml"),
    ("IC-018","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-23-018.yaml"),
    ("IC-019","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-24-019.yaml"),
    ("IC-020","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-24-020.yaml"),
    ("IC-021","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-24-021.yaml"),
    ("IC-022","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-24-022.yaml"),
    ("IC-023","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-24-023.yaml"),
    ("IC-024","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-24-024.yaml"),
    ("IC-025","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-24-025.yaml"),
    ("IC-026","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-24-026.yaml"),
    ("IC-028","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-24-028.yaml"),
    ("IC-024-G1","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-24-024-G1.yaml"),
    ("IC-024-G2","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-24-024-G2.yaml"),
    ("IC-024-G3","LEGACY_PROVENANCE","thytabakman-jpg/Reaserch:projects/improvement-core/versions/IC-2026-09-24-024-G3.yaml"),
    ("IC-016","UNRECOVERED_GAP","no canonical version artifact recovered"),
    ("IC-027","UNRECOVERED_GAP","no canonical version artifact recovered"),
    ("IC-029","LEGACY_RESEARCH_SUCCESSOR","thytabakman-jpg/Reaserch:architecture/IC029_IMPROVED_CORE_SELF_AUDITED_MAP_076.md"),
    ("IC-030","LEGACY_RESEARCH_SUCCESSOR","thytabakman-jpg/Reaserch:architecture/IC030_RECURSIVE_IMPROVEMENTCORE_MANAGER_001.md"),
    ("IC-031","LEGACY_RESEARCH_SUCCESSOR","thytabakman-jpg/Reaserch:architecture/IC031_COMPOUNDING_DISCOVERY_IMPROVEMENTCORE_001.md"),
    ("IC-032","LEGACY_RESEARCH_SUCCESSOR","thytabakman-jpg/Reaserch:architecture/IC032_CUMULATIVE_EXPERIMENTAL_IMPROVECORE_001.md"),
    # Later named ICC objects.
    ("ICC","CURRENT_INTEGRATED_STACK","ICC_AUTONOMOUS_STEWARDSHIP.md"),
    ("ICC-107","MENTIONED_UNRECOVERED","conversation-recovered label; no defining repository artifact recovered"),
    ("ICC-108","MENTIONED_UNRECOVERED","conversation-recovered label; no defining repository artifact recovered"),
    ("ICC-118","UNRECOVERED_FORMAL_OBJECT","recovered completion-guard mention; no canonical formal object recovered"),
    ("IC-121","UNRESOLVED_HISTORICAL_IDENTITY","conversation-recovered historical identity; defining artifact not recovered"),
    ("IC-122","UNRESOLVED_HISTORICAL_IDENTITY","conversation-recovered historical identity; defining artifact not recovered"),
    ("ICC-123","RECOVERED_HISTORICAL_OBJECT","integration/ICC123_THREE_DAY_RECOVERY_STATE_001_2026-09-25.md"),
    ("ICC-124","LINEAGE_OPEN","integration/ICC124_LINEAGE_RECOVERY_001_2026-09-25.md"),
    ("ICC-128-LEGACY","PRESERVED_LEGACY_OBJECT","legacy/icc128-legacy/MANIFEST.yaml"),
    ("ICC-128-CURRENT","CURRENT_CONFIGURED_IDENTITY_VIEW","integration/CURRENT_ICC128_CONVERSATION_CONTROL.md"),
)

ICC_ALIASES={
    "ICC-022":"IC-022",
    "ICC-023":"IC-023",
    "ICC-024":"IC-024",
    "IC028":"IC-028",
    "ICC128":"ICC-128-CURRENT",
}


def icc_variant_specs()->tuple[ProjectObjectSpec,...]:
    out=[]
    reverse={}
    for alias,target in ICC_ALIASES.items():
        reverse.setdefault(target,[]).append(alias)
    for object_id,status,source in ICC_VARIANTS:
        out.append(ProjectObjectSpec(
            object_id=object_id,
            display_name=object_id,
            species="ICC_VARIANT",
            status=status,
            source_refs=(source,),
            aliases=tuple(reverse.get(object_id,())),
        ))
    return tuple(out)


def all_project_specs()->tuple[ProjectObjectSpec,...]:
    return current_tool_specs()+icc_variant_specs()


def package_relroot(spec:ProjectObjectSpec)->str:
    family="current-tools" if spec.current_tool else "icc-variants"
    return f"{family}/{slug(spec.object_id)}"


def _bullets(values:Iterable[str])->str:
    rows=tuple(str(x) for x in values if str(x))
    return "\n".join(f"- {x}" for x in rows) if rows else "- none"


def _tool_manifest_projection(spec:ProjectObjectSpec)->dict[str,Any]:
    if not spec.current_tool:
        return {}
    manifest=manifest_for(spec.object_id)
    witness=compilation_witness(spec.object_id)
    return {
        "native_semantics":manifest.native_semantics,
        "geometry_policy":manifest.geometry_policy,
        "closure_contract":manifest.closure_contract,
        "reentry_contract":manifest.reentry_contract,
        "lineage_contract":manifest.lineage_contract,
        "behaviors":tuple(
            (b.behavior_id,b.phase,b.implementation,b.witness)
            for b in manifest.bindings
        ),
        "entrypoint":witness.entrypoint,
        "required_environment":tuple(witness.required_environment),
        "realization_status":witness.status,
    }


def render_readme(spec:ProjectObjectSpec)->str:
    return f"""# {spec.display_name} project package

Object ID: {spec.object_id}
Species: {spec.species}
Package status: {spec.status}

## Purpose

This package organizes the object without becoming a second semantic authority.

## Entry order

1. CURRENT_STATE.md
2. AUTHORITY_REGISTRY.md
3. IDENTITY.md
4. MATHEMATICS.md
5. RUNTIME.md
6. PROTECTED_BEHAVIORS.md
7. DEPENDENCIES.md
8. OPEN_QUESTIONS.md
9. SOURCE_MAP.md
10. coverage/ only for coverage evidence

## Anti-loss rule

Do not overwrite history, decisions, lessons, run evidence, or coverage-cell evidence.
Current projections may change only through explicit change control and retained lineage.
"""


def render_manifest(spec:ProjectObjectSpec)->str:
    coverage="\n".join(
        f"- coverage/{coverage_name(i,s,f)}"
        for i,s,f in coverage_cells()
    )
    core="\n".join(f"- {x}" for x in CORE_FILES)
    return f"""# Package manifest: {spec.display_name}

Object ID: {spec.object_id}
Species: {spec.species}
Status: {spec.status}
Coverage surface: Scope x ModeFace
Coverage cells: 36

## Required files

{core}

## Coverage pages

{coverage}

## Separate 36-surface warning

SourceScope x TargetScope is a different 36-cell handoff surface. It is not
stored in coverage/. See HANDOFF_SURFACE.md.
"""


def render_authority(spec:ProjectObjectSpec)->str:
    return f"""# Authority registry: {spec.display_name}

Status: CURRENT PACKAGE ROUTING

| Object | Owner |
|---|---|
| package identity/status routing | this package |
| current configured-tool identity | runtime/tool_run_registry.py |
| current protected tool identity | runtime/tool_manifest.py |
| current executable realization | runtime/portable_tool_conductor.py |
| historical/lineage evidence | SOURCE_MAP.md pointers |
| package current projection | CURRENT_STATE.md |
| unresolved package questions | OPEN_QUESTIONS.md |
| decisions | DECISION_LOG.md, append-only |
| lessons | LESSONS_LEDGER.md, append-only |
| run evidence | runs/, append-only |
| evidence entries | evidence/, append-only |
| coverage findings | coverage/*.md, audit evidence only |

## Collision rule

A package file does not acquire authority merely by repeating content from an
external canonical source. When two locations appear to own the same mutable
truth, fix the routing before editing either one.
"""


def render_current(spec:ProjectObjectSpec)->str:
    p=_tool_manifest_projection(spec)
    extra=""
    if p:
        extra=f"""
Configured identity: REGISTERED
Manifest identity: EXPLICIT
Native realization: {p['realization_status']}
Runtime entrypoint: {p['entrypoint'] or 'OPEN'}
Required environment: {', '.join(p['required_environment']) if p['required_environment'] else 'none'}
"""
    return f"""# Current state: {spec.display_name}

Projection status: CURRENT
Object status: {spec.status}
Species: {spec.species}
{extra}
## Projection rule

This file is a disposable current projection over retained authority and evidence.
It does not erase history and it does not supersede external semantic authority
without an explicit admitted change.
"""


def render_identity(spec:ProjectObjectSpec)->str:
    return f"""# Identity: {spec.display_name}

Object ID: {spec.object_id}
Species: {spec.species}
Status: {spec.status}
Aliases: {', '.join(spec.aliases) if spec.aliases else 'none'}

## Identity rule

Names are routing labels. Identity is not inferred from lexical similarity,
shared numbering, or equal cardinality of structures.
"""


def render_math(spec:ProjectObjectSpec)->str:
    p=_tool_manifest_projection(spec)
    if p:
        body=f"""Current native-semantics projection:

{p['native_semantics']}

Geometry policy:

{p['geometry_policy']}

Lineage authority:

{p['lineage_contract']}
"""
    else:
        body=f"""No mathematics is copied into this organizational package.

Current disposition:

{spec.status}

Resolve mathematics only from the sources in SOURCE_MAP.md. Missing mathematics
remains explicit OPEN rather than being reconstructed from the label alone.
"""
    return f"""# Mathematics pointer: {spec.display_name}

## Non-duplication rule

This page is a routing projection, not the canonical mathematical definition.

{body}
"""


def render_runtime(spec:ProjectObjectSpec)->str:
    p=_tool_manifest_projection(spec)
    if not p:
        body="This historical/ICC variant is not admitted into the current configured runtime by this package."
    else:
        body=f"""Entrypoint: {p['entrypoint'] or 'OPEN'}
Realization status: {p['realization_status']}
Required environment:
{_bullets(p['required_environment'])}

Closure contract: {p['closure_contract']}
Reentry contract: {p['reentry_contract']}
"""
    return f"""# Runtime pointer: {spec.display_name}

{body}

## Rule

Package existence is not execution evidence. A plan, runtime entrypoint, run,
receipt, and parent closure remain distinct objects.
"""


def render_behaviors(spec:ProjectObjectSpec)->str:
    p=_tool_manifest_projection(spec)
    if not p:
        rows="- unresolved / source-relative"
    else:
        rows="\n".join(
            f"- {bid} | phase={phase} | implementation={impl} | witness={wit}"
            for bid,phase,impl,wit in p["behaviors"]
        ) or "- no tool-specific behavior beyond admitted generic configured behavior"
    return f"""# Protected behaviors: {spec.display_name}

{rows}

## Rule

This is a projection of current manifest bindings. Edit protected behavior at its
canonical authority, then regenerate/reconcile this projection with retained lineage.
"""


def render_dependencies(spec:ProjectObjectSpec)->str:
    p=_tool_manifest_projection(spec)
    env=p.get("required_environment",()) if p else ()
    return f"""# Dependencies: {spec.display_name}

## Canonical dependencies

{_bullets(spec.source_refs)}

## Runtime environment dependencies

{_bullets(env)}

## Rule

A dependency change reopens the affected cone. Unaffected package state remains protected.
"""


def render_source_map(spec:ProjectObjectSpec)->str:
    return f"""# Source map: {spec.display_name}

## Direct sources

{_bullets(spec.source_refs)}

## Shared current authorities

- runtime/tool_run_registry.py
- runtime/tool_manifest.py
- integration/CURRENT_TOOL_REALITY.md
- projects/tool-system/AUTHORITY_REGISTRY.md

## Rule

Pointers preserve provenance. This package does not copy legacy evidence merely
to make the folder look complete.
"""


def render_open(spec:ProjectObjectSpec)->str:
    if spec.current_tool:
        body="- package-specific open questions are added here only when they are not already owned by a canonical source"
    else:
        body=f"- semantic/currentness reconstruction remains governed by status {spec.status}\n- do not infer missing role from numbering or neighboring variants"
    return f"""# OPEN questions: {spec.display_name}

{body}

## Rule

OPEN is durable state. Closing an item requires evidence and a receipt; deleting
the line because a later summary is shorter is forbidden.
"""


def render_change(spec:ProjectObjectSpec)->str:
    return f"""# Change control: {spec.display_name}

Delta = <request, owner, old_state, proposed_state, reason, dependencies, tests, decision, receipt>.

Change the smallest authority that owns the property.
Do not clean-rebuild this package because one coordinate changed.
Inspect the affected dependency cone after every admitted material delta.
Retain old evidence and record supersession rather than rewriting history.
"""


def render_regression(spec:ProjectObjectSpec)->str:
    return f"""# Regression contract: {spec.display_name}

A valid package keeps all of these true:

- required core files exist
- exactly 36 Scope x ModeFace coverage pages exist
- coverage pages are audit evidence, not semantic authority
- the distinct SourceScope x TargetScope surface is not merged into coverage
- decisions, lessons, runs, and evidence are append-only
- package generation never overwrites changed existing files
- current configured tools have one package each
- aliases do not create duplicate mutable authority
- missing semantics/runtime/evidence remain typed OPEN
"""


def render_decisions(spec:ProjectObjectSpec)->str:
    return f"""# Decision log: {spec.display_name}

Append-only.

## 2026-09-27 D001

Created the non-destructive project package. Existing semantic/runtime authority
was preserved in place; this package owns organization, routing, and retained
package-local state only.
"""


def render_lessons(spec:ProjectObjectSpec)->str:
    return f"""# Lessons ledger: {spec.display_name}

Append-only.

## 2026-09-27 L001

Separating dimensions into owned pages prevents one analysis dimension from
silently rewriting another.

## 2026-09-27 L002

Current projection, historical evidence, semantic authority, runtime reality,
and run evidence are different objects and require different owners.
"""


def render_handoff(spec:ProjectObjectSpec)->str:
    return f"""# Handoff surface: {spec.display_name}

The package coverage directory uses:

Scope x ModeFace = 6 x 6 = 36.

The separate semantic handoff surface is:

SourceScope x TargetScope = 6 x 6 = 36.

Equal cardinality does not make these the same object.

When {spec.display_name} has result-sensitive directed handoff semantics, those
belong in the semantic-object package / directed-handoff authority, not in the
Scope x ModeFace coverage pages.
"""


def render_stream(spec:ProjectObjectSpec,name:str)->str:
    return f"""# {name}: {spec.display_name}

This directory is append-only.
Create a new uniquely named record for each material entry.
Do not replace an older record with a newer one.
"""


def render_coverage_readme(spec:ProjectObjectSpec)->str:
    return f"""# 36-cell coverage: {spec.display_name}

Surface: Scope x ModeFace.
Role: audit / discovery / regression evidence only.
Cells: 36.

Each cell owns findings for one coordinate. A finding becomes canonical only
through the authority and change-control path.
"""


def render_coverage_cell(spec:ProjectObjectSpec,index:int,scope:Scope,face:ModeFace)->str:
    return f"""# {spec.display_name}: {scope.value} x {face.value}

Object ID: {spec.object_id}
Coverage cell: {index:02d}/36
Scope: {scope.value}
Mode face: {face.value}
Authority: AUDIT_EVIDENCE_ONLY
Disposition: OPEN

## Findings

- none admitted yet

## OPEN

- determine whether this coordinate exposes a result-sensitive distinction for this object

## Non-overwrite rule

Add evidence here without replacing findings owned by another coverage cell.
Canonical semantic changes route through AUTHORITY_REGISTRY.md and CHANGE_CONTROL.md.
"""


def package_files(spec:ProjectObjectSpec)->dict[str,str]:
    root=package_relroot(spec)
    files={
        f"{root}/README.md":render_readme(spec),
        f"{root}/MANIFEST.md":render_manifest(spec),
        f"{root}/AUTHORITY_REGISTRY.md":render_authority(spec),
        f"{root}/CURRENT_STATE.md":render_current(spec),
        f"{root}/IDENTITY.md":render_identity(spec),
        f"{root}/MATHEMATICS.md":render_math(spec),
        f"{root}/RUNTIME.md":render_runtime(spec),
        f"{root}/PROTECTED_BEHAVIORS.md":render_behaviors(spec),
        f"{root}/DEPENDENCIES.md":render_dependencies(spec),
        f"{root}/SOURCE_MAP.md":render_source_map(spec),
        f"{root}/OPEN_QUESTIONS.md":render_open(spec),
        f"{root}/CHANGE_CONTROL.md":render_change(spec),
        f"{root}/REGRESSION_CONTRACT.md":render_regression(spec),
        f"{root}/DECISION_LOG.md":render_decisions(spec),
        f"{root}/LESSONS_LEDGER.md":render_lessons(spec),
        f"{root}/HANDOFF_SURFACE.md":render_handoff(spec),
        f"{root}/evidence/README.md":render_stream(spec,"Evidence"),
        f"{root}/runs/README.md":render_stream(spec,"Run evidence"),
        f"{root}/history/README.md":render_stream(spec,"History"),
        f"{root}/coverage/README.md":render_coverage_readme(spec),
    }
    for i,scope,face in coverage_cells():
        files[f"{root}/coverage/{coverage_name(i,scope,face)}"]=render_coverage_cell(spec,i,scope,face)
    return files


def materialize_package(base:Path,spec:ProjectObjectSpec)->tuple[Path,...]:
    written=[]
    for rel,content in package_files(spec).items():
        path=base/rel
        path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists():
            existing=path.read_text(encoding="utf-8")
            if existing!=content:
                raise ToolProjectPackageCollision(str(path))
            continue
        path.write_text(content,encoding="utf-8")
        written.append(path)
    return tuple(written)


def materialize_all(base:Path)->tuple[Path,...]:
    written=[]
    for spec in all_project_specs():
        written.extend(materialize_package(base,spec))
    return tuple(written)


def append_record(base:Path,spec:ProjectObjectSpec,stream:str,record_id:str,content:str)->Path:
    if stream not in {"evidence","runs","history"}:
        raise ValueError("APPEND_STREAM_INVALID")
    rid=slug(record_id)
    if not rid:
        raise ValueError("RECORD_ID_REQUIRED")
    path=base/PACKAGE_ROOT/package_relroot(spec)/stream/f"{rid}.md"
    path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():
        raise FileExistsError(str(path))
    path.write_text(content,encoding="utf-8")
    return path


def audit_materialized(base:Path)->dict[str,Any]:
    missing=[]
    bad_coverage=[]
    root=base/PACKAGE_ROOT
    for spec in all_project_specs():
        p=root/package_relroot(spec)
        for rel in CORE_FILES:
            if not (p/rel).is_file():
                missing.append(f"{spec.object_id}:{rel}")
        expected={coverage_name(i,s,f) for i,s,f in coverage_cells()}
        cdir=p/"coverage"
        actual={x.name for x in cdir.glob("*.md") if x.name!="README.md"} if cdir.is_dir() else set()
        if actual!=expected:
            bad_coverage.append(spec.object_id)
    current_dirs={slug(x) for x in MATERIAL_TOOLS}
    represented={slug(s.object_id) for s in current_tool_specs()}
    registry_parity=current_dirs==represented
    return {
        "status":"CLOSED_RELATIVE" if not missing and not bad_coverage and registry_parity else "OPEN",
        "object_count":len(all_project_specs()),
        "current_tool_count":len(current_tool_specs()),
        "icc_variant_count":len(icc_variant_specs()),
        "missing":tuple(missing),
        "bad_coverage":tuple(bad_coverage),
        "registry_parity":registry_parity,
    }
