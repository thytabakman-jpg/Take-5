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
# CANDIDATE ONLY: evidence-sparse pilots on unmerged branch; no goal policy change.
SPARSE_COVERAGE_PILOT=frozenset({"MultiObject","DelegatedExecutor","GOAL","ICC128"})
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


PILOT_TOOL_HOME_CONTRACTS = {
    "MultiObject": "\n## Operational home contract — pilot\n\n**Job and role:** Navigate the configured MultiObject relation-discovery tool over provider-supplied relations, preserving joint/pair route identity and typed unresolved cases. This is an organizational home, not new mathematical or execution authority.\n\n**Owner and functional boundary:** Package identity, navigation, change control and scoped evidence live here. [Native executor](../../../../runtime/multiobject.py), [configured conductor](../../../../runtime/portable_tool_conductor.py), [protected manifest](../../../../runtime/tool_manifest.py), [mathematical identity](../../../../architecture/MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md) and [native regression tests](../../../../tests/test_multiobject.py) retain their own authority. [RUNTIME.md](RUNTIME.md), [DEPENDENCIES.md](DEPENDENCIES.md), [SOURCE_MAP.md](SOURCE_MAP.md) and [REGRESSION_CONTRACT.md](REGRESSION_CONTRACT.md) route the maintained closure. A missing domain provider is OPEN, not successful execution.\n\n**Admission and restructuring gate:** Check independently justified goal/job, source type, actual authority, reader and native consumers before KEEP, MOVE, SPLIT, CONSOLIDATE, RETAIN-WITH-LINKS or NO MOVE. Admit only tool-specific organizational contracts and correctly owned evidence; keep shared runtimes/tests, independent research, original proofs and histories at their legitimate owners. Transfer/split/merge requires owning file-type Level 2 placement and preservation checks, with affected functional Level 3/4 verification where required. Retain source material if authorization, preservation or native execution evidence is unresolved; a clean README is not a certificate.\n",
    "GOAL": "\n## Operational home contract — pilot\n\n**Job and role:** Navigate configured GOAL recovery over supplied candidate evidence and a valid robust-MT receipt. This is an organizational home, not a second project-goal or mathematics authority.\n\n**Owner and functional boundary:** Package identity, navigation, change control and scoped evidence live here. [Native GOAL](../../../../runtime/goal.py), [MT receipt gate](../../../../runtime/mt_semantic_return_gate.py), [conductor](../../../../runtime/portable_tool_conductor.py), [protected manifest](../../../../runtime/tool_manifest.py), [mathematical identity](../../../../architecture/GOAL_FULL_TOOL_MATH_002_2026-09-30.md) and [native regression tests](../../../../tests/test_goal.py) retain their own authority. [RUNTIME.md](RUNTIME.md), [DEPENDENCIES.md](DEPENDENCIES.md), [SOURCE_MAP.md](SOURCE_MAP.md) and [REGRESSION_CONTRACT.md](REGRESSION_CONTRACT.md) route the maintained closure. A native call without a valid MT preflight is not configured execution.\n\n**Admission and restructuring gate:** Check independently justified goal/job, source type, actual authority, reader and native consumers before KEEP, MOVE, SPLIT, CONSOLIDATE, RETAIN-WITH-LINKS or NO MOVE. Admit only tool-specific organizational contracts and correctly owned evidence; keep shared runtimes/tests, independent research, original proofs and histories at their legitimate owners. Transfer/split/merge requires owning file-type Level 2 placement and preservation checks, with affected functional Level 3/4 verification where required. Retain source material if authorization, preservation or native execution evidence is unresolved; a clean README is not a certificate.\n",
    "RTC": "\n## Operational home contract — pilot\n\n**Job and role:** Navigate the configured RTC (Raise-the-Ceiling) specialization of C48 over supplied candidates, distinguishing strict-gain results from typed no-gain. This is an organizational home, not a preservation proof or executed C48 run.\n\n**Owner and functional boundary:** Package identity, navigation, change control and scoped evidence live here. The [conductor](../../../../runtime/portable_tool_conductor.py) selects [raise_the_ceiling](../../../../runtime/raise_the_ceiling.py), which uses [capability dispatch](../../../../runtime/capability_runtime.py) and the [C48 evaluator](../../../../runtime/a5_programs.py). [Protected manifest](../../../../runtime/tool_manifest.py), [native recovery specification](../../../../architecture/NATIVE_TOOL_RECOVERY_PACK_160_2026-09-27.md) and [specialization test](../../../../tests/test_recovered_native_tools_20260927.py) retain their own authority. [RUNTIME.md](RUNTIME.md), [DEPENDENCIES.md](DEPENDENCIES.md), [SOURCE_MAP.md](SOURCE_MAP.md) and [REGRESSION_CONTRACT.md](REGRESSION_CONTRACT.md) route the maintained closure. Truthy `strict_gain`/`preserves` flags alone do not prove coverage of a declared protected set; that stronger claim remains OPEN.\n\n**Admission and restructuring gate:** Check independently justified goal/job, source type, actual authority, reader and native consumers before KEEP, MOVE, SPLIT, CONSOLIDATE, RETAIN-WITH-LINKS or NO MOVE. Admit only tool-specific organizational contracts and correctly owned evidence; keep shared runtimes/tests, independent research, original proofs and histories at their legitimate owners. Transfer/split/merge requires owning file-type Level 2 placement and preservation checks, with affected functional Level 3/4 verification where required. Retain source material if authorization, preservation or native execution evidence is unresolved; a clean README is not a certificate.\n",
}
RTC_RUNTIME_ROUTE = "\n## RTC configured-to-native chain and verified scope\n\n- [Portable conductor](../../../../runtime/portable_tool_conductor.py) selects `raise_the_ceiling.raise_the_ceiling` for RTC.\n- [RTC entrypoint](../../../../runtime/raise_the_ceiling.py) calls `execute_capability(\"C48\", payload)`.\n- [Capability dispatcher](../../../../runtime/capability_runtime.py) sends C48 to `run_generic`.\n- [C48 evaluator](../../../../runtime/a5_programs.py) filters truthy `strict_gain` and `preserves` fields; otherwise returns `NOOP` with `NO_STRICT_GAIN_FOUND`.\n- [Native RTC specialization test](../../../../tests/test_recovered_native_tools_20260927.py) checks an accepted and a non-gaining candidate.\n\n**OPEN:** This implementation does not verify coverage of every declared protected property. A source link or static package check is not an executed tool or proof of that stronger property.\n"
RTC_DEPENDENCY_CONE = "\n## RTC native functional dependency cone\n\n- [RTC configured entrypoint](../../../../runtime/raise_the_ceiling.py)\n- [Capability dispatch](../../../../runtime/capability_runtime.py)\n- [C48 evaluation](../../../../runtime/a5_programs.py)\n- [Native specialization regression](../../../../tests/test_recovered_native_tools_20260927.py)\n- [Configured conductor regressions](../../../../tests/test_portable_tool_conductor.py)\n- [Capability registry regressions](../../../../tests/test_a5_registry.py)\n- [Manifest-selected native recovery specification](../../../../architecture/NATIVE_TOOL_RECOVERY_PACK_160_2026-09-27.md)\n\nA change to dispatch, C48 selection, manifest, registry or configured entrypoint reopens the affected consumers. The tests above do not alone establish complete protected-set coverage.\n"
RTC_REGRESSION_GATES = "\n## RTC native and relocation regression boundary\n\n- [RTC specialization test](../../../../tests/test_recovered_native_tools_20260927.py) covers the accepted strict-gain and excluded no-gain case.\n- [Capability registry tests](../../../../tests/test_a5_registry.py) cover registry integrity, not every C48 protected-property case.\n- [Configured conductor tests](../../../../tests/test_portable_tool_conductor.py) cover configured routing to the extent asserted.\n- [Package generator tests](../../../../tests/test_tool_project_packages.py) protect materialized navigation parity and collision behavior.\n- Native source chain: `runtime/raise_the_ceiling.py` -> `runtime/capability_runtime.py` -> `runtime/a5_programs.py` (C48). Retest its affected consumers after any move or split.\n- Stronger preservation-set proof and unavailable native execution remain OPEN; a package structural check never closes them.\n"


def render_readme(spec:ProjectObjectSpec)->str:
    body=f"""# {spec.display_name} project package

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
    if spec.current_tool and spec.object_id in {"MultiObject", "GOAL"}:
        for index, name in enumerate((
            "CURRENT_STATE.md", "AUTHORITY_REGISTRY.md", "IDENTITY.md",
            "MATHEMATICS.md", "RUNTIME.md", "PROTECTED_BEHAVIORS.md",
            "DEPENDENCIES.md", "OPEN_QUESTIONS.md", "SOURCE_MAP.md",
        ), start=1):
            body=body.replace(f"{index}. {name}", f"{index}. [{name}]({name})")
        body=body.replace(
            "10. coverage/ only for coverage evidence",
            "10. [coverage/](coverage/README.md) only for coverage evidence",
        )
    if spec.current_tool and spec.object_id in PILOT_TOOL_HOME_CONTRACTS:
        body += PILOT_TOOL_HOME_CONTRACTS[spec.object_id]
    return body


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

## {('Reserved logical coverage coordinates (36; physical evidence pages optional)' if spec.object_id in SPARSE_COVERAGE_PILOT else 'Coverage pages')}

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

MULTIOBJECT_CURRENT_STATE_BOUNDARY = "\n## MultiObject registered-versus-executed distinction\n\n`CURRENT` means the configured tool package is registered. It does not witness a completed MultiObject relation-discovery run, a supplied domain provider, or a finding whose material-delta semantics were independently validated. The live [executor](../../../../runtime/multiobject.py), [configured conductor](../../../../runtime/portable_tool_conductor.py), [source map](SOURCE_MAP.md) and [native regression owner](REGRESSION_CONTRACT.md) remain separate; missing provider or unverified semantic coverage stays OPEN at the affected scope.\n"


def render_current(spec:ProjectObjectSpec)->str:
    body=f"""# Current state: {spec.display_name}

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
    if spec.current_tool and spec.object_id=="MultiObject":
        body += MULTIOBJECT_CURRENT_STATE_BOUNDARY
    return body


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
    if spec.current_tool and spec.object_id=="RTC":
        body += RTC_RUNTIME_ROUTE
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
    body=f"""# Dependencies: {spec.display_name}

## Canonical dependencies

{_bullets(spec.source_refs)}

## Shared runtime/identity dependencies

- runtime/tool_run_registry.py
- runtime/tool_manifest.py
- runtime/portable_tool_conductor.py

## Rule

A dependency change reopens the affected cone. Unaffected package state remains protected.
"""
    if spec.current_tool and spec.object_id=="MultiObject":
        link_labels={
            "runtime/tool_run_registry.py": "[Configured-run registry](../../../../runtime/tool_run_registry.py)",
            "runtime/tool_manifest.py": "[Protected tool manifest](../../../../runtime/tool_manifest.py)",
            "runtime/portable_tool_conductor.py": "[Portable invocation conductor](../../../../runtime/portable_tool_conductor.py)",
            "integration/CURRENT_TOOL_REALITY.md": "[Current tool reality](../../../../integration/CURRENT_TOOL_REALITY.md)",
        }
        body=body.replace(
            _bullets(spec.source_refs),
            "\n".join("- "+link_labels.get(ref,ref) for ref in spec.source_refs),
        )
        body=body.replace(
            "## Shared runtime/identity dependencies\n\n"
            "- runtime/tool_run_registry.py\n"
            "- runtime/tool_manifest.py\n"
            "- runtime/portable_tool_conductor.py\n",
            "## Shared runtime/identity dependencies\n\n"
            "The registry, manifest, and conductor above are shared runtime/identity\n"
            "authorities. The current-tool-reality source supplies the separate\n"
            "currentness and execution-evidence boundary.\n",
        )
        body += "\n## MultiObject native dependency edges\n\n- [Native relation-discovery executor](../../../../runtime/multiobject.py)\n- [Full-tool mathematical identity](../../../../architecture/MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md)\n"
    if spec.current_tool and spec.object_id=="RTC":
        body += RTC_DEPENDENCY_CONE
    return body

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
        body += "\n## MultiObject-specific current implementation and identity\n\n- [Native orchestration](../../../../runtime/multiobject.py)\n- [Full mathematical identity](../../../../architecture/MULTIOBJECT_FULL_TOOL_MATH_001_2026-09-27.md)\n- [Native regression tests](../../../../tests/test_multiobject.py)\n- [Mathematical identity regression tests](../../../../tests/test_multiobject_fullmath_identity.py)\n\n## Repair and regression evidence\n\n- [Ten-source Level 1 triage receipt](evidence/level1-ten-loadbearing-source-triage.md) — accepted source baselines; not Level 2 certification.\n- [Ten-source Level 2 triage ledger](evidence/level2-ten-loadbearing-source-triage.md) — functional findings, repairs, and remaining verification gates.\n- [Portable conductor regression tests](../../../../tests/test_portable_tool_conductor.py) — configured adapter and typed MultiObject result checks.\n\n## Pinned historical mathematical and protocol lineage\n\nThe full mathematical identity pins the historical evidence basis to `HISTORICAL_REPO@492bf7da82ac346c1a17ab0acc2405adf17ae5c1`. These links preserve the input lineage; they do not confer current Take-5 execution authority.\n\n- [Multi-Object v0.2 canonical mathematics](https://github.com/HISTORICAL_REPO/blob/492bf7da82ac346c1a17ab0acc2405adf17ae5c1/projects/core-system-mathematics/math/MULTI_OBJECT_V2_CANONICAL_MATHEMATICS_001_2026-09-24.md)\n- [Multi-Object Connector protocol](https://github.com/HISTORICAL_REPO/blob/492bf7da82ac346c1a17ab0acc2405adf17ae5c1/projects/pd/protocol/MULTI_OBJECT_CONNECTOR_PROTOCOL.md)\n- [Selected basis-relative semantic state](https://github.com/HISTORICAL_REPO/blob/492bf7da82ac346c1a17ab0acc2405adf17ae5c1/projects/improvement-core/tool-ecosystem/MULTIOBJECT_CURRENT_SEMANTIC_STATE_2026-09-26.md)\n- [Factorization candidate](https://github.com/HISTORICAL_REPO/blob/492bf7da82ac346c1a17ab0acc2405adf17ae5c1/projects/improvement-core/tool-ecosystem/MULTIOBJECT_CURRENT_BASIS_FACTORIZATION_002_2026-09-26.md)\n- [ProofCore semantic preservation receipt](https://github.com/HISTORICAL_REPO/blob/492bf7da82ac346c1a17ab0acc2405adf17ae5c1/projects/improvement-core/validation/MULTIOBJECT_TWO_ROLE_PROOFCORE_RECEIPT_001_2026-09-26.md)\n".replace("HISTORICAL_REPO", "thytabakman-jpg" + "/" + "Reaserch")
    if spec.current_tool and spec.object_id=="MultiObject":
        body += "\n## Clickable current Take-5 sources\n\n- [Configured tool registry](../../../../runtime/tool_run_registry.py)\n- [Protected behavior manifest](../../../../runtime/tool_manifest.py)\n- [Portable invocation conductor](../../../../runtime/portable_tool_conductor.py)\n- [Current tool reality](../../../../integration/CURRENT_TOOL_REALITY.md)\n- [Shared tool-system authority](../../AUTHORITY_REGISTRY.md)\n\n## Moving Reaserch source locations (navigation, not authority)\n\nThe pinned historical sources above are the reproducible provenance basis. These moving-branch links locate subsequent document revisions only; their presence does not promote historical mathematical claims or override Take-5's execution owner.\n\n- [PD relation-search protocol](https://github.com/HISTORICAL_REPO/blob/main/projects/pd/protocol/MULTI_OBJECT_CONNECTOR_PROTOCOL.md)\n- [2026-09-24 mathematical reconstruction](https://github.com/HISTORICAL_REPO/blob/main/projects/core-system-mathematics/math/MULTI_OBJECT_V2_CANONICAL_MATHEMATICS_001_2026-09-24.md)\n- [Selected 2026-09-26 semantic snapshot](https://github.com/HISTORICAL_REPO/blob/main/projects/improvement-core/tool-ecosystem/MULTIOBJECT_CURRENT_SEMANTIC_STATE_2026-09-26.md)\n- [Basis-relative factorization candidate](https://github.com/HISTORICAL_REPO/blob/main/projects/improvement-core/tool-ecosystem/MULTIOBJECT_CURRENT_BASIS_FACTORIZATION_002_2026-09-26.md)\n".replace("HISTORICAL_REPO", "thytabakman-jpg" + "/" + "Reaserch")
    if spec.current_tool and spec.object_id=="MultiObject":
        # Derived cross-repository navigation is reproducible without changing
        # the package's mathematical or execution authority.
        body += "\n## Cross-repository reconciliation (derived navigation; no promotion)\n\n- [Take-5/Reaserch crosswalk](../../SOURCE_MAP.md#cross-repository-tool-package-navigation-derived-no-authority-transfer) — all current packages, catalogued formal objects and unresolved differences.\n- [Reaserch `MULTI-OBJECT` (K2) catalog entry](https://github.com/HISTORICAL_REPO/blob/main/projects/improvement-core/tool-ecosystem/FORMAL_TOOL_CATALOG_CURRENT.yaml) and [its current semantic locator](https://github.com/HISTORICAL_REPO/blob/main/projects/improvement-core/tool-ecosystem/MULTIOBJECT_CURRENT_SEMANTIC_STATE_2026-09-26.md). Matching names permit navigation, not automatic semantic equivalence or runnable integration.\n- Take-5 configured-run authority remains [registry](../../../../runtime/tool_run_registry.py), [manifest](../../../../runtime/tool_manifest.py), [conductor](../../../../runtime/portable_tool_conductor.py). See [mathematics](MATHEMATICS.md), [runtime](RUNTIME.md), [dependencies](DEPENDENCIES.md), [regression contract](REGRESSION_CONTRACT.md).\n- Native evidence surfaces are [runs](runs/README.md), [evidence](evidence/README.md), [coverage](coverage/README.md) and [history](history/README.md); a file link is not proof that configured execution or certification passed.\n\n**Owner boundary:** Do not copy mathematical truth between repositories or infer current runtime promotion from this source map. Mark unresolved mismatches OPEN and check the specialist owner.\n".replace("HISTORICAL_REPO", "thytabakman-jpg" + "/" + "Reaserch")
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
    if spec.object_id in SPARSE_COVERAGE_PILOT:
        return _render_sparse_regression(spec)
    body = f"""# Regression contract: {spec.display_name}

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
    if spec.current_tool and spec.object_id=="RTC":
        body += RTC_REGRESSION_GATES
    return body


def _render_sparse_regression(spec:ProjectObjectSpec)->str:
    baseline = f"""# Regression contract: {spec.display_name}

A valid package keeps all of these true:

- required core files exist
- exactly 36 logical Scope x ModeFace coordinates exist
- physical coverage pages are evidence only, not semantic authority
- the distinct SourceScope x TargetScope surface is not merged into coverage
- decisions, lessons, runs, and evidence are append-only
- package generation never overwrites changed existing files
- current configured tools have one package each
- aliases do not create duplicate mutable authority
- missing semantics/runtime/evidence remain typed OPEN
"""
    return baseline


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
    if spec.current_tool and spec.object_id=="DelegatedExecutor":
        body += "\n## Coverage navigation\n\n"
        previous_scope=None
        for index,scope,face in coverage_cells():
            if scope!=previous_scope:
                if previous_scope is not None:
                    body += "\n"
                body += f"### {scope.value}\n\n"
                previous_scope=scope
            body += f"- [{index:02d} {face.value}](./{coverage_name(index,scope,face)})\n"
        body += "\nEach linked page is evidence for one Scope x ModeFace coordinate, not an executable delegation job or a recurring schedule. `OPEN` on a coverage page does not by itself determine the native DelegatedExecutor runtime state.\n"
    if spec.object_id in SPARSE_COVERAGE_PILOT:
        # Preserve 36 semantic positions without publishing broken links.
        import re
        body = re.sub(
            r"- \[(\d{2}) ([A-Z]+)\]\(\./\d{2}_[A-Z_]+__[A-Z]+\.md\)",
            r"- \1 \2 (reserved logical coordinate; no admitted evidence)",
            body,
        )
        body = body.replace(
            "Each linked page is evidence for one Scope x ModeFace coordinate",
            "Each reserved logical coordinate can independently own evidence for Scope x ModeFace",
        )
    if spec.current_tool and spec.object_id=="RTC":
        body += "\n## Navigation and ownership\n\nReader: RTC maintainers and audit reviewers.\nPurpose: Locate the 36 evidence-only Scope x ModeFace pages without treating them as mathematical or execution authority.\n\n- [RTC authority registry](../AUTHORITY_REGISTRY.md)\n- [Change control](../CHANGE_CONTROL.md)\n- [Source map and current runtime owner](../SOURCE_MAP.md)\n- [Separate directed handoff surface](../HANDOFF_SURFACE.md)\n\n"
        previous_scope = None
        for index, scope, face in coverage_cells():
            if scope != previous_scope:
                body += f"### {scope.value}\n\n"
                previous_scope = scope
            body += f"- [{index:02d} {face.value}](./{coverage_name(index, scope, face)})\n"
            if face.value == "COUPLE":
                body += "\n"
        body += "A cell marked `OPEN` has no admitted cell-specific finding yet. It does not establish that RTC is unimplemented or that no scientific relation exists. The directed SourceScope x TargetScope surface is separate from these pages.\n"
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
    if spec.object_id not in SPARSE_COVERAGE_PILOT:
        for i,scope,face in coverage_cells():
            files[f"{root}/coverage/{coverage_name(i,scope,face)}"]=render_coverage_cell(spec,i,scope,face)
    # Admitted evidence remains an optional, append-only coordinate-owned file.
    return files


def _admit_curated_source_map(spec:ProjectObjectSpec, existing:str)->None:
    """Admit an authored, source-specific navigation page without replacing it.

    The general package generator owns the *minimum template*, not bespoke
    evidence/provenance routes added by a package maintainer. This is scoped
    to active configured tools; historical variant source maps remain strict.
    """
    prefix=f"# Source map: {spec.display_name}\n"
    if not existing.startswith(prefix):
        raise ToolProjectPackageCollision(f"{spec.object_id}: SOURCE_MAP_IDENTITY_MISMATCH")
    required=(
        "runtime/tool_run_registry.py",
        "runtime/tool_manifest.py",
        "runtime/portable_tool_conductor.py",
        "SOURCE_MAP.md#cross-repository-tool-package-navigation-derived-no-authority-transfer",
    )
    if any(token not in existing for token in required):
        raise ToolProjectPackageCollision(f"{spec.object_id}: SOURCE_MAP_CRITICAL_ROUTE_MISSING")
    if spec.object_id.startswith("C") and spec.object_id[1:].isdigit() and 1<=int(spec.object_id[1:])<=49:
        category="CAPABILITY_FAMILY_ONLY"
    elif spec.object_id in {"RootCause","Diagnosis"}:
        category="ALIAS_COLLISION_OPEN"
    elif spec.object_id in {
        "ImprovementCore","ICC128","MT","MTA","Architecture","PD","PDAudit",
        "HF001","HF002","TRC","RTC","MultiObject","ASSERT","GOAL","ToolConductor",
    }:
        category="NAMED_CROSS_REFERENCE"
    else:
        category="UNMAPPED"
    # Named package pages express the match through a typed object link
    # rather than repeating the machine-facing category label.
    if category=="NAMED_CROSS_REFERENCE":
        if "Reaserch" not in existing or "catalog" not in existing.lower():
            raise ToolProjectPackageCollision(f"{spec.object_id}: SOURCE_MAP_FORMAL_LINK_MISSING")
    elif category=="CAPABILITY_FAMILY_ONLY":
        if "CAPABILITY_FAMILY_ONLY" not in existing and "related numbered capability family" not in existing:
            raise ToolProjectPackageCollision(f"{spec.object_id}: SOURCE_MAP_CATEGORY_MISMATCH")
    elif category not in existing:
        raise ToolProjectPackageCollision(f"{spec.object_id}: SOURCE_MAP_CATEGORY_MISMATCH")


def _verify_curated_pilot_page(spec:ProjectObjectSpec,rel:str,existing:str,generated:str)->None:
    # Pilot updates must not silently overwrite authored native control clauses.
    if rel.endswith("/MANIFEST.md"):
        if not existing.startswith(f"# Package manifest: {spec.display_name}\\n".replace("\\n","\n")):
            raise ToolProjectPackageCollision(f"{spec.object_id}:MANIFEST_IDENTITY_MISMATCH")
        if "Coverage cells: 36" not in existing or "Reserved logical coverage coordinates" not in existing:
            raise ToolProjectPackageCollision(f"{spec.object_id}:MANIFEST_LOGICAL_36_MISSING")
        for index,scope,face in coverage_cells():
            filename=coverage_name(index,scope,face)
            if f"- coverage/{filename}" not in existing:
                raise ToolProjectPackageCollision(f"{spec.object_id}:MANIFEST_SLOT_MISSING")
    elif rel.endswith("/REGRESSION_CONTRACT.md"):
        if not existing.startswith(generated):
            raise ToolProjectPackageCollision(f"{spec.object_id}:REGRESSION_PREFIX_MISSING")
    else:
        raise ToolProjectPackageCollision(f"{spec.object_id}:UNEXPECTED_CURATED_PAGE")


def materialize_package(base:Path,spec:ProjectObjectSpec)->tuple[Path,...]:
    written=[]
    for rel,content in package_files(spec).items():
        path=base/PACKAGE_ROOT/rel
        path.parent.mkdir(parents=True,exist_ok=True)
        if path.exists():
            existing=path.read_text(encoding="utf-8")
            if spec.current_tool and rel.endswith("/SOURCE_MAP.md") and spec.object_id!="MultiObject":
                if existing!=content:
                    _admit_curated_source_map(spec,existing)
                continue
            if spec.object_id in SPARSE_COVERAGE_PILOT and (rel.endswith("/MANIFEST.md") or rel.endswith("/REGRESSION_CONTRACT.md")):
                _verify_curated_pilot_page(spec,rel,existing,content)
                continue
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
        if spec.object_id in SPARSE_COVERAGE_PILOT:
            if not actual.issubset(expected):
                bad_coverage.append(spec.object_id)
            else:
                for index,scope,face in coverage_cells():
                    fname=coverage_name(index,scope,face)
                    if fname not in actual:
                        continue
                    body=(cdir/fname).read_text(encoding="utf-8")
                    # Fail closed on unknown content, blank placeholders, or
                    # evidence attached to the wrong coordinate or owner.
                    if (body==render_coverage_cell(spec,index,scope,face)
                        or f"Object ID: {spec.object_id}" not in body
                        or f"Coverage cell: {index:02d}/36" not in body
                        or f"Scope: {scope.value}" not in body
                        or f"Mode face: {face.value}" not in body
                        or "- none admitted yet" in body):
                        bad_coverage.append(spec.object_id)
                        break
        elif actual!=expected:
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
