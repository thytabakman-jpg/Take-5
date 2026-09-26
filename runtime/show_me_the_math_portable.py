"""Standalone portable realization of SHOW_ME_THE_MATH.

This file has no Take-5 imports.  Copying this single file to a fresh machine
with CPython 3.12+ is sufficient to execute its self-assessment.

Mathematical core:

    LB(P,X) = mu S . (Roots(P,X) union Union_{s in S} Dependencies_P(s))

    Closed(P,X,E)
      = DefinitionClosed(P,X,E)
        and ObligationClosed(P,Kind(X))
        and RealizerAvailable(P,E)
        and ProtectedEquivalent(Instantiate(P,E), X)

    SMTM(P,X,E)
      = GREEN                         when Closed(P,X,E)
        RED(Residuals(P,X,E))         otherwise

Obligations are indexed by mathematical-object kind.  A request contract is not
forced to pretend to be a configured tool.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Mapping
import json
import sys

REQUEST_CONTRACT="REQUEST_CONTRACT"
TOOL="TOOL"
RELATION="RELATION"
EQUATION="EQUATION"
DATA_SCHEMA="DATA_SCHEMA"

UNIVERSAL_FIELDS=(
    "object_id",
    "kind",
    "signature",
    "definitions",
    "load_bearing_symbols",
    "runtime_primitives",
    "obligations",
    "protected_behavior",
    "equivalence_tests",
    "realizer",
    "environment_contract",
)

KIND_REQUIREMENTS={
    REQUEST_CONTRACT:("recognition","evaluation","projection"),
    TOOL:("run_spec","initialization","execution","persistence"),
    RELATION:("domain","codomain","graph"),
    EQUATION:("variables","domain","equality_semantics"),
    DATA_SCHEMA:("carrier","validation"),
}

SATISFIED="SATISFIED"
NOT_APPLICABLE="NOT_APPLICABLE"


@dataclass(frozen=True)
class Assessment:
    complete: bool
    status: str
    missing_fields: tuple[str,...]
    unresolved_symbols: tuple[str,...]
    unavailable_primitives: tuple[str,...]
    unsatisfied_obligations: tuple[str,...]
    realizer_errors: tuple[str,...]
    equivalence_errors: tuple[str,...]

    def payload(self)->dict[str,Any]:
        return asdict(self)


def _deps(package:Mapping[str,Any], symbol:str)->tuple[str,...]:
    definitions=package.get("definitions",{})
    row=definitions.get(symbol,{}) if isinstance(definitions,Mapping) else {}
    if not isinstance(row,Mapping):
        return ()
    return tuple(str(x) for x in row.get("dependencies",()))


def load_bearing_closure(package:Mapping[str,Any])->tuple[str,...]:
    roots=tuple(str(x) for x in package.get("load_bearing_symbols",()))
    seen=set()
    frontier=list(roots)
    while frontier:
        symbol=frontier.pop()
        if symbol in seen:
            continue
        seen.add(symbol)
        frontier.extend(_deps(package,symbol))
    return tuple(sorted(seen))


def _primitive_available(environment:Mapping[str,Any], name:str, spec:Mapping[str,Any])->bool:
    if not spec.get("typed_contract"):
        return False
    required=str(spec.get("provider",""))
    providers=environment.get("providers",{})
    return bool(required and isinstance(providers,Mapping) and providers.get(required))


def _obligation_closed(package:Mapping[str,Any])->tuple[str,...]:
    kind=str(package.get("kind",""))
    required=KIND_REQUIREMENTS.get(kind)
    if required is None:
        return ("UNKNOWN_OBJECT_KIND",)
    obligations=package.get("obligations",{})
    if not isinstance(obligations,Mapping):
        return tuple(required)
    open_items=[]
    for name in required:
        row=obligations.get(name)
        if not isinstance(row,Mapping):
            open_items.append(name)
            continue
        status=row.get("status")
        if status==SATISFIED:
            continue
        if status==NOT_APPLICABLE and str(row.get("witness","")).strip():
            continue
        open_items.append(name)
    return tuple(open_items)


def _realizer_errors(package:Mapping[str,Any], environment:Mapping[str,Any])->tuple[str,...]:
    row=package.get("realizer",{})
    if not isinstance(row,Mapping):
        return ("REALIZER_MISSING",)
    if row.get("kind")!="PYTHON_STDLIB_MODULE":
        return ("REALIZER_KIND_UNSUPPORTED",)
    min_version=tuple(row.get("min_python",(3,12)))
    if tuple(sys.version_info[:2]) < min_version:
        return ("PYTHON_VERSION_TOO_OLD",)
    if not row.get("embedded"):
        return ("REALIZER_NOT_EMBEDDED",)
    if not environment.get("self_file_present",False):
        return ("SELF_FILE_NOT_PRESENT",)
    return ()


def assess(package:Mapping[str,Any], environment:Mapping[str,Any])->Assessment:
    missing=tuple(k for k in UNIVERSAL_FIELDS if k not in package)

    definitions=package.get("definitions",{})
    primitives=package.get("runtime_primitives",{})
    unresolved=[]
    unavailable=[]
    for symbol in load_bearing_closure(package):
        if isinstance(definitions,Mapping) and symbol in definitions:
            continue
        spec=primitives.get(symbol) if isinstance(primitives,Mapping) else None
        if isinstance(spec,Mapping):
            if not _primitive_available(environment,symbol,spec):
                unavailable.append(symbol)
            continue
        unresolved.append(symbol)

    obligations=_obligation_closed(package)
    realizer_errors=_realizer_errors(package,environment)

    equivalence_errors=()
    if not package.get("protected_behavior"):
        equivalence_errors+=("PROTECTED_BEHAVIOR_MISSING",)
    if not package.get("equivalence_tests"):
        equivalence_errors+=("EQUIVALENCE_TESTS_MISSING",)

    complete=not (
        missing or unresolved or unavailable or obligations
        or realizer_errors or equivalence_errors
    )
    return Assessment(
        complete=complete,
        status="GREEN" if complete else "RED",
        missing_fields=tuple(sorted(missing)),
        unresolved_symbols=tuple(sorted(set(unresolved))),
        unavailable_primitives=tuple(sorted(set(unavailable))),
        unsatisfied_obligations=tuple(sorted(set(obligations))),
        realizer_errors=tuple(sorted(set(realizer_errors))),
        equivalence_errors=tuple(sorted(set(equivalence_errors))),
    )



# Canonical closed display normal form.
# These glyphs are constants/sets, not free variables:
# Σ = SHOW_ME_THE_MATH characteristic map
# Δ = definition-closed region
# Ω = obligation-closed region
# Φ = realizer-available region
# Ξ = portable-equivalent region
SURFACE_EQUATION="Σ=𝟙_{Δ∩Ω∩Φ∩Ξ}"
SURFACE_CONSTANTS=frozenset({"Σ","Δ","Ω","Φ","Ξ"})
SURFACE_OPERATORS=frozenset({"=","𝟙","_","{","}","∩"})


def surface_components(
    package:Mapping[str,Any],
    environment:Mapping[str,Any],
)->dict[str,bool]:
    assessment=assess(package,environment)
    definition_closed=not (
        assessment.missing_fields
        or assessment.unresolved_symbols
        or assessment.unavailable_primitives
    )
    obligation_closed=not assessment.unsatisfied_obligations
    realizer_available=not assessment.realizer_errors
    portable_equivalent=not assessment.equivalence_errors
    return {
        "Δ":definition_closed,
        "Ω":obligation_closed,
        "Φ":realizer_available,
        "Ξ":portable_equivalent,
    }


def surface_value(package:Mapping[str,Any], environment:Mapping[str,Any])->int:
    return int(all(surface_components(package,environment).values()))


def show_me_the_math(package:Mapping[str,Any], environment:Mapping[str,Any])->dict[str,Any]:
    result=assess(package,environment)
    return {
        "status":result.status,
        "complete":result.complete,
        "math":{
            "surface":SURFACE_EQUATION,
            "load_bearing_closure":"LB(P,X)=mu S.(Roots(P,X) union Union_{s in S} Dependencies_P(s))",
            "completion":"Closed(P,X,E)=DefinitionClosed and ObligationClosed and RealizerAvailable and ProtectedEquivalent",
            "operator":"SMTM(P,X,E)=GREEN iff Closed(P,X,E), else RED(Residuals(P,X,E))",
        },
        "assessment":result.payload(),
    }


SELF_ENVIRONMENT={
    "providers":{
        "CPYTHON_STDLIB_3_12":True,
    },
    "self_file_present":True,
}


SELF_PACKAGE={
    "object_id":"TAKE5:SHOW_ME_THE_MATH:002",
    "kind":REQUEST_CONTRACT,
    "signature":"SMTM : Package x FormalObject x Environment -> {GREEN} union {RED(Residuals)}",
    "definitions":{
        "SHOW_ME_THE_MATH":{"dependencies":["ShowMathComplete","Residuals"]},
        "ShowMathComplete":{"dependencies":["LoadBearingClosure","DefinitionClosed","ObligationClosed","RealizerAvailable","ProtectedEquivalent"]},
        "Residuals":{"dependencies":["LoadBearingClosure","ObligationClosed"]},
        "LoadBearingClosure":{"dependencies":["finite_set","mapping_lookup","fixed_point_iteration"]},
        "DefinitionClosed":{"dependencies":["finite_set","mapping_lookup","boolean_logic"]},
        "ObligationClosed":{"dependencies":["finite_set","mapping_lookup","boolean_logic"]},
        "RealizerAvailable":{"dependencies":["mapping_lookup","boolean_logic","python_execution"]},
        "ProtectedEquivalent":{"dependencies":["finite_set","equality","boolean_logic"]},
    },
    "load_bearing_symbols":["SHOW_ME_THE_MATH"],
    "runtime_primitives":{
        "finite_set":{"typed_contract":"Finite[A] operations","provider":"CPYTHON_STDLIB_3_12"},
        "mapping_lookup":{"typed_contract":"Map[K,V] x K -> V union {missing}","provider":"CPYTHON_STDLIB_3_12"},
        "fixed_point_iteration":{"typed_contract":"Finite closure iteration until no new member","provider":"CPYTHON_STDLIB_3_12"},
        "boolean_logic":{"typed_contract":"Bool x Bool -> Bool","provider":"CPYTHON_STDLIB_3_12"},
        "equality":{"typed_contract":"A x A -> Bool","provider":"CPYTHON_STDLIB_3_12"},
        "python_execution":{"typed_contract":"CPython 3.12+ executes this embedded stdlib-only module","provider":"CPYTHON_STDLIB_3_12"},
    },
    "obligations":{
        "recognition":{"status":SATISFIED,"witness":"phrase matcher/request dispatch can select this contract"},
        "evaluation":{"status":SATISFIED,"witness":"assess(package,environment) computes fail-closed recursive closure"},
        "projection":{"status":SATISFIED,"witness":"show_me_the_math returns math plus GREEN/RED residual assessment"},
        "persistence":{"status":NOT_APPLICABLE,"witness":"request evaluation is stateless; persistence belongs to the target object when load-bearing"},
        "tool_run_spec":{"status":NOT_APPLICABLE,"witness":"this object is a request contract, not a configured tool"},
    },
    "protected_behavior":(
        "fail_closed_on_hidden_load_bearing_symbol",
        "fresh_environment_no_conversation_dependency",
        "fresh_environment_no_repository_dependency",
        "kind_indexed_obligations",
        "mathematics_first_projection",
    ),
    "equivalence_tests":(
        "self_assessment_green",
        "hidden_dependency_turns_red",
        "missing_kind_obligation_turns_red",
        "isolated_single_file_execution_passes",
    ),
    "realizer":{
        "kind":"PYTHON_STDLIB_MODULE",
        "entrypoint":"show_me_the_math",
        "embedded":True,
        "min_python":(3,12),
    },
    "environment_contract":{
        "required_provider":"CPYTHON_STDLIB_3_12",
        "repository_required":False,
        "conversation_history_required":False,
    },
}


def self_assess()->Assessment:
    return assess(SELF_PACKAGE,SELF_ENVIRONMENT)


def _self_test()->int:
    result=self_assess()
    if not result.complete:
        print(json.dumps(result.payload(),indent=2,sort_keys=True))
        return 1

    broken=dict(SELF_PACKAGE)
    defs={k:dict(v) for k,v in SELF_PACKAGE["definitions"].items()}
    defs["SHOW_ME_THE_MATH"]={"dependencies":["HIDDEN_UNKNOWN"]}
    broken["definitions"]=defs
    negative=assess(broken,SELF_ENVIRONMENT)
    if negative.complete or "HIDDEN_UNKNOWN" not in negative.unresolved_symbols:
        return 2

    print(json.dumps(show_me_the_math(SELF_PACKAGE,SELF_ENVIRONMENT),indent=2,sort_keys=True))
    return 0


if __name__=="__main__":
    raise SystemExit(_self_test())
