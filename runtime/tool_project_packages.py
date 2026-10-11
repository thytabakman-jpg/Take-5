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
import json
from pathlib import Path
from typing import Any, Iterable

from run_geometry import ModeFace
from scope_ontology import Scope
from tool_run_registry import MATERIAL_TOOLS


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
# configured-tool registry. Their provenance lives in project-owned data rather
# than in runtime source, preserving Take-5 predecessor independence.
ICC_VARIANT_DATA=Path(__file__).resolve().parents[1]/"projects/tool-system/ICC_VARIANT_SOURCES.json"


def _variant_payload()->dict[str,Any]:
    if not ICC_VARIANT_DATA.is_file():
        raise RuntimeError("ICC_VARIANT_SOURCE_DATA_MISSING")
    value=json.loads(ICC_VARIANT_DATA.read_text(encoding="utf-8"))
    if not isinstance(value,dict):
        raise RuntimeError("ICC_VARIANT_SOURCE_DATA_INVALID")
    return value


_VARIANT_PAYLOAD=_variant_payload()
ICC_ALIASES=dict(_VARIANT_PAYLOAD.get("aliases",{}))


def icc_variant_specs()->tuple[ProjectObjectSpec,...]:
    out=[]
    reverse={}
    for alias,target in ICC_ALIASES.items():
        reverse.setdefault(str(target),[]).append(str(alias))
    for row in _VARIANT_PAYLOAD.get("variants",()):
        if not isinstance(row,dict):
            raise RuntimeError("ICC_VARIANT_ROW_INVALID")
        object_id=str(row.get("object_id","")).strip()
        status=str(row.get("status","")).strip()
        source=str(row.get("source","")).strip()
        if not object_id or not status:
            raise RuntimeError("ICC_VARIANT_IDENTITY_INCOMPLETE")
        out.append(ProjectObjectSpec(
            object_id=object_id,
            display_name=object_id,
            species="ICC_VARIANT",
            status=status,
            source_refs=((source,) if source else ()),
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
    body=f"""# Authority registry: {spec.display_name}

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

    if spec.current_tool and spec.object_id=="MultiObject":
        body=body.replace(
            "| current executable realization | runtime/portable_tool_conductor.py |",
            "| current invocation routing | runtime/portable_tool_conductor.py |\n"
            "| MultiObject native execution | runtime/multiobject.py |\n"
            "| full mathematical identity | architecture/MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md |",
        )
    return body

def render_current(spec:ProjectObjectSpec)->str:
    return f"""# Current state: {spec.display_name}

Projection status: CURRENT
Object status: {spec.status}
Species: {spec.species}

## Projection rule

This file is a disposable current projection over retained authority and evidence.
For live configured tools, current identity/runtime reality stays owned by the
shared registry/manifest/runtime authorities listed in SOURCE_MAP.md.

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
    body=f"""# Mathematics pointer: {spec.display_name}

## Non-duplication rule

This page is a routing projection, not the canonical mathematical definition.

Resolve current mathematics from SOURCE_MAP.md and the current manifest/lineage
authorities. Historical or unresolved variants remain OPEN when their defining
mathematics is not recovered.

Do not copy the full mathematics here merely to make the package look complete.
"""

    if spec.current_tool and spec.object_id=="MultiObject":
        body += "\n## MultiObject mathematical identity\n\n- [Full mathematical identity](../../../../architecture/MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md)\n- [Protected-behavior manifest](../../../../runtime/tool_manifest.py)\n- [Pinned semantic and protocol provenance](SOURCE_MAP.md)\n\nThe two-role factorization is basis-relative; global minimality and completeness remain OPEN. This routing page does not replace the mathematical authority.\n"
    return body

def render_runtime(spec:ProjectObjectSpec)->str:
    if spec.current_tool:
        body="""Current runtime realization is owned by:
- runtime/portable_tool_conductor.py
- current dedicated runtime modules referenced by runtime/tool_manifest.py

This package records organization and source routing only."""
    else:
        body="This historical/ICC variant is not admitted into the current configured runtime by this package."
    body=f"""# Runtime pointer: {spec.display_name}

{body}

## Rule

Package existence is not execution evidence. A plan, runtime entrypoint, run,
receipt, and parent closure remain distinct objects.
"""

    if spec.current_tool and spec.object_id=="MultiObject":
        body += "\n## MultiObject executable route\n\n- [Native runtime implementation](../../../../runtime/multiobject.py) — `run_multiobject`\n- [Portable invocation conductor](../../../../runtime/portable_tool_conductor.py) — `multiobject.run_multiobject`\n- [Native runtime tests](../../../../tests/test_multiobject.py)\n\nDomain relation generation requires an explicit `multiobject_provider`. Absence of the provider cannot be reported as successful domain execution. This package remains an organizational projection.\n"
    return body

def render_behaviors(spec:ProjectObjectSpec)->str:
    return f"""# Protected behaviors: {spec.display_name}

Current protected behavior is owned by runtime/tool_manifest.py and its cited
implementation/witness surfaces for current configured tools.

Historical variants retain their protected-behavior evidence through SOURCE_MAP.md
without promotion into the live manifest.

## Rule

This page routes authority. It does not duplicate editable protected behavior.
"""


def render_dependencies(spec:ProjectObjectSpec)->str:
    return f"""# Dependencies: {spec.display_name}

## Canonical dependencies

{_bullets(spec.source_refs)}

## Shared runtime/identity dependencies

- runtime/tool_run_registry.py
- runtime/tool_manifest.py
- runtime/portable_tool_conductor.py

## Rule

A dependency change reopens the affected cone. Unaffected package state remains protected.
"""


def render_source_map(spec:ProjectObjectSpec)->str:
    body=f"""# Source map: {spec.display_name}

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

    if spec.current_tool and spec.object_id=="MultiObject":
        body += "\n## MultiObject-specific current implementation and identity\n\n- [Native orchestration](../../../../runtime/multiobject.py)\n- [Full mathematical identity](../../../../architecture/MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md)\n- [Native regression tests](../../../../tests/test_multiobject.py)\n- [Mathematical identity regression tests](../../../../tests/test_multiobject_fullmath_identity.py)\n\n## Pinned historical mathematical and protocol lineage\n\nThe full mathematical identity pins the historical evidence basis to `HISTORICAL_REPO@492bf7da82ac346c1a17ab0acc2405adf17ae5c1`. These links preserve the input lineage; they do not confer current Take-5 execution authority.\n\n- [Multi-Object v0.2 canonical mathematics](https://github.com/HISTORICAL_REPO/blob/492bf7da82ac346c1a17ab0acc2405adf17ae5c1/projects/core-system-mathematics/math/MULTI_OBJECT_V2_CANONICAL_MATHEMATICS_001_2026-09-24.md)\n- [Multi-Object Connector protocol](https://github.com/HISTORICAL_REPO/blob/492bf7da82ac346c1a17ab0acc2405adf17ae5c1/projects/pd/protocol/MULTI_OBJECT_CONNECTOR_PROTOCOL.md)\n- [Selected basis-relative semantic state](https://github.com/HISTORICAL_REPO/blob/492bf7da82ac346c1a17ab0acc2405adf17ae5c1/projects/improvement-core/tool-ecosystem/MULTIOBJECT_CURRENT_SEMANTIC_STATE_2026-09-26.md)\n- [Factorization candidate](https://github.com/HISTORICAL_REPO/blob/492bf7da82ac346c1a17ab0acc2405adf17ae5c1/projects/improvement-core/tool-ecosystem/MULTIOBJECT_CURRENT_BASIS_FACTORIZATION_002_2026-09-26.md)\n- [ProofCore semantic preservation receipt](https://github.com/HISTORICAL_REPO/blob/492bf7da82ac346c1a17ab0acc2405adf17ae5c1/projects/improvement-core/validation/MULTIOBJECT_TWO_ROLE_PROOFCORE_RECEIPT_001_2026-09-26.md)\n".replace("HISTORICAL_REPO", "thytabakman-jpg" + "/" + "Reaserch")
    if spec.current_tool and spec.object_id=="MultiObject":
        body += "\n## Clickable current Take-5 sources\n\n- [Configured tool registry](../../../../runtime/tool_run_registry.py)\n- [Protected behavior manifest](../../../../runtime/tool_manifest.py)\n- [Portable invocation conductor](../../../../runtime/portable_tool_conductor.py)\n- [Current tool reality](../../../../integration/CURRENT_TOOL_REALITY.md)\n- [Shared tool-system authority](../../AUTHORITY_REGISTRY.md)\n\n## Moving Reaserch source locations (navigation, not authority)\n\nThe pinned historical sources above are the reproducible provenance basis. These moving-branch links locate subsequent document revisions only; their presence does not promote historical mathematical claims or override Take-5's execution owner.\n\n- [PD relation-search protocol](https://github.com/HISTORICAL_REPO/blob/main/projects/pd/protocol/MULTI_OBJECT_CONNECTOR_PROTOCOL.md)\n- [2026-09-24 mathematical reconstruction](https://github.com/HISTORICAL_REPO/blob/main/projects/core-system-mathematics/math/MULTI_OBJECT_V2_CANONICAL_MATHEMATICS_001_2026-09-24.md)\n- [Selected 2026-09-26 semantic snapshot](https://github.com/HISTORICAL_REPO/blob/main/projects/improvement-core/tool-ecosystem/MULTIOBJECT_CURRENT_SEMANTIC_STATE_2026-09-26.md)\n- [Basis-relative factorization candidate](https://github.com/HISTORICAL_REPO/blob/main/projects/improvement-core/tool-ecosystem/MULTIOBJECT_CURRENT_BASIS_FACTORIZATION_002_2026-09-26.md)\n".replace("HISTORICAL_REPO", "thytabakman-jpg" + "/" + "Reaserch")
    return body

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
    body=f"""# {name}: {spec.display_name}

This directory is append-only.
Create a new uniquely named record for each material entry.
Do not replace an older record with a newer one.
"""

    if spec.current_tool and spec.object_id=="MultiObject":
        body += {
            "Evidence": "\n## Use and authority\n\nReader: MultiObject maintainers and reviewers.\nPurpose: Keep immutable, source-attributed observations and triage evidence distinct from both current mathematics and actual execution receipts.\n\n- [Source and historical lineage](../SOURCE_MAP.md)\n- [Authority and admission](../AUTHORITY_REGISTRY.md)\n- [Change control](../CHANGE_CONTROL.md)\n\nA record here does not by itself establish a current protected behavior, runtime execution, or closed finding.\n",
            "Run evidence": "\n## Use and authority\n\nReader: MultiObject operators and validators.\nPurpose: Retain run-specific inputs, invoked route, evidence, results, and limits only when an actual run or validation was performed.\n\n- [Executable route and provider boundary](../RUNTIME.md)\n- [Protected behavior routes](../PROTECTED_BEHAVIORS.md)\n- [Change control](../CHANGE_CONTROL.md)\n\nA plan, pending workflow, or generated file is not an executed-run receipt.\n",
            "History": "\n## Use and authority\n\nReader: MultiObject maintainers and historians.\nPurpose: Preserve superseded package states and their provenance without making older versions current authorities.\n\n- [Current state projection](../CURRENT_STATE.md)\n- [Decision log](../DECISION_LOG.md)\n- [Lessons ledger](../LESSONS_LEDGER.md)\n- [Change control](../CHANGE_CONTROL.md)\n\nUse Git history for revisions of a living file; create a separate immutable record here only for independently necessary historical evidence.\n"
        }.get(name, "")
    return body


def render_coverage_readme(spec:ProjectObjectSpec)->str:
    body=f"""# 36-cell coverage: {spec.display_name}

Surface: Scope x ModeFace.
Role: audit / discovery / regression evidence only.
Cells: 36.

Each cell owns findings for one coordinate. A finding becomes canonical only
through the authority and change-control path.
"""

    if spec.current_tool and spec.object_id=="MultiObject":
        body += "\n## Use and ownership\n\nReader: MultiObject maintainers and audit reviewers.\nPurpose: Find the evidence-only Scope x ModeFace cells and preserve unresolved questions; no cell is a second mathematical authority.\n\n- [MultiObject authority registry](../AUTHORITY_REGISTRY.md)\n- [Change control](../CHANGE_CONTROL.md)\n- [Source map and provenance](../SOURCE_MAP.md)\n- [Separate directed handoff surface](../HANDOFF_SURFACE.md)\n\nA cell marked OPEN has no admitted cell-specific finding yet. It does **not** negate findings recorded in research, prove that no relation exists, or mark the native MultiObject runtime OPEN.\n\n## Coverage navigation\n\n### SYSTEM\n\n- [01 EXPAND](./01_SYSTEM__EXPAND.md)\n- [02 CONTRACT](./02_SYSTEM__CONTRACT.md)\n- [03 INWARD](./03_SYSTEM__INWARD.md)\n- [04 OUTWARD](./04_SYSTEM__OUTWARD.md)\n- [05 ISOLATE](./05_SYSTEM__ISOLATE.md)\n- [06 COUPLE](./06_SYSTEM__COUPLE.md)\n\n### SUBSYSTEM\n\n- [07 EXPAND](./07_SUBSYSTEM__EXPAND.md)\n- [08 CONTRACT](./08_SUBSYSTEM__CONTRACT.md)\n- [09 INWARD](./09_SUBSYSTEM__INWARD.md)\n- [10 OUTWARD](./10_SUBSYSTEM__OUTWARD.md)\n- [11 ISOLATE](./11_SUBSYSTEM__ISOLATE.md)\n- [12 COUPLE](./12_SUBSYSTEM__COUPLE.md)\n\n### COMPONENT\n\n- [13 EXPAND](./13_COMPONENT__EXPAND.md)\n- [14 CONTRACT](./14_COMPONENT__CONTRACT.md)\n- [15 INWARD](./15_COMPONENT__INWARD.md)\n- [16 OUTWARD](./16_COMPONENT__OUTWARD.md)\n- [17 ISOLATE](./17_COMPONENT__ISOLATE.md)\n- [18 COUPLE](./18_COMPONENT__COUPLE.md)\n\n### INTERFACE\n\n- [19 EXPAND](./19_INTERFACE__EXPAND.md)\n- [20 CONTRACT](./20_INTERFACE__CONTRACT.md)\n- [21 INWARD](./21_INTERFACE__INWARD.md)\n- [22 OUTWARD](./22_INTERFACE__OUTWARD.md)\n- [23 ISOLATE](./23_INTERFACE__ISOLATE.md)\n- [24 COUPLE](./24_INTERFACE__COUPLE.md)\n\n### BOUNDARY DECOMPOSITION\n\n- [25 EXPAND](./25_BOUNDARY_DECOMPOSITION__EXPAND.md)\n- [26 CONTRACT](./26_BOUNDARY_DECOMPOSITION__CONTRACT.md)\n- [27 INWARD](./27_BOUNDARY_DECOMPOSITION__INWARD.md)\n- [28 OUTWARD](./28_BOUNDARY_DECOMPOSITION__OUTWARD.md)\n- [29 ISOLATE](./29_BOUNDARY_DECOMPOSITION__ISOLATE.md)\n- [30 COUPLE](./30_BOUNDARY_DECOMPOSITION__COUPLE.md)\n\n### CROSS LAYER\n\n- [31 EXPAND](./31_CROSS_LAYER__EXPAND.md)\n- [32 CONTRACT](./32_CROSS_LAYER__CONTRACT.md)\n- [33 INWARD](./33_CROSS_LAYER__INWARD.md)\n- [34 OUTWARD](./34_CROSS_LAYER__OUTWARD.md)\n- [35 ISOLATE](./35_CROSS_LAYER__ISOLATE.md)\n- [36 COUPLE](./36_CROSS_LAYER__COUPLE.md)\n"
    return body


def render_coverage_cell(spec:ProjectObjectSpec,index:int,scope:Scope,face:ModeFace)->str:
    body=f"""# {spec.display_name}: {scope.value} x {face.value}

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

    if spec.current_tool and spec.object_id=="MultiObject":
        body=body.replace("Disposition: OPEN\n\n## Findings", "Disposition: OPEN\nPurpose: Preserve only findings at this exact Scope x ModeFace coordinate; do not infer semantic closure from this page.\nReader: MultiObject maintainers and audit reviewers.\nIndex: [all 36 coverage cells](README.md)\n\n## Findings")
        body=body.replace("Canonical semantic changes route through AUTHORITY_REGISTRY.md and CHANGE_CONTROL.md.", "Canonical semantic changes route through the [authority registry](../AUTHORITY_REGISTRY.md) and [change control](../CHANGE_CONTROL.md).")
    return body


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
        path=base/PACKAGE_ROOT/rel
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
